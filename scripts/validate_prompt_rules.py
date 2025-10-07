#!/usr/bin/env python3
"""
Validate markdown files against the content generation prompt rules.
Checks for formatting violations and content quality issues.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple


class PromptValidator:
    def __init__(self):
        self.issues = defaultdict(list)
        self.file_count = 0
        self.total_issues = 0

    def validate_file(self, filepath: Path) -> Dict[str, List[str]]:
        """Validate a single markdown file against prompt rules."""
        file_issues = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return {"error": [f"Could not read file: {e}"]}

        # Get file type from name
        file_type = self._get_file_type(filepath.name)

        # Check H1 issues
        file_issues.extend(self._check_h1_violations(content, lines))

        # Check code blocks
        file_issues.extend(self._check_code_blocks(content, lines))

        # Check heading structure
        file_issues.extend(self._check_heading_structure(lines))

        # Check for emojis
        file_issues.extend(self._check_emojis(lines))

        # Check admonitions
        file_issues.extend(self._check_admonitions(content, lines, file_type))

        # Check for forbidden phrases
        file_issues.extend(self._check_forbidden_phrases(content, lines))

        # Check for code without explanation
        file_issues.extend(self._check_code_explanations(lines))

        # Check for metadata format
        file_issues.extend(self._check_metadata(lines, file_type))

        return {"issues": file_issues}

    def _get_file_type(self, filename: str) -> str:
        """Determine file type from filename."""
        if 'loeng' in filename or 'lecture' in filename:
            return 'loeng'
        elif 'labor' in filename or 'lab' in filename:
            return 'labor'
        elif 'kodutoo' in filename or 'homework' in filename:
            return 'kodutoo'
        elif 'lisapraktika' in filename:
            return 'lisapraktika'
        elif 'tunnikava' in filename or 'tunniplaanid' in filename:
            return 'tunnikava'
        elif filename in ['index.md', 'README.md']:
            return 'index'
        else:
            return 'other'

    def _check_h1_violations(self, content: str, lines: List[str]) -> List[str]:
        """Check for H1 violations: multiple H1s, emojis, time markers."""
        issues = []
        h1_pattern = re.compile(r'^# (.+)$', re.MULTILINE)
        h1_matches = h1_pattern.findall(content)

        # Check for multiple H1s
        if len(h1_matches) == 0:
            issues.append("❌ No H1 heading found")
        elif len(h1_matches) > 1:
            issues.append(
                f"❌ Multiple H1 headings found ({len(h1_matches)}). Should be exactly ONE.")
            for i, h1 in enumerate(h1_matches, 1):
                issues.append(f"   H1 #{i}: {h1[:50]}")

        # Check H1 content
        if h1_matches:
            h1_text = h1_matches[0]

            # Check for time markers in H1
            time_marker_pattern = r'\(?\d+[×xX]\d+\s*min\)?|\(?\~?\d+[-–]\d+\s*(h|min|tund)'
            if re.search(time_marker_pattern, h1_text):
                issues.append(f"❌ H1 contains time marker: '{h1_text}'")
                issues.append(
                    "   Time estimates should be in metadata paragraph after H1")

            # Check for emojis in H1
            emoji_pattern = re.compile(
                r'[\U0001F300-\U0001F9FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U00002600-\U000027BF]')
            if emoji_pattern.search(h1_text):
                issues.append(f"❌ H1 contains emoji: '{h1_text}'")

        return issues

    def _check_code_blocks(self, content: str, lines: List[str]) -> List[str]:
        """Check for code blocks without language tags."""
        issues = []

        # Find code blocks without language tags
        no_lang_pattern = re.compile(r'^```\s*$', re.MULTILINE)
        matches = list(no_lang_pattern.finditer(content))

        if matches:
            issues.append(
                f"❌ Found {len(matches)} code block(s) without language tags")
            for match in matches[:5]:  # Show first 5
                line_num = content[:match.start()].count('\n') + 1
                issues.append(
                    f"   Line {line_num}: Code block missing language tag (should be ```bash, ```yaml, etc.)")

        return issues

    def _check_heading_structure(self, lines: List[str]) -> List[str]:
        """Check for improper heading usage."""
        issues = []

        for i, line in enumerate(lines, 1):
            # Check for "Samm N" or "Osa N" headings
            if re.match(r'^#+\s*(Samm|Osa|Step|Part)\s+\d+', line, re.IGNORECASE):
                issues.append(
                    f"❌ Line {i}: Forbidden heading format: '{line.strip()}'")
                issues.append(
                    "   Use numbered sections like '## 1. Section Name' instead")

            # Check for excessive heading levels (H5, H6)
            if line.startswith('#####'):
                issues.append(
                    f"⚠️  Line {i}: H5/H6 heading found - consider simplifying hierarchy")

            # Check for heading with only emoji or very short
            heading_match = re.match(r'^(#+)\s*(.+)$', line)
            if heading_match:
                level, text = heading_match.groups()
                if len(text.strip()) < 3:
                    issues.append(
                        f"❌ Line {i}: Heading too short: '{line.strip()}'")

        return issues

    def _check_emojis(self, lines: List[str]) -> List[str]:
        """Check for emojis in body text and headings (except in admonitions)."""
        issues = []
        emoji_pattern = re.compile(
            r'[\U0001F300-\U0001F9FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U00002600-\U000027BF]')

        in_admonition = False
        for i, line in enumerate(lines, 1):
            # Track if we're in an admonition
            if line.startswith('!!!'):
                in_admonition = True
                continue
            elif in_admonition and line and not line.startswith(' '):
                in_admonition = False

            # Only check for emojis outside admonitions
            if not in_admonition and emoji_pattern.search(line):
                # Skip if it's in a code block or comment
                if not line.strip().startswith('```') and not line.strip().startswith('<!--'):
                    issues.append(
                        f"❌ Line {i}: Emoji found in body text: '{line.strip()[:60]}'")
                    issues.append(
                        "   Emojis only allowed in README/index admonition titles")

        return issues

    def _check_admonitions(self, content: str, lines: List[str], file_type: str) -> List[str]:
        """Check admonition usage based on file type."""
        issues = []

        # Count admonitions
        admonition_pattern = re.compile(r'^!!!\s+\w+', re.MULTILINE)
        admonitions = admonition_pattern.findall(content)
        admonition_count = len(admonitions)

        # Check limits based on file type
        if file_type == 'loeng' and admonition_count > 3:
            issues.append(
                f"⚠️  loeng.md has {admonition_count} admonitions (recommended max: 2-3)")
            issues.append("   Use sparingly for pedagogical emphasis only")

        elif file_type == 'labor' and admonition_count > 2:
            issues.append(
                f"⚠️  labor.md has {admonition_count} admonitions (recommended max: 1-2)")
            issues.append("   Use only for critical warnings")

        elif file_type == 'kodutoo' and admonition_count > 2:
            issues.append(
                f"⚠️  kodutoo.md has {admonition_count} admonitions (recommended max: 1-2)")
            issues.append("   Use only for submission requirements")

        elif file_type == 'lisapraktika' and admonition_count > 0:
            issues.append(
                f"❌ lisapraktika.md has {admonition_count} admonitions (should have NONE)")
            issues.append("   Keep lisapraktika clean and text-based")

        # Check for emojis in non-README admonitions
        if file_type not in ['index', 'other']:
            for i, line in enumerate(lines, 1):
                if line.startswith('!!!'):
                    emoji_pattern = re.compile(
                        r'[\U0001F300-\U0001F9FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U00002600-\U000027BF]')
                    if emoji_pattern.search(line):
                        issues.append(
                            f"❌ Line {i}: Emoji in admonition: '{line.strip()}'")
                        issues.append(
                            "   NO emojis in admonitions for loeng/labor/kodutoo files")

        return issues

    def _check_forbidden_phrases(self, content: str, lines: List[str]) -> List[str]:
        """Check for forbidden childish or unprofessional language."""
        issues = []

        forbidden_patterns = [
            (r'\bselgita vanaisale\b', 'childish phrase "selgita vanaisale"'),
            (r'\blambike\b', 'childish phrase "lambike"'),
            (r'\bWow!', 'excessive enthusiasm "Wow!"'),
            (r'\bAmazing!', 'excessive enthusiasm "Amazing!"'),
            (r'\bSuper!', 'excessive enthusiasm "Super!"'),
            (r'\bAwesome!', 'excessive enthusiasm "Awesome!"'),
        ]

        for pattern, description in forbidden_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in matches[:3]:  # Show first 3
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(f"❌ Line {line_num}: Found {description}")
                    issues.append("   Use professional vocational school tone")

        return issues

    def _check_code_explanations(self, lines: List[str]) -> List[str]:
        """Check if code blocks have explanations before them."""
        issues = []

        for i, line in enumerate(lines):
            if line.startswith('```') and i > 0:
                # Check if there's explanatory text in previous 3 lines
                prev_lines = lines[max(0, i-3):i]
                has_explanation = False

                for prev_line in reversed(prev_lines):
                    # Skip empty lines and headings
                    if prev_line.strip() and not prev_line.startswith('#'):
                        # Check if it's actual explanatory text (not just a heading or list item)
                        if len(prev_line.strip()) > 20 and not prev_line.strip().startswith('-'):
                            has_explanation = True
                            break

                if not has_explanation:
                    issues.append(
                        f"⚠️  Line {i+1}: Code block without explanation before it")
                    issues.append("   Always explain code BEFORE showing it")

        return issues

    def _check_metadata(self, lines: List[str], file_type: str) -> List[str]:
        """Check metadata formatting after H1."""
        issues = []

        if file_type in ['loeng', 'labor', 'kodutoo', 'tunnikava']:
            # Find H1
            h1_line = -1
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    h1_line = i
                    break

            if h1_line >= 0 and h1_line + 1 < len(lines):
                # Check next few lines for metadata
                next_lines = lines[h1_line+1:min(h1_line+5, len(lines))]
                has_metadata = False

                for line in next_lines:
                    if '**Eeldused:**' in line or '**Kestus:**' in line or '**Platvorm:**' in line:
                        has_metadata = True
                        # Check if metadata is properly formatted (single paragraph, not list)
                        if line.startswith('-') or line.startswith('*'):
                            issues.append(
                                f"⚠️  Metadata should be a paragraph, not a list")
                        break

                if not has_metadata and file_type != 'tunnikava':
                    issues.append(
                        f"⚠️  Missing metadata paragraph after H1 for {file_type}.md")
                    issues.append(
                        "   Should include: **Eeldused:** ... • **Platvorm:** ...")

        return issues

    def validate_directory(self, directory: Path, recursive: bool = True) -> Dict[str, List[str]]:
        """Validate all markdown files in a directory."""
        results = {}

        pattern = '**/*.md' if recursive else '*.md'
        md_files = sorted(directory.glob(pattern))

        for filepath in md_files:
            # Skip certain files
            if any(skip in str(filepath) for skip in ['node_modules', 'venv', 'site', '.git']):
                continue

            self.file_count += 1
            relative_path = filepath.relative_to(directory)

            print(f"Validating: {relative_path}", file=sys.stderr)

            file_results = self.validate_file(filepath)
            if file_results.get("issues") or file_results.get("error"):
                results[str(relative_path)] = file_results
                if file_results.get("issues"):
                    self.total_issues += len(file_results["issues"])

        return results

    def generate_report(self, results: Dict[str, List[str]], output_file: Path = None) -> str:
        """Generate a formatted validation report."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("PROMPT RULES VALIDATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")

        report_lines.append(f"Files checked: {self.file_count}")
        report_lines.append(f"Files with issues: {len(results)}")
        report_lines.append(f"Total issues found: {self.total_issues}")
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Categorize issues by severity
        critical_files = []
        warning_files = []

        for filepath, file_data in sorted(results.items()):
            if file_data.get("error"):
                critical_files.append(filepath)
            else:
                issues = file_data.get("issues", [])
                if any("❌" in issue for issue in issues):
                    critical_files.append(filepath)
                else:
                    warning_files.append(filepath)

        # Report critical issues first
        if critical_files:
            report_lines.append("🔴 CRITICAL ISSUES (Must Fix)")
            report_lines.append("-" * 80)
            report_lines.append("")

            for filepath in critical_files:
                file_data = results[filepath]
                report_lines.append(f"📄 {filepath}")
                report_lines.append("")

                if file_data.get("error"):
                    for error in file_data["error"]:
                        report_lines.append(f"  {error}")
                else:
                    critical_issues = [i for i in file_data.get(
                        "issues", []) if "❌" in i]
                    for issue in critical_issues:
                        report_lines.append(f"  {issue}")

                report_lines.append("")

        # Report warnings
        if warning_files:
            report_lines.append("⚠️  WARNINGS (Should Fix)")
            report_lines.append("-" * 80)
            report_lines.append("")

            for filepath in warning_files:
                file_data = results[filepath]
                report_lines.append(f"📄 {filepath}")
                report_lines.append("")

                warning_issues = [i for i in file_data.get(
                    "issues", []) if "⚠️" in i]
                for issue in warning_issues:
                    report_lines.append(f"  {issue}")

                report_lines.append("")

        # Summary
        report_lines.append("=" * 80)
        report_lines.append("SUMMARY")
        report_lines.append("=" * 80)
        report_lines.append("")
        report_lines.append(f"✅ Clean files: {self.file_count - len(results)}")
        report_lines.append(
            f"🔴 Files with critical issues: {len(critical_files)}")
        report_lines.append(f"⚠️  Files with warnings: {len(warning_files)}")
        report_lines.append("")

        report = "\n".join(report_lines)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\nReport saved to: {output_file}", file=sys.stderr)

        return report


def main():
    """Main validation function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate markdown files against prompt rules')
    parser.add_argument('directory', type=Path, help='Directory to validate')
    parser.add_argument('-o', '--output', type=Path, help='Output report file')
    parser.add_argument('--no-recursive', action='store_true',
                        help='Don\'t search recursively')

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(1)

    validator = PromptValidator()
    results = validator.validate_directory(
        args.directory, recursive=not args.no_recursive)
    report = validator.generate_report(results, args.output)

    print("\n" + report)

    # Exit with error code if issues found
    sys.exit(1 if results else 0)


if __name__ == '__main__':
    main()
