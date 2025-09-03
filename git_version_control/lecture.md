# 📚 Git Version Control: Versioonihaldus ja GitHub

**Kestus:** 3 tundi  
**Eesmärk:** Omandada Git'i täielikud oskused - alates kohalikust kasutamisest kuni meeskonnatööni GitHub'is

---

## 📖 Moodul 1: Sissejuhatus Versioonihaldusesse

### Git'i Ajalugu

**Git'i looja:** Linus Torvalds (2005)

**Miks loodi Git?**
- Linus Torvalds vajas versioonihaldussüsteemi Linux kernel'i jaoks
- Olemasolevad süsteemid (BitKeeper) ei sobinud
- Ta lõi Git'i 2 nädalaga!
- Nimi "Git" tähendab briti slängis "loll inimene" (Torvalds ise ütles, et ta on "egotistical bastard")

**Git'i areng:**
- 2005: Esimene versioon
- 2008: GitHub loodi Git'i hostimiseks
- Tänapäev: Maailma populaarseim versioonihaldussüsteem

### Miks on versioonihaldus vajalik?

Kujutage ette olukorda, kus kirjutate olulist koodi:
- Teete muudatusi ja midagi läheb katki
- Ei mäleta, mida täpselt muutsite  
- Kolleeg muudab sama faili samal ajal
- Vana töötav versioon on kadunud

**Git lahendab kõik need probleemid!**

### Git vs Teised Versioonihaldussüsteemid

**Git'i eelised:**
- **Hajutatud** - iga arendaja omab täielikku ajalugu
- **Kiire** - kõik operatsioonid toimuvad lokaalses masinas
- **Branching** - hõlbus paralleelsete arendusliinide loomine
- **Tööstusstandard** - kasutatakse kõikjal

### Põhimõisted

Git'i töövoog koosneb neljast põhilises osast, mis moodustavad kogu versioonihalduse protsessi. Iga osa on oluline ja mõistmine aitab sul Git'i tõhusamalt kasutada.

```mermaid
graph LR
    A[Working Directory<br/>Töökaust] --> B[Staging Area<br/>Ettevalmistus]
    B --> C[Local Repository<br/>Kohalik Repo]
    C --> D[Remote Repository<br/>GitHub]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e8
```



#### Working Directory (Töökaust)
**Mis on Working Directory?**
Working Directory on sinu projekti kaust, kus sa tegelikult töötad. See on kõige olulisem osa Git'i töövoost, sest siin sa teed kõik oma muudatused.

- **Failid, millega töötad** - sinu kood, dokumentid, pildid
- **Kohalik kaust** - kus sa redigeerid faile
- **Git jälgib seda** - näeb, millised failid on muutunud
- **Sinu "töölaud"** - kus sa teed kõik muudatused

**Näide:**
```
minu-projekt/
├── app.py          ← Working Directory (sinu failid)
├── config.py       ← Working Directory
├── README.md       ← Working Directory
└── .git/           ← Git'i sisemised failid (ei ole Working Directory)
```

**Working Directory vs Git:**
- **Working Directory**: Sinu failid, mida sa näed ja redigeerid
- **Git**: Salvestab ajaloo ja jälgib muudatusi
- **Kui sa muudad faili**: Working Directory muutub, aga Git ei salvesta seda kohe

#### Staging Area (Index) - Ettevalmistusala
**Mis on Staging Area?**
Staging Area on nagu "korv" või "ooteala", kus sa kogud kõik muudatused enne nende salvestamist. See võimaldab sul kontrollida, millised failid ja muudatused lähevad järgmise commit'i.

- **"Ooteala"** - kus sa valmistad faile commit'i jaoks
- **Git'i sisemine indeks** - mis failid lähevad järgmise commit'i
- **Kontrollitud muudatused** - sa otsustad, mida salvestada
- **"Korv"** - kus sa kogud muudatused enne salvestamist

