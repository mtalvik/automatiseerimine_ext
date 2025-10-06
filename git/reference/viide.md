#  Git Käsud Viitematerjal

**Eesmärk:** Kiire viide kõigile Git käsudele  
**Kasutamine:** Kasutage seda viidet, kui vajate kiiret abi Git käskude kohta

---

##  Põhilised Käsud

### Seadistamine
```bash
git config --global user.name "Teie Nimi"
git config --global user.email "teie.email@example.com"
git config --list
```

### Repository Loomine
```bash
git init                    # Uue repo loomine
git clone URL               # Olemasoleva repo kopeerimine
```

### Põhiline Töövoog
```bash
git status                  # Vaata olekut
git add .                   # Lisa kõik muudatused
git commit -m "Sõnum"       # Salvesta muudatused
git push origin main        # Saada muudatused
git pull origin main        # Võta uusimad muudatused
```

##  Info ja Ajalugu

### Muudatuste Vaatamine
```bash
git diff                    # Töökausta vs staging
git diff --staged           # Staging vs viimane commit
git diff HEAD~1             # Viimase commit'iga võrdlus
git show                    # Viimane commit
git show commit-hash        # Konkreetne commit
git show --stat             # Statistika koos
```

### Ajaloo Vaatamine
```bash
git log --oneline          # Kompaktne vaade
git log --graph            # Visuaalne harudemudel  
git log --author="Nimi"    # Konkreetse autori commit'id
git blame fail.txt         # Kes millise rea muutis
```

##  Harude (Branches) Haldamine

### Harude Loomine ja Vahetamine
```bash
git branch                  # Vaata harusid
git branch -v               # Koos viimase commit'iga
git branch -a               # Kõik harud (ka remote)
git branch funktsioon-login # Loo uus haru
git checkout -b funktsioon-login  # Loo ja vaheta haru
git checkout main          # Vaheta main harule
git switch -c funktsioon-login  # Uuem süntaks
git switch main            # Uuem süntaks
```

### Harude Ühendamine
```bash
git merge branch-nimi       # Ühenda haru
git merge --no-ff branch-nimi  # Merge ilma fast-forward'ta
git merge --abort          # Katkesta merge
```

### Rebase
```bash
git rebase origin/main      # Rebase kohalikud commit'id
git rebase -i origin/main   # Interaktiivne rebase
git rebase -i HEAD~3        # Viimased 3 commit'i
git rebase --abort          # Katkesta rebase
git rebase --continue       # Jätka pärast konfliktide lahendamist
```

##  Kaugrepositooriumid (Remote)

### Remote'ide Haldamine
```bash
git remote -v              # Vaata remote'ide URL'e
git remote show origin     # Remote'i info
git remote add origin URL  # Lisa remote
git remote rename origin upstream  # Nimetage remote ümber
git remote remove old-remote      # Eemalda remote
git remote set-url origin uus-url # Muuda URL'i
```

### Fetch ja Pull
```bash
git fetch origin           # Too info serverist
git fetch origin main      # Konkreetse haru info
git fetch --all            # Kõigi remote'ide info
git pull origin main       # Fetch + merge
git pull --rebase origin main  # Rebase pull
git pull --ff-only origin main # Ainult fast-forward
```

### Push
```bash
git push origin main       # Saada muudatused
git push -u origin main    # Esimene kord (tracking)
git push origin funktsioon-login  # Uue haru saatmine
git push origin --delete funktsioon-login  # Haru kustutamine
```

##  Failide Haldamine

### Failide Lisamine ja Eemaldamine
```bash
git add failinimi.txt      # Lisa konkreetne fail
git add .                  # Lisa kõik muudatused
git rm failinimi.txt       # Kustuta fail Git'ist ja süsteemist
git rm --cached failinimi.txt  # Kustuta ainult Git'ist
git mv vana.txt uus.txt    # Nimetage fail ümber
```

