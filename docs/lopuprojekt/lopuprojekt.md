# Lõpuprojekt Labor: Projekti Alustamine ja Esitamine

**Eeldused:** Git, Docker, Ansible, CI/CD põhioskused  
**Platvorm:** GitHub + 3 tööriista enda valikul

---

## Õpivälјundid

Pärast laborit oskate:
- Valib sobiva projekti idee
- Integreerib 4+ tööriista
- Kirjutab professionaalse README
- Esitab töötava projekti

---

## 1. Projekti Nõuded

**Kohustuslikud tööriistad (4 miinimum):**
1. **Git** - versioonihaldus (kohustuslik)
2. **CI/CD** - GitHub Actions või GitLab CI (kohustuslik)
3. **Enda valik 1** - vali: Docker / Ansible / Terraform / Kubernetes
4. **Enda valik 2** - vali: Docker / Ansible / Terraform / Kubernetes / Monitoring

**Projekt:**
- **SINA valid projekti idee** (veebirakendus, API, infrastruktuur, muu)
- Kood peab töötama
- Kõik 4 tööriista peavad olema päriselt kasutusel

---

## 2. Vali Projekt

**Mõtle välja oma projekt. Näiteid inspiratsiooniks:**

- Veebirakendus millegi jaoks
- API teenus
- Automatiseeritud infrastruktuur
- Monitoring süsteem
- Midagi mis sind huvitab

**Küsimused endale:**
- Mis probleem see lahendab?
- Millised 4 tööriista sobivad?
- Kas jõuad 2 nädalaga valmis?

---

## 3. Repository Loomine

```bash
mkdir lopuprojekt
cd lopuprojekt
git init
git branch -M main
```

Loo GitHub'is repository ja seosta:
```bash
git remote add origin https://github.com/[kasutaja]/lopuprojekt.git
```

---

## 4. README Struktuur (KOHUSTUSLIK)

Loo `README.md` järgmise sisuga:

```markdown
# Projekti Nimi

Üks lause mis kirjeldab projekti.

## Kirjeldus

Kirjelda oma projekti:
- Mis see teeb?
- Mis probleem see lahendab?
- Kes seda kasutaks?

## Arhitektuur

[Lisa diagramm või kirjeldus kuidas süsteem töötab]

## Tööriistad ja Põhjendused

### 1. Git
Miks: [selgita miks valisid Git'i selle projekti jaoks]

### 2. GitHub Actions / GitLab CI
Miks: [selgita miks valisid selle CI/CD tööriista]

### 3. [Sinu 3. tööriist]
Miks: [selgita miks valisid]
Kuidas integreerib teiste tööriistadega: [selgita]

### 4. [Sinu 4. tööriist]
Miks: [selgita miks valisid]
Kuidas integreerib teiste tööriistadega: [selgita]

## Eeltingimused

Mis on vaja et projekti käivitada:
- Docker 24.0+ (kui kasutad)
- [Lisa kõik vajalik]

## Käivitamine

### Samm 1: Kloon repository
```bash
git clone https://github.com/[kasutaja]/[projekt].git
cd [projekt]
```

### Samm 2: [Järgmine samm]
```bash
[Käsud]
```

### Samm 3: [Järgmine samm]
```bash
[Käsud]
```

Tulemus: [Mis peaks juhtuma? Kus rakendus on? Milline URL?]

## Projekti Struktuur

```
projekt/
├── [Sinu kaustad ja failid]
└── README.md
```

## Kuidas Tööriistad Töötavad Koos

Kirjelda kuidas sinu 4 tööriista integreerivad:

1. [Esimene samm]
2. [Teine samm]
3. [Kolmas samm]
4. [Neljas samm]

## Testimine

Kuidas testida et kõik töötab:
```bash
[Testimise käsud]
```

## Tehnilised Otsused

### Miks valisin [tööriist 3]?
Põhjendus: [alternatiivid, miks see sobib]

### Miks valisin [tööriist 4]?
Põhjendus: [alternatiivid, miks see sobis paremini]

## Autorid

- [Sinu nimi] - [GitHub]
```

---

## 5. CI/CD Pipeline (KOHUSTUSLIK)

Loo `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Lisa siia oma sammud:
      # - testimine
      # - build
      # - deploy
```

---

## 6. Failide Struktuur

Loo endale sobiv struktuur. Näiteks:

```bash
mkdir -p .github/workflows
mkdir -p [sinu kaustad]
touch .github/workflows/ci-cd.yml
touch .gitignore
```

`.gitignore`:
```
node_modules/
*.log
.env
.DS_Store
```

---

## 7. Arendamine

**Sina oled arendaja - sina teed:**

1. Mõtle välja mis tehnoloogiad kasutad
2. Kirjuta kood
3. Tee Dockerfile / Ansible playbook / K8s manifests / vms
4. Seadista CI/CD
5. Testi et töötab
6. Dokumenteeri README's

**Commit'i regulaarselt:**
```bash
git add .
git commit -m "Describe what you did"
git push
```

---

## 8. Esitamise Kontroll

Enne esitamist kontrolli:

**Repository:**
- [ ] README.md on täielik
- [ ] Kõik 4 tööriista on dokumenteeritud
- [ ] Selgitatud MIKS iga tööriist valitud
- [ ] Käivitamise juhised on selged
- [ ] CI/CD pipeline töötab (GitHub Actions roheline)

**Funktsionaalsus:**
- [ ] Projekt käivitub README juhiste järgi
- [ ] Kõik 4 tööriista on päriselt kasutusel (mitte lihtsalt olemas)
- [ ] Demo on ette valmistatud

**Kood:**
- [ ] Kood on commit'itud
- [ ] Struktuur on loogiline
- [ ] Repository on avalik või õpetajale ligipääs

---

## 9. Demo Ettevalmistus

**Valmista ette 5-minutiline esitlus:**

1. **Mis projekt on** (30 sek)
2. **Millised 4 tööriista ja MIKS** (2 min)
3. **Live demo** (2 min)
4. **Mis õppisid** (30 sek)

**Tips:**
- Testi demo enne
- Screenshot'id kui live demo ei tööta
- Selgita kuidas tööriistad integreerivad

---

## 10. Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|-----------|---------|-----------|
| Töötab | 30% | Projekt käivitub ja töötab |
| 4 tööriista | 30% | Kõik 4 korrektselt kasutatud ja integreeritud |
| README | 20% | Täielik, selge, professionaalne |
| Põhjendused | 10% | Tehnilised otsused põhjendatud |
| Kood | 10% | Loetav, struktureeritud |

**Boonus (+10%):**
- 5+ tööriista
- Eriti hästi integreeritud
- Põhjalik dokumentatsioon
- Automatiseeritud testid

---

## 11. Projekti Esitamine

**Google Classroom'is esita:**
- GitHub repository link
- Lühike kirjeldus (2-3 lauset)

**Reede on esitlused + söömine!**

---

## Abi

Kui jooksed probleemi:
- Vaata labori materjale
- Vaata loenguid
- Küsi abi

**Edu! Sa said selle!** 🚀