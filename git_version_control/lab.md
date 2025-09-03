# Git Version Control Lab: Git & GitHub Actions

**Kestus:** 2 tundi  
**Eesmärk:** Praktiliselt harjutada kõiki Git'i peamisi funktsioone

---

## 🎯 Samm 1: Git Basics ja Kohalik Kasutamine (45 min)

### Harjutus 1.1: Git Setup ja Esimene Repository (15 min)

**Seadistage Git:**
```bash
# Kontrollige, kas Git on installeeritud
git --version

# Seadistage kasutajainfo (kasutage oma andmeid)
git config --global user.name "Teie Nimi"
git config --global user.email "teie.email@example.com"

# Kontrollige seadistusi
git config --list

# Seadistage editor (valikuline)
git config --global core.editor "code --wait"  # VS Code
```

**Looge esimene repository:**
```bash
# Looge kaust
mkdir git-practice-lab
cd git-practice-lab

# Algatage Git repository
git init

# Kontrollige olukorda
git status

# Looge esimene fail
echo "# Git Practice Lab" > README.md
echo "See on minu Git harjutuste projekt." >> README.md

# Tehke esimene commit
git add README.md
git status
git commit -m "Esimene commit: lisa README"

# Vaadake ajalugu
git log
git log --oneline
```

**Kontrollpunkt:** Teil peaks olema Git repository ühe commit'iga.

### Harjutus 1.2: Põhiline Git Workflow (15 min)

**Looge ja muutke faile:**
```bash
# Looge Python script
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print("Calculator: 2 + 3 =", add(2, 3))
EOF

# Kontrollige olukorda
git status

# Lisage fail ja tehke commit
git add calculator.py
git status
git commit -m "Lisa lihtne kalkulaator"

# Muutke faili
echo "" >> calculator.py
echo "def multiply(a, b):" >> calculator.py
echo "    return a * b" >> calculator.py

# Vaadake muudatusi
git diff
git status

# Commit muudatused
git add calculator.py
git commit -m "Lisa korrutamise funktsioon"
```

**Harjutage erinevaid Git käske:**
```bash
# Vaadake commit'ide ajalugu
git log --oneline --graph

# Vaadake konkreetse commit'i detaile
git show HEAD
git show HEAD~1

# Looge veel faile
echo "print('Tere, Git!')" > hello.py
echo "*.pyc" > .gitignore
echo "__pycache__/" >> .gitignore

# Lisage kõik korraga
git add .
git status
git commit -m "Lisa hello script ja gitignore"
```

**Kontrollpunkt:** Teil peaks olema 3-4 commit'i erinevate failidega.

### Harjutus 1.3: Advanced Git Operations (15 min)

**Staging area vahele jätmine:**
```bash
# Muutke calculator.py
echo "" >> calculator.py
echo "def divide(a, b):" >> calculator.py
echo "    if b != 0:" >> calculator.py
echo "        return a / b" >> calculator.py
echo "    return 'Error: Division by zero'" >> calculator.py

# Commit otse ilma git add'ita
git commit -am "Lisa jagamise funktsioon"

# Vaadake erinevusi
git diff HEAD~1
git show --stat HEAD
```

**Failide kustutamine ja ümbernimetamine:**
```bash
# Looge ajutine fail
echo "Ajutine sisu" > temp.txt
git add temp.txt
git commit -m "Lisa ajutine fail"

# Kustutage fail
git rm temp.txt
git status
git commit -m "Kustuta ajutine fail"

# Nimetage fail ümber
git mv hello.py greeting.py
git status
git commit -m "Nimeta hello.py ümber greeting.py"
```

**Muudatuste tagasivõtmine:**
```bash
# Tehke mõni muudatus
echo "Vigane kood" >> calculator.py

# Vaadake muudatust
git diff

# Võtke muudatus tagasi
git checkout -- calculator.py

# Kontrollige
git status

# Tehke muudatus ja lisage staging'u
echo "Veel üks muudatus" >> calculator.py
git add calculator.py

# Eemaldage staging'st
git reset HEAD calculator.py
git status

# Tühistage töökausta muudatus
git checkout -- calculator.py
```

