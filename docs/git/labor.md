# Git Labor

**Eeldused:** Käsurea põhitõed, teksti redaktor (VS Code, nano, vim)  
**Platvorm:** Git, GitHub  
**Kestus:** Umbes 3 tundi (võib teha mitmes sessioonis)

## Õpiväljundid

Pärast laborit oskate:

1. **Seadistada** Git keskkonda ja konfigureerida kasutajainfot
2. **Luua** lokaalseid repositooriume ja teha tähenduslikke commit'e
3. **Hallata** branch'e, merge'ida muudatusi ja lahendada konflikte
4. **Ühendada** kohalikku repositooriumi GitHub'iga läbi SSH
5. **Rakendada** pull request workflow'i meeskonnatöös

---

## 1. Git Keskkonna Seadistamine

Esimene samm on kontrollida, et Git on installitud ja õigesti konfigureeritud. Seadistus on ühekordne tegevus, kuid oluline - iga commit salvestab sinu nime ja e-maili.

### 1.1 Installatsioonikontroll

Ava terminal ja kontrolli Git'i olemasolu:
```bash
git --version
```

Oodatav väljund on midagi sarnast:
```
git version 2.40.0
```

Kui Git'i ei ole, paigalda see:

**Windows:**
```bash
winget install --id Git.Git -e --source winget
```

**macOS:**
```bash
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

### 1.2 Kasutajainfo Seadistamine

Git salvestab iga commit'iga sinu nime ja e-maili. Seadista need globaalselt:
```bash
git config --global user.name "Sinu Nimi"
git config --global user.email "sinu.email@example.com"
```

Asenda "Sinu Nimi" ja "sinu.email@example.com" oma tegelike andmetega. Kui töötad kooli arvutis, kasuta kooli e-maili.

Kontrolli seadistust:
```bash
git config --list
```

Peaksid nägema:
```
user.name=Sinu Nimi
user.email=sinu.email@example.com
...
```

### 1.3 Editor Seadistamine (Valikuline)

Git avab mõnikord editori (näiteks commit sõnumite jaoks). Seadista oma eelistatud editor:
```bash
# VS Code
git config --global core.editor "code --wait"

# Nano (lihtne terminali editor)
git config --global core.editor "nano"

# Vim
git config --global core.editor "vim"
```

### Kontrollnimekiri

Enne edasi liikumist veendu:

- [ ] `git --version` töötab ja näitab versiooni
- [ ] `git config user.name` näitab sinu nime
- [ ] `git config user.email` näitab sinu e-maili

---

## 2. Esimene Repositoorium ja Põhitöövoog

Nüüd lood oma esimese Git repositooriumi ja õpid põhilist töövoogu: muuda faile → lisa staging area'sse → tee commit.

### 2.1 Repositooriumi Loomine

Loo uus kataloog ja alusta Git'i kasutamist:
```bash
mkdir git-labor
cd git-labor
git init
```

Väljund peaks olema:
```
Initialized empty Git repository in /path/to/git-labor/.git/
```

Kontrolli, mis toimus:
```bash
ls -la
```

Näed `.git` kataloogi - see sisaldab kogu Git'i andmebaasi.

### 2.2 Esimene Fail ja Commit

Loo README.md fail:
```bash
echo "# Git Labor Projekt" > README.md
echo "See on minu esimene Git repositoorium." >> README.md
```

Kontrolli repositooriumi seisu:
```bash
git status
```

Väljund:
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present
```

Git näitab, et README.md on "untracked" - Git ei jälgi seda veel. Lisa fail staging area'sse:
```bash
git add README.md
```

Kontrolli uuesti:
```bash
git status
```

Nüüd näed:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
```

README.md on nüüd staging area's ja valmis commit'iks. Tee esimene commit:
```bash
git commit -m "Esimene commit: lisa README"
```

Väljund:
```
[main (root-commit) a1b2c3d] Esimene commit: lisa README
 1 file changed, 2 insertions(+)
 create mode 100644 README.md
