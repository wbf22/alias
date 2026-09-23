#!/usr/bin/env python3

import subprocess
import sys
from collections import Counter
from datetime import date, timedelta


# Aim for a GitHub-like graph that fits comfortably in a terminal.
MAX_COLUMNS = 80


def git(*args):
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def get_commits():
    output = git(
        "log",
        "--all",
        "--format=%cd",
        "--date=format:%Y-%m-%d",
    )
    return [date.fromisoformat(x) for x in output.splitlines() if x]


def add_months(d, n):
    m = d.month - 1 + n
    return date(d.year + m // 12, m % 12 + 1, 1)


def choose_scale(first, last):
    days = (last - first).days + 1
    months = (last.year - first.year) * 12 + last.month - first.month + 1
    years = last.year - first.year + 1

    # Daily: exactly the same basic unit as GitHub's contribution graph.
    # Monthly: useful once a daily graph would get too wide.
    # Yearly: for very old repositories.
    if days <= MAX_COLUMNS * 7:
        return "day"
    if months <= MAX_COLUMNS:
        return "month"
    return "year"


def activity_level(value, maximum):
    if value == 0:
        return 0
    if maximum <= 4:
        return value
    return min(4, (value * 4 + maximum - 1) // maximum)


RESET = "\033[0m"

# Distinct hues (truecolor) so each activity level is easy to pick out.
SHADE_COLORS = (
    "",
    "\033[38;2;88;166;255m",   # blue
    "\033[38;2;63;185;80m",    # green
    "\033[38;2;227;179;65m",   # yellow
    "\033[38;2;248;81;73m",    # red
)


def shade(level):
    char = " ░▒▓█"[level]
    if level == 0:
        return char
    return f"{SHADE_COLORS[level]}{char}{RESET}"


def print_legend():
    blocks = " ".join(shade(level) * 2 for level in range(1, 5))
    print()
    print(f"low {blocks} high")


def render_daily(commits, first, last):
    # GitHub-style: 7 rows (Sun-Sat), one column per week.
    # Monday is used internally because Python's weekday() is Monday=0.
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    end = last + timedelta(days=(5 - last.weekday()) % 7)

    weeks = []
    current = start
    while current <= end:
        weeks.append([current + timedelta(days=i) for i in range(7)])
        current += timedelta(days=7)

    counts = Counter(commits)
    values = [counts[d] for week in weeks for d in week]
    maximum = max(values, default=0)

    print()
    print(f"Commits — daily view ({first} → {last})")
    print()

    # Month labels above the columns, similar to GitHub.
    print("      ", end="")
    previous_month = None
    for week in weeks:
        month = next((d for d in week if d.day <= 7), week[0])
        label = month.strftime("%b") if month.month != previous_month else ""
        print(f"{label:<3}", end="")
        previous_month = month.month
    print()

    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for row, name in enumerate(day_names):
        print(f"{name:>3} |", end="")
        for week in weeks:
            d = week[row]
            level = activity_level(counts.get(d, 0), maximum)
            print(f"{shade(level)} ", end="")
        print()

    print()
    print(f"Total commits: {sum(counts.values()):,}")
    print_legend()


def render_monthly(commits, first, last):
    # Monthly analogue: 12 rows (Jan-Dec), one column per year.
    years = list(range(first.year, last.year + 1))
    counts = Counter((d.year, d.month) for d in commits)
    values = [counts[(y, m)] for y in years for m in range(1, 13)]
    maximum = max(values, default=0)

    print()
    print(f"Commits — monthly view ({first} → {last})")
    print()

    print("     ", end="")
    for y in years:
        print(f"{str(y)[-2:]:^3}", end="")
    print()

    for month in range(1, 13):
        name = date(2000, month, 1).strftime("%b")
        print(f"{name:>3} |", end="")
        for year in years:
            level = activity_level(counts.get((year, month), 0), maximum)
            print(f"{shade(level) * 2} ", end="")
        print()

    print()
    print(f"Total commits: {sum(counts.values()):,}")
    print_legend()


def render_yearly(commits, first, last):
    # For very old repositories, one square represents one year.
    years = list(range(first.year, last.year + 1))
    counts = Counter(d.year for d in commits)
    maximum = max(counts.values(), default=0)

    print()
    print(f"Commits — yearly view ({first.year} → {last.year})")
    print()

    print("      ", end="")
    for year in years:
        print(f"{year} ", end="")
    print()

    print("Year  |", end="")
    for year in years:
        level = activity_level(counts.get(year, 0), maximum)
        print(f"{shade(level)}  ", end="")
    print()

    print()
    print(f"Total commits: {sum(counts.values()):,}")
    print_legend()


def main():
    try:
        git("rev-parse", "--git-dir")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: this is not a Git repository.", file=sys.stderr)
        sys.exit(1)

    try:
        commits = get_commits()
    except subprocess.CalledProcessError as exc:
        print(f"Error reading Git history: {exc}", file=sys.stderr)
        sys.exit(1)

    if not commits:
        print("No commits found.")
        return

    first = min(commits)
    last = max(commits)
    scale = choose_scale(first, last)

    if scale == "day":
        render_daily(commits, first, last)
    elif scale == "month":
        render_monthly(commits, first, last)
    else:
        render_yearly(commits, first, last)


if __name__ == "__main__":
    main()
