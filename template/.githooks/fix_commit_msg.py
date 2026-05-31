#!/usr/bin/env python3
"""Auto-fix mechanical commit message formatting issues before linting."""

import sys
from pathlib import Path


def fix(path: Path) -> None:
    text = path.read_text()
    lines = text.splitlines(keepends=True)

    fixed = []
    for i, line in enumerate(lines):
        if line.startswith("#"):
            fixed.append(line)
            continue

        # Strip trailing whitespace on every line
        line = line.rstrip() + "\n"

        # Strip leading whitespace from subject line (first content line)
        if i == 0 or all(ln.startswith("#") for ln in lines[:i]):
            line = line.lstrip()

        # Convert hard tabs to four spaces
        line = line.replace("\t", "    ")

        fixed.append(line)

    # Ensure blank line between subject and body if body is present
    first = next((i for i, ln in enumerate(fixed) if not ln.startswith("#")), None)
    if first is not None and first + 1 < len(fixed):
        next_content = next(
            (
                i
                for i, ln in enumerate(fixed[first + 1 :], first + 1)
                if not ln.startswith("#")
            ),
            None,
        )
        if (
            next_content is not None
            and next_content == first + 1
            and fixed[first + 1].strip()
        ):
            fixed.insert(first + 1, "\n")

    path.write_text("".join(fixed))


if __name__ == "__main__":
    fix(Path(sys.argv[1]))
