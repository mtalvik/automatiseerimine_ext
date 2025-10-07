# Git Lisapraktika

**Eeldused:** Git põhiteadmised (loeng.md ja labor.md läbitud), GitHub konto, käsurea kasutamine

Need kolm harjutust käsitlevad production-ready Git tehnikaid: automatiseeritud kvaliteedikontroll, CI/CD pipeline ja ajaloo puhastamine. Iga harjutus võtab umbes 30-45 minutit.

---

## 1. Git Hooks: Automaatne Koodikontroll

### 1.1 Probleem

Meeskonnas juhtub, et keegi commit'ib koodi, mis sisaldab süntaksi vigu, debug print'e või halbu commit sõnumeid. Iga selline commit võib blokeerida CI pipeline'i ja teiste tööd. Manuaalne kontroll enne iga commit'i on tüütu ja unustatakse ära.

### 1.2 Lahendus

Git hooks on skriptid `.git/hooks/` kaustas, mis käivituvad automaatselt. Pre-commit hook käivitub enne commit'i tegemist - kui script ebaõnnestub, commit tühistatakse.

Näide Python projektile:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$PYTHON_FILES" ]; then
    exit 0
fi

for file in $PYTHON_FILES; do
    python3 -m py_compile "$file"
    if [ $? -ne 0 ]; then
        echo "Syntax error in $file"
        exit 1
    fi
done

if grep -n "print(" $PYTHON_FILES; then
    echo "Found debug print() statements"
    exit 1
fi

if command -v flake8 &> /dev/null; then
    flake8 $PYTHON_FILES || exit 1
fi

echo "Pre-commit checks passed!"
```

Commit sõnumite kontroll:

```bash
#!/bin/bash
# .git/hooks/commit-msg

COMMIT_MSG=$(cat "$1")

if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|refactor|test|chore)(\(.+\))?: .{10,}"; then
    echo "Invalid commit format!"
    echo "Use: type(scope): description"
    echo "Example: feat(auth): add login validation"
    exit 1
fi
```

### 1.3 Harjutus: Implementeeri Hooks

**Nõuded:**
- [ ] Loo pre-commit hook, mis kontrollib vähemalt 2 asja
- [ ] Loo commit-msg hook Conventional Commits formaadi jaoks
- [ ] Tee hook'id käivitatavaks: `chmod +x .git/hooks/*`
- [ ] Testi mõlemat - veendu, et halvad commit'id blokeeritakse

**Näpunäiteid:**
- Hook'id ei liigu clone'iga - production'is kasuta framework'e
- Ajutine vahele jätmine: `git commit --no-verify`
- Kontrolli ainult staged faile: `git diff --cached --name-only`

**Testimine:**
```bash
echo "print('debug')" > test.py
git add test.py
git commit -m "feat: test"  # Peaks ebaõnnestuma
```

**Boonus:**
- Lisa kontroll failide suuruse kohta
- Integreeri code formatter
- Lisa secrets detection

---

## 2. GitHub Actions: CI/CD Pipeline

### 2.1 Probleem

Meeskonnas push'itakse PR'e iga päev. Kui ei käivita teste automaatselt, võib keegi merge'ida koodi, mis lõhub testid, ei builda production'is või sisaldab turvavigu. Manuaalne testimine ei skaleeru.

### 2.2 Lahendus

GitHub Actions käivitab workflow'sid iga push/PR peale. Workflow on YAML fail `.github/workflows/` kaustas.

Põhiline CI workflow:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

Matrix strategy (mitu versiooni paralleelselt):

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

Artifacts ja deployment:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v3
        with:
          name: dist
      - run: echo "Deploy to production"
```

### 2.3 Harjutus: CI/CD Pipeline

**Nõuded:**
- [ ] Loo `.github/workflows/ci.yml` fail
- [ ] Workflow käivitub push'il ja PR'il
- [ ] Sisaldab vähemalt 3 job'i: lint, test, build
- [ ] Kasuta matrix strategy (vähemalt 2 versiooni)

**Näpunäiteid:**
- Alusta lihtsast ja lisa komplekssust järk-järgult
- Kasuta `npm ci` mitte `npm install`
- Cache dependency'sid: `cache: 'npm'`

**Testimine:**
```bash
mkdir -p .github/workflows
# Lisa CI YAML fail
git add .github/
git commit -m "ci: add workflow"
git push origin main
# Vaata GitHubis: Actions tab
```

**Boonus:**
- Lisa security scanning
- Seadista Slack notificationid
- Deploy production serverisse

---

## 3. Interactive Rebase: Ajaloo Puhastamine

### 3.1 Probleem

Teed feature jaoks 7 commit'i: feat, typo fix, oops, wip, actually fix, final, really final. PR ajalugu on räpane. Tahad puhast ajalugu, kus on 2-3 loogilist commit'i.

### 3.2 Lahendus

Interactive rebase võimaldab ajaloo ümberkirjutamist: squash commit'id kokku, muuda sõnumeid, eemalda commit'e.

```bash
git rebase -i HEAD~5
```

Avaneb editor:

```
pick a1b2c3d feat(auth): add login
pick d4e5f6g fix: typo
pick h7i8j9k wip
pick k1l2m3n feat(auth): add logout
pick n4o5p6q fix: oops
```

Puhasta:

```
pick a1b2c3d feat(auth): add login
fixup d4e5f6g fix: typo
drop h7i8j9k wip
pick k1l2m3n feat(auth): add logout
fixup n4o5p6q fix: oops
```

Tulemus: 5 commit → 2 commit. Commands: `pick` (use), `reword` (edit message), `squash` (merge, keep message), `fixup` (merge, discard message), `drop` (remove).

Rebase main'i peale:

```bash
git checkout feature
git rebase main
```

**HOIATUS:** Rebase'i ainult lokaalset ajalugu! Kui push'isid, rebase rikub teiste ajaloo.

### 3.3 Harjutus: Puhasta Feature Branch

**Nõuded:**
- [ ] Loo feature branch ja tee 5-7 "räpast" commit'i
- [ ] Kasuta `git rebase -i` et squash'ida 2-3 puhtaks commit'iks
- [ ] Muuda vähemalt ühe commit'i sõnumit
- [ ] Rebase feature main'i peale

**Näpunäiteid:**
- Backup enne: `git branch backup-feature`
- Kui läks katki: `git rebase --abort`
- Force push pärast: `git push --force-with-lease`

**Testimine:**
```bash
git checkout -b feature/cleanup
for i in {1..5}; do
  echo "v$i" > file.txt
  git add . && git commit -m "wip $i"
done

git log --oneline  # 5 commit'i
git rebase -i HEAD~5  # Squash kokku
git log --oneline  # 1 commit
```

**Boonus:**
- Õpi `git reflog` - leia "kaotatud" commit'e
- Proovi `git rebase --autosquash`
- `git cherry-pick` - võta commit teisest branch'ist

---

## Kasulikud Ressursid

**Dokumentatsioon:**
- [Git Hooks](https://git-scm.com/docs/githooks)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Git Rebase](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)

**Tööriistad:**
- **pre-commit** - Hook'ide framework: `pip install pre-commit`
- **act** - GitHub Actions lokaalselt: `brew install act`
- **git-filter-repo** - Ajaloo puhastamine: `pip install git-filter-repo`

**Näited:**
- [GitHub Actions starter workflows](https://github.com/actions/starter-workflows)

Need harjutused on mõeldud süvendama teie Git oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole.