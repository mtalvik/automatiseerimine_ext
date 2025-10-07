#!/usr/bin/env python3
"""
Fix orphaned backticks - where a line ends without closing backtick,
and the next line contains just a single backtick.
"""

import os
import re

def fix_orphan_backticks(content):
    """Fix lines where closing backtick is on the next line"""
    lines = content.split('\n')
    i = 0
    fixed_lines = []
    changes = 0
    
    while i < len(lines):
        # Check if next line is just a single backtick
        if i + 1 < len(lines) and lines[i+1].strip() == '`':
            current_line = lines[i].rstrip()
            # Check if current line contains an opening backtick but no closing one at the end
            # Count backticks
            backtick_count = current_line.count('`')
            if backtick_count % 2 == 1:  # Odd number means unclosed
                # Move the closing backtick from next line to end of current line
                fixed_lines.append(current_line + '`')
                changes += 1
                i += 2  # Skip both lines
                continue
        
        fixed_lines.append(lines[i])
        i += 1
    
    return '\n'.join(fixed_lines), changes

def process_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changes = fix_orphan_backticks(content)
        
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
    
    print(f"\nTotal: {total_changes} orphan backticks fixed in {total_files_fixed} files")

if __name__ == '__main__':
    main()

