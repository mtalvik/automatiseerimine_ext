#!/usr/bin/env python3
import re
from pathlib import Path


PREFIXES = (
    "Validation",
    "Nõuded",
    "Näpunäiteid",
    "Hindeskaalaa",
    "Dokumentatsioon",
    "Näited",
    "Probleemid hard-code'imisega",
)


def split_inline_list_line(line: str) -> str:
    # Match: "Label: - item - item" (supports checkboxes "- [ ]") or plain dashes
    m = re.match(r"^(?P<prefix>[^\n:]{2,}):\s*(?P<rest>.+)$", line.strip())
    if not m:
        return line

    prefix = m.group("prefix").strip()
    rest = m.group("rest").strip()

    # Only convert for known prefixes (keeps false positives low)
    if prefix not in PREFIXES and not re.match(r"^[A-ZÄÖÜÕa-zäöüõ].{0,40}$", prefix):
        return line

    # Must contain at least one dash-delimited item
    if " - " not in rest and " – " not in rest:
        return line

    parts = re.split(r"\s+[–-]\s+", rest)
    # If splitting yields less than 2 items, skip
    if len(parts) < 2:
        return line

    rebuilt = [f"{prefix}:", ""]  # Add empty line after heading
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # Normalize leading checkbox if present
        # e.g. "[ ] text" or "[x] text"
        if p.startswith("[ ") or p.startswith("[x") or p.startswith("[X"):
            rebuilt.append(f"- {p}")
        else:
            rebuilt.append(f"- {p}")
    return "\n".join(rebuilt)


def transform_content(content: str) -> str:
    # Split content into lines, process line by line, but skip code blocks
    lines = content.split('\n')
    result = []
    in_code_block = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if we're entering or leaving a code block
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        # If in code block, don't modify
        if in_code_block:
            result.append(line)
            i += 1
            continue

        # Process the line for inline lists
        transformed = split_inline_list_line(line)

        # If line was transformed (contains newlines), it became multiple lines
        if '\n' in transformed and transformed != line:
            result.extend(transformed.split('\n'))
        else:
            result.append(line)

        i += 1

    return '\n'.join(result)


def main():
    root = Path(__file__).resolve().parents[1] / "docs"
    changed = 0
    for md in root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        new_text = transform_content(text)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Updated files: {changed}")


if __name__ == "__main__":
    main()
