# Lõpuprojekt Labor: Projekti Alustamine

**Eeldused:** Git põhiteadmised, Docker basics, YAML süntaks, Linux CLI  
**Platvorm:** GitHub, Docker Desktop/Podman, oma valik (Kubernetes/Terraform/Ansible)

---

## Õpivälјundid

Pärast laborit oskate:
- Loob struktureeritud projekti repository ja dokumentatsiooni
- Seadistab lihtsa CI/CD pipeline'i GitHub Actions'iga
- Käivitab Docker-põhise arenduskeskkonna
- Dokumenteerib esimesed tehnilised otsused
- Alustab tööd valitud tööriistadega

---

## 1. Projekti ja Tööriistade Valik

Valige üks tööriistakomplekt ja projektitüüp. Ärge kulutage rohkem kui 15 minutit otsustamisele - saate hiljem muuta.

### Tööriistakomplektid

**Kombinatsioon A: Docker + Kubernetes**
- Konteinerite orkestreerimise stack
- Kõrge õppimiskõver, industry standard

**Kombinatsioon B: Terraform + Ansible**
- Infrastruktuuri automatiseerimise stack
- Server-based projektidele

**Kombinatsioon C: Docker + CI/CD**
- Lihtsustatud arenduse stack
- Madalam kompleksus, kiire alustamine

**Kombinatsioon D: Kubernetes + Monitoring**
- Operatsioonide ja observability stack
- Prometheus + Grafana fookus

### Projektitüübid

**Veebirakendus:** Frontend + Backend + DB  
**REST API:** API server + DB + dokumentatsioon  
**Monitoring Dashboard:** Metrics collector + visualisatsioon

Kirjutage üles:
```
Minu valik: [Kombinatsioon X + Projektitüüp Y]
Põhjus: [1 lause]
```

**Validatsioon:**
- [ ] Olete valinud ühe kombinatsiooni
- [ ] Olete valinud ühe projektitüübi
- [ ] Oskate ühes lauses selgitada miks

---

## 2. Repository ja Dokumentatsiooni Loomine

Loome minimaalse struktuuri millega saab alustada.

### 2.1 Põhistruktuur

```bash
# Loo directory ja initialiseeri Git
mkdir lopuprojekt-[teie-nimi]
cd lopuprojekt-[teie-nimi]
git init
git branch -M main

# Loo põhiline struktuur
mkdir -p docs
mkdir -p infrastructure
mkdir -p application
mkdir -p .github/workflows
```

### 2.2 README.md

```bash
cat > README.md << 'EOF'
# [Projekti Nimi]

[Ühe lause kirjeldus]

## Ülevaade

- **Mis:** [Mida see teeb]
- **Kellele:** [Kes seda kasutab]
- **Kuidas:** [Peamised tehnoloogiad]

## Kiire Alustamine

```bash
# Klooni ja käivita
git clone [url]
cd lopuprojekt-[nimi]
docker-compose up
```

## Dokumentatsioon

- [Arhitektuur](architecture.md)
- [Tehnilised Otsused](decisions.md)
EOF
```

### 2.3 Esimesed Dokumendid

**architecture.md:**

```markdown
# Arhitektuur

## Komponendid

### [Komponendi Nimi]
- **Tehnoloogia:** [Tech]
- **Roll:** [Mida teeb]
- **Port:** [Kui on]

## Andmevoog

```
Kasutaja → Frontend → Backend → Database
```

## Järgmised Sammud

- [ ] Lisa diagramm
- [ ] Täpsusta komponente
```

**decisions.md:**

```markdown
# Tehnilised Otsused

## 2024-XX-XX: [Otsuse Nimi]

**Probleem:** [Mis vajab lahendamist]

**Otsus:** [Mida valisime]

**Miks:**
- [Põhjus 1]
- [Põhjus 2]

**Trade-off:**
- [Mis jäi kaotsi]
```

**Validatsioon:**

```bash
# Kontrolli struktuuri
tree -L 2

# Peaks näitama:
# ├── README.md
# ├── docs/
# │   ├── architecture.md
# │   └── decisions.md
# ├── .github/workflows/
# ├── application/
# └── infrastructure/
```

---

## 3. Git Workflow ja Esimene Commit

```bash
# Loo .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
venv/
__pycache__/

# Environment
.env
*.env

# Build
dist/
build/

# IDE
.vscode/
.idea/

# Terraform
.terraform/
*.tfstate*

# Logs
*.log
EOF

# Lisa failid
git add .

# Esimene commit
git commit -m "chore: initial project structure

- Create directory layout
- Add README and docs templates
- Configure gitignore"

# Loo develop branch
git checkout -b develop
```

**GitHub'i üles:**

```bash
# Loo GitHub'is repository, siis:
git remote add origin https://github.com/[username]/lopuprojekt-[nimi].git
git push -u origin main
git push -u origin develop
```

**Validatsioon:**
- [ ] Repository on GitHub'is
- [ ] Main ja develop branch'id on olemas
- [ ] Kõik failid on commit'itud

---

## 4. Lihtne CI/CD Pipeline

Loome minimaalse pipeline'i mis kontrollib et kood compilerib.

### 4.1 GitHub Actions Workflow

`.github/workflows/ci.yml:`

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Verify structure
        run: |
          echo "Checking project structure..."
          test -f README.md
          test -d docs
          test -f architecture.md
          test -f decisions.md
          echo "✅ Structure OK"

      - name: Check documentation
        run: |
          echo "Checking docs are not empty..."
          [ -s README.md ] || exit 1
          [ -s architecture.md ] || exit 1
          echo "✅ Documentation OK"

  docker:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check Dockerfile exists
        run: |
          if [ -f Dockerfile ]; then
            echo "✅ Dockerfile found"
            docker build -t test .
          else
            echo "⚠️  No Dockerfile yet"
          fi