```

Vaata ajalugu:
```bash
git log
```

Näed oma commit'i koos kõigi detailidega. Kompaktsem vaade:
```bash
git log --oneline
```

### 2.3 Töövoog: Muuda → Add → Commit

Muuda README.md faili:
```bash
echo "" >> README.md
echo "## Projekti eesmärk" >> README.md
echo "Õpime Git'i põhitõdesid." >> README.md
```

Vaata, mis muutus:
```bash
git status
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md
```

Vaata täpseid muudatusi:
```bash
git diff
```

Näed punasega eemaldatud read (pole praegu) ja rohelisega lisatud read.

Lisa muudatused staging area'sse ja commit'i:
```bash
git add README.md
git commit -m "Lisa projekti eesmärk README'sse"
```

### 2.4 Mitme Faili Haldamine

Loo uus Python fail:
```bash
cat > hello.py << 'EOF'
def greet(name):
    return f"Tere, {name}!"

if __name__ == "__main__":
    print(greet("Git"))
EOF
```

Loo veel üks fail:
```bash
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
EOF
```

Kontrolli olukorda:
```bash
git status
```

Näed kahte untracked faili. Lisa mõlemad korraga:
```bash
git add .
```

Punkt (.) tähendab "kõik muudatused praeguses kataloogis". Kontrolli:
```bash
git status
```

Commit:
```bash
git commit -m "Lisa Python skriptid: tervitus ja kalkulaator"
```

Vaata ajalugu graafina:
```bash
git log --oneline --graph
```

### Kontrollnimekiri

- [ ] Sul on Git repositoorium vähemalt 3 commit'iga
- [ ] `git status` näitab "working tree clean"
- [ ] `git log --oneline` näitab kõiki commit'e
- [ ] Mõistad vahet `git add` ja `git commit` vahel

### Troubleshooting

**Probleem:** Teinud commit'i, aga unustas faili lisada.

**Lahendus:** Lisa fail ja kasuta `git commit --amend`:
```bash
echo "# Unustatud fail" > forgotten.txt
git add forgotten.txt
git commit --amend --no-edit
```

**Probleem:** Tahtlikult valed muudatused staging area's.

**Lahendus:** Eemalda staging area'st:
```bash
git reset HEAD fail.txt
```

---

## 3. .gitignore ja Repositooriumi Hügieen

Kõik failid ei peaks repositooriumis olema. Õpime, mida ignoreerida ja miks.

### 3.1 Probleemsed Failid

Loo mõned failid, mida ei peaks versioonihaldusse panema:
```bash
# Log fail
echo "Error: something happened" > debug.log

# Python cache
mkdir __pycache__
touch __pycache__/calculator.cpython-39.pyc

# Keskkonna muutujad
cat > .env << 'EOF'
API_KEY=secret123
DATABASE_URL=postgresql://localhost/db
EOF

# Suur fail (simulatsioon)
echo "Suur video fail" > video.mp4
```

Kontrolli olukorda:
```bash
git status
```

Näed 4 untracked "faili/kausta". Need EI TOHIKS repositooriumisse minna.

### 3.2 .gitignore Loomine

Loo .gitignore fail:
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtuaalsed keskkonnad
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Keskkonna muutujad
.env
.env.local

# Logid
*.log

# OS failid
.DS_Store
Thumbs.db

# Meedia failid
*.mp4
*.avi
*.mov
*.mkv
EOF
```

Kontrolli uuesti:
```bash
git status
```

Nüüd näed ainult `.gitignore` faili untracked'ina. Teised failid on ignoreeritud!

Lisa .gitignore repositooriumisse:
```bash
git add .gitignore
git commit -m "Lisa .gitignore Python projektile"
```

### 3.3 Miks Need Reeglid?

Ava .gitignore ja vaata iga sektsiooni:

**Python cache** - genereeritud failid, mida saab uuesti luua. Ei ole vaja repos.

**Virtuaalsed keskkonnad** - dependency'de koopiad, võivad olla gigabaidid. Kasuta `requirements.txt` asemel.

**IDE seaded** - isiklikud eelistused, ei pruugi teistele sobida.

**Keskkonna muutujad** - sisaldavad saladusi (API võtmed, paroolid). KRIITILISELT OLULINE IGNOREERIDA!

**Logid** - ajutised failid, võivad kasvada suureks.

**OS failid** - operatsioonisüsteemi metadata, pole projekti osa.

**Meedia failid** - suured binaarfailid, mida Git ei oska efektiivselt hallata.

### Kontrollnimekiri

