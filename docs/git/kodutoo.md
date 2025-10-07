# Git Kodutöö: Isiklik Projekt Repositoorium

See kodutöö võtab umbes 1.5-2 tundi ja nõuab labori ajal õpitud Git oskuste rakendamist väikeses projektis. Loote GitHub repositooriumi ja rakendate põhilist Git workflow'i.

**Eeldused:** Git Labor läbitud, GitHub konto olemas, SSH seadistatud  
**Esitamine:** GitHub repositooriumi URL e-posti või Moodle kaudu  
**Tähtaeg:** Nädal pärast laborit

---

## 1. Ülesande Kirjeldus

Loote avaliku GitHub repositooriumi, mis sisaldab väikest projekti või skriptide kogumit. See ei pea olema keeruline - fookus on Git'i õigel kasutamisel, mitte programmeerimise keerukusel.

Minimaalse nõuded:

- Avalik GitHub repositoorium
- Vähemalt 5 tähenduslikku commit'i
- README.md koos projekti kirjelduse ja refleksiooniga
- .gitignore fail
- Vähemalt 3 erinevat faili projektis

Valige üks projektitüüp allpool või pakkuge välja oma idee (lihtne variant).

---

## 2. Repositooriumi Loomine

### 2.1 GitHub Setup

Logige GitHub'i ja looge uus repositoorium:

- Nimi: `git-homework` või kirjeldav nimi
- Kirjeldus: Lühike kokkuvõte
- **Public** (avalik)
- EI lisa README ega .gitignore (loote ise)
- Lisa MIT License

### 2.2 Kloonimine ja Initsiaalseadistamine
```bash
git clone git@github.com:TEIE-KASUTAJANIMI/git-homework.git
cd git-homework
```

Kontrollige:
```bash
git status
git remote -v
```

---

## 3. Projekti Valik

Valige ÜKS järgnevatest. Ärge üle keeruliseks tehke - fookus on Git'il, mitte koodil.

### Variant A: Python Kalkulaator (Lihtne)

Looge 2 faili:

**calculator.py:**
```python
def add(a, b):
    """Liida kaks arvu."""
    return a + b

def subtract(a, b):
    """Lahuta."""
    return a - b

def multiply(a, b):
    """Korruta."""
    return a * b

def divide(a, b):
    """Jaga."""
    if b == 0:
        return "Error: jagamine nulliga"
    return a / b

if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
    print("4 * 3 =", multiply(4, 3))
    print("10 / 2 =", divide(10, 2))
```

**.gitignore:**
```
__pycache__/
*.pyc
.vscode/
.DS_Store
```

### Variant B: HTML Lihtne Leht

Looge 3 faili:

**index.html:**
```html
<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <title>Minu Leht</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Tere! Mina olen [Sinu Nimi]</h1>
    <p>See on minu Git kodutöö projekt.</p>
    
    <h2>Oskused</h2>
    <ul>
        <li>Git ja GitHub</li>
        <li>HTML/CSS põhitõed</li>
    </ul>
</body>
</html>
```

**style.css:**
```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    background-color: #f4f4f4;
}

h1 {
    color: #333;
}

ul {
    list-style-type: square;
}
```

**.gitignore:**
```
.DS_Store
Thumbs.db
.vscode/
```

### Variant C: Bash Skriptid

Looge 2 skripti:

**backup.sh:**
```bash
#!/bin/bash
# Lihtne varundusskript

SOURCE_DIR="${1:-.}"
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$SOURCE_DIR"

echo "Backup created: $BACKUP_DIR/backup_$DATE.tar.gz"
```

**cleanup.sh:**
```bash
#!/bin/bash
# Puhasta ajutised failid

echo "Cleaning temporary files..."
find . -name "*.log" -delete
find . -name "*.tmp" -delete
echo "Cleanup complete!"
```

**.gitignore:**
```
*.log
*.tmp
backups/
.DS_Store
```

