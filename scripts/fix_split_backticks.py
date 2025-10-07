#!/usr/bin/env python3
"""
Fix broken code fences and inline code where backticks are split across lines.
"""

import os
import re


def fix_split_backticks(content):
    """Fix various backtick splitting issues"""
    lines = content.split('\n')
    i = 0
    fixed_lines = []
    changes = 0

    while i < len(lines):
        # Pattern 1: Three consecutive lines with single backticks (broken code fence)
        if (i + 2 < len(lines) and
            lines[i].strip() == '`' and
            lines[i+1].strip() == '`' and
                lines[i+2].strip() == '`'):
            fixed_lines.append('```')
            changes += 1
            i += 3
            continue

        # Pattern 2: Line ending with backtick, next line is just backtick (broken inline code)
        if i + 1 < len(lines) and lines[i+1].strip() == '`':
            # Check if current line ends with a backtick
            if lines[i].rstrip().endswith('`'):
                # This is likely a heading or text with inline code at the end that got split
                current = lines[i].rstrip()
                # Move the closing backtick to the end of the current line
                if not current.endswith('`'):
                    # The backtick is on the next line, merge it back
                    fixed_lines.append(current + '`')
                    changes += 1
                    i += 2  # Skip the line with just `
                    continue
                else:
                    # Already has backtick, just skip the orphaned one
                    fixed_lines.append(lines[i])
                    changes += 1
                    i += 2
                    continue

        fixed_lines.append(lines[i])
        i += 1

    return '\n'.join(fixed_lines), changes


def process_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, changes = fix_split_backticks(content)

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
                    print(f"Fixed {changes} instances in: {filepath}")
                    total_files_fixed += 1
                    total_changes += changes

    print(
        f"\nTotal: {total_changes} split backticks fixed in {total_files_fixed} files")


if __name__ == '__main__':
    main()