- [ ] `.gitignore` fail on loodud ja committitud
- [ ] Debug.log, .env ja __pycache__ ei ilmu `git status` väljundis
- [ ] Mõistad, miks keskkonna muutujaid ei tohi repositooriumisse panna

### Troubleshooting

**Probleem:** Committisin .env faili enne .gitignore loomist.

**Lahendus:** Eemalda failist repositooriumist (kuid säilita kohalikult):
```bash
git rm --cached .env
git commit -m "Eemalda .env repositooriumist"
```

---

## 4. Branching: Paralleeltöö

Branch'id võimaldavad arendada uusi funktsioone ilma põhikoodi segamata. Õpime branch'ide loomist, vahetamist ja merge'imist.

### 4.1 Branch'ide Vaatamine ja Loomine

Vaata olemasolevaid branch'e:
```bash
git branch
```

Näed ainult `main` (või `master`). Tärn (*) näitab käesolevat branch'i.

Loo uus branch:
```bash
git branch feature/math-operations
```

Kontrolli:
```bash
git branch
```

Nüüd näed kahte branch'i, kuid oled ikka `main` branch'is. Vaheta branch'i:
```bash
git checkout feature/math-operations
```

Väljund:
```
Switched to branch 'feature/math-operations'
```

Või loo ja vaheta ühe käsuga:
```bash
git checkout -b feature/string-utils
```

### 4.2 Töö Branch'is

Oled `feature/string-utils` branch'is. Loo uus fail:
```bash
cat > string_utils.py << 'EOF'
def reverse(text):
    """Pööra string tagurpidi."""
    return text[::-1]

def count_words(text):
    """Loe sõnade arv."""
    return len(text.split())

def to_uppercase(text):
    """Muuda suurtähtedeks."""
    return text.upper()

if __name__ == "__main__":
    sample = "tere git maailm"
    print(f"Original: {sample}")
    print(f"Reversed: {reverse(sample)}")
    print(f"Words: {count_words(sample)}")
    print(f"Uppercase: {to_uppercase(sample)}")
EOF
```

Commit:
```bash
git add string_utils.py
git commit -m "Lisa string utiliitide moodul"
```

Vaheta tagasi main'i:
```bash
git checkout main
```

Kontrolli:
```bash
ls -la
```

`string_utils.py` on kadunud! See on normaalne - see fail on ainult `feature/string-utils` branch'is.

### 4.3 Töö Teises Branch'is

Loo ja vaheta uude branch'i:
```bash
git checkout -b feature/math-operations
```

Lisa calculator.py'sse uued funktsioonid:
```bash
cat >> calculator.py << 'EOF'

def multiply(a, b):
    """Korruta kaks arvu."""
    return a * b

def divide(a, b):
    """Jaga kaks arvu."""
    if b == 0:
        return "Error: jagamine nulliga"
    return a / b

def power(base, exponent):
    """Arvu astendamine."""
    return base ** exponent
EOF
```

Commit:
```bash
git add calculator.py
git commit -m "Lisa korrutamine, jagamine ja astendamine"
```

Vaata branch'ide ajalugu:
```bash
git log --oneline --graph --all
```

Näed mitut "haru" - branch'id on divergeerunud.

### Kontrollnimekiri

- [ ] Oskad luua uut branch'i
- [ ] Oskad branch'ide vahel vahetada
- [ ] Mõistad, et iga branch on eraldatud "paralleeluniversum"
- [ ] `git log --oneline --graph --all` näitab mitut branch'i

---

## 5. Merging: Branch'ide Ühendamine

Nüüd ühendame branch'ide tööd tagasi main'i.

### 5.1 Fast-Forward Merge

Vaheta main'i:
```bash
git checkout main
```

Merge string-utils branch:
```bash
git merge feature/string-utils
```

Väljund:
```
Updating a1b2c3d..e4f5g6h
Fast-forward
 string_utils.py | 20 ++++++++++++++++++++
 1 file changed, 20 insertions(+)
 create mode 100644 string_utils.py
```

"Fast-forward" tähendab, et main ei ole vahepeal muutunud - lihtsalt liigutas osuti edasi.

Kontrolli:
```bash
ls -la
```

`string_utils.py` on nüüd main'is!

### 5.2 Three-Way Merge

Merge math-operations branch:
```bash
git merge feature/math-operations
```