**Kontrollpunkt:** Oskate faile kustutada, ümbernimetada ja muudatusi tühistada.

---

## 🎯 Samm 2: Branching ja Merging (45 min)

### Harjutus 2.1: Harude Loomine ja Haldamine (20 min)

**Looge uus branch:**
```bash
# Vaadake praeguseid branch'e
git branch

# Looge uus branch
git branch feature/advanced-math

# Vahetage branch'i
git checkout feature/advanced-math

# Või tehke mõlemad koos
git checkout -b feature/string-utils

# Kontrollige, kus olete
git branch
```

**Arendage eri branch'ides:**
```bash
# Olge feature/string-utils branch'is
cat > string_utils.py << 'EOF'
def reverse_string(text):
    return text[::-1]

def count_words(text):
    return len(text.split())

def capitalize_words(text):
    return ' '.join(word.capitalize() for word in text.split())

if __name__ == "__main__":
    test_text = "tere git maailm"
    print("Original:", test_text)
    print("Reversed:", reverse_string(test_text))
    print("Word count:", count_words(test_text))
    print("Capitalized:", capitalize_words(test_text))
EOF

git add string_utils.py
git commit -m "Lisa string utiliitide moodul"

# Minge teise branch'i
git checkout feature/advanced-math

cat > advanced_math.py << 'EOF'
import math

def power(base, exponent):
    return base ** exponent

def square_root(number):
    return math.sqrt(number)

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    print("2^3 =", power(2, 3))
    print("sqrt(16) =", square_root(16))
    print("5! =", factorial(5))
EOF

git add advanced_math.py
git commit -m "Lisa täpsema matemaatika moodul"

# Vaadake branch'ide ajalugu
git log --oneline --graph --all
```

**Kontrollpunkt:** Teil on kaks feature branch'i erinevate failidega.

### Harjutus 2.2: Branch'ide Merging (15 min)

**Merge esimene branch main'i:**
```bash
# Minge main branch'i
git checkout main

# Merge string-utils
git merge feature/string-utils

# Vaadake tulemust
git log --oneline --graph
ls -la

# Testage merged koodi
python3 string_utils.py
```

**Merge teine branch:**
```bash
# Merge advanced-math
git merge feature/advanced-math

# Vaadake tulemust
git log --oneline --graph --all
ls -la

# Testage
python3 advanced_math.py
```

**Kontrollpunkt:** Mõlemad feature'id on main'is merge'itud.

### Harjutus 2.3: Merge Conflicts (10 min)

**Looge konflikt:**
```bash
# Looge kaks branch'i, mis muudavad sama faili
git checkout -b fix/calculator-output

# Muutke calculator.py
sed -i 's/print("Calculator: 2 + 3 =", add(2, 3))/print("Kalkulaator: 2 + 3 =", add(2, 3))/' calculator.py

git add calculator.py
git commit -m "Muuda väljund eestikeelseks"

# Minge main'i ja tehke konfliktne muudatus
git checkout main

# Muutke sama rida teisiti
sed -i 's/print("Calculator: 2 + 3 =", add(2, 3))/print("CALC RESULT: 2 + 3 =", add(2, 3))/' calculator.py

git add calculator.py
git commit -m "Muuda väljund lühemaks"

# Proovige merge'ida - konflikt!
git merge fix/calculator-output
```

**Lahendage konflikt:**
```bash
# Vaadake konfliktset faili
cat calculator.py

# Redigeerige käsitsi või kasutage merge tool'i
# Eemaldage konfliktimärgid ja valige õige versioon

# Näiteks jätke eestikeelne versioon:
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    return 'Error: Division by zero'

if __name__ == "__main__":
    print("Kalkulaator: 2 + 3 =", add(2, 3))
EOF

# Lõpetage merge
git add calculator.py
git status
git commit

# Vaadake tulemust
git log --oneline --graph
```