Tee skriptid käivitatavaks:
```bash
chmod +x backup.sh cleanup.sh
```

---

## 4. Git Workflow - 5 Commit'i

Tehke vähemalt 5 commit'i järgmises stiilis. Iga commit teeb ÜHE loogilise asja.

### Commit 1: Algstruktuur
```bash
touch README.md
git add README.md
git commit -m "Initial commit: create README"
git push origin main
```

### Commit 2: Lisa .gitignore
```bash
# Loo .gitignore fail (vali variant projektile)
git add .gitignore
git commit -m "Add .gitignore for [Python/Web/Bash] project"
git push origin main
```

### Commit 3: Lisa põhifail
```bash
# Loo põhifail (calculator.py, index.html või backup.sh)
git add calculator.py  # või teine fail
git commit -m "Add main calculator functions"
git push origin main
```

### Commit 4: Lisa teine komponent
```bash
# Loo teine fail (style.css, cleanup.sh vms)
git add style.css  # või teine fail
git commit -m "Add [description of what this file does]"
git push origin main
```

### Commit 5: Täienda README
```bash
# Kirjuta README.md (vt sektsioon 5)
git add README.md
git commit -m "Add project documentation and usage instructions"
git push origin main
```

**Oluline:** Iga commit sõnum peab olema kirjeldav ja selgitama MIKS.

**Head näited:**
```
Add calculator module with basic operations
Fix division by zero error handling
Add CSS styling for better readability
Update README with installation instructions
```

**Halvad näited (ära kasuta):**
```
update
fix
asdf
wip
changes
```

---

## 5. README.md Dokumentatsioon

Teie README.md peab sisaldama järgmisi sektsioone:
```markdown
# Projekti Nimi

Lühike kirjeldus 1-2 lausega.

## Kirjeldus

2-3 lõiku, mis selgitavad:
- Mis see projekt on
- Miks te selle tegite
- Mida see teeb

## Kasutamine

### Nõuded
- Python 3.x (või muud nõuded)
- Git

### Paigaldamine
```bash
git clone git@github.com:KASUTAJANIMI/git-homework.git
cd git-homework
```

### Käivitamine
```bash
python calculator.py
# või
open index.html
# või
./backup.sh
```

## Failide Struktuur
```
git-homework/
├── calculator.py  (või teised failid)
├── README.md
├── .gitignore
└── LICENSE
```

## Autor

[Teie Nimi]  
GitHub: [@teie-kasutajanimi](https://github.com/teie-kasutajanimi)

## Litsents

MIT License

## Refleksioon

(Vasta allpool olevatele küsimustele)
```

Lisage README.md lõppu "## Refleksioon" sektsioon.

---

## 6. Refleksioon

Lisage README.md lõppu "## Refleksioon" sektsioon ja vastake järgmistele küsimustele (2-3 lauset igaüks):

1. **Mis oli kõige raskem ja kuidas lahendasid?**
2. **Milline Git kontseptsioon oli suurim "ahaa!" hetk?**
3. **Kuidas kasutaksid Git'i tulevikus?**
4. **Kuidas selgitaksid sõbrale, mis on Git?**
5. **Mis oli kõige huvitavam osa?**

---

## 7. Esitamine

### Kontroll Enne Esitamist

Kontrollige, et olete kõik teinud:

- [ ] Repositoorium on avalik (public)
- [ ] Vähemalt 5 commit'i (vaadake: `git log --oneline`)
- [ ] Commit sõnumid on kirjeldavad ja selged
- [ ] README.md sisaldab kõiki sektsioone
- [ ] Refleksioon on täielik (5 küsimust, 2-3 lauset igaüks)
- [ ] .gitignore fail on olemas
- [ ] Projekt töötab (saab käivitada)
- [ ] Kõik on push'itud GitHub'i

### Esitamise Formaat

upEsitage Google Classroom'is:

