# Git Labor

**Eeldused:** VirtualBox, Vagrant, VS Code  
**Platvorm:** Ubuntu VM, Git, GitHub  
**Kestus:** ~3 tundi

## Õpiväljundid

Pärast laborit oskate:

1. **Seadistada** Git + GitHub SSH workflow'i algusest peale
2. **Rakendada** branch + Pull Request töövooge (nagu päris meeskonnas)
3. **Lahendada** merge konflikte kahe arendaja stsenaariumi põhjal
4. **Hallata** kohalikku ja remote repositooriumi korraga

---

## 1. VS Code Remote-SSH Seadistamine

Masinad on juba olemas Proxmox'is. Seadistame VS Code ühenduse, et saaksime mugavalt töötada.

### 1.1 SSH Config

**Windows:** `C:\Users\SINUNIMI\.ssh\config`  
**Linux/Mac:** `~/.ssh/config`

Lisa oma masina andmed:

```sshconfig
Host git-vm
    HostName 192.168.X.X
    User kasutajanimi
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
```

### 1.2 Ühenda VS Code

VS Code:

1. `Ctrl+Shift+P`
2. `Remote-SSH: Connect to Host`
3. Vali `git-vm`
4. Platform: `Linux`
5. Open Folder: `/home/kasutajanimi`

Kontrolli: vasakul all peaks olema `SSH: git-vm`

**Kontrollnimekiri:**
- [ ] SSH ühendus töötab
- [ ] VS Code näitab remote masina faile

---

## 2. Git + GitHub Põhiseadistus

> **Töömaailmas:** Alati seadista local + remote koos. Ei ole mõtet teha tööd, mida keegi teine ei näe.

### 2.1 Kontrolli Git

```bash
git --version
```

Kui puudub:

```bash
sudo apt update
sudo apt install -y git
```

### 2.2 Konfigureeri Identiteet

Git vajab teada, kes sa oled. Iga commit salvestab selle info.

```bash
git config --global user.name "Sinu Nimi"
git config --global user.email "sinu.email@example.com"
git config --global core.editor "nano"
git config --global init.defaultBranch main
```

Kontrolli:

```bash
git config --list | grep user
```

### 2.3 GitHub Konto

Kui sul pole:

1. Mine `https://github.com` → Sign up
2. Kinnita e-post
3. Settings → Two-factor authentication (valikuline, aga soovitatav)

**Kontrollnimekiri:**
- [ ] `git --version` töötab
- [ ] `git config user.name` näitab sinu nime
- [ ] GitHub konto olemas ja sisse logitud

---

## 3. SSH Võtmed GitHub'iga

> **Miks SSH, mitte HTTPS?** HTTPS küsib paroolid pidevalt. SSH võti = üks kord setup, seejärel automaatne auth. Töömaailmas standard.

### 3.1 Genereeri SSH Võti VM-is

```bash
ssh-keygen -t ed25519 -C "sinu.email@example.com"
```

Vajuta ENTER kõigile küsimustele (no passphrase).

Käivita SSH agent ja lisa võti:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Kopeeri **public key** (NB! .pub lõpuga):

```bash
cat ~/.ssh/id_ed25519.pub
```

Kopeeri kogu väljund (algab `ssh-ed25519 ...`).

### 3.2 Lisa GitHub'i

1. GitHub → Settings (profiili all)
2. SSH and GPG keys (vasakult menüüst)
3. New SSH key
4. Title: `VM controller` (või mis tahes kirjeldav nimi)
5. Key: kleebi public key
6. Add SSH key

### 3.3 Testi Ühendust

```bash
ssh -T git@github.com
```

**Oodatav vastus:**

```
Hi KASUTAJANIMI! You've successfully authenticated...
```

Kui küsib "Are you sure (yes/no)?" → kirjuta `yes`

**Kontrollnimekiri:**
- [ ] SSH võti genereeritud
- [ ] Public key GitHub'is
- [ ] `ssh -T git@github.com` kinnitab autentimist

---

## 4. Loo GitHub Repositoorium (Remote Esmalt!)

> **Workflow pärismaailmas:** Tavaliselt lood GitHub repo esmalt, siis clone'id kohalikku. Teeme sama.

### 4.1 GitHub'is

1. GitHub → "+" (üleval paremal) → New repository
2. Repository name: `git-labor`
3. Description: `Git labor harjutusprojekt`
4. **Public** (et saaksid hiljem näidata)
5. **ÄRA MÄRGI** "Add README" (teeme kohalikult)
6. Create repository