**Kontrollpunkt:** Olete edukalt merge konflikti lahendanud.

---

## 🎯 Samm 3: GitHub ja Remote Repositories (45 min)

### Harjutus 3.1: GitHub Setup ja SSH (15 min)

**SSH võtmete seadistamine:**
```bash
# Kontrollige, kas SSH võtmed on olemas
ls -la ~/.ssh/

# Kui pole, looge uued (kasutage oma email'i)
ssh-keygen -t ed25519 -C "teie.email@example.com"

# Käivitage SSH agent
eval "$(ssh-agent -s)"

# Lisage võti agendile
ssh-add ~/.ssh/id_ed25519

# Kopeerige avalik võti
cat ~/.ssh/id_ed25519.pub
```

**GitHub'is:**
1. Minge Settings → SSH and GPG keys
2. Click "New SSH key"
3. Kleepige avalik võti
4. Save

**Testuge SSH ühendust:**
```bash
ssh -T git@github.com
```

**Kontrollpunkt:** SSH ühendus GitHub'iga töötab.

### Harjutus 3.2: Remote Repository ja Collaboration (20 min)

**GitHub'is looge uus repository:**
1. Click "New repository"
2. Nimi: `git-practice-lab`
3. Public repository
4. ÄRA lisa README (meil on juba)
5. Create repository

**Ühendage kohalik repo GitHub'iga:**
```bash
# Lisage remote
git remote add origin git@github.com:TEIE-KASUTAJANIMI/git-practice-lab.git

# Kontrollige remote'e
git remote -v

# Push'ige esimest korda
git push -u origin main

# Push'ige kõik branch'id
git push origin feature/advanced-math
git push origin fix/calculator-output
```

**Pull/Push workflow:**
```bash
# Simuleerige meeskonnatööd
# GitHub'is tehke muudatus otse veebi kaudu:
# 1. Avage README.md
# 2. Lisage rida "Muudatus GitHub'is"
# 3. Commit directly to main

# Kohalikult pull'ige muudatus
git pull origin main

# Tehke kohalik muudatus
echo "" >> README.md
echo "Kohalik muudatus" >> README.md

git add README.md
git commit -m "Lisa kohalik muudatus"

# Push'ige
git push origin main
```

**Kontrollpunkt:** Kohalik ja remote repository on sünkroniseeritud.

### Harjutus 3.3: Pull Requests (10 min)

**Looge uus feature:**
```bash
# Looge uus branch
git checkout -b feature/documentation

# Looge dokumentatsioon
cat > USAGE.md << 'EOF'
# Git Practice Lab Kasutamine

## Failide kirjeldus

- `calculator.py` - Põhilised matemaatilised operatsioonid
- `advanced_math.py` - Täpsemad matemaatikafunktsioonid  
- `string_utils.py` - Stringide töötlemise utiliidid
- `greeting.py` - Lihtne tervitusprogramm

## Kasutamine

```bash
python3 calculator.py
python3 advanced_math.py
python3 string_utils.py
python3 greeting.py
```

## Arendamine

1. Fork'ige repository
2. Looge feature branch
3. Tehke muudatused
4. Looge Pull Request
EOF

git add USAGE.md
git commit -m "Lisa kasutamise dokumentatsioon"

# Push'ige branch
git push origin feature/documentation
```

**GitHub'is looge Pull Request:**
1. Minge oma repository lehele
2. Click "Compare & pull request"
3. Kirjutage hea pealkiri ja kirjeldus
4. Create pull request
5. Merge pull request
6. Delete branch

**Kohalikult puhastage:**
```bash
git checkout main
git pull origin main
git branch -d feature/documentation
git push origin --delete feature/documentation
```

**Kontrollpunkt:** Olete edukalt teinud Pull Request'i workflow.

---

## 🎯 Samm 4: Advanced Git Features (15 min)

