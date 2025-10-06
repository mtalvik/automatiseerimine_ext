#  Git Labor: Põhitõed (3×45 min)

## Struktuur ja eesmärgid
- Eesmärk: repo loomine, tähenduslikud commit’id, töövoog add → commit → (push)
- Vorm: 3 × 45 min plokki, paaristöö, lühikesed kontrollid

### Blokk 1 (45 min) – Alustamine
- Tegevused: Git seadistus; `git init`; esimene ja teine commit (README + muudatus)
- Kiirküsitlus (fun, 30s): Kumba teed tihemini: Ctrl+Z või commit? 
- Kontrollnimekiri:
  - [ ] Repo olemas, 2 commit’i
  - [ ] Sõnumid selgitavad „miks“
- Kontrollküsimused: Mis vahe on `add` ja `commit` vahel?
- Refleksioon (1–2 min): Mis aitas, mis oli raske? Kui Git oleks loom, mis ta oleks ja miks? 

### Blokk 2 (45 min) – Töövoog ja nähtavus
- Tegevused: uus fail → `add/commit`; `git status`/`git log`; (võimalusel) remote + `push`
- Kiirküsitlus (fun, 30s): Mis on parem commit‑sõnum? A) "fix" B) "Lisa README, et selgitada paigaldust" 
- Kontrollnimekiri:
  - [ ] ≥3 commit’i
  - [ ] Töövoog on põhjendatud (millal add/commit/push)
- Kontrollküsimused: Millal on mõistlik `push` teha?
- Refleksioon (1–2 min): Mis infot saad `git log --oneline` väljundist? Kirjelda seda kui ilmakaarti 

### Blokk 3 (45 min) – Kvaliteet ja `.gitignore`
- Tegevused: lisa `.gitignore` (nt `*.log`, `__pycache__/`) ja põhjenda; veel 1 selgitav commit
- Kiirküsitlus (fun, 30s): Kas `.mp4` faile peaks repos hoidma? A) jah B) ei C) ainult kassivideod 
- Kontrollnimekiri:
  - [ ] `.gitignore` olemas ja põhjendatud
  - [ ] Viimane commit‑sõnum seletab „miks“
- Kontrollküsimused: Mida ei tohi repos hoida ja miks?
- Refleksioon (1–2 min): Mida teeksid järgmisel korral teisiti? 6 sõnaga mikro‑päevik.

---

#  Git Labor: GitHub Actions


---

##  Õpiväljundid

Pärast laborit oskate:
- Seadistada Git keskkonna ja teha esimesi commit'e
- Hallata branch'e ja merge'ida muudatusi
- Töötada GitHub'is ja teha pull request'e
- Lahendada merge konflikte
- Kasutada Git Flow workflow'i

---

##  Samm 1: Git Basics ja Kohalik Kasutamine (45 min)

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

##  Samm 2: Branching ja Merging (45 min)

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

##  Samm 3: GitHub ja Remote Repositories (45 min)

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

##  Kiire lõbusaine: Commit Meme Check (60s)
- Kirjuta üks hea commit‑sõnum kui see oleks meemi pealkiri (ilma ära keeramata sisulist mõtet). 
- Näide: "docs(readme): päästan õpetaja närvid ja lisan setup'i"

---

##  Boonus (valikuline, kui lõpetasid kiiremini)

**Kui sul on aega järele**, proovi neid lisaülesandeid:

### Boonus 1: Git Tags ja Releases (10 min)
```bash
# Loo tag
git tag -a v1.0 -m "Esimene versioon"

# Vaata kõiki tag'e
git tag

# Push tag'id GitHubi
git push origin v1.0
git push origin --tags

# Loo GitHub'is release (veebi kaudu)
```

### Boonus 2: Git Aliases (5 min)
```bash
# Loo lühendid
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"

# Nüüd saad kasutada:
git st
git lg
```

### Boonus 3: Git Stash (10 min)
```bash
# Tee muudatusi, mis sa ei taha veel commit'ida
echo "Poolik töö" >> calculator.py

# Salvesta ajutiselt
git stash

# Vaata stash'e
git stash list

# Taasta stash
git stash pop
```

### Boonus 4: GitHub README Ilu (15 min)
Lisa oma README.md-le:
- Badge'id (näiteks: ![GitHub](https://img.shields.io/github/stars/USERNAME/REPO))
- Illustratsioonid või GIF'id
- Sisukord (Table of Contents)
- Code examples koos syntax highlighting'uga
- Emojid 

**Vaata täiendavaid edasijõudnud ülesandeid:** `lisapraktika.md`