**Repository link:** `https://github.com/teie-kasutajanimi/git-homework`

Veenduge, et:

- Repository on **public** (avalik)
- README.md sisaldab projekti kirjeldust
- Kõik failid on commit'itud ja push'itud

---

## 8. Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|-----------|---------|-----------|
| **Repositooriumi Struktuur** | 20% | Loogiline failide paigutus; .gitignore olemas ja töötab (ei ole soovimatud failid nagu `__pycache__`, `.DS_Store`); Projekt on korrektne struktuuriga |
| **Commit Kvaliteet** | 30% | Vähemalt 5 commit'i; Commit sõnumid on kirjeldavad ja selgitavad MIKS (mitte lihtsalt "update"); Iga commit teeb üht loogilist asja; Ajalugu on loogiline |
| **Git Workflow** | 15% | `add → commit → push` õigesti kasutatud; `git status`, `git log` kasutamise märgid; Ei ole segadust workflow'ga |
| **Projekt Funktsionaalsus** | 10% | Projekt käivitub ilma vigadeta; Teeb seda, mida kirjeldus ütleb; Kood/HTML on loetav |
| **README Dokumentatsioon** | 10% | Projekti kirjeldus on selge; Kasutamise juhised on täielikud; Struktuur on korras |
| **Refleksioon** | 15% | Kõik 5 küsimust vastatud; Iga vastus 2-3 lauset; Vastused on sisukad ja ausad; Näitavad mõistmist |

**Kokku: 100%**

---

## Boonus (Valikuline, +10%)

**Git Branch (+5%):** Tee üks feature branch, arenda seal, merge tagasi main'i.
```bash
git checkout -b feature/new-function
# tee muudatus
git add .
git commit -m "Add new feature"
git checkout main
git merge feature/new-function
git push origin main
```

**GitHub README Badge (+5%):** Lisa README.md'sse badge (näiteks litsents või tähed).
```markdown
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
```

Vaata: https://shields.io/

---

## Abimaterjalid

**Dokumentatsioon:**

- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub .gitignore templates](https://github.com/github/gitignore)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)

**Kursuseomane:**

- `loeng.md`
- Git põhitõed
- `labor.md`
- Käed-külge harjutused
- `lisapraktika.md`
- Edasijõudnud tehnikad

**Troubleshooting:**

Levinud probleemid:

**Probleem:** Unustasin midagi commit'ist välja jätta.

**Lahendus:**
```bash
# Lisa fail ja muuda viimast commit'i
git add forgotten-file.txt
git commit --amend --no-edit
git push --force-with-lease origin main
```

**Probleem:** Committisin .env faili kogemata.

**Lahendus:**
```bash
# Lisa .gitignore'sse
echo ".env" >> .gitignore

# Eemalda repos'ist, säilita kohalikult
git rm --cached .env
git commit -m "Remove .env from repository"
git push origin main
```

**Probleem:** Commit sõnum on vale.

**Lahendus:**
```bash
# Muuda viimast commit sõnumit
git commit --amend -m "Parandatud sõnum"
git push --force-with-lease origin main
```

---

## Näpunäited

**Aeg:** Ärge kulutage rohkem kui 2 tundi. Kui projekt keeruline, lihtsustage. Fookus on Git'il, mitte koodil.

**Commit sagedus:** Ärge tehke kõike ühes commit'is. Tehke väikeseid samme: loo fail → commit, muuda faili → commit.

**README:** Kirjutage README nii, nagu selgitaksite projektist kellelegi, kes seda esimest korda näeb.

**Refleksioon:** Olge ausad. Ei pea olema perfektne. Näidake, et mõtlesite asjade üle.

**Abi:** Kui kinni jääte, vaadake `labor.md` või küsige klassikaaslastelt/õpetajalt.

---

Edu! Meeles pidage: see ei ole ainult hinne, vaid oskus, mida kasutate kogu oma IT karjääri vältel.