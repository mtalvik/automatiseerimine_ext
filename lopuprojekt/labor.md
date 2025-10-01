# Lõpuprojekt Labor: Projekti Alustamine

**Kestus:** 2 tundi  
**Eesmärk:** Alustada lõpuprojekti ja seadistada põhistruktuur

---

## 🎯 Õpiväljundid

Pärast laborit oskate:
- Valida sobiva projekti teema
- Planeerida projekti arhitektuuri
- Seadistada repository struktuuri
- Alustada dokumentatsiooni kirjutamist
- Seadistada põhilise CI/CD pipeline'i

---

## 📋 Samm 1: Projekti Valik (30 min)

### 1.1 Projekti valik

Valige üks järgmistest projektidest või tehke oma ettepanek:

**Valik A: Lihtne Veebirakendus**
- Komponendid: Frontend, Backend API, Andmebaas
- Funktsioonid: CRUD operatsioonid, kasutajad
- Tehnoloogiad: HTML/CSS/JS või React, Node.js/Python, SQLite/PostgreSQL

**Valik B: API Teenus**
- Komponendid: API server, Andmebaas, Dokumentatsioon
- Funktsioonid: REST API, andmete haldamine
- Tehnoloogiad: Node.js/Python, PostgreSQL, Swagger

**Valik C: Monitoring Dashboard**
- Komponendid: Dashboard, Data API, Andmebaas
- Funktsioonid: Andmete visualiseerimine, graafikud
- Tehnoloogiad: React/Vue.js, Python, SQLite

### 1.2 Tööriistade valik

Valige 2-3 tööriista, mida soovite kasutada:

**Valik A: Docker + Kubernetes**
- Docker: Konteineriseerimine
- Kubernetes: Deployment ja scaling
- CI/CD: Automatiseerimine

**Valik B: Terraform + Ansible**
- Terraform: Infrastruktuuri automatiseerimine
- Ansible: Serverite konfigureerimine
- CI/CD: Deployment automatiseerimine

**Valik C: Docker + CI/CD**
- Docker: Konteineriseerimine
- CI/CD: Build ja deploy automatiseerimine
- Testing: Automatiseeritud testimine

**Valik D: Kubernetes + Monitoring**
- Kubernetes: Rakenduse orkestreerimine
- Monitoring: Prometheus, Grafana
- Alerting: Hoiatused

### 1.3 Projekti kirjeldus

Kirjutage lühike kirjeldus (2-3 lauset):
- Mis probleemi lahendab?
- Kes on sihtrühm?
- Millised on peamised funktsioonid?
- Millised tööriistad kasutate?

---

## 📋 Samm 2: Arhitektuuri Planeerimine (45 min)

### 2.1 Arhitektuuridiagramm

Joonistage lihtne arhitektuuridiagramm, mis näitab:

**Komponendid:**
- Frontend (kasutajaliides)
- Backend API (äriloogika)
- Database (andmete salvestamine)
- Cache (jõudluse parandamine)
- File storage (failide hoidmine)

**Ühendused:**
- Kuidas komponendid suhtlevad?
- Millised on andmevoogud?
- Kus on turvalisuse punktid?

### 2.2 Tehnilised otsused

Dokumenteerige otsused:

**Infrastructure:**
- Millist pilve kasutate? (AWS, Azure, GCP, local)
- Kuidas deploy'ite? (Kubernetes, Docker Swarm, VMs)
- Kuidas hallate konfiguratsiooni? (Ansible, Terraform)

**Development:**
- Millised keeled ja framework'id?
- Kuidas testite? (Unit, Integration, E2E)
- Kuidas hallate sõltuvusi? (Package managers)

**Operations:**
- Kuidas monitorite? (Prometheus, Grafana)
- Kuidas logite? (ELK, Fluentd)
- Kuidas backup'ite? (Automated backups)

---

## 📋 Samm 3: Repository Seadistamine (30 min)

### 3.1 GitHub repository

