#  Git Kodutöö: Minu Git Portfolio (1.5h)

**Tähtaeg:** Järgmise nädala algus  


---

##  Mis sa teed?

Loo GitHubis oma avalik repositoorium nimega `git-portfolio` (või muu nimi, mis sulle meeldib). See on nagu sinu CV, aga koodis – näita, et oskad Git'i kasutada nagu proff! 

---

##  Samm-sammult juhend

### Osa 1: Ettevalmistus (0–15 min)

1. **Loo GitHubis uus avalik repositoorium:**
   - Nimi: `git-portfolio` (või `minu-esimene-git-projekt`)
   - Avalik (public)
   - Lisa **README.md** kohe (linnuke)
   - Lisa **.gitignore** (vali Python, Node, või muu, mis sobib)
   - Lisa **MIT License** (linnuke)

2. **Klooni oma arvutisse:**
   ```bash
   git clone https://github.com/SINU-KASUTAJANIMI/git-portfolio.git
   cd git-portfolio
   ```

3. **Kontrolli, et töötab:**
   ```bash
   git status
   git log --oneline
   ```

---

### Osa 2: Projekt ja commit'id (15–60 min)

**Vali üks projektitüüp:**

**Variant A: Python kalkulaator**
- `calculator.py` – lihtne kalkulaator (add, subtract, multiply, divide)
- `README.md` – kuidas kasutada
- `.gitignore` – ignoreeri `*.pyc`, `__pycache__/`

**Variant B: HTML/CSS veebileht**
- `index.html` – lihtne portfolio leht
- `style.css` – disain
- `README.md` – kuidas avada
- `.gitignore` – ignoreeri `.DS_Store`, `Thumbs.db`

**Variant C: Bash/Python skriptid**
- `backup.sh` või `backup.py` – faili varukoopia skript
- `cleanup.sh` või `cleanup.py` – temp failide puhastus
- `README.md` – kuidas kasutada
- `.gitignore` – ignoreeri `*.log`, `*.tmp`

**Vaba variant:** Tee midagi enda huvitavat! (väike mäng, script, veebileht, jne)

---

**Tee vähemalt 5 commit'i:**

Näited headest commit-sõnumitest:
```bash
git add README.md
git commit -m "Lisa README projekti kirjeldusega"

git add calculator.py
git commit -m "Lisa põhilised matemaatilised funktsioonid (add, subtract)"

git add calculator.py
git commit -m "Lisa multiply ja divide funktsioonid"

git add .gitignore
git commit -m "Lisa .gitignore Python cache failide jaoks"

git add README.md
git commit -m "Täienda README kasutamisjuhendiga ja näidetega"
```

 **Halvad näited (ära tee nii):**
```bash
git commit -m "fix"
git commit -m "update"
git commit -m "asdf"
git commit -m "WIP"
```

---

**Näpunäiteid:**

- Tee `git status` enne iga commit'i – vaata, mis on muutunud
- Kasuta `git log --oneline` – vaata oma ajalugu
- Kasuta `git diff` – vaata täpselt, mida muutsid
- Iga commit peaks olema **üks loogiline muudatus**, mitte kõik korraga

---

### Osa 3: Push ja viimistlus (60–90 min)

1. **Push'i oma muudatused GitHubi:**
   ```bash
   git push origin main
   ```

2. **Kontrolli GitHubis:**
   - Kas kõik failid on nähtavad?
   - Kas commit-sõnumid on loetavad?
   - Kas `.gitignore` töötab? (temp failid ei ole repos)

3. **Täienda README.md:**
   Lisa oma README.md faili lõppu **refleksioon** (vastused küsimustele):

---

##  Refleksioon (kirjuta README.md lõppu)

Lisa oma README.md faili lõppu peatükk **"## Refleksioon"** ja vasta järgmistele küsimustele:

### Küsimused (vasta 2-3 lausega igaühele):

1. **Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?**
   - Näide: "Kõige raskem oli mõista, mis vahe on `git add` ja `git commit` vahel. Aitasin end sellest välja, et lugesin dokumentatsiooni ja tegin mitu testkorda."

2. **Milline Git käsk või kontseptsioon oli sulle kõige suurem "ahaa!"-elamus ja miks?**
   - Näide: "Git log --oneline oli mulle suur avastus, sest nägin esimest korda oma projekti ajalugu nagu ajajoont!"

3. **Kuidas saaksid Git'i kasutada oma teistes koolitöödes või isiklikes projektides?**
   - Näide: "Võiksin Git'i kasutada oma matemaatika kodutööde jaoks, et jälgida, kuidas mu lahendused arenevad."

