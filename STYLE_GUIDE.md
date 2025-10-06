You need **validation rules** - a checklist AI (or linter) can enforce automatically.

Here's the machine-readable spec:

---

## Markdown Validation Rules (AI/Linter Enforceable)

### 1. H1 Structure Rules

```yaml
rules:
  h1_format:
    - MUST have exactly ONE H1 per file
    - loeng.md: "# [Module Name]"
    - labor.md: "# [Module Name] Labor"
    - kodutoo.md: "# [Module Name] Kodutöö"
    - lisapraktika.md: "# [Module Name] Lisapraktika"
    
  h1_forbidden:
    - NO time markers: "(3 x 45 min)", "(1.5h)", "~2h"
    - NO difficulty: "(Edasijõudnutele)", "(Advanced)", "(Beginner)"
    - NO target audience: "(Terraform'i oskajatele)"
    - NO emojis: "🎯", "📚", "💻"
    
  h1_after:
    - MUST have paragraph immediately after H1 (not **Eesmärk:**)
    - MUST have horizontal rule --- before next section
```

**Regex patterns to reject:**
```regex
^# .* \(.*min.*\)     # Time in H1
^# .* \(.*h\)         # Hours in H1
^# .* \(Advanced\)    # Difficulty
^# .* 🎯              # Emoji
```

---

### 2. H2+ Structure Rules

```yaml
rules:
  h2_after_h1:
    - loeng.md: MUST have "## Õpiväljundid" as first H2
    - labor.md: MUST have "## Õpiväljundid" as first H2
    - kodutoo.md: NO "## Õpiväljundid" allowed
    - lisapraktika.md: NO "## Õpiväljundid" allowed
    
  h2_forbidden_text:
    - "## Kodutöö Ülesanne" → should be "## Ülesanne"
    - "## Labor Samm" → should be "## Samm" or "## N. Samm"
    - "## Lab'i eesmärk" → forbidden heading
    - "## Eesmärk" → use paragraph instead
    
  h2_no_repeat_type:
    - In kodutoo.md: NO "Kodutöö" in H2+
    - In labor.md: NO "Labor" in H2+
    - In lisapraktika.md: NO "Lisapraktika" in H2+
```

**Regex patterns to reject:**
```regex
^## (Kodutöö|Labor|Lisapraktika) .+   # Type repetition in H2
^## Lab'i eesmärk                      # Bad heading
^## Eesmärk$                           # Use paragraph
```

---

### 3. Forbidden Metadata (Student Docs)

```yaml
rules:
  forbidden_inline_metadata:
    - "**Aeg:**"
    - "**Õpetajale:**"
    - "**Vorm:**"
    
  allowed_metadata:
    - "**Eeldused:**" (OK)
```

**Regex to reject:**
```regex
\*\*Kestus:\*\*
\*\*Aeg:\*\*
\*\*Sihtgrupp:\*\*
\*\*Õpetajale:\*\*
```

---

### 4. Code Block Rules

```yaml
rules:
  code_blocks:
    - MUST have language tag: ```bash not ```
    - Allowed: bash, hcl, yaml, python, dockerfile, json, text
    - Empty blocks (```) = ERROR
    
  inline_code:
    - Commands: `terraform init` ✓
    - Filenames: `main.tf` ✓
    - Variables: `${var.name}` ✓