```bash
# Loo uus repository
mkdir lopuprojekt-[teie-nimi]
cd lopuprojekt-[teie-nimi]
git init

# Loo põhistruktuur
mkdir -p docs infrastructure application kubernetes ci-cd monitoring
mkdir -p application/frontend application/backend application/docker
mkdir -p infrastructure/terraform infrastructure/ansible
```

### 3.2 Põhifailid

**README.md:**
```markdown
# [Projekti Nimi]

## Kirjeldus
[Lühike kirjeldus]

## Arhitektuur
[Põhiteemad]

## Kiire alustamine
[Deploy'imise juhend]

## Dokumentatsioon
- [Arhitektuur](docs/architecture.md)
- [Tehnilised otsused](docs/decisions.md)
- [Deploy'imine](docs/deployment.md)
```

**docs/architecture.md:**
```markdown
# Arhitektuur

## Ülevaade
[Põhiteemad]

## Komponendid
[Iga komponendi kirjeldus]

## Andmevoog
[Kuidas andmed liiguvad]

## Turvalisus
[Turvalisuse aspektid]
```

### 3.3 Git seadistamine

```bash
# Lisa failid
git add .
git commit -m "Initial project setup"

# Loo branch'id
git checkout -b develop
git checkout -b feature/infrastructure
git checkout -b feature/application
git checkout -b feature/monitoring

# Tagasi main branch'i
git checkout main
```

---

## 📋 Samm 4: CI/CD Alustamine (15 min)

### 4.1 GitHub Actions

Loo `.github/workflows/ci.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
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
        node-version: '18'
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests
      run: npm test
    
    - name: Build application
      run: npm run build

  infrastructure:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
    
    - name: Terraform Init
      run: terraform init
    
    - name: Terraform Plan
      run: terraform plan
```

### 4.2 Docker alustamine

Loo `application/docker/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

---

## 📋 Samm 5: Dokumentatsiooni Alustamine (15 min)

### 5.1 Tehnilised otsused

Loo `docs/decisions.md`:

```markdown
# Tehnilised Otsused

## 2024-XX-XX: Frontend Framework

**Otsus:** Kasutame React'it

**Põhjendus:**
- Suur kogukond
- Palju komponente
- Hea TypeScript tugi

**Alternatiivid:**
- Vue.js (lihtsam, vähem funktsioone)
- Angular (keerulisem, rohkem funktsioone)

## 2024-XX-XX: Database

**Otsus:** PostgreSQL

**Põhjendus:**
- ACID tugi
- Hea jõudlus
- Rikad funktsioonid

**Alternatiivid:**
- MongoDB (NoSQL, kiirem arendamine)
- MySQL (lihtsam, vähem funktsioone)
```

### 5.2 Deploy'imise juhend

Loo `docs/deployment.md`:

```markdown
# Deploy'imise Juhend

## Eeltingimused
- Docker installitud
- kubectl seadistatud
- Terraform installitud

## Kohalik arendamine
```bash
# Klooni repository
git clone [repository-url]
cd lopuprojekt-[nimi]

# Käivita rakendus
docker-compose up
```

## Production deploy'imine
```bash
# Deploy'i infrastruktuuri
cd infrastructure/terraform
terraform init
terraform apply

# Deploy'i rakenduse
kubectl apply -f kubernetes/
```
```

---

## 🎯 Labori Kokkuvõte

Pärast seda laborit on teil:

- [ ] Projekti teema valitud
- [ ] Arhitektuur planeeritud
- [ ] Repository seadistatud
- [ ] Põhiline dokumentatsioon kirjutatud
- [ ] CI/CD pipeline alustatud
- [ ] Docker konfiguratsioon loodud

### Järgmised sammud:

1. **Infrastruktuur** - Loo Terraform konfiguratsioon
2. **Rakendus** - Alusta koodi kirjutamist
3. **Kubernetes** - Seadista deployment'id
4. **Monitoring** - Lisa Prometheus ja Grafana
5. **Testimine** - Kirjuta testid
6. **Dokumentatsioon** - Täienda dokumentatsiooni

**Edu projekti jätkamisel!** 🚀
