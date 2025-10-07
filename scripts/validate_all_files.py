#!/usr/bin/env python3
"""
Comprehensive validation of all Markdown files.
Checks for code block and list formatting issues.
"""

import os
import re
from pathlib import Path

def check_file(filepath):
    """Check a single file for formatting issues"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check 1: Single backticks on separate lines
        for i, line in enumerate(lines, 1):
            if line.strip() == '`':
                issues.append(f"Line {i}: Single backtick on separate line")
        
        # Check 2: Escaped backticks
        for i, line in enumerate(lines, 1):
            if '\\`\\`\\`' in line:
                issues.append(f"Line {i}: Escaped backticks found")
        
        # Check 3: Text directly touching code fences (no newline before)
        for i in range(len(lines) - 1):
            if lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('-') and not lines[i].strip().startswith('```'):
                if lines[i+1].strip().startswith('```'):
                    # Check if line ends with something that suggests it should have a newline
                    if lines[i].rstrip().endswith(':') or lines[i].rstrip().endswith('.'):
                        issues.append(f"Line {i+1}: Code block might need blank line before it (after line {i})")
        
        # Check 4: Inline lists (Label: - item - item pattern)
        for i, line in enumerate(lines, 1):
            # Look for patterns like "Text: - item - item"
            if ':' in line and ' - ' in line:
                # Check if it looks like an inline list
                match = re.match(r'^([^:]+):\s*-\s+.*\s+-\s+', line)
                if match:
                    issues.append(f"Line {i}: Possible inline list detected: {line[:80]}")
        
        # Check 5: Three backticks split across lines
        for i in range(len(lines) - 2):
            if (lines[i].strip() == '`' and 
                lines[i+1].strip() == '`' and 
                lines[i+2].strip() == '`'):
                issues.append(f"Line {i+1}-{i+3}: Three backticks split across lines")
        
        # Check 6: Unclosed code blocks
        code_fence_count = 0
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```') or line.strip().startswith('~~~'):
                code_fence_count += 1
        if code_fence_count % 2 != 0:
            issues.append(f"File has unclosed code block (odd number of fences: {code_fence_count})")
        
        return issues
        
    except Exception as e:
        return [f"Error reading file: {e}"]

def main():
    docs_dir = Path(__file__).resolve().parents[1] / 'docs'
    
    all_files = sorted(docs_dir.rglob('*.md'))
    
    print("=" * 80)
    print("COMPREHENSIVE MARKDOWN VALIDATION")
    print("=" * 80)
    print()
    
    total_files = 0
    files_with_issues = 0
    total_issues = 0
    
    for filepath in all_files:
        total_files += 1
        rel_path = filepath.relative_to(docs_dir.parent)
        issues = check_file(filepath)
        
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"❌ {rel_path}")
            for issue in issues:
                print(f"   {issue}")
            print()
        else:
            print(f"✅ {rel_path}")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files checked: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files OK: {total_files - files_with_issues}")
    print(f"Total issues found: {total_issues}")
    print()
    
    if files_with_issues == 0:
        print("🎉 ALL FILES PASS VALIDATION! Ready to publish!")
    else:
        print("⚠️  Some files need attention")
    
    return 0 if files_with_issues == 0 else 1

if __name__ == '__main__':
    exit(main())