GitHub näitab nüüd setupi juhiseid. Ignoreeri neid - järgime oma plaani.

### 4.2 Clone Repositoorium VM-i

Kopeeri SSH URL GitHub'ist (Code → SSH → kopeeri):

```
git@github.com:KASUTAJANIMI/git-labor.git
```

VM-is:

```bash
cd ~
git clone git@github.com:KASUTAJANIMI/git-labor.git
cd git-labor
```

Kontrolli remote:

```bash
git remote -v
```

Peaks näitama:

```
origin  git@github.com:KASUTAJANIMI/git-labor.git (fetch)
origin  git@github.com:KASUTAJANIMI/git-labor.git (push)
```

**Kontrollnimekiri:**
- [ ] GitHub repo loodud
- [ ] Clone'itud SSH kaudu
- [ ] `git remote -v` näitab origin'i

---

## 5. Esimesed Commit'id ja Push

> Nüüd on local + remote ühendatud. Iga muudatus läheb kohalikku, siis push'ime GitHub'i.

### 5.1 Loo README

```bash
cat > README.md << 'EOF'
# Git Labor Projekt

**Autor:** Sinu Nimi  
**Kuupäev:** 2025-XX-XX

## Eesmärk

Õppida Git workflow'sid, branch'e ja koostööd GitHub'iga.

## Tehnoloogiad

- Git
- GitHub
- Bash
EOF
```

### 5.2 Esimene Commit

```bash
git status
```

Näed `README.md` punases (untracked).

```bash
git add README.md
git status
```

Nüüd rohelises (staged).

```bash
git commit -m "Initial commit: lisa README"
```

### 5.3 Push GitHub'i

```bash
git push -u origin main
```

`-u` = set upstream (edaspidi piisab lihtsalt `git push`)

Mine GitHub'i → refresh → näed README'd!

### 5.4 Lisa Skriptid

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Tere, Git!"
EOF

chmod +x hello.sh
```

```bash
cat > notes.txt << 'EOF'
Git Labor Märkmed
=================

1. git clone - kopeeri remote repo
2. git add - lisa muudatused staged'i
3. git commit - salvesta snapshot
4. git push - saada GitHub'i
5. git pull - too GitHub'ist
EOF
```

Commit ja push:

```bash
git add .
git commit -m "Lisa hello skript ja märkmed"
git push
```

Kontrolli GitHub'is - uued failid seal!

**Kontrollnimekiri:**
- [ ] README GitHub'is näha
- [ ] Vähemalt 2 commit'i
- [ ] Push töötab ilma vigadeta

---

## 6. .gitignore - Mis EI lähe GitHub'i

> **Probleem:** Logifailid, secrets, temp failid ei tohiks kunagi GitHub'i minna. .gitignore defineerib mustri "ignoreeri neid".

### 6.1 Loo Probleemsed Failid

```bash
echo "Error: something broke" > debug.log
mkdir temp
touch temp/cache.tmp
cat > .env << 'EOF'
API_KEY=secret123456
DATABASE_URL=postgresql://localhost/mydb
PASSWORD=SuperSecret
EOF
```

```bash
git status
```

Git näitab KÕIKI neid! Aga .env sisaldab secrete - see EI TOHI GitHub'i minna.

### 6.2 Loo .gitignore

```bash
cat > .gitignore << 'EOF'
# Logid
*.log

# Temp
temp/
*.tmp

# Secrets
.env
.env.local
*.key

# OS specific
.DS_Store
Thumbs.db
EOF
```

Nüüd kontrolli:

```bash
git status
```

Näed AINULT `.gitignore` - ülejäänud ignoreeritud!

```bash
git add .gitignore
git commit -m "Lisa .gitignore (ignoreeri logid ja secrets)"
git push
```

**Kontrollnimekiri:**
- [ ] .gitignore loodud
- [ ] `git status` EI näita .env ega *.log
- [ ] .gitignore GitHub'is

---

## 7. Branch + Pull Request Workflow (Päris Viis!)

> **Töömaailmas:** Keegi EI tee commit'e otse main'i. Alati: loo branch → tee muudatused → push → Pull Request → review → merge.

### 7.1 Miks Branch'e?

**Stsenaarium:** Tahad lisada uue feature, aga main peab jääma töökorras. Branch = isoleeritud koopia, kus eksperimenteerid.

```
main: [v1] → [v2] → [v3]
               ↓
feature:      [A] → [B] → [C]
                             ↓
                     (merge tagasi)
