#  Git Lisapraktika

**Eesmärk:** Süvendada Git oskusi täiendavate praktiliste ülesannetega  
**Eeltingimused:** Git põhiteadmised, GitHub konto

---

##  Ülevaade

See fail sisaldab lisapraktikaid ja boonusülesandeid Git versioonihalduse mooduli jaoks, sealhulgas GitHub Actions tutvustus ja edasijõudnud Git funktsioonid.

---

##  Õpiväljundid

Pärast lisapraktikat oskate:

- GitHub Actions workflow'ide loomine
- Edasijõudnud Git funktsioonide kasutamine
- Git hooks ja automatiseerimine
- Submodules ja monorepo haldamine

##  GitHub Actions Tutvustus

### Lihtne CI/CD Workflow

Loo `.github/workflows/ci.yml` fail:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: npm install
      
    - name: Run tests
      run: npm test
      
    - name: Build project
      run: npm run build
      
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-files
        path: dist/
```

### Deployment Workflow

Loo `.github/workflows/deploy.yml` fail:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to server
      run: |
        echo "Deploying to production..."
        # Lisa siia oma deployment skript
```

##  Git Hooks

### Pre-commit Hook

Loo `.git/hooks/pre-commit` fail:

```bash
#!/bin/bash

echo "Running pre-commit checks..."

# Kontrolli süntaksit
if command -v node &> /dev/null; then
  echo "Checking JavaScript syntax..."
  node -c src/*.js
  if [ $? -ne 0 ]; then
    echo "JavaScript syntax errors found!"
    exit 1
  fi
fi

# Kontrolli linting'ut
if command -v eslint &> /dev/null; then
  echo "Running ESLint..."
  eslint src/
  if [ $? -ne 0 ]; then
    echo "ESLint errors found!"
    exit 1
  fi
fi

echo "Pre-commit checks passed!"
```

### Commit-msg Hook

Loo `.git/hooks/commit-msg` fail:

```bash
#!/bin/bash

# Kontrolli commit sõnumi formaati
commit_msg=$(cat "$1")

# Peamised reeglid
if [[ ! $commit_msg =~ ^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: ]]; then
  echo "Error: Invalid commit message format!"
  echo "Use format: type(scope): description"
  echo "Types: feat, fix, docs, style, refactor, test, chore"
  exit 1
fi

if [[ ${#commit_msg} -lt 10 ]]; then
  echo "Error: Commit message too short!"
  exit 1
fi

echo "Commit message format is valid!"
```

##  Git Submodules

### Submodule Lisamine

```bash
# Lisa submodule
git submodule add https://github.com/user/repo.git external/repo

# Initsialiseeri submodule
git submodule init
git submodule update

# Värskenda submodule'i
git submodule update --remote
```

### Submodule Haldamine

```bash
# Vaata submodule'ite staatust
git submodule status

# Kustuta submodule
git submodule deinit external/repo
git rm external/repo
git commit -m "Remove submodule repo"
```

##  Edasijõudnud Git Käsud

### Git Reflog

```bash
# Vaata kõiki tegevusi
git reflog

# Taasta kaotatud commit
git checkout -b recovery-branch HEAD@{5}

# Taasta kaotatud fail
git checkout HEAD@{1} -- lost-file.txt
```

### Git Bisect

```bash
# Alusta bisect protsessi
git bisect start

# Märgi halb commit
git bisect bad HEAD

# Märgi hea commit
git bisect good v1.0

# Git automaatselt kontrollib commit'e
git bisect run npm test
```

### Git Worktree

```bash
# Loo uus worktree
git worktree add ../feature-branch feature-branch

# Vaata kõiki worktree'e
git worktree list

# Kustuta worktree
git worktree remove ../feature-branch
```

##  Monorepo Struktuur

### Projekti Struktuur

```
my-monorepo/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── packages/
│   ├── frontend/
│   │   ├── package.json
│   │   └── src/
│   ├── backend/
│   │   ├── package.json
│   │   └── src/
│   └── shared/
│       ├── package.json
│       └── src/
├── tools/
│   └── scripts/
├── .gitignore
├── package.json
└── README.md
```

### Root Package.json

```json
{
  "name": "my-monorepo",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "build": "lerna run build",
    "test": "lerna run test",
    "lint": "lerna run lint",
    "clean": "lerna clean"
  },
  "devDependencies": {
    "lerna": "^6.0.0"
  }
}
```

##  Testimine ja Valideerimine

### Git Hook Testimine

```bash
# Tee hook käivitatavaks
chmod +x .git/hooks/pre-commit

# Testi hook'i
echo "test" > test.js
git add test.js
git commit -m "test: testing pre-commit hook"
```

### Workflow Testimine

```bash
# Testi workflow'i kohalikult
act -j test

# Testi konkreetset event'i
act push -W .github/workflows/ci.yml
```

##  Lisapraktika Ülesanded

### Ülesanne 1: GitHub Actions Workflow

Loo GitHub Actions workflow, mis:
- Käivitub igal push'il ja pull request'il
- Installib sõltuvused
- Käivitab testid
- Ehitab projekti
- Uploadib build artifacts

### Ülesanne 2: Git Hooks

Implementeeri Git hooks, mis:
- Kontrollivad koodi kvaliteeti
- Valideerivad commit sõnumeid
- Käivitavad automatiseeritud testid
- Kontrollivad faili suurusi

### Ülesanne 3: Monorepo Haldamine

Loo monorepo struktuur, mis:
- Kasutab workspaces
- Haldab mitut paketti
- Keskse CI/CD pipeline'i
- Jagatud konfiguratsioone

##  Kasulikud Ressursid

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Git Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Monorepo Best Practices](https://monorepo.tools/)

##  Hindamine

- **GitHub Actions (40%):** Workflow'ide loomine ja konfigureerimine
- **Git Hooks (30%):** Automatiseeritud kontrollide implementeerimine
- **Edasijõudnud Funktsioonid (30%):** Submodules, worktree, monorepo

---

** Edu lisapraktika läbimisel!**