Git avab editori merge commit sõnumiga. Salvesta ja sulge.

Väljund:
```
Merge made by the 'recursive' strategy.
 calculator.py | 15 +++++++++++++++
 1 file changed, 15 insertions(+)
```

See on "three-way merge" - Git lõi merge commit'i, sest mõlemad branch'id muutsid ajalugu paralleelselt.

Vaata ajalugu:
```bash
git log --oneline --graph --all
```

Näed merge commit'i kahe "vanemaga".

### 5.3 Puhastamine

Kustuta merged branch'id:
```bash
git branch -d feature/string-utils
git branch -d feature/math-operations
```

Kontrolli:
```bash
git branch
```

Jäi ainult `main`.

### Kontrollnimekiri

- [ ] Merge'isid vähemalt 2 branch'i main'i
- [ ] Mõistad vahet fast-forward ja three-way merge vahel
- [ ] Oskad branch'e kustutada pärast merge'imist

---

## 6. Merge Konfliktid

Konfliktid juhtuvad, kui kaks branch'i muudavad sama faili sama kohta. Õpime neid lahendama.

### 6.1 Konflikti Loomine

Loo kaks branch'i, mis muudavad sama rida:
```bash
git checkout -b fix/greeting-estonian
```

Muuda hello.py:
```bash
cat > hello.py << 'EOF'
def greet(name):
    return f"Tere, {name}! Kuidas sul läheb?"

if __name__ == "__main__":
    print(greet("Git"))
EOF
```

Commit:
```bash
git add hello.py
git commit -m "Lisa pikem tervitus eesti keeles"
```

Vaheta main'i ja tee konfliktne muudatus:
```bash
git checkout main
cat > hello.py << 'EOF'
def greet(name):
    return f"Hello, {name}! Welcome!"

if __name__ == "__main__":
    print(greet("Git"))
EOF
```

Commit:
```bash
git add hello.py
git commit -m "Muuda tervitus inglise keeleks"
```

Nüüd merge'i - konflikt!
```bash
git merge fix/greeting-estonian
```

Väljund:
```
Auto-merging hello.py
CONFLICT (content): Merge conflict in hello.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 6.2 Konflikti Lahendamine

Vaata konflikti:
```bash
git status
```
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   hello.py
```

Ava hello.py:
```bash
cat hello.py
```

Näed:
```python
def greet(name):
<<<<<<< HEAD
    return f"Hello, {name}! Welcome!"
=======
    return f"Tere, {name}! Kuidas sul läheb?"
>>>>>>> fix/greeting-estonian

if __name__ == "__main__":
    print(greet("Git"))
```

Konfliktimärgid:
- `<<<<<<< HEAD` - sinu praegune versioon (main)
- `=======` - eraldaja
- `>>>>>>> fix/greeting-estonian` - merge'itav versioon

Redigeeri faili ja vali või kombineeri versioone:
```bash
cat > hello.py << 'EOF'
def greet(name):
    """Tervitab kasutajat nii eesti kui inglise keeles."""
    return f"Tere / Hello, {name}!"

if __name__ == "__main__":
    print(greet("Git"))
EOF
```

Märgi konflikt lahendatuks:
```bash
git add hello.py
```

Lõpeta merge:
```bash
git commit
```

Git avab editori vaikimisi merge sõnumiga. Salvesta ja sulge.

Kontrolli ajalugu:
```bash
git log --oneline --graph --all
```

### Kontrollnimekiri

- [ ] Lõid ja lahendas merge konflikti
- [ ] Mõistad konfliktimärkide tähendust
- [ ] Oskad konflikti lahendada ja merge'i lõpetada

---

## 7. GitHub: Remote Repository

Nüüd ühendame kohaliku repositooriumi GitHub'iga.

### 7.1 SSH Võtmete Seadistamine

Kontrolli, kas SSH võtmed on olemas:
```bash
ls -la ~/.ssh/
```

Kui näed `id_ed25519` ja `id_ed25519.pub`, võtmed on olemas. Kui mitte, loo need:
```bash
ssh-keygen -t ed25519 -C "sinu.email@example.com"
```

Vajuta Enter kõigile küsimustele (vaikevastused on OK).

Käivita SSH agent:
```bash
eval "$(ssh-agent -s)"
```

Lisa võti:
```bash
ssh-add ~/.ssh/id_ed25519
```