main:  [v1] → [v2] → [v3] → [v4 (sisaldab A+B+C)]
```

### 7.2 Loo Feature Branch

```bash
git checkout -b feature/backup-script
```

See teeb kaks asja:
1. Loob `feature/backup-script` branch'i
2. Vahetab sinna kohe (`checkout`)

Kontrolli:

```bash
git branch
```

Näed * `feature/backup-script` (aktiivne) ja `main`.

### 7.3 Tööta Branch'is

```bash
cat > backup.sh << 'EOF'
#!/bin/bash
# Lihtne varundamise skript

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "Alustan varundamist..."

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" notes.txt README.md

echo "Varundus valmis: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
EOF

chmod +x backup.sh
```

Testi:

```bash
./backup.sh
ls backups/
```

Commit:

```bash
git add backup.sh
git commit -m "Lisa backup skript koos timestampiga"
```

### 7.4 Push Branch'i GitHub'i

```bash
git push -u origin feature/backup-script
```

Mine GitHub'i → näed branch'i dropdown'is `feature/backup-script`!

### 7.5 Tee Pull Request

GitHub'is:

1. Kollane banner: "feature/backup-script had recent pushes" → **Compare & pull request**
2. Base: `main` ← Compare: `feature/backup-script`
3. Title: `Lisa backup skript`
4. Description:

```markdown
## Muudatused
- Lisasin backup.sh skripti
- Loob timestamped archive'id notes.txt ja README'st

## Testimine
- [x] Skript käivitub ilma vigadeta
- [x] Backup fail luuakse õigesti
```

5. **Create pull request**

### 7.6 Review ja Merge (Üksinda Õppides)

Päriselt oleks teine inimene review'iks. Õppides teeme ise:

1. **Files changed** tab → vaata diff'i
2. Lisaks comment rida peale (valikuline)
3. **Merge pull request**
4. **Confirm merge**
5. **Delete branch** (GitHub'is)

### 7.7 Uuenda Lokaalne

GitHub'is on nüüd `main` uuendatud, aga su local `main` on vana!

```bash
git checkout main
git pull origin main
```

Nüüd `backup.sh` on main'is!

Kustuta lokaalne branch:

```bash
git branch -d feature/backup-script
```

**Kontrollnimekiri:**
- [ ] Feature branch loodud
- [ ] Commit'id branch'is tehtud
- [ ] Push'itud GitHub'i
- [ ] Pull Request loodud ja merge'itud
- [ ] Local main uuendatud

---

## 8. Teine Feature: Dokumentatsioon

Korda sama workflow'd teise feature'ga.

### 8.1 Loo Branch

```bash
git checkout main  # alati alusta main'ist!
git pull           # võta viimased muudatused
git checkout -b feature/documentation
```

### 8.2 Lisa Dokumentatsioon

```bash
cat > INSTALL.md << 'EOF'
# Paigaldusjuhend

## Eeldused

- Git 2.0+
- Bash
- Linux/macOS või WSL (Windows)

## Installimine

1. Clone repositoorium:

```bash
git clone git@github.com:KASUTAJANIMI/git-labor.git
cd git-labor
```

2. Tee skriptid käivitatavaks:

```bash
chmod +x *.sh
```

3. Testi:

```bash
./hello.sh
./backup.sh
```

## Kasutamine

Vaata `notes.txt` põhikäskude jaoks.
EOF
```

```bash
cat > USAGE.md << 'EOF'
# Kasutamisjuhend

## Skriptid

### hello.sh

Lihtne tervitusskript:

```bash
./hello.sh
```

### backup.sh

Varundab olulised failid `backups/` kausta:

```bash
./backup.sh
```

Archive'id nimetatakse timestampiga: `backup_20250123_143022.tar.gz`

## Git Workflow

