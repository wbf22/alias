#!/usr/bin/env python3
"""terminal disk-usage chart: show where space is going under a path."""

import argparse
import os
import shutil
import sys

PARTIALS = " ▏▎▍▌▋▊▉"
FULL = "█"
RESET = "\033[0m"
DIM = "\033[2m"


class Node:
    __slots__ = ("name", "path", "size", "is_dir", "children")

    def __init__(self, name, path, is_dir):
        self.name = name
        self.path = path
        self.size = 0
        self.is_dir = is_dir
        self.children = []


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if n < 1024 or unit == "PB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def _fill(node, seen, errors, keep_empty=False):
    try:
        entries = list(os.scandir(node.path))
    except OSError as e:
        errors.append(f"{node.path}: {e}")
        return 0
    total = 0
    for entry in entries:
        try:
            child_st = entry.stat(follow_symlinks=False)
        except OSError as e:
            errors.append(f"{entry.path}: {e}")
            continue
        if entry.is_symlink():
            continue
        if entry.is_dir(follow_symlinks=False):
            child = Node(entry.name, entry.path, True)
            child.size = _fill(child, seen, errors, keep_empty)
            node.children.append(child)
            total += child.size
        else:
            key = (child_st.st_dev, child_st.st_ino)
            if key in seen:
                continue
            seen.add(key)
            if child_st.st_size or keep_empty:
                child = Node(entry.name, entry.path, False)
                child.size = child_st.st_size
                node.children.append(child)
                total += child_st.st_size

    node.children.sort(key=lambda c: c.size, reverse=True)
    return total


def bar(fraction, width, color):
    fraction = max(0.0, min(1.0, fraction))
    cells = fraction * width
    whole = int(cells)
    out = FULL * whole
    if whole < width and PARTIALS:
        idx = int((cells - whole) * len(PARTIALS))
        out += PARTIALS[idx]
    out += " " * max(0, width - len(out))
    return f"{color}{out}{RESET}" if color else out


def read_color():
    return "\033[36m"


def row(size, frac, name, indent, bar_w, name_w, color):
    vis = "  " * indent + name
    if len(vis) > name_w:
        vis = "…" + vis[-(name_w - 1):]
    return f"{human(size):>9}  {frac * 100:5.1f}%  {bar(frac, bar_w, color)}  {vis}"


def render(node, total, args, layout, color, indent=0):
    if indent > args.depth:
        return
    bar_w, name_w = layout
    for child in node.children:
        if child.size < args.min and indent > 0:
            continue
        frac = child.size / total if total > 0 else 0.0
        name = child.name + "/" if child.is_dir else child.name
        print(row(child.size, frac, name, indent, bar_w, name_w, color))
        if child.is_dir:
            render(child, total, args, layout, color, indent + 1)


def collect_files(node, out):
    if not node.is_dir:
        out.append(node)
        return
    for c in node.children:
        collect_files(c, out)


def main():
    ap = argparse.ArgumentParser(description="chart where disk space goes under a path")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("-d", "--depth", type=int, default=1, help="folder nesting to show (default 1)")
    ap.add_argument("-n", "--top", type=int, default=10, help="largest files to list (default 10)")
    ap.add_argument("-m", "--min", type=float, default=0, help="hide entries smaller than this many bytes")
    ap.add_argument("-a", "--all", action="store_true", help="show every file/folder all the way down")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()

    if args.all:
        args.depth = sys.maxsize
        args.min = 0

    target = os.path.abspath(os.path.expanduser(args.path))
    if not os.path.exists(target):
        print(f"no such path: {target}", file=sys.stderr)
        return 1

    width = min(shutil.get_terminal_size((100, 24)).columns, 120)
    color = "" if args.no_color or not sys.stdout.isatty() else read_color()
    bar_w = max(8, min(32, width // 3))
    name_w = max(16, width - 19 - bar_w)
    layout = (bar_w, name_w)

    seen, errors = set(), []
    if os.path.isdir(target) and not os.path.islink(target):
        root = Node(target, target, True)
        root.size = _fill(root, seen, errors, args.all)
    else:
        try:
            size = os.path.getsize(target)
        except OSError as e:
            print(f"cannot stat {target}: {e}", file=sys.stderr)
            return 1
        root = Node(os.path.basename(target), target, False)
        root.size = size

    total = root.size
    print()
    print(f"{target}")
    print(f"total: {human(total)}")
    print("─" * width)
    render(root, total, args, layout, color)

    if args.top:
        files = []
        collect_files(root, files)
        files.sort(key=lambda f: f.size, reverse=True)
        files = [f for f in files if f.size >= args.min][: args.top]
        if files:
            print()
            print(f"largest files (top {len(files)})")
            print("─" * width)
            largest = files[0].size or 1
            for f in files:
                frac = f.size / largest
                rel = os.path.relpath(f.path, target)
                print(row(f.size, frac, rel, 0, bar_w, name_w, color))

    if errors:
        print()
        print(f"{DIM}{len(errors)} item(s) skipped (permission or IO errors){RESET}")

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
