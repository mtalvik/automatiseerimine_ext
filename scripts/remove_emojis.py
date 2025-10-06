#!/usr/bin/env python3
import re
from pathlib import Path

EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]",
    flags=re.UNICODE,
)

# Also remove common checkmarks/crosses and variation selectors
EXTRA = {
    "✓": "",
    "❌": "",
    "️": "",  # variation selector
}

def strip_emojis(text: str) -> str:
    for k, v in EXTRA.items():
        text = text.replace(k, v)
    return EMOJI_PATTERN.sub("", text)


def should_skip(path: Path) -> bool:
    # Skip style guide and anything in tunniplaanid
    if path.name == "STYLE_GUIDE.md":
        return True
    parts = {p for p in path.parts}
    if "tunniplaanid" in parts:
        return True
    return False


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    cleaned = strip_emojis(original)
    if cleaned != original:
        path.write_text(cleaned, encoding="utf-8")
        return True
    return False


def main():
    repo = Path(__file__).resolve().parents[1]
    changed = 0
    for md in repo.rglob("**/*.md"):
        if should_skip(md):
            continue
        if process_file(md):
            changed += 1
            print(f"Cleaned: {md}")
    print(f"Done. Files updated: {changed}")

if __name__ == "__main__":
    main()