1. Loo feature branch: `git checkout -b feature/nimi`
2. Tee muudatused ja commit'i
3. Push: `git push -u origin feature/nimi`
4. Tee Pull Request GitHub'is
5. Merge ja kustuta branch
EOF
```

### 8.3 Commit ja Push

```bash
git add INSTALL.md USAGE.md
git commit -m "Lisa paigaldus- ja kasutamisjuhendid"
git push -u origin feature/documentation
```

### 8.4 Pull Request

GitHub'is:

1. Compare & pull request
2. Title: `Lisa dokumentatsioon (INSTALL ja USAGE)`
3. Description: "Lisasin kasutaja- ja arendajadokumentatsiooni"
4. Create PR → Merge → Delete branch

### 8.5 Uuenda Lokaalne

```bash
git checkout main
git pull
git branch -d feature/documentation
```

**Kontrollnimekiri:**
- [ ] Teine PR tehtud ja merge'itud
- [ ] INSTALL.md ja USAGE.md main'is

---

## 9. Merge Konfliktid (Kahe Arendaja Stsenaarium)

> **Päris probleem:** Sina ja kolleeg muudate sama faili sama kohta. Git ei tea, kumb on õige → konflikt.

Simuleerime: sina töötad branch'is, aga keegi push'is main'i vahepeal muudatuse samasse faili.

### 9.1 Loo Branch ja Muuda hello.sh

```bash
git checkout main
git pull
git checkout -b feature/greeting-estonian
```

Muuda hello.sh:

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Tere, Git! Kuidas sul läheb täna?"
echo "See on pikendatud tervitus."
EOF
```

```bash
git add hello.sh
git commit -m "Pikenda tervitust eesti keeles"
```

**ÄRA PUSH'I VEEL!**

### 9.2 Simuleerime Kolleegi: Muuda main'i Otse

Vaheta tagasi main'i ja tee konflikteeriv muudatus:

```bash
git checkout main
```

Muuda sama fail:

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Hello, Git! Welcome to the project!"
echo "This is an extended greeting in English."
EOF
```

```bash
git add hello.sh
git commit -m "Muuda tervitus inglise keeleks"
git push
```

Nüüd main GitHub'is on **erinev** su feature branch'ist!

### 9.3 Proovi Merge'ida - Konflikt!

Vaheta tagasi feature branch'i:

```bash
git checkout feature/greeting-estonian
```

Proovi saada GitHub'i:

```bash
git push -u origin feature/greeting-estonian
```

See õnnestub (branch ei konflikti). Aga **Pull Request'is** tekib konflikt!

Mine GitHub'i → **Compare & pull request**

GitHub näitab: ❌ **This branch has conflicts that must be resolved**

### 9.4 Lahenda Konflikt Lokaalselt

GitHub'is võid lahendada veebis, aga töömaailmas tehakse lokaalselt.

Võta main'i muudatused oma branch'i:

```bash
git checkout feature/greeting-estonian
git pull origin main
```

**Konflikt!**

```
CONFLICT (content): Merge conflict in hello.sh
Automatic merge failed; fix conflicts and then commit the result.
```

Vaata faili:

```bash
cat hello.sh
```

Näed:

```bash
#!/bin/bash
<<<<<<< HEAD
echo "Tere, Git! Kuidas sul läheb täna?"
echo "See on pikendatud tervitus."
=======
echo "Hello, Git! Welcome to the project!"
echo "This is an extended greeting in English."
>>>>>>> main
```

**Selgitus:**
- `<<<<<<< HEAD` = sinu branch
- `=======` = eraldaja
- `>>>>>>> main` = main'i versioon

### 9.5 Vali Lahendus

Otsusta, mis jääb. Oletame, et tahame **mõlemat**:

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Tere / Hello, Git!"
echo "Kuidas sul läheb täna? / How are you today?"
EOF
```

Märgi lahendatuks:

```bash
git add hello.sh
```

Lõpeta merge:

```bash
git commit -m "Lahenda konflikt: lisa mõlemakeelne tervitus"
```

Push:

```bash
git push
```

Mine GitHub'i → PR on nüüd merge'itav! ✅

### 9.6 Merge Pull Request

GitHub'is:

1. Refresh PR lehte
2. **Merge pull request**
3. **Confirm**
4. **Delete branch**

Uuenda lokaalne:

```bash
git checkout main
git pull
git branch -d feature/greeting-estonian
```

**Kontrollnimekiri:**
- [ ] Konflikt tekitatud
- [ ] Lahendatud käsitsi
- [ ] Merge lõpetatud GitHub'is

---

## 10. Fast-Forward Merge (Lokaalne Näide)

> **Erand:** Kui branch pole põhiharu edasi liikunud, tehakse "fast-forward" - lihtne pointeri nihutamine.

Seda kasutatakse harvemini (PR workflow on standard), aga hea teada.

### 10.1 Loo Branch

```bash
git checkout main
git checkout -b quickfix/typo
```

### 10.2 Paranda Typo

Oletame README's on viga:

```bash
nano README.md
```

Muuda midagi (nt lisa rida "## Viimased Uuendused").

```bash
git add README.md
git commit -m "Paranda README typo"
```

