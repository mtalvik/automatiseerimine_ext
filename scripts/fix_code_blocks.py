#!/usr/bin/env python3
"""Fix broken code blocks where text directly touches ``` without newline."""
import re
from pathlib import Path


def fix_code_blocks(content: str) -> str:
    """Fix code blocks that are missing newlines before opening fence."""
    # Pattern 1: text (not starting line)``` followed optionally by language
    # Replace with: text\n```language
    content = re.sub(
        r'([^\n])(```(?:\w+)?)',
        r'\1\n\2',
        content
    )
    
    # Pattern 2: **Bold text:**``` (common pattern for labels)
    # Already caught by pattern 1, but ensure consistency
    
    # Pattern 3: closing fence without newline after
    # text```\n should become text\n```\n
    content = re.sub(
        r'([^\n])(```)\n',
        r'\1\n\2\n',
        content
    )
    
    return content


def main():
    root = Path(__file__).resolve().parents[1] / "docs"
    changed = 0
    
    for md in root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        new_text = fix_code_blocks(text)
        
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"Fixed: {md.relative_to(root.parent)}")
    
    print(f"\nTotal files fixed: {changed}")


if __name__ == "__main__":
    main()