### Harjutus 4.1: Git Rebase ja History Cleanup

**Interactive Rebase:**
```bash
# Looge mitu väikest commit'i
echo "# TODO" >> TODO.md
git add TODO.md
git commit -m "Lisa TODO fail"

echo "- Lisa testid" >> TODO.md
git add TODO.md
git commit -m "Lisa esimene ülesanne"

echo "- Paranda dokumentatsiooni" >> TODO.md
git add TODO.md
git commit -m "Lisa teine ülesanne"

echo "- Optimiseeri kood" >> TODO.md
git add TODO.md
git commit -m "Lisa kolmas ülesanne"

# Vaadake ajalugu
git log --oneline -5

# Ühendage viimased 4 commit'i üheks
git rebase -i HEAD~4

# Editor avaneb - muutke:
# pick → squash (või s) viimastel 3 real
# Jätke esimene "pick"

# Salvestage ja sulgege editor
# Uus editor commit sõnumiga - redigeerige vajadusel
```

### Harjutus 4.2: Git Stash

```bash
# Alustage muudatusi
echo "Pooleli töö" >> calculator.py

# Aga vajate kiiresti minna teise branch'i
git stash

# Kontrollige olukorda
git status

# Minge teise branch'i, tehke tööd
git checkout feature/advanced-math
echo "Kiire parandus" >> advanced_math.py
git add advanced_math.py
git commit -m "Kiire parandus advanced math'is"

# Minge tagasi ja taastage stash
git checkout main
git stash pop

# Lõpetage töö
git add calculator.py
git commit -m "Lõpeta pooleli töö"
```

### Harjutus 4.3: Cherry-pick

```bash
# Oletame, et feature branch'is on hea commit, mida tahate main'is
git log --oneline feature/advanced-math

# Võtke konkreetne commit main'i (kasutage õiget hash'i)
git cherry-pick COMMIT-HASH

# Vaadake tulemust
git log --oneline -3
```

**Kontrollpunkt:** Oskate kasutada Git'i täpsemaid funktsioone.

---

## 🎯 Kokkuvõte ja Kontrolljaarati (10 min)

### Lõplik kontroll

**Kontrollige oma oskusi:**
```bash
# 1. Repository struktuur
ls -la
git log --oneline --graph -10

# 2. Remote'id
git remote -v

# 3. Branch'id
git branch -a

# 4. Viimased commit'id
git log --oneline -5

# 5. Git config
git config --list | grep user
```

### Mida te nüüd oskate:

- Git'i seadistamine ja põhikäsud
- Staging area kasutamine
- Branch'ide loomine ja merge'imine
- Merge konfliktide lahendamine
- SSH seadistamine GitHub'iga
- Remote repository workflow
- Pull Request'ide tegemine
- Advanced Git features (rebase, stash, cherry-pick)

### Järgmised sammud:

1. **Harjutage iga päev** - Git on nagu jalgrattasõit
2. **Liituge open source projektidega** - tehke PR'e
3. **Seadistage Git aliases** - kiiremaks töötamiseks
4. **Õppige Git GUI tööriistu** - GitKraken, SourceTree
5. **Uurige GitHub Actions** - CI/CD automatiseerimine

### Git Aliases (boonusülesanne):

```bash
# Kasulikud aliased
git config --global alias.st status
git config --global alias.co checkout  
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
git config --global alias.lg 'log --oneline --graph --all'

# Testage
git st
git lg
```

**🎉 Õnnitleme! Olete läbinud Git'i põhilise väljaõppe.**

---

## 🚀 **BOONUSÜLESANDED** (juba Git'i oskajatele)

### Samm B1: Advanced Git Features (30 min)

