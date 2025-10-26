# Git Kodutöö: Isiklik Projekt Repositoorium

**Kestus:** 2-3h  
**Eesmärk:** Õppida Git'i läbi reaalse töövoo, kus töötad nii lokaalselt kui GitHubis paralleelselt.

---

## Mis sa õpid?

- ✅ Remote repo ühendamine
- ✅ Branch'idega töötamine (eraldi arendus)
- ✅ Merge konfliktide lahendamine
- ✅ VSCode Source Control kasutamine
- ✅ GitHub ja lokaali paralleelne jälgimine
- ✅ Pull request workflow
- ✅ Ajas liikumine (checkout vanad versioonid)

---

## Osa 1: Setup ja esimene push

### 1.1 GitHub repo loomine

1. Mine [github.com](https://github.com)
2. **New repository**
3. Nimi: `git-treening`
4. **Public**
5. **ÄRA** lisa README, .gitignore ega license
6. **Create repository**

**GitHub näitab sulle nüüd kahte varianti:**

```bash
# ...create a new repository on the command line
echo "# git-treening" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/KASUTAJANIMI/git-treening.git
git push -u origin main
```

**STOP!** Ära kopeeri veel. Vaatame, mis need käsud teevad.

---

### 1.2 Lokaalne repo loomine

```bash
mkdir git-treening
cd git-treening
git init
```

**Väljund:**
```
Initialized empty Git repository in /path/to/git-treening/.git/
```

**Kontrolli:**
```bash
git status
```

**Näed:**
```
On branch master
No commits yet
nothing to commit (create/copy files and use "git add" to track)
```

**Ava VSCode:**
```bash
code .
```

**VSCode Source Control (Ctrl+Shift+G):**
- Näitab: "No source control providers registered"
- Või: tühi puu, kuna pole veel faile

---

### 1.3 Esimene fail ja commit

**Loo index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Git Treening</title>
</head>
<body>
    <h1>Versioon 1</h1>
    <p>See on algversioon</p>
</body>
</html>
```

**VSCode Source Control:**
- Näed "U" (Untracked) index.html kõrval
- See tähendab: Git ei jälgi veel seda faili

**Käsurealt:**
```bash
git status
```

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html

nothing added to commit but untracked files present
```

**Stage fail:**

**VSCode-s:** Vajuta `+` faili kõrval

**VÕI käsurealt:**
```bash
git add index.html
```

**VSCode näitab nüüd:** "A" (Added/Staged)

**Tee commit:**

**VSCode-s:**
- Kirjuta üles: `Initial commit`
- Vajuta ✓

**VÕI käsurealt:**
```bash
git commit -m "Initial commit"
```

**Kontrolli:**
```bash
git log
```

Näed oma esimest commit'i!

---

### 1.4 Ühenda GitHubiga

**GitHub käsud (mäletad?):**
```bash
git branch -M main
git remote add origin https://github.com/KASUTAJANIMI/git-treening.git
git push -u origin main
```

**Mis need teevad?**

1. `git branch -M main` - muuda haru nimi "master" → "main"
2. `git remote add origin URL` - ütle Git'ile, kus on remote repo
3. `git push -u origin main` - saada kõik GitHubi

**Kontrolli remote:**
```bash
git remote -v
```

```
origin  https://github.com/KASUTAJANIMI/git-treening.git (fetch)
origin  https://github.com/KASUTAJANIMI/git-treening.git (push)
```

**Push:**
```bash
git push -u origin main
```

**Mine GitHubi ja refreshi lehte** - index.html peaks seal olema!

**VSCode alt vasakul:** Näed nüüd "main" ↓0 ↑0 (kõik sync-itud)

---

## Osa 2: Branch workflow

### 2.1 Loo styling branch

**VSCode-s:**
- Alt vasak: vajuta "main"
- "Create new branch from..."
- Nimi: `feature/styling`

**VÕI käsurealt:**
```bash
git checkout -b feature/styling
```

```
Switched to a new branch 'feature/styling'
```

**VSCode alt:** Näitab nüüd "feature/styling"

---

### 2.2 Lisa CSS

**Loo style.css:**
```css
body {
    background-color: #f5f5f5;
    font-family: Arial, sans-serif;
    padding: 20px;
}

h1 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
}
```

**Muuda index.html:**
```html
<head>
    <title>Git Treening</title>
    <link rel="stylesheet" href="style.css">
</head>
```

**VSCode Source Control:**
- Näed kahte faili:
  - "U" style.css (uus)
  - "M" index.html (modified)

**Stage + commit:**
- VSCode: Stage mõlemad → commit "Add CSS styling"

**VÕI:**
```bash
git add .
git commit -m "Add CSS styling"
```

---

### 2.3 Push branch GitHubi

```bash
git push -u origin feature/styling
```

**VÕI VSCode-s:** vajuta "Publish Branch"

**Mine GitHubi:**
- Branches dropdown → näed `feature/styling`
- **Vaheta main ja feature/styling vahel** - näed, et main-is pole CSS'i!

**See on võimas!** Kaks paralleelset versiooni eksisteerib korraga.

---

### 2.4 Täienda CSS branch-is

**Jätka feature/styling-s:**
```css
/* Lisa style.css lõppu */
p {
    font-size: 18px;
    line-height: 1.6;
    color: #555;
}
```

**Commit:**
```bash
git add style.css
git commit -m "Improve paragraph styling"
git push
```

**Kontrolli GitHubis:**
- feature/styling → 2 commits ahead of main
- Vaata "Compare" - näed kõiki muudatusi!

---

## Osa 3: Konfliktid ja merge

### 3.1 Paralleelne töö main-is

**Mine tagasi main-i:**
```bash
git checkout main
```

**VSCode:**
- style.css KADUS (see on normaalne!)
- Alt näitab: "main"

**Muuda index.html:**
```html
<body>
    <h1>Versioon 2 - main harus</h1>
    <p>See on algversioon</p>
</body>
```

**Commit + push:**
```bash
git add index.html
git commit -m "Update heading in main"
git push
```

**Kontrolli GitHubis main-is** - CSS pole ikka veel seal, aga heading muutus!

---

### 3.2 Tekita konflikt

**Mine feature/styling-sse:**
```bash
git checkout feature/styling
```

**Muuda SAMAS kohas:**
```html
<body>
    <h1>Versioon 2 - koos stylinguga</h1>
    <p>See on algversioon</p>
</body>
```

**Commit:**
```bash
git add index.html
git commit -m "Update heading in feature branch"
git push
```

**Nüüd sul on kaks erinevat muudatust samas kohas!**

---

### 3.3 Merge ja konflikt

**Mine main-i:**
```bash
git checkout main
git merge feature/styling
```

**BOOM! Konflikt:**
```
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

**VSCode Source Control:**
- Näed "!" index.html kõrval (conflict)
- Ava fail

**VSCode näitab:**
```html
<body>
<<<<<<< HEAD
    <h1>Versioon 2 - main harus</h1>
=======
    <h1>Versioon 2 - koos stylinguga</h1>
>>>>>>> feature/styling
    <p>See on algversioon</p>
    <link rel="stylesheet" href="style.css">
</body>
```

**VSCode pakub nuppe:**
- Accept Current Change (jätab main-i versiooni)
- Accept Incoming Change (võtab feature/styling)
- Accept Both Changes
- Compare Changes

**Vali "Accept Both" VÕI kirjuta käsitsi:**
```html
<h1>Versioon 3 - liitmine valmis</h1>
```

**Kustuta konfliktimärgid:**
```html
<body>
    <h1>Versioon 3 - liitmine valmis</h1>
    <p>See on algversioon</p>
    <link rel="stylesheet" href="style.css">
</body>
```

**Stage + commit:**
```bash
git add index.html
git commit -m "Merge feature/styling, resolve conflicts"
git push
```

**Kontrolli GitHubis:**
- Commits → näed merge commit'i
- Insights → Network → näed graafiliselt hargnemist ja liitmist!

---

## Osa 4: Ajas liikumine

### 4.1 Vaata ajalugu

```bash
git log --oneline --graph --all
```

```
*   a1b2c3d (HEAD -> main) Merge feature/styling
|\  
| * d4e5f6g (feature/styling) Update heading in feature branch
| * g7h8i9j Improve paragraph styling
| * j1k2l3m Add CSS styling
* | m4n5o6p Update heading in main
|/  
* p7q8r9s Initial commit
```

**Kopeeri mõni vana hash, nt `p7q8r9s`**

---

### 4.2 Mine tagasi ajas

```bash
git checkout p7q8r9s
```

```
Note: switching to 'p7q8r9s'.
You are in 'detached HEAD' state.
```

**VSCode:**
- Alt näitab: "detached at p7q8r9s"
- Ava index.html - näed ALGSET versiooni!
- style.css PUUDUB

**See on võimas!** Sa ei kustutanud midagi, lihtsalt vaatad vana hetke.

**Tule tagasi:**
```bash
git checkout main
```

---

### 4.3 VSCode Timeline

**VSCode-s:**
- Parem klikk index.html-l
- "Open Timeline"
- Näed kõiki muudatusi kellaajaga
- Kliki vana versiooni - avaneb diff!

---

## Osa 5: Pull ja sync

### 5.1 Keegi muutis GitHubis

**Mine oma GitHub repo:**
1. Vajuta index.html
2. Pencil ikoon (edit)
3. Lisa:
```html
<p>See rida lisati otse GitHubis!</p>
```
4. Commit changes (all vasakul)

**Nüüd GitHub on sinu lokallist ees!**

---

### 5.2 Pull muudatused alla

**VSCode alt:** Näitab ↓1 (üks commit tulla)

**Pull:**
```bash
git pull origin main
```

**VÕI VSCode-s:** vajuta "sync" ikoonile

**Ava index.html** - uus rida on seal!

---

## Osa 6: Pull Request workflow

### 6.1 Loo uus feature

```bash
git checkout -b feature/footer
```

**Lisa index.html lõppu:**
```html
<footer>
    <p>&copy; 2025 Git Treening</p>
</footer>
```

**Lisa style.css lõppu:**
```css
footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #ccc;
    text-align: center;
    color: #777;
}
```

**Commit + push:**
```bash
git add .
git commit -m "Add footer"
git push -u origin feature/footer
```

---

### 6.2 Tee Pull Request GitHubis

**GitHub näitab bänneri:**
"feature/footer had recent pushes - Compare & pull request"

**Vajuta nuppu:**
1. Pealkiri: "Add footer section"
2. Kirjeldus:
```
## Muudatused
- Lisasin footer sektsiooni
- Lisasin footer CSS

