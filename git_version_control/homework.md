# Nädal 9 Kodutöö: Git Projekti Portfolio

**Tähtaeg:** Järgmise nädala alguseks  
**Eesmärk:** Demonstreerida Git'i ja GitHub'i oskusi  
**Aeg:** 2 tundi praktilist tööd

---

## 🎯 Ülesande Kirjeldus

Looge lihtne projekt, mis demonstreerib kõiki Git'i ja GitHub'i peamisi oskusi. **Fookus on Git workflow'l, mitte koodi keerukusel.**

## 🔄 OLULINE: Õige Git Flow

```
main (toodang)        ●─────────●─────────●
                       \         \         \  
develop (test)          ●─────●───●─────●───●
                         \     \ /     /
feature branch'id        ●─────●─────●
```

**ALATI järgige:** feature → develop → main

**MITTE KUNAGI:** feature → main

---

## 🚀 Juhend

### Samm 1: Repository Loomine (20 min)

1. **GitHub'is looge uus repository**
   - Nimi: `its-git-demo` (või sarnane)
   - Public, README, MIT license

2. **Kloonige repository**
   ```bash
   git clone https://github.com/teie-nimi/its-git-demo.git
   cd its-git-demo
   ```

3. **Looge põhilised failid**
   - Muutke README.md
   - Looge .gitignore: `echo "*.log\n*.tmp" > .gitignore`

4. **Esimene commit**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### Samm 2: Lihtne Script (25 min)

1. **Looge develop branch**
   - Minge main branch'ilt develop branch'ile
   - Push'ige develop branch GitHub'i

2. **Looge feature branch**
   - Develop branch'ilt looge uus branch, näiteks "feature/system-info"
   - Vahetage sellele branch'ile

3. **Kirjutage lihtne script**
   - Looge bash script fail (näiteks system_info.sh)
   - **Kopeerige see kood:**
     ```bash
     #!/bin/bash
     echo "=== System Information ==="
     echo "Date: $(date)"
     echo "User: $(whoami)"
     echo "Current directory: $(pwd)"
     echo "Home directory: $HOME"
     echo ""
     echo "=== Disk Usage ==="
     df -h | head -5
     echo ""
     echo "=== Memory Info ==="
     free -h 2>/dev/null || echo "Memory info not available"
     echo ""
     echo "Script completed successfully!"
     ```
   - Tehke script käivitatavaks: `chmod +x system_info.sh`
   - Testige script'i: `./system_info.sh`

4. **Looge dokumentatsioon**
   - Looge USAGE.md fail
   - **Kopeerige see sisu:**
     ```markdown
     # Usage Guide
     
     ## System Info Script
     
     ### Purpose
     Shows basic system information.
     
     ### Usage
     ```bash
     ./system_info.sh
     ```
     
     ### Output
     Script displays:
     - Current date and time
     - Current user name
     - Current directory path
     - Disk usage information
     - Memory information
     
     ### Requirements
     - Bash shell
     - Unix/Linux system
     ```

5. **Seadistage GitHub Actions**
   - Looge `.github/workflows` kaust
   - Looge test.yml fail:
   ```yaml
   name: Test
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       - run: |
           bash -n system_info.sh
           chmod +x system_info.sh
           ./system_info.sh
   ```