```

**Regex to detect:**
```regex
^```$           # Code block without language (ERROR)
^```\n[^`]      # Code block without language tag
```

---

### 5. List Rules

```yaml
rules:
  checkmarks_inline:
    - FORBIDDEN: "text: - ✅ item - ✅ item"
    - REQUIRED: Convert to proper list with line breaks
    
  list_format:
    - Sequential steps → numbered (1. 2. 3.)
    - Independent items → bullets (-)
    - >2 items → use list (not paragraph)
```

**Regex to detect:**
```regex
\-\s*✅\s*\w+\s*\-\s*✅   # Inline checkmarks (ERROR)
```

---

### 6. Paragraph Rules

```yaml
rules:
  paragraph_length:
    - Max 4 sentences per paragraph
    - Empty line MUST separate paragraphs
    
  count_as_error:
    - 5+ sentences in one paragraph without line break
```

**Algorithm:**
```python
def check_paragraph(text):
    paragraphs = text.split('\n\n')
    for p in paragraphs:
        sentences = p.split('. ')
        if len(sentences) > 4:
            return ERROR("Paragraph too long: max 4 sentences")
```

---

### 7. Emoji Rules

```yaml
rules:
  emoji_forbidden:
    - In H1, H2, H3, H4 headings
    - In bullet lists
    - In normal text
    
  emoji_allowed:
    - Inside admonitions: !!! warning "⚠️ Hoiatus"
    - In tables (rarely)
```

**Regex to detect:**
```regex
^#+\s+.*[\p{Emoji}]    # Emoji in heading (ERROR)
^-\s+[\p{Emoji}]       # Emoji in list (ERROR)
```

---

### 8. Admonition Rules

```yaml
rules:
  admonition_types:
    - Primary: warning, tip, example
    - Secondary (use rarely): info, note, danger, success, question
    
  usage:
    - !!! = always visible (critical info)
    - ??? = collapsible (optional info, >30 lines)
```

---

### 9. Bold Text Rules

```yaml
rules:
  bold_usage:
    - Max 2-3 **bold** terms per section
    - Use for first occurrence of key terms only
    
  count_as_warning:
    - >3 bold terms in one section
```

**Algorithm:**
```python
def check_bold(section):
    bold_count = section.count('**') / 2
    if bold_count > 3:
        return WARNING("Too many bold terms")
```

---

### 10. Collapsible Rules

```yaml
rules:
  when_to_fold:
    - Code >30 lines → MUST use <details> or ???
    - Code 15-30 lines → SHOULD consider folding
    - Code <15 lines → DO NOT fold
    
  solutions:
    - Homework solutions → MUST use ??? success
```

**Algorithm:**
```python
def check_code_length(code_block):
    lines = code_block.count('\n')
    if lines > 30 and not wrapped_in_details():
        return ERROR("Code >30 lines must be folded")
```

---

## Implementation: Validation Script

```python
# validate_markdown.py

import re
from pathlib import Path

RULES = {
    'h1_time_marker': r'^#\s+.*\(.*\d+.*min.*\)',
    'h1_emoji': r'^#\s+.*[\p{Emoji}]',
    'h2_type_repeat': r'^##\s+(Kodutöö|Labor|Lisapraktika)\s+',
    'forbidden_metadata': r'\*\*(Kestus|Aeg|Sihtgrupp|Õpetajale):\*\*',
    'code_no_lang': r'^```$\n',
    'inline_checkmarks': r'\-\s*✅.*\-\s*✅',
}

def validate_file(filepath):
    with open(filepath) as f:
        content = f.read()
        lines = content.split('\n')
    
    errors = []
    
    # Check H1 count
    h1_count = sum(1 for l in lines if l.startswith('# '))
    if h1_count != 1:
        errors.append(f"ERROR: Must have exactly 1 H1, found {h1_count}")
    
    # Check rules
    for rule_name, pattern in RULES.items():
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            errors.append(f"ERROR: {rule_name} violated: {matches[0][:50]}")
    
    # Check õpiväljundid
    if 'loeng.md' in str(filepath) or 'labor.md' in str(filepath):
        if '## Õpiväljundid' not in content:
            errors.append("ERROR: Missing '## Õpiväljundid' heading")
    
    return errors

# Run on all files
for md_file in Path('docs').rglob('*.md'):
    errors = validate_file(md_file)
    if errors:
        print(f"\n{md_file}:")
        for err in errors:
            print(f"  {err}")
```

---

## GitHub Action / Pre-commit Hook

```yaml
# .github/workflows/validate-docs.yml
name: Validate Markdown

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install pyyaml
      - run: python validate_markdown.py
      - name: Fail if errors
        run: |
          if [ -f errors.txt ]; then
            cat errors.txt
            exit 1
          fi
```