#!/usr/bin/env python3
"""
Fix escaped backticks in code fences - \`\`\` should be ```
"""

import os
import re


def fix_escaped_backticks(content):
    """Replace escaped backticks with normal backticks"""
    # Replace \`\`\` with ```
    new_content = content.replace('\\`\\`\\`', '```')

    changes = content.count('\\`\\`\\`')

    return new_content, changes


def process_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, changes = fix_escaped_backticks(content)

        if changes > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, changes
        return False, 0
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False, 0


def main():
    docs_dir = 'docs'
    total_files_fixed = 0
    total_changes = 0

    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fixed, changes = process_file(filepath)
                if fixed:
                    print(f"Fixed {changes} escaped backticks in: {filepath}")
                    total_files_fixed += 1
                    total_changes += changes

    print(
        f"\nTotal: {total_changes} escaped backticks fixed in {total_files_fixed} files")


if __name__ == '__main__':
    main()