6. **Commit ja push kõik muudatused**
   - **Staging area selgitus:** Git'is on 3 ala:
     - Working Directory (teie failid)
     - Staging Area (failid valmis commit'iks) ⬅️ SIIN
     - Repository (commit'itud failid)
   - Lisage kõik failid staging area'le: `git add .`
   - Vaadake olekut: `git status` (rohelised failid on staging area's)
   - Tehke commit selge sõnumiga: `git commit -m "feat: add system info script and docs"`
   - Push'ige feature branch GitHub'i: `git push origin feature/system-info`

### Samm 3: GitHub Features (35 min)

1. **Looge Issues GitHub'is**
   - Issue #1: "Add system info script" - märgistage label'iga "enhancement"
   - Issue #2: "Improve documentation" - märgistage label'iga "documentation"

2. **Tehke Pull Request**
   - GitHub'is looge PR: feature/system-info → develop
   - **OLULINE:** PR PEAB minema develop branch'i, MITTE main'i
   - Kirjutage hea pealkiri ja kirjeldus
   - Mainige, et see lahendab Issue #1 ("Closes #1")
   - Merge'ige PR (ise endale)

3. **Cleanup pärast PR merge'it**
   - Minge develop branch'ile: `git checkout develop`
   - Pull'ige muudatused: `git pull origin develop`
   - Kustutage feature branch: `git branch -d feature/system-info`
   - Kustutage remote feature branch: `git push origin --delete feature/system-info`

4. **Testige GitHub Actions**
   - Vaadake GitHub'is Actions tab'is
   - Veenduge, et workflow töötab
   - Kui ei tööta, parandage vead

### Samm 4: Git Advanced Features (25 min)

1. **Looge tahtlikult merge conflict**
   - Minge develop branch'ile: `git checkout develop`
   - Muutke README.md faili (lisage rida lõppu): "Develop branch versioon"
   - Commit'ige: `git commit -am "docs: update from develop"`
   
   - Minge main branch'ile: `git checkout main`  
   - Muutke README.md SAMA KOHTA teisiti: "Main branch versioon"
   - Commit'ige: `git commit -am "docs: update from main"`
   
   - Nüüd merge develop → main: `git merge develop`
   - Git ütleb konflikt! ✅

2. **Lahendage merge conflict**
   - Avage README.md ja näete konflikti märke
   - **Konflikti näide:**
     ```
     <<<<<<< HEAD
     Main branch versioon
     =======
     Develop branch versioon
     >>>>>>> develop
     ```
   - Otsustage, kumba versiooni hoida või kombineerige
   - Eemaldage konflikti märgid (<<<<, ====, >>>>)
   - Lisage fail staging area'le
   - Lõpetage merge commit'iga

3. **Näidake rebase kasutamist**
   - Looge uus feature branch develop'ist: `git checkout -b feature/rebase-demo`
   - Tehke seal mõni muudatus ja commit
   - Kasutage git rebase käsku main branch'i peale: `git rebase main`
   - Merge'ige muudatus develop'i

4. **TÄHTIS: Merge develop → main (toodangusse)**
   - Kui develop on valmis: `git checkout main`
   - Merge develop: `git merge develop`
   - Push toodangusse: `git push origin main`

5. **Looge tagged release'd**
   - Tag'ige praegune main versioon v1.0.0: `git tag v1.0.0`
   - Push'ige tag'id GitHub'i: `git push origin v1.0.0`
   - GitHub'is looge Release v1.0.0 tag'i põhjal

### Samm 5: Finalize (15 min)

1. **Uuendage README.md**
   - **Kopeerige see sisu README.md faili:**
     ```markdown
     # Git Demo Project
     
     Lihtne projekt Git ja GitHub oskuste demonstreerimiseks.
     
     ## Eesmärk
     See projekt näitab:
     - Git branching ja merging
     - GitHub collaboration
     - Automatiseeritud testimine
     - Dokumentatsiooni haldus
     
     ## Git Oskused
     - ✅ Repository seadistamine
     - ✅ Feature branch workflow
     - ✅ Merge conflict lahendamine
     - ✅ Pull Request'id
     - ✅ GitHub Actions
     - ✅ Tagged release'id
     
     ## Failid
     - `system_info.sh` - Süsteemi info script
     - `USAGE.md` - Kasutamise juhend
     - `.github/workflows/test.yml` - Automaatne testimine
     
     ## Kasutamine
     ```bash
     ./system_info.sh
     ```
     
     See on õppeprojekt Git workflow demonstreerimiseks.
     ```

2. **Tehke teine release**
   - Commit'ige README muudatused develop branch'is
   - Merge develop → main
   - Tag'ige versioon v1.1.0
   - Push'ige kõik muudatused ja tag'id

3. **Lõplik kontroll**
   - Veenduge, et GitHub'is on näha:
     - Vähemalt 10 commit'i
     - Mitu branch'i
     - Issues ja PR
     - GitHub Actions töötab
     - 2 tag'i/release'i

---

 