```mermaid
graph TD
    A[Working Directory<br/>app.py muudetud] -->|git add app.py| B[Staging Area<br/>app.py valmis]
    C[Working Directory<br/>config.py muudetud] -->|git add config.py| D[Staging Area<br/>config.py valmis]
    B -->|git commit| E[Local Repository<br/>Commit salvestatud]
    D -->|git commit| E
    
    style A fill:#ffebee
    style B fill:#fff3e0
    style C fill:#ffebee
    style D fill:#fff3e0
    style E fill:#f3e5f5
```

**Näide:**
```bash
# 1. Muuda faili Working Directory's
echo "uus sisu" >> app.py

# 2. Lisa Staging Area'le
git add app.py

# 3. Tee commit
git commit -m "Lisa uus funktsioon"
```

**Staging Area vs Working Directory:**
- **Working Directory**: Kõik sinu failid ja muudatused
- **Staging Area**: Ainult need failid, mida sa tahad commit'ida
- **git add**: Liigutab faile Working Directory'st Staging Area'le
- **git commit**: Salvestab Staging Area'st Repository'sse

---

## 📖 Moodul 2: Git'i Kohalik Kasutamine

### Git'i Installimine

| OS | Installimise käsk | Alternatiiv |
|----|-------------------|-------------|
| **Windows** | `winget install --id Git.Git` | [Download](https://git-scm.com/download/win) |
| **macOS** | `brew install git` | `xcode-select --install` |
| **Ubuntu/Debian** | `sudo apt install git` | - |
| **CentOS/RHEL** | `sudo yum install git` | - |
| **Fedora** | `sudo dnf install git` | - |

**Kontrolli installimist:**
```bash
git --version
```

### Git Bash vs Bash

**Git Bash** on Windows'i versioon Bash'ist:
- **Bash** = Unix/Linux shell
- **Git Bash** = Bash Windows'ile
- **Sama funktsionaalsus** - kõik Bash käsud töötavad
- **Git'i käsud** töötavad paremini kui PowerShell'is

**Erinevused:**
- **Bash**: Linux/macOS terminal
- **Git Bash**: Windows terminal (Bash emulator)
- **Käsud**: Täpselt samad
- **Keskkond**: Windows failisüsteem

### Esmakordne Seadistamine

```bash
# Kasutaja info seadistamine
git config --global user.name "Teie Nimi"
git config --global user.email "teie.email@example.com"

# Seadistuste kontrollimine
git config --list
```

### Repository Loomine: git init vs git clone

Git'i kasutamiseks pead sa esmalt looma või kopeerima repository. Selleks on kaks põhilist viisi, mis sõltuvad sellest, kas alustad uut projekti või jätkad olemasolevat.

**Kaks erinevat viisi repository alustamiseks:**

#### git init - Uue projekti alustamine
```bash
# Loo kaust ja mine sinna
mkdir minu-projekt
cd minu-projekt

# Alusta Git repository
git init

# Lisa failid ja alusta tööd
echo "# Minu projekt" > README.md
git add README.md  #adding file to staging area
git commit -m "Esimene commit"
```

**Millal kasutada git init:**
- Alustad täiesti uut projekti
- Sul pole olemasolevat koodi
- Tahad luua kohaliku repository

#### git clone - Olemasoleva projekti kopeerimine
```bash
# Kopeeri olemasolev repository
git clone https://github.com/kasutaja/projekt.git
cd projekt

# Projekt on kohe kasutamiseks
git status
```

**Millal kasutada git clone:**
- Jätkad teise inimese projekti
- Kopeerid GitHub'ist projekti
- Sul on juba olemasolev kood

### Põhilised Käsud Algajatele

Git'i õppimisel on oluline alustada lihtsate käsudega ja järk-järgult keerukamaid asju õppida. Siin on kolm kõige olulisemat käsku, mida sa kasutad iga päev.

**Kolme käsuga alusta:**
```bash
git status              # Vaata, mis on muutunud
git add .               # Lisa kõik muudatused
git commit -m "Sõnum"   # Salvesta muudatused
```

**Lihtne töövoog:**
1. **Tee muudatusi** failides
2. **`git status`** - vaata, mis muutus
3. **`git add .`** - lisa kõik muudatused
4. **`git commit -m "sõnum"`** - salvesta

**Näide:**
```bash
# 1. Muuda faili
echo "uus sisu" >> app.py

# 2. Vaata olekut
git status

# 3. Lisa muudatused
git add .

# 4. Salvesta
git commit -m "Lisa uus funktsioon"
```

### Olulised Käsud Lab'i ja Kodutöö Jaoks

**Põhilised käsud, mida kasutad iga päev:**
```bash
git status                  # Vaata olekut
git add .                   # Lisa muudatused
git commit -m "Sõnum"       # Salvesta
git push origin main        # Saada muudatused
git pull origin main        # Võta uusimad muudatused
```

> **📋 Täielik käskude nimekiri:** Vaata faili [`git_commands_reference.md`](./git_commands_reference.md) kõigi käskude ja nende selgitustega.

### Sageli Kasutatavad Käsud

**Kõige populaarsemad käsud:**
```bash
git diff                   # Vaata muudatusi
git log --oneline          # Kompaktne ajalugu
git branch                 # Vaata harusid
git checkout -b uus-haru   # Loo ja vaheta haru
git merge haru-nimi        # Ühenda haru
```

> **📋 Rohkem käskude:** Vaata täielikku nimekirja failis [`git_commands_reference.md`](./git_commands_reference.md).

---

## 💡 Lisaressurs: Lõbusad Commit Sõnumid

### whatthecommit.com

[whatthecommit.com](https://whatthecommit.com/) genereerib lõbusaid commit sõnumeid. **Ainult kohaliku Git'i jaoks!**

```bash
# Lisa alias
alias gitcommit='git commit -m "$(curl -s https://whatthecommit.com/index.txt)"'

# Kasuta
git add .
gitcommit
```

> ⚠️ **Ainult testis!** Ära kasuta tõsises projektis.
> 
> **📖 Täielik juhend:** Vaata faili [`whatthecommit_guide.md`](./whatthecommit_guide.md) seadistamise ja kasutamise juhiste jaoks.



### Staging Area Vahele Jätmine

Sageli pole vaja staging area'te kasutada:

```bash
# Kõigi muudetud failide kohene commit
git commit -am "Kiire commit kõigist muudatustest"

# Konkreetse faili kohene commit
git add failinimi.txt && git commit -m "Sõnum"
```

**Millal kasutada:**
- Väiksed, kiired muudatused
- Kõik muudatused on seotud
- Pole vaja faile eraldi kontrollida



> **💡 Lisaressurs:** Kui soovid õppida, kuidas lugeda `git diff` väljundit ja mõista, mida iga sümbol tähendab, vaata faili [`git_diff_examples.md`](./git_diff_examples.md) praktiliste näidete ja harjutustega.
>
> **🔧 Lisaressurs:** Kui soovid õppida, kuidas rakendada muudatusi patch failidest ja diff väljundist, vaata faili [`git_apply_changes.md`](./git_apply_changes.md) praktiliste näidete ja harjutustega.















### Harude (Branches) Loomine ja Haldamine

Harud (branches) on Git'i üks võimsamaid funktsioone. Need võimaldavad sul töötada paralleelselt erinevate funktsionaalsustega, ilma et see mõjutaks põhiharju. See on nagu eraldi "töölaud" iga funktsionaalsuse jaoks.

```mermaid
gitgraph
    commit
    branch funktsioon-login
    checkout funktsioon-login
    commit
    commit
    checkout main
    commit
    merge funktsioon-login
```

```bash
# Uue haru loomine
git branch funktsioon-login

# Haru loomine ja sellele vahetamine
git checkout -b funktsioon-login

# Uuem süntaks (Git 2.23+)
git switch -c funktsioon-login

# Harude vaatamine
git branch                  # Kohalikud harud
git branch -v               # Koos viimase commit'iga
git branch -a               # Kõik harud (ka remote)
```



### Harude Ühendamine (Merging)

Kui oled oma funktsionaalsuse valmis töötanud, pead sa selle ühendama põhiharuga. See protsess nimetatakse merge'iks. Merge võimaldab sul kombineerida erinevate harude muudatused ühte.

```mermaid
graph LR
    subgraph "Enne Merge'i"
        A[main: A---B---C]
        B[feature: A---B---D---E]
    end
    
    subgraph "Pärast Merge'i"
        C[main: A---B---C---F<br/>merge commit]
        D[feature: A---B---D---E]
    end
    
    A --> C
    B --> C
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

```bash
# Lihtne merge
git checkout main
git merge funktsioon-login

# Merge ilma fast-forward'ta
git merge --no-ff funktsioon-login

# Merge'i katkestamine konflikti korral
git merge --abort

# Merge'i jätkamine pärast konfliktide lahendamist
git add .
git commit                  # Sõnum genereeritakse automaatselt
```

### Merge Konfliktide Lahendamine

Konfliktid tekivad, kui Git ei suuda automaatselt ühendada muudatusi. See juhtub tavaliselt, kui mõlemal harus on muudetud sama faili samu ridu. Konfliktide lahendamine on oluline oskus, mida sa pead valdama.

Konflikti näide failis:
```
<<<<<<< HEAD
Praeguse haru sisu
=======
Ühendatava haru sisu  
>>>>>>> funktsioon-login
```

Lahendamise sammud:
1. Avage konfliktne fail redaktoris
2. Otsustage, millist versiooni säilitada
3. Eemaldage konfliktimärgid (`<<<<`, `====`, `>>>>`)
4. Salvestage fail
5. `git add konfliktne-fail.txt`
6. `git commit`

```bash
# Konfliktide vaatamine
git status                  # Näitab konfliktilisi faile
git diff                    # Näitab konfliktide detaile

# Merge'i tool'ide kasutamine
git mergetool              # Avab graafilise lahendaja
```



---

## 📖 Moodul 3: Kaugrepositooriumidega Töötamine

### Mis on GitHub?

GitHub on maailma suurim platvorm Git repositooriumide hostimiseks ja koostööks. See on nagu "Facebook" programmeerijatele - siin saad jagada oma koodi, töötada koos teistega ja õppida teistelt.

GitHub on:
- **Git hosting teenus** - hoiab teie repositooriume pilves
- **Koostöö platvorm** - meeskondlik arendus
- **Portfolio** - näidake oma tööd tööandjatele  
- **Open source kodu** - miljonid avalikud projektid

GitHub vs Git:
- **Git** = versioonihaldussüsteem (tööriist)
- **GitHub** = teenus Git repositooriumide hostimiseks

### Põhiline GitHub'i Interaktsioon

```bash
# Repository kloneerimine
git clone https://github.com/kasutaja/projekt.git
git clone git@github.com:kasutaja/projekt.git    # SSH variant

# Olemasoleva projekti ühendamine GitHub'iga
git remote add origin https://github.com/kasutaja/projekt.git

# Remote'ide vaatamine
git remote -v
git remote show origin
```

### Mis on Remote?

Remote on link kaugrepositooriumile:

```bash
# Remote'ide lisamine
git remote add origin https://github.com/kasutaja/projekt.git
git remote add upstream https://github.com/originaal/projekt.git

# Remote'ide haldamine  
git remote rename origin upstream
git remote remove old-remote
git remote set-url origin uus-url
```



### Remote'idega Töötamine

```bash
# Info toomine serverist (ei muuda kohalikke faile)
git fetch origin

# Konkreetse haru toomine
git fetch origin main

# Kõigi remote'ide uuendamine
git fetch --all

# Remote branch'ide vaatamine
git branch -r
git branch -a                # Kõik branch'id
```

### Uute Muudatuste Toomine

```bash
# Fetch + merge = pull
git pull origin main

# Pull'i erinevad variandid
git pull --rebase origin main    # Rebase pull
git pull --ff-only origin main   # Ainult fast-forward

# Automaatne remote tracking
git push -u origin main          # Esimene kord
git pull                         # Edaspidi piisab lühikesest
```

### Kohaliku Repository Uuendamine

```bash
# Tavaliselt pull piisab
git pull origin main

# Samm-sammuline lähenemisviis
git fetch origin
git diff HEAD origin/main        # Vaata erinevusi
git merge origin/main            # Ühenda muudatused

# Konfliktide korral
git pull origin main
# ... lahenda konfliktid ...
git add .
git commit
```

### Pull-Merge-Push Workflow

Kui töötad meeskonnas, pead sa järgima kindlat töövoogu, et vältida konflikte ja tagada, et kõik on sünkroniseeritud. See workflow on nagu "kuldne reegel" meeskonnatöös.

See on tavaline töövoog meeskonnatöös:

```mermaid
sequenceDiagram
    participant Dev as Arendaja
    participant Local as Kohalik Repo
    participant Remote as GitHub
    
    Dev->>Local: git pull origin main
    Local->>Remote: fetch latest changes
    Remote-->>Local: new commits
    Local-->>Dev: updated files
    
    Dev->>Local: git add & commit
    Local->>Local: save changes
    
    Dev->>Local: git pull origin main
    Local->>Remote: check for new changes
    Remote-->>Local: no new changes
    
    Dev->>Local: git push origin main
    Local->>Remote: send commits
    Remote-->>Local: confirmation
```

```bash
# 1. PULL - võta uusimad muudatused
git pull origin main

# 2. WORK - tee oma tööd
# ... koodi redigeerimine ...
git add .
git commit -m "Minu muudatused"

# 3. PULL (jälle) - võta võimalikud uued muudatused  
git pull origin main

# 4. PUSH - saada oma muudatused
git push origin main
```



### Remote Branch'ide Saatmine

```bash
# Uue branch'i saatmine
git push origin funktsioon-login

# Branch'i tracking seadistamine
git push -u origin funktsioon-login

# Edaspidi piisab
git push

# Branch'i kustutamine remote'ist
git push origin --delete funktsioon-login
```

### Oma Muudatuste Rebasing

Rebase on nagu lause ümber kirjutamine. Kujutle, et sul on lause "Auto on punane" ja sa tahad lisada sõna "meil" - "Meil on punane auto".

**Enne rebase'i:**
- Main branch: "Auto on punane"
- Sinu branch: "Auto on punane" + "Meil on punane auto"

**Pärast rebase'i:**
- Main branch: "Auto on punane" 
- Sinu branch: "Auto on punane" → "Meil on punane auto"

Rebase "ümber kirjutab" sinu muudatused nii, et need tunduvad olevat tehtud pärast viimaseid muudatusi.

```mermaid
graph LR
    subgraph "Enne Rebase'i"
        A[main: "Auto on punane"]
        B[sinu: "Auto on punane" + "Meil on punane auto"]
    end
    
    subgraph "Pärast Rebase'i"
        C[main: "Auto on punane"]
        D[sinu: "Auto on punane" → "Meil on punane auto"]
    end
    
    A --> C
    B --> D
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e3f2fd
    style D fill:#e8f5e8
```

```bash
# Rebase kohalikud commit'id remote'i peale
git pull --rebase origin main

# Käsitsi rebase
git fetch origin
git rebase origin/main

# Interaktiivne rebase (commit'ide korrastamine)
git rebase -i origin/main
git rebase -i HEAD~3             # Viimased 3 commit'i

# Rebase'i katkestamine/jätkamine
git rebase --abort              # Katkesta
git rebase --continue           # Jätka pärast konfliktide lahendamist
```



### SSH Protocol ja Turvalisus

SSH on turvalisem kui HTTPS parooli:

```bash
# SSH võtme genereerimine
ssh-keygen -t ed25519 -C "teie.email@example.com"

# Avaliku võtme vaatamine
cat ~/.ssh/id_ed25519.pub

# SSH agendi käivitamine
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Ühenduse testimine
ssh -T git@github.com
```

**GitHub'is SSH võtme lisamine:**
1. Settings → SSH and GPG keys
2. New SSH key
3. Kleebi avalik võti
4. Save

### API Keys ja Personal Access Tokens

HTTPS kasutamiseks GitHub'iga (parooli asemel):

```bash
# Token'i genereerimine GitHub'is:
# Settings → Developer settings → Personal access tokens

# Token'i kasutamine
git clone https://username:token@github.com/kasutaja/projekt.git

# Või credentials cache'iga
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'
```

### Konfliktide Lahendamine Remote'iga

```bash
# Tavaliselt juhtub pull'i käigus
git pull origin main
# Konflikt!

# Lahenda konfliktid failides
# ...

# Jätka normaalset workflow'd
git add .
git commit -m "Lahenda merge konflikt"
git push origin main
```

---

## 📖 Moodul 4: Koostöö ja Projektihaldus

### Pull Request'ide Workflow

Pull Request (PR) on GitHub'i võimsaim funktsioon meeskonnatööks. See võimaldab sul esitada oma muudatused ülevaatuseks ja ühendamiseks põhiharuga. PR on nagu "ettepanek" muudatuste tegemiseks.

Pull Request (PR) on professionaalse arenduse alus:

```mermaid
flowchart TD
    A[Fork Repository] --> B[Clone Fork]
    B --> C[Create Feature Branch]
    C --> D[Make Changes]
    D --> E[Commit Changes]
    E --> F[Push to Fork]
    F --> G[Create Pull Request]
    G --> H{Code Review}
    H -->|Approved| I[Merge to Main]
    H -->|Changes Needed| J[Update PR]
    J --> D
    
    style A fill:#e1f5fe
    style G fill:#fff3e0
    style I fill:#e8f5e8
    style J fill:#ffebee
```

**1. Fork & Clone:**
```bash
# GitHub'is vajuta "Fork"
git clone https://github.com/teie-nimi/projekt.git
cd projekt
git remote add upstream https://github.com/originaal/projekt.git
```

**2. Feature Branch:**
```bash
git checkout -b funktsioon-uus-omadus
# ... tee tööd ...
git add .
git commit -m "Lisa uus omadus"
```

**3. Push & PR:**
```bash
git push origin funktsioon-uus-omadus
# GitHub'is loo Pull Request
```

**4. Update PR:**
```bash
# Kui vaja muudatusi PR'is
git add .
git commit -m "Paranda ülevaate järgi"
git push origin funktsioon-uus-omadus  # PR uueneb automaatselt
```

### Tüüpiline Pull Request Workflow GitHub'is

**PR Loomine:**
1. Navigate to repository
2. "Compare & pull request"
3. Kirjuta selge pealkiri ja kirjeldus
4. Määra reviewer'id
5. Lisa label'id ja milestone

**PR Template näide:**
```markdown
## Muudatuste kirjeldus
Lisa lühike kokkuvõte muudatustest

## Kontroll
- [ ] Kood on testitud
- [ ] Dokumentatsioon on uuendatud
- [ ] Ei ole breaking changes

## Screenshots
Kui UI muudatused, lisa pildid
```

### Olemasoleva Pull Request'i Uuendamine

```bash
# Lihtne variant - lisa commit'e
git add .
git commit -m "Paranda review märkusi"
git push origin funktsioon-branch

# Puhtam variant - amend commit
git add .
git commit --amend --no-edit
git push --force-with-lease origin funktsioon-branch
```

**Millal kasutada force push:**
- Ainult oma branch'ides
- Mitte kunagi shared branch'ides
- Kasuta `--force-with-lease` mitte `--force`

### Muudatuste Squashing

Squashing ühendab mitu commit'i üheks:

```bash
# Interaktiivne rebase viimase 3 commit'iga
git rebase -i HEAD~3

# Editor avaneb:
pick a1b2c3d Esimene commit
squash e4f5g6h Teine commit  
squash i7j8k9l Kolmas commit

# Salvesta ja välju
# Uus editor commit sõnumiga - redigeeri vajadusel
```

**GitHub'i Squash Merge:**
- PR merge'imisel vali "Squash and merge"
- Kõik PR commit'id ühendatakse üheks
- Main branch jääb puhtaks

### Code Review

**Hea Code Review:**

```bash
# Koodi läbivaatamine lokaalses
git fetch origin
git checkout pr-branch-name
git log main..pr-branch-name    # PR'i commit'id
git diff main...pr-branch-name  # PR'i muudatused
```



### Koostöö Haldamine

**Branch protection rules:**
- Main branch on kaitstud
- Nõuab PR'e
- Nõuab review'e
- Nõuab passing teste

**Project management:**
```bash
# Issues'ide linkimine commit'idega
git commit -m "Paranda login bug

Fixes #123
Closes #456"

# Commit'ide linkimine PR'idega  
git commit -m "Lisa uus feature (#789)"
```

### Issue'de Jälgimine

**Lihtne Issue näide:**
```markdown
## Bug Report

**Probleem:**
Login nupp ei tööta

**Mida juhtus:**
Vajutasin login nuppu, aga midagi ei juhtunud

**Mida peaks juhtuma:**
Peaks avanema login leht
```

### Pidev Integratsioon (CI)

Pidev Integratsioon (CI) on protsess, kus kood testitakse automaatselt iga kord, kui tehakse muudatusi. See aitab leida vigu varakult ja tagada koodi kvaliteeti. GitHub Actions on üks populaarsemaid CI tööriistu.

Lihtne GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [ main ]
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
        node-version: '16'
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests
      run: npm test
    
    - name: Code quality check
      run: npm run lint
```



---

## 🔄 Kokkuvõte ja Praktilised Soovitused

### Git'i Workflow Kokkuvõte

Git'i kasutamine on nagu rutiin - mida rohkem sa seda teed, seda loomulikumaks see muutub. Siin on kaks põhilist töövoogu, mida sa kasutad erinevates olukordades.

```mermaid
graph TD
    subgraph "Iga päev"
        A1[git status] --> A2[git pull origin main]
        A2 --> A3[tee tööd]
        A3 --> A4[git add .]
        A4 --> A5[git commit]
        A5 --> A6[git push origin main]
    end
    
    subgraph "Uue feature töötamisel"
        B1[git checkout main] --> B2[git pull origin main]
        B2 --> B3[git checkout -b feature]
        B3 --> B4[tee tööd]
        B4 --> B5[git push origin feature]
        B5 --> B6[Loo PR GitHub'is]
    end
    
    style A1 fill:#e1f5fe
    style A6 fill:#e8f5e8
    style B1 fill:#e1f5fe
    style B6 fill:#e8f5e8
```



### Olulised Git'i Käsud Reference

| Kategooria | Käsk | Kirjeldus |
|------------|------|-----------|
| **Setup** | `git config --global user.name "Nimi"` | Kasutaja seadistamine |
| **Basics** | `git init`, `git add`, `git commit` | Põhilised operatsioonid |
| **Info** | `git status`, `git log`, `git diff` | Oluku vaatamine |
| **Branching** | `git branch`, `git checkout`, `git merge` | Harude haldamine |
| **Remote** | `git clone`, `git push`, `git pull` | Kaugrepositooriumid |

> **📋 Täielik käskude nimekiri:** Vaata faili [`git_commands_reference.md`](./git_commands_reference.md) kõigi käskude ja nende selgitustega.

### Parimad Praktikad

Git'i kasutamisel on oluline järgida häid tavasid, mis aitavad sul ja teistel mõista, mida sa teed. Need on nagu "koodi etikett" - nad teevad sinu töö professionaalsemaks.

1. **Commit'ide sõnumid:**
   - Alusta verbiga: "Lisa", "Paranda", "Eemalda"
   - Esimene rida < 50 tähemärki
   - Selgita "miks", mitte "mis"

2. **Branch'ide nimetamine:**
   - `feature/kasutaja-login`
   - `bugfix/paranda-valideerimist`
   - `hotfix/kiire-turvauuendus`

3. **Merge vs Rebase:**
   - **Merge** - säilitab ajaloo, aga on segasem
   - **Rebase** - puhas ajalugu, aga keerulisem

4. **Turvalisus:**
   - Kasuta SSH võtmeid
   - Ära kommiti saladusi (API keys, paroolid)
   - Kasuta .gitignore faili

### Järgmised Sammud

Pärast seda loengut peaksite oskama:
- ✅ Git'i kohalikult kasutada
- ✅ GitHub'iga töötada
- ✅ Meeskonnatööd Pull Request'idega
- ✅ Konflikte lahendada
- ✅ CI/CD põhimõtteid mõista

**Praktiseerige neid oskusi iga päev - Git on nagu jalgrattasõit, harjutamine teeb meistriks!**

---

*Materjal põhineb tööstuse standarditel ja GitHub'i ametlikul dokumentatsioonil*