### Muudatuste Tagasivõtmine
```bash
git checkout -- failinimi.txt  # Taasta fail viimase commit'i olekusse
git checkout -- .              # Taasta kõik failid
git reset HEAD failinimi.txt   # Eemalda fail staging'ust
git reset HEAD                 # Eemalda kõik failid staging'ust
```

##  Commit'ide Haldamine

### Commit'ide Muutmine
```bash
git commit --amend -m "Uus sõnum"  # Muuda viimast commit'i
git commit --amend --no-edit       # Lisa faile viimase commit'i
git commit -am "Sõnum"             # Lisa ja commit kõik muudetud failid
```

### Commit'ide Tagasivõtmine
```bash
git revert commit-hash      # Turvaline tagasivõtmine (loob uue commit'i)
git revert commit1..commit2 # Mitme commit'i tagasivõtmine
git reset --soft HEAD~1     # Jätab muudatused staging'u
git reset --mixed HEAD~1    # Jätab muudatused töökausta
git reset --hard HEAD~1     # Kustutab muudatused täielikult
```

### Commit'ide Identifitseerimine
```bash
git show HEAD               # Viimane commit
git show HEAD~1             # Eelmine commit
git show HEAD~2             # Kaks commit'i tagasi
git show branch-name^       # Eelmine commit
git show branch-name~3      # Kolm commit'i tagasi
git show a1b2c3d            # Lühike hash
git show v1.0.0             # Tag
```

##  Ajutine Salvestamine (Stash)

```bash
git stash                   # Salvesta muudatused ajutiselt
git stash pop              # Taasta salvestatud muudatused
git stash list             # Vaata stash'e
git stash apply stash@{0}  # Taasta konkreetne stash
git stash drop stash@{0}   # Kustuta stash
git stash clear            # Kustuta kõik stash'ed
```

##  Otsimine ja Filtreerimine

```bash
git log --grep="sõna"      # Otsi commit'ides
git log -S "sõna"          # Otsi muudatuste sisus
git log --since="2023-01-01"  # Filtreeri kuupäeva järgi
git log --until="2023-12-31"  # Filtreeri kuupäeva järgi
git log --author="Nimi"    # Filtreeri autori järgi
git log --oneline -10      # Viimased 10 commit'i
```

##  Tag'id

```bash
git tag v1.0.0             # Loo tag
git tag -a v1.0.0 -m "Sõnum"  # Annotated tag
git tag -l                 # Vaata tag'e
git show v1.0.0            # Vaata tag'i info
git push origin v1.0.0     # Saada tag
git push origin --tags     # Saada kõik tag'id
```

##  Konfliktide Lahendamine

```bash
git status                 # Näitab konfliktilisi faile
git diff                   # Näitab konfliktide detaile
git mergetool              # Avab graafilise lahendaja
git add konfliktne-fail.txt # Pärast konfliktide lahendamist
```

##  Alias'id ja Konfiguratsioon

### Kasulikud Alias'id
```bash
# Lisa need git config'u
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

### Kasutamine
```bash
git st                     # git status
git co main               # git checkout main
git br                    # git branch
git ci -m "sõnum"        # git commit -m "sõnum"
git unstage fail.txt     # git reset HEAD -- fail.txt
```

##  Hoiatused ja Nõuanded

### Ära tee kunagi:
- `git push --force` shared branch'ides
- `git reset --hard` salvestamata muudatustega
- `git clean -fd` ilma kontrollimata
- Commit'i saladusi (API keys, paroolid)

### Kasuta alati:
- `git push --force-with-lease` force push'i asemel
- `git status` enne keerulisi operatsioone
- Selgeid commit sõnumeid
- `.gitignore` faili

##  Lisaressursid

- [Git'i ametlik dokumentatsioon](https://git-scm.com/doc)
- [Git'i visuaalne õpetus](https://git-scm.com/book/en/v2)
- [Git'i cheatsheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Git'i branching model](https://nvie.com/posts/a-successful-git-branching-model/)

---

*See viide sisaldab kõige populaarsemaid ja kasulikumaid Git käske. Täpsem info leiad Git'i ametlikust dokumentatsioonist.*