Kopeeri avalik võti:
```bash
cat ~/.ssh/id_ed25519.pub
```

Kopeeri väljund lõikelauale.

### 7.2 SSH Võtme Lisamine GitHub'i

1. Mine GitHub'i → Settings (paremal üleval ikoon → Settings)
2. Külgmenüüs: SSH and GPG keys
3. Click "New SSH key"
4. Title: "Minu arvuti" (või muu kirjeldav nimi)
5. Key: kleebi kopeeritud avalik võti
6. Click "Add SSH key"

Testi ühendust:
```bash
ssh -T git@github.com
```

Oodatav väljund:
```
Hi TEIE-KASUTAJANIMI! You've successfully authenticated, but GitHub does not provide shell access.
```

### 7.3 GitHub Repository Loomine

1. Mine GitHub'i
2. Click "+" paremal üleval → "New repository"
3. Repository name: `git-labor`
4. Jäta repository tühjaks (EI lisa README, .gitignore ega license)
5. Click "Create repository"

GitHub näitab sulle juhiseid. Kasuta "push an existing repository from the command line" sektsiooni.

### 7.4 Remote'i Ühendamine

Lisa remote repositoorium:
```bash
git remote add origin git@github.com:TEIE-KASUTAJANIMI/git-labor.git
```

Asenda `TEIE-KASUTAJANIMI` oma GitHub kasutajanimega.

Kontrolli:
```bash
git remote -v
```

Väljund:
```
origin  git@github.com:TEIE-KASUTAJANIMI/git-labor.git (fetch)
origin  git@github.com:TEIE-KASUTAJANIMI/git-labor.git (push)
```

Push esimest korda:
```bash
git push -u origin main
```

`-u` seab tracking'u - edaspidi piisab lihtsalt `git push`.

### 7.5 Push ja Pull Workflow

Tee kohalik muudatus:
```bash
echo "" >> README.md
echo "## GitHub'i Integratsioon" >> README.md
echo "See repositoorium on nüüd GitHub'is!" >> README.md

git add README.md
git commit -m "Dokumenteeri GitHub'i integratsiooni"
```

Push GitHub'i:
```bash
git push
```

Simuleerime meeskonnatööd. Mine GitHub'i (veebi kaudu):

1. Ava README.md fail
2. Click "Edit" (pliiatsi ikoon)
3. Lisa rida: "Muudatus tehtud otse GitHub'is"
4. Scroll alla → "Commit changes"
5. Lisa commit sõnum: "Lisa märkus GitHub'ist"
6. Click "Commit changes"

Nüüd GitHub on ees. Pull muudatused:
```bash
git pull
```

Väljund:
```
remote: Enumerating objects: 5, done.
...
Updating a1b2c3d..e4f5g6h
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
```

Vaata README.md:
```bash
cat README.md
```

Näed GitHub'is tehtud muudatust!

### Kontrollnimekiri

- [ ] SSH võtmed on seadistatud ja testitud
- [ ] GitHub repositoorium on loodud
- [ ] Remote on ühendatud: `git remote -v` näitab origin'i
- [ ] Push ja pull workflow töötab
- [ ] Oskad muuta faile nii lokaalselt kui GitHub'is

---

## 8. Pull Requests ja Koostöö

Pull request (PR) on GitHub'i mehhanism koodi ülevaatuseks enne merge'imist.

### 8.1 Feature Branch Loomine

Loo uus feature:
```bash
git checkout -b feature/documentation
```

Loo USAGE.md fail:
```bash
cat > USAGE.md << 'EOF'
# Kasutamisjuhend

## Projektis Olevad Skriptid

### hello.py
Lihtne tervitusprogramm, mis demonstreerib funktsioonide kasutamist.

Kasutamine:
```bash
python3 hello.py
```

### calculator.py
Põhilised ja täiustatud matemaatilised operatsioonid.

Kasutamine:
```bash
python3 calculator.py
```

### string_utils.py
Stringide töötlemise utiliidid.

Kasutamine:
```bash
python3 string_utils.py
```

## Arendamine

1. Loo uus branch: `git checkout -b feature/uus-funktsioon`
2. Tee muudatused
3. Commit: `git commit -m "Lisa uus funktsioon"`
4. Push: `git push origin feature/uus-funktsioon`
5. Tee Pull Request GitHub'is

## Paigaldamine
```bash
git clone git@github.com:KASUTAJANIMI/git-labor.git
cd git-labor
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt  # kui on dependency'sid
```
EOF
```