#### Interactive Rebase - Commit'ide Ühendamine
```bash
# Looge mitu väikest commiti
echo "Feature 1" > feature1.txt && git add . && git commit -m "Add feature 1"
echo "Feature 2" > feature2.txt && git add . && git commit -m "Add feature 2" 
echo "Fix typo" >> feature1.txt && git add . && git commit -m "Fix typo in feature 1"

# Interactive rebase - ühendage commitid
git rebase -i HEAD~3
# Muutke "pick" -> "squash" kahel viimasel real
# Salvestage ja sulgege editor
```

#### Cherry-pick ja Advanced Stash
```bash
# Stash koos metadata'ga
echo "Pooleli töö" > wip.txt
git add .
git stash push -m "WIP: new authentication feature"

# Cherry-pick - kopeerige konkreetne commit
git log --oneline -5  # Leidke commit hash
git cherry-pick <commit-hash>

# Stash management
git stash list
git stash show stash@{0}
git stash pop  # või git stash apply
```

#### Advanced Log ja Blame
```bash
# Graafiline commit history
git log --graph --pretty=format:'%h -%d %s (%cr) <%an>' --abbrev-commit --all

# Failispetsiifilised muutused
git log --follow -p -- filename.txt

# Blame - kes kirjutas millise rea
git blame README.md
git blame -L 10,20 README.md  # Ainult read 10-20

# Commit range'ide võrdlus
git diff main..feature-branch
git log main..feature-branch --oneline
```

### Samm B2: Git Hooks ja Workflow Automation (25 min)

#### Pre-commit Hook (automaatne kvaliteedikontroll)
```bash
# Looge pre-commit hook
mkdir -p .git/hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔍 Kontrollime koodi enne commit'i..."

# Kontrolli, et ei commitita suuri faile
find . -size +1M -type f -exec ls -lh {} \; | grep -E '\.(jpg|png|gif|mp4|zip)$' 
if [ $? -eq 0 ]; then
  echo "❌ Suured failid leitud! Kasutage Git LFS."
  exit 1
fi

# Kontrolli, et ei ole debug koodi
grep -r "console.log\|debugger\|TODO" --include="*.js" .
if [ $? -eq 0 ]; then
  echo "⚠️  Debug kood leitud! Kas olete kindel?"
  echo "Jätkamiseks vajutage Enter, katkestamiseks Ctrl+C"
  read
fi

echo "✅ Pre-commit kontroll OK!"
EOF

chmod +x .git/hooks/pre-commit

# Testige hook'i
echo "console.log('test')" > debug.js
git add debug.js
git commit -m "Test hook" # Hook küsib kinnitust
```

#### Post-merge Hook (automaatne cleanup)
```bash
cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash
echo "🧹 Post-merge cleanup..."

# Kustuta vanale branch'id
git branch --merged | grep -v "\*\|main\|master" | xargs -n 1 git branch -d

# Update dependencies kui package.json muutus
if [ -f package.json ] && git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "package.json"; then
  echo "📦 package.json muutus, updatein dependencies..."
  npm install
fi

echo "✅ Post-merge cleanup lõpetatud!"
EOF

chmod +x .git/hooks/post-merge
```

### Samm B3: Git Submodules ja Worktrees (20 min)

#### Submodules - Dependency Management
```bash
# Lisa library submodule'ina
git submodule add https://github.com/lodash/lodash.git vendor/lodash
git commit -m "Add lodash as submodule"

# Clone repo koos submodule'itega
git clone --recursive <your-repo-url>

# Update submodule'id
git submodule update --remote --merge

# Eemalda submodule
git submodule deinit vendor/lodash
git rm vendor/lodash
```

#### Worktrees - Parallel Development
```bash
# Loo worktree uue feature jaoks
git worktree add ../feature-payment feature/payment
cd ../feature-payment
# Nüüd saate töödata samaaegselt main ja feature branch'idega

# List worktrees
git worktree list

# Remove worktree
cd ../git-practice-lab
git worktree remove ../feature-payment
```

### Samm B4: Advanced Git Performance (15 min)

