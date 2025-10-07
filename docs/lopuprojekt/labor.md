# Lõpuprojekt Labor: Projekti Alustamine

**Eeldused:** Oled teinud Git ja Docker moodulid  
**Platvorm:** GitHub, Docker

---

## Õpivälјundid

Pärast laborit oskate:
- Loob Git repository projekti jaoks
- Valib 2 tööriista mida kasutada
- Kirjutab lihtsa README ja plaani
- Teeb esimese commit'i

---

## 1. Mis on Lõpuprojekt?

Lõpuprojekt on sinu võimalus näidata mida oled õppinud. Kasutad 2-3 tööriista mida me kursuselt õppisime.

**Ei pea olema perfektne!** Peab ainult töötama ja näitama et oskad tööriistu kasutada.

---

## 2. Vali 2 Tööriista

Vali 2 tööriista mida kasutad:

**Lihtsamad kombinatsioonid:**
- ✅ Git + Docker (kõige lihtsam)
- ✅ Docker + Ansible
- ✅ Git + Ansible

**Keerulisemad (ainult kui juba oskad):**
- Docker + Kubernetes
- Terraform + Ansible
- Kubernetes + Monitoring

**Kirjuta üles:**
```
Minu valik: Git + Docker
Miks: Tean neid juba ja saan kiiresti alustada
```

---

## 3. Vali Projekt

Vali lihtne projekt:

**Valik 1: Lihtne Veebirakendus**
- HTML lehekülg + andmebaas
- Näiteks: TODO list, blog, portfol

**Valik 2: Mingi Teenus**
- Backend API
- Näiteks: kasutajad, tooted, ilm

**Valik 3: Midagi Oma**
- Mis sind huvitab
- Aga peab olema LIHTNE!

**Kirjuta üles:**
```
Minu projekt: TODO list veebirakendus
Mis see teeb: Kasutaja saab lisada ja kustutada ülesandeid
```

---

## 4. Loo GitHub Repository

```bash
# Loo kaust
mkdir lopuprojekt
cd lopuprojekt

# Alusta Git'i
git init
git branch -M main

# Loo README
nano README.md
```

Kirjuta README'sse:

```markdown
# [Projekti Nimi]

## Mis see on?

[1-2 lauset]

## Kuidas kasutada?

Tuleb hiljem...

## Mis tööriistu kasutan?

- Git - versioonihaldus
- Docker - rakenduse käivitamine

## TODO

- [ ] Kirjuta kood
- [ ] Tee Dockerfile
- [ ] Testa
```

Salvesta: `Ctrl+O`, `Enter`, `Ctrl+X`

```bash
# Tee esimene commit
git add README.md
git commit -m "Initial commit"

# Loo GitHub'is uus repository ja siis:
git remote add origin https://github.com/[sinu-nimi]/lopuprojekt.git
git push -u origin main
```

**Kontrolli:**
- [ ] Repository on GitHub'is
- [ ] README on seal

---

## 5. Tee Plaan

Loo `PLAAN.md` fail:

```markdown
# Projekti Plaan

## Nädal 1

### Esmaspäev-Kolmapäev
- [ ] Kirjuta HTML/CSS
- [ ] Tee lihtne backend (kui vaja)
- [ ] Testi lokaalselt

### Neljapäev-Reede
- [ ] Loo Dockerfile
- [ ] Testi Docker'iga
- [ ] Kirjuta dokumentatsiooni

## Nädal 2

### Esmaspäev-Kolmapäev
- [ ] Lisa 2. tööriist (Ansible/K8s/vms)
- [ ] Testi et töötab
- [ ] Paranda vigu

### Neljapäev
- [ ] Vii kõik korras
- [ ] Kontrolli et dokumentatsioon on täielik
- [ ] Valmista ette esitlust

### Reede
- [ ] Esitlus!
```

```bash
git add PLAAN.md
git commit -m "Add project plan"
git push
```

---

## 6. Alusta Kodeerimist!

Nüüd on aeg alustada tööd:

### Kui teed veebirakendust:

```bash
# Loo failid
touch index.html
touch style.css
mkdir app
```

### Kui teed API't:

```bash
# Loo failid
mkdir app
touch app/server.js  # või app.py
touch requirements.txt  # või package.json
```

### Alusta lihtsalt!

```html
<!-- index.html näide -->
<!DOCTYPE html>
<html>
<head>
    <title>Minu Projekt</title>
</head>
<body>
    <h1>Tere!</h1>
    <p>See töötab!</p>
</body>
</html>
```

Testi: ava brauser ja ava `index.html`

```bash
# Commit
git add .
git commit -m "Add basic HTML"
git push
```

---

## 7. Kontrollnimekiri

Enne labori lõppu kontrolli:

- [ ] GitHub repository on loodud
- [ ] README.md on olemas
- [ ] PLAAN.md on olemas
- [ ] Oled valinud 2 tööriista
- [ ] Oled valinud projekti teema
- [ ] Oled teinud vähemalt 2 commit'i

---

## Järgmised Sammud

**Kodutöö:** Alusta koodi kirjutamist!

1. Kirjuta lihtne versioon oma rakendusest
2. Testi et töötab
3. Tee commit'id tihti (iga päev!)
4. Järgmine tund: Docker'i lisamine

**Ära muretse kui ei tea täpselt mis teha** - järgmine kord aitame!

Edu! 🚀