Commit ja push:
```bash
git add USAGE.md
git commit -m "Lisa kasutamisjuhend dokumentatsioon"
git push -u origin feature/documentation
```

### 8.2 Pull Request'i Loomine

Mine GitHub'i (veebilehitseja):

1. Näed bänneri: "feature/documentation had recent pushes"
2. Click "Compare & pull request"
3. Täida PR vorm:
   - **Title:** Lisa kasutamisjuhend
   - **Description:**
   
```
   ## Muudatused
   - Lisasin USAGE.md faili
   - Dokumenteeritud kõik skriptid
   - Lisatud paigaldamisjuhised
   
   ## Kontrollnimekiri
   - [x] Dokumentatsioon on täielik
   - [x] Näited on testitud
   - [x] Failid on õigesti vormindatud
   
```
4. Click "Create pull request"

### 8.3 Code Review ja Merge

Enda PR puhul (reaalses töös teeks keegi teine):

1. Vaata "Files changed" tab'i
2. Lisa kommentaar reale (hõljuta rea number kohale, click +)
3. Näiteks: "Hea näide! Võib lisada ka vigade käsitlust."
4. Click "Start review" → "Submit review" → "Approve"

Merge PR:

1. Click "Merge pull request"
2. Vali merge tüüp: "Create a merge commit" (vaikimisi)
3. Click "Confirm merge"
4. Delete branch: Click "Delete branch"

### 8.4 Kohaliku Repositooriumi Uuendamine

Vaheta tagasi main'i ja pull:
```bash
git checkout main
git pull origin main
```

Kustuta lokaalne feature branch:
```bash
git branch -d feature/documentation
```

Kontrolli:
```bash
git log --oneline --graph
```

Näed merge commit'i PR'ist.

### Kontrollnimekiri

- [ ] Lõid feature branch'i ja push'isid GitHub'i
- [ ] Tegid Pull Request'i
- [ ] Merge'isid PR'i GitHub'is
- [ ] Pull'isid muudatused tagasi lokaalsesse repositooriumisse
- [ ] Kustutasid merged branch'i nii GitHub'is kui lokaalselt

---

## Lõplik Kontrollnimekiri

Enne laborit lõpetatuks lugemist veendu:

- [ ] Git on seadistatud: nimi, e-mail, editor
- [ ] Oskad luua repositooriume ja teha commit'e
- [ ] Mõistad staging area rolli
- [ ] .gitignore fail on olemas ja töötab
- [ ] Oskad luua, vahetada ja merge'ida branch'e
- [ ] Oskad lahendada merge konflikte
- [ ] SSH võtmed on seadistatud GitHub'iga
- [ ] Oskad push'ida ja pull'ida
- [ ] Tead, kuidas teha Pull Request'e

---

## Troubleshooting

### Probleemid SSH'ga

**Probleem:** `Permission denied (publickey)`

**Lahendus:**
```bash
# Kontrolli, kas SSH agent töötab
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Testi uuesti
ssh -T git@github.com
```

### Probleemid Push'imisega

**Probleem:** `rejected - non-fast-forward`

**Lahendus:** Keegi teine push'is vahepeal. Pull esmalt:
```bash
git pull origin main
# Lahenda konfliktid, kui on
git push origin main
```

### Probleemid Merge'imisega

**Probleem:** Merge läks katki, ei tea, mis teha.

**Lahendus:** Tühista merge:
```bash
git merge --abort
```

### Probleemid Branch'idega

**Probleem:** Ei saa branch'i kustutada: "not fully merged"

**Lahendus:** Kasuta force delete (ainult kui oled kindel):
```bash
git branch -D branch-name
```

---

## Järgmised Sammud

Oled nüüd läbinud Git'i põhitõed! Edasi:

1. **Kodutöö:** Vaata `kodutoo.md` - rakenda teadmisi päris projektis
2. **Lisapraktika:** Tutvu `lisapraktika.md` - CI/CD, hooks, advanced Git
3. **Praktiline:** Alusta oma projekti Git'iga, tee commit'e iga päev

Edu!

```