#### Git LFS - Large File Storage
```bash
# Installi Git LFS
git lfs install

# Track suured failid
git lfs track "*.png"
git lfs track "*.jpg"
git lfs track "*.pdf"
git add .gitattributes

# Test LFS
echo "Large file content" > large-file.png
git add large-file.png
git commit -m "Add large file with LFS"
```

#### Repository Optimization
```bash
# Cleanup unreachable objects
git gc --aggressive --prune=now

# Shallow clone performance'iks
git clone --depth 1 <repo-url> quick-clone

# Partial clone (Git 2.19+)
git clone --filter=blob:none <repo-url> partial-clone
```

### Samm B5: Expert Level Debugging (25 min)

#### Git Bisect - Bug Hunt
```bash
# Simuleerige bug'i otsimist
# Looge 10 commiti, millest üks on "broken"
for i in {1..10}; do
  if [ $i -eq 7 ]; then
    echo "broken code" > app.js
  else
    echo "good code $i" > app.js
  fi
  git add app.js
  git commit -m "Version $i"
done

# Kasuta bisect bug'i leidmiseks
git bisect start
git bisect bad HEAD
git bisect good HEAD~10

# Test iga commit (Git pakub)
while true; do
  if grep -q "broken" app.js; then
    git bisect bad
  else
    git bisect good
  fi
  # Jätka kuni Git leiab probleemse commiti
done

git bisect reset
```

#### Custom Git Commands
```bash
# Looge custom Git command
mkdir -p ~/.local/bin
cat > ~/.local/bin/git-summary << 'EOF'
#!/bin/bash
echo "📊 Repository Summary:"
echo "====================="
echo "📍 Current branch: $(git branch --show-current)"
echo "📈 Total commits: $(git rev-list --count HEAD)"
echo "👥 Contributors: $(git log --format='%an' | sort -u | wc -l)"
echo "⏰ Last commit: $(git log -1 --format='%cr')"
echo "📝 Lines of code:"
git ls-files | xargs wc -l | tail -1
echo "🌿 Branches:"
git branch -a | head -5
EOF

chmod +x ~/.local/bin/git-summary

# Kasutage: git summary
export PATH="$HOME/.local/bin:$PATH"
git summary
```

#### Advanced Conflict Resolution
```bash
# Seadista merge tool
git config --global merge.tool vimdiff
# või
git config --global merge.tool code

# 3-way merge conflicts
git config --global mergetool.keepBackup false

# Resolve konflikti merge tool'iga
# (simuleerige konflikti ja kasutage)
git mergetool
```

### Samm B6: Git Flow ja Release Management (20 min)

```bash
# Git Flow setup (kui installitud)
git flow init

# Feature development
git flow feature start user-authentication
echo "auth code" > auth.js
git add auth.js && git commit -m "Add authentication"
git flow feature finish user-authentication

# Release management
git flow release start v1.0.0
echo "1.0.0" > VERSION
git add VERSION && git commit -m "Version bump to 1.0.0"
git flow release finish v1.0.0

# Hotfix
git flow hotfix start critical-security-fix
echo "security fix" > security.patch
git add security.patch && git commit -m "Security fix"
git flow hotfix finish critical-security-fix
```

### Samm B7: Git Best Practices Enforcement (15 min)

```bash
# Conventional commits hook
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format!"
    echo "Use: type(scope): description"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo "Example: feat(auth): add user login functionality"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg

# Test conventional commits
git commit -m "feat(auth): add user authentication"
git commit -m "fix: resolve login bug"
```

---

## 📝 Lab'i esitamine

**Esitage järgmine GitHub repository link:**
- Repository nimi: `git-practice-lab`
- Peab sisaldama kõiki harjutuste faile
- Clean Git history nähtav
- Vähemalt üks Pull Request tehtud ja merge'itud

**Hindamiskriteeriumid:**
- Repository õigesti seadistatud (20%)
- Kõik harjutused tehtud (50%)
- Clean Git history (20%)
- Pull Request workflow (10%)

---

*Lab koostatud Git tööstuse parimate praktikate põhjal*