## Testimine
Ava index.html brauseris ja kontrolli footer-it
```
3. **Create pull request**

**Nüüd näed:**
- "Files changed" tab - diff kõigist muudatustest
- "Commits" tab - kõik commit-id selles PR-is

**Merge pull request:**
1. Vajuta rohelist nuppu
2. Confirm merge
3. Delete branch (soovi korral)

---

### 6.3 Uuenda lokaali

```bash
git checkout main
git pull origin main
```

**footer on nüüd main-is!**

**Kontrolli:**
```bash
git log --oneline
```

Näed merge commit-i PR-ist.

---

## Osa 7: Rollback ja cleanup

### 7.1 Soft reset (säilita muudatused)

**Kui teed vea commit-is:**
```bash
git reset --soft HEAD~1
```

**Muudatused jäävad staged-ks**, saad commit message'i parandada.

---

### 7.2 Hard reset (kustuta kõik)

**Kui tahad viimase commit-i TÄIELIKULT ära visata:**
```bash
git reset --hard HEAD~1
```

**HOIATUS:** Kaotad kõik muudatused!

---

### 7.3 Kustuta branch

**Lokaalselt:**
```bash
git branch -d feature/styling
```

**Remote-lt:**
```bash
git push origin --delete feature/styling
```

**VÕI GitHubis:** Branches → prügikast ikoon

---

## Lõplik harjutus: Full workflow

**Nüüd tee iseseisvalt:**

1. Loo branch `feature/colors`
2. Muuda CSS-is värve (h1, body background)
3. Commit + push
4. GitHubis: tee Pull Request
5. Lisa PR-ile kommentaar: "Palun vaata värve"
6. Merge
7. Lokaalselt: pull main
8. Kustuta feature/colors branch

---

## Kontrollküsimused

Pead oskama vastata:

1. **Mis vahe on `git fetch` ja `git pull` vahel?**
2. **Kuidas näha, mis branch-is sa oled?**
3. **Mis tähendab "detached HEAD"?**
4. **Kuidas tühistada staged fail?** (git reset HEAD file)
5. **Kus VSCode-s näed merge konflikte?**
6. **Mis juhtub, kui teed push aga keegi tegi pull request samal ajal?**
7. **Kuidas kustutada remote branch?**

---

## Reflection

Lisa README.md lõppu:

```markdown
## Minu kogemus

### Mis oli keeruline?
[2-3 lauset]

### Mis oli "ahaa!" hetk?
[2-3 lauset]

### VSCode vs käsurida
Kumba kasutaksid igapäevaselt ja miks?
[2-3 lauset]

### Pull Request workflow
Miks see on parem kui otse main-i push-ida?
[2-3 lauset]
```

---

## Esitamine

**Kontrolli:**
- [ ] Vähemalt 10 commit-i
- [ ] Vähemalt 2 branch-i loodud
- [ ] 1 merge konflikt lahendatud
- [ ] 1 Pull Request tehtud ja merge-tud
- [ ] README refleksiooniga

**Esita:**
`https://github.com/KASUTAJANIMI/git-treening`

---

**Edu! 🦧**