```

See on minimaalne pipeline - ta ainult kontrollib et failid on olemas. Kui projekt kasvab, lisame teste ja build'e.

**Commit ja push:**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add basic GitHub Actions workflow"
git push
```

**Validatsioon:**

Minge GitHub'i → Actions tab → peaks nägema CI run'i.

---

## 5. Docker Setup (Kui Valisite Docker'iga Kombinatsiooni)

Ainult kui teie kombinatsioon kasutab Docker'it.

### 5.1 Lihtne Dockerfile

```dockerfile
# Dockerfile
FROM node:20-alpine

WORKDIR /app

# Placeholder - asendage oma rakendusega
COPY package*.json ./
RUN npm install || echo "No package.json yet"

COPY . .

EXPOSE 3000

CMD ["node", "-e", "console.log('Replace with your app'); process.exit(0)"]
```

### 5.2 Docker Compose Local Development'ile

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Test:**

```bash
# Build image
docker-compose build

# Käivita (exitib kohe kuna placeholder app)
docker-compose up

# Kui näete "Replace with your app" - töötab! ✅
```

**Validatsioon:**
- [ ] Dockerfile on loodud
- [ ] docker-compose.yml on loodud
- [ ] Image ehitub ilma erroriteta
- [ ] Container käivitub (isegi kui exitib kohe)

---

## 6. Esimene Tehniline Otsus

Dokumenteerige oma esimene oluline otsus `decisions.md` failis.

**Näide:**

```markdown
## 2024-10-07: Docker kui Konteineriseerimise Platvorm

**Probleem:**
Vajame viisi tagada et rakendus töötab ühtemoodi development, staging ja production keskkondades.

**Valikud:**
1. Docker - industry standard, suur ökosüsteem
2. Podman - daemon-less, turvalinem
3. Otsest VM'e - lihtsam, aga raskem skaleerida

**Otsus:**
Valime Docker'i.

**Miks:**
- Meeskond tunneb seda juba
- Suur kogukond = lihtsam leida abi
- Hea integratsioon Kubernetes'ega (võimalik tulevikus)
- Industry standard = kasulik CV'le

**Trade-off:**
- Docker daemon vajab root õigusi (turvaoht)
- Vendor lock-in (aga OCI standard leevendab)
- Õppimiskõver neile kes pole varem kasutanud

---

## 2024-10-07: [Teie Teine Otsus]

[Dokumenteerige järgmine oluline valik]
```

**Dokumenteerige vähemalt 2 otsust:**
1. Konteineriseerimise/infrastruktuuri tööriist
2. CI/CD platvorm (GitHub Actions/GitLab CI/jne)

**Validatsioon:**
- [ ] decisions.md sisaldab vähemalt 2 otsust
- [ ] Iga otsus on dateeritud
- [ ] Iga otsus sisaldab probleem/valikud/otsus/põhjendus

---

## 7. Kontrollnimekiri

Enne labori lõpetamist kontrollige:

### Struktuur
- [ ] Repository on GitHub'is
- [ ] README.md on täidetud
- [ ] docs/ kaust sisaldab architecture.md ja decisions.md
- [ ] .gitignore on seadistatud

### Git
- [ ] Main ja develop branch'id olemas
- [ ] Vähemalt 2 commit'i tehtud
- [ ] Commit messages on kirjeldavad

### CI/CD
- [ ] .github/workflows/ci.yml on olemas
- [ ] CI pipeline jookseb GitHub'is
- [ ] Pipeline näitab rohelist checkmarki

### Docker (Kui Kasutate)
- [ ] Dockerfile on loodud
- [ ] docker-compose.yml on loodud
- [ ] `docker-compose build` töötab

### Dokumentatsioon
- [ ] architecture.md sisaldab komponente
- [ ] decisions.md sisaldab 2+ otsust
- [ ] README selgitab projekti eesmärki

---

## Troubleshooting

### GitHub Actions ei käivitu

```bash
# Kontrolli workflow file'i asukohta
ls -la .github/workflows/ci.yml

# Kontrolli YAML syntax'it
cat .github/workflows/ci.yml

# Commit ja push
git add .github/workflows/
git commit -m "ci: fix workflow"
git push
```

### Docker build failib

```bash
# Kontrolli Docker'i staatust
docker info

# Restart Docker (Mac/Windows - restart app, Linux:)
sudo systemctl restart docker

# Proovi uuesti
docker build -t test .
```

### "Permission denied" error

```bash
# Lisa executable õigused
chmod +x scripts/*.sh

# Või käivita bash'iga
bash scripts/setup.sh
```

---

## Järgmised Sammud

Nüüd kui põhistruktuur on paigas:

**Nädalaks 2:**
1. Implementeeri põhiline rakendus
2. Lisa testid
3. Täienda CI/CD pipeline'i build ja test jobidega

**Nädalaks 3:**
1. Setup infrastructure (Terraform/Kubernetes/Ansible)
2. Lisa deployment stage CI/CD'sse
3. Dokumenteeri deployment protsessi

**Nädalaks 4:**
1. Lisa monitoring (kui kasutate)
2. Performance tuning
3. Täienda dokumentatsiooni
4. Valmista ette esitlust

**KodutÃ¶Ã¶ks (vt kodutoo.md):**
- Implementeeri valitud projektitüübi põhifunktsioonid
- Seadista valitud tööriistakomplekt
- Dokumenteeri arhitektuur detailselt
- Lisa automated tests

Edu projekti jätkamisel!