4. **Kui peaksid oma sõbrale selgitama, mis on Git ja miks see on kasulik, siis mida ütleksid?**
   - Näide: "Git on nagu Ctrl+Z aga superjõul – saad alati tagasi minna ja vaadata, mis sa tegid!"

5. **Mis oli selle projekti juures kõige lõbusam või huvitavam osa?**
   - Näide: "Mulle meeldis, et ma sain oma koodi GitHubi panna ja nüüd saavad teised seda näha!"

---

##  Kontrollnimekiri (enne esitamist)

**Kontrolli need asjad:**

- [ ] GitHubis on avalik repositoorium `git-portfolio` (või muu nimi)
- [ ] Repos on vähemalt 3 erinevat faili (README, projekt, .gitignore)
- [ ] Ajalugu sisaldab **vähemalt 5 tähenduslikku commit'i**
- [ ] Iga commit-sõnum on selge ja kirjeldab **MIKS** sa selle muudatuse tegid
- [ ] `.gitignore` fail on olemas ja töötab (temp failid ei ole repos)
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus (mis see on?)
  - [ ] Kuidas kasutada (käivitamise juhend)
  - [ ] Refleksioon (5 küsimuse vastused, 2-3 lauset igaüks)
- [ ] Kõik muudatused on GitHubi push'itud
- [ ] Repository on **avalik** ja ligipääsetav

---

##  Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Repo struktuur** | 15% | Repo on korras, `.gitignore` töötab, failid organiseeritud |
| **Commit kvaliteet** | 40% | ≥5 commit'i; sõnumid selged, kirjeldavad ja põhjendavad |
| **Töövoog** | 15% | `add → commit → push` õigesti kasutatud; `status`/`log` nähtav |
| **README** | 15% | Projekti kirjeldus, kasutamisjuhend, selge ja informatiivne |
| **Refleksioon** | 15% | 5 küsimust vastatud, sisukas, näitab mõistmist (2-3 lauset/küsimus) |

**Kokku: 100%**

---

##  Abimaterjalid ja lugemine (enne kodutöö tegemist)

**Kiirviited:**
- [Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
- [Kuidas kirjutada head commit-sõnumit?](../reference/commit_guide.md)
- [`.gitignore` näited](https://github.com/github/gitignore)

**Video tutor'id (valikuline):**
- [Git in 15 minutes](https://www.youtube.com/watch?v=USjZcfj8yxE) (inglise keeles)
- [GitHub for Beginners](https://www.youtube.com/watch?v=RGOj5yH7evk) (inglise keeles)

**Kui abi vaja:**
1. Vaata `lisapraktika.md` faili täiendavate näidete jaoks
2. Kasuta `git --help` või `git <käsk> --help`
3. Küsi klassikaaslaselt või õpetajalt

---

##  Boonus (valikuline, +10%)

**Kui tahad ekstra punkte, tee üks või mitu neist:**

1. **Lisa Git tag:** Märgi oma "1.0 versioon" tag'iga
   ```bash
   git tag -a v1.0 -m "Esimene töötav versioon"
   git push origin v1.0
   ```

2. **Lisa GitHub README badge:** Näiteks "Made with " või "License: MIT"
   - [Shields.io](https://shields.io/) badge generaator

3. **Tee branch ja merge:** Loo `feature/new-feature` branch, tee muudatus, merge main'i
   ```bash
   git checkout -b feature/lisafunktsioon
   # tee muudatus
   git add .
   git commit -m "Lisa uus funktsioon"
   git checkout main
   git merge feature/lisafunktsioon
   git push origin main
   ```

4. **Paranda oma GitHub profiil:** Lisa profile README (vaata [neid näiteid](https://github.com/abhisheknaiidu/awesome-github-profile-readme))

---

##  Esitamine

**Kuidas esitada:**

1. Veendu, et repositoorium on **avalik** (public)
2. Mine oma GitHub repo lehele
3. Kopeeri URL (näiteks: `https://github.com/SINU-KASUTAJANIMI/git-portfolio`)
4. Esita see link õpetajale (e-mail või õppeplatvorm)

**Alternatiiv (kui ei saa GitHubi kasutada):**
- Tee `.zip` fail oma projektist
- Lisa juurde `git_log.txt` fail: `git log --oneline > git_log.txt`
- Esita ZIP fail

---

**Edu ja head Git'itamist!** 

**P.S.** Pärast kodutöö esitamist võid jätkata projekti arendamist ja lisada sinna rohkem asju – see on sinu enda portfoolio!  
