#!/usr/bin/env python3

import sys
import re


def format_table(lines):
    rows = []

    for line in lines:
        # Split cells, ignoring optional leading/trailing pipes
        cells = line.strip().strip('|').split('|')
        cells = [cell.strip() for cell in cells]
        rows.append(cells)

    if not rows:
        return lines

    # Find maximum number of columns
    num_cols = max(len(row) for row in rows)

    # Normalize rows
    for row in rows:
        row.extend([''] * (num_cols - len(row)))

    # Calculate column widths
    widths = [0] * num_cols

    for row in rows:
        for i, cell in enumerate(row):
            # Ignore alignment colons and dashes when calculating
            # separator row widths
            if not re.fullmatch(r':?-+:?', cell):
                widths[i] = max(widths[i], len(cell))

    # Ensure separator rows are wide enough
    widths = [max(w, 3) for w in widths]

    # Format rows
    formatted = []

    for row in rows:
        cells = []

        for i, cell in enumerate(row):
            if re.fullmatch(r':?-+:?', cell):
                # Preserve alignment indicators
                left = cell.startswith(':')
                right = cell.endswith(':')

                dashes = '-' * max(3, widths[i] - left - right)
                cell = (':' if left else '') + dashes + (':' if right else '')
                cells.append(cell)
            else:
                cells.append(cell.ljust(widths[i]))

        formatted.append('| ' + ' | '.join(cells) + ' |')

    return formatted


def format_markdown(content):
    lines = content.splitlines()
    output = []

    table = []

    def flush_table():
        nonlocal table

        if table:
            output.extend(format_table(table))
            table = []

    for line in lines:
        stripped = line.strip()

        # A table row starts and ends with a pipe
        if stripped.startswith('|') and stripped.endswith('|'):
            table.append(line)
        else:
            flush_table()
            output.append(line)

    flush_table()

    return '\n'.join(output) + '\n'


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 format_md.py <file.md>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    formatted = format_markdown(content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(formatted)

    print(f"Formatted: {filename}")


if __name__ == '__main__':
    main()