### 10.3 Merge Lokaalselt

```bash
git checkout main
git merge quickfix/typo
```

Output:

```
Updating abc1234..def5678
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

**Fast-forward:** main lihtsalt "liikus edasi". Pole 3-way merge'i vaja.

Kustuta branch:

```bash
git branch -d quickfix/typo
```

Push:

```bash
git push
```

**Märkus:** Töömaailmas tehaks siiski PR, aga väikeste fiksidega võib ka lokaalselt merge'ida.

**Kontrollnimekiri:**
- [ ] Fast-forward merge tehtud
- [ ] Push'itud main'i

---

## 11. GitHub Actions Sneak Peek (Valikuline)

> Pull Request'idel saab automaatselt teste käitada. Töömaailmas standard - ükski kood ei lähe production'i ilma testideta.

### 11.1 Loo Workflow

```bash
git checkout main
git pull
git checkout -b feature/ci
```

```bash
mkdir -p .github/workflows
cat > .github/workflows/test.yml << 'EOF'
name: Test Scripts

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Test hello.sh
        run: |
          chmod +x hello.sh
          ./hello.sh
      
      - name: Test backup.sh
        run: |
          chmod +x backup.sh
          ./backup.sh
          ls backups/
EOF
```

```bash
git add .github/
git commit -m "Lisa GitHub Actions testid"
git push -u origin feature/ci
```

Tee PR → GitHub'is näed **Actions** tab'i → testid käivad automaatselt!

Merge PR, kui testid õnnestusid.

**Kontrollnimekiri:**
- [ ] CI workflow loodud
- [ ] Testid käivituvad PR'is

---

## Lõplik Kontrollnimekiri

**Setup:**
- [ ] VS Code remote ühendus töötab
- [ ] Git konfigureeritud (name, email)
- [ ] SSH võti GitHub'is
- [ ] Repositoorium clone'itud

**Põhitöövoog:**
- [ ] 5+ commit'i tehtud
- [ ] .gitignore seadistatud
- [ ] Push/pull töötab

**Branch + PR:**
- [ ] 3+ Pull Request'i tehtud ja merge'itud
- [ ] Branch'id kustutatud pärast merge'i
- [ ] Local main uuendatud iga kord

**Konfliktid:**
- [ ] Merge konflikt tekitatud
- [ ] Lahendatud käsitsi
- [ ] Merge lõpetatud

**Valikuline:**
- [ ] CI/CD workflow (GitHub Actions)

---

## Troubleshooting

### SSH Permission Denied

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
```

Kui ikka ei tööta:
- Kontrolli, kas public key on GitHub'is
- Kontrolli, kas kasutad SSH URL'd (mitte HTTPS)

### Push Rejected (Conflict)

```bash
git pull origin main
# Lahenda konfliktid
git add .
git commit -m "Merge main into feature"
git push
```

### Abort Merge

Kui eksid:

```bash
git merge --abort
```

### Force Delete Branch

Kui Git ei lase kustutada:

```bash
git branch -D branch-name
```

### Reset Viimane Commit (Kohalik!)

```bash
git reset --soft HEAD~1  # commit tagasi, failid jäävad
git reset --hard HEAD~1  # kõik kaob!
```

**HOIATUS:** ÄRA kunagi `git reset --hard` pärast push'i!

---

## Esitamine

1. Kontrolli, et kõik on push'itud:

```bash
git checkout main
git pull
git log --oneline --graph --all
git push --all origin
```

2. README.md alguses peavad olema:

```markdown
**Autor:** Sinu Nimi  
**Kuupäev:** 2025-XX-XX  
**GitHub:** https://github.com/KASUTAJANIMI/git-labor
```

3. Kontrolli GitHub'is:
   - Vähemalt 5 commit'i
   - Kõik failid olemas (README, skriptid, .gitignore, dokid)
   - Closed PR'id (vähemalt 3)

4. Esita link õpetajale: `https://github.com/KASUTAJANIMI/git-labor`

---

## Refleksioon

Mõtle läbi ja vasta (ei pea kirjalikult esitama, aga mõtle järele):

1. **Miks branch'id on paremad kui töötamine otse main'is?**
2. **Mis juhtub, kui kaks inimest muudavad sama faili sama kohta?**
3. **Miks .gitignore on kriitiline (eriti .env failide puhul)?**
4. **Kuidas PR workflow aitab meeskonnatööd?**
5. **Mis on erinevus `git pull` ja `git fetch` vahel?** (Google'da, kui ei tea)
