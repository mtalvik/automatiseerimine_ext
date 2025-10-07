# Pidev Integratsioon ja Tarnimine (CI/CD) Lisapraktika

**Eeldused:** GitHub Actions labor, Docker põhitõed, CI/CD loeng

Täiendavad harjutused neile, kes tegid lab'i läbi ja tahavad rohkem väljakutset. Need harjutused on mõeldud süvendama teie CI/CD oskusi, keskendudes production-ready tehnikatele mida kasutatakse päris projektides.

---

## 1. Multi-Branch Deployment Strategy

### 1.1 Probleem

Praegu sinu pipeline käivitub kõikidel branch'idel ühtemoodi. Päris projektides on see ebaefektiivne ja ohtlik. Feature branch'idel ei ole vaja Docker image'it buildida ega staging'u deployda. Development branch'il ei peaks olema võimalik production'i deployda. Main branch peab olema kaitstud ning nõudma code review'd.

Branch strategy puudumine põhjustab mitmeid probleeme. Arendajad peavad ootama 10 minutit pipeline'i lõppu, kui nad tegelikult vajasid ainult testide tulemust. Kogemata võib keegi deployda pooliku feature'i production'i. Resources kulutatakse asjatult - Docker Registry täitub test image'idega.

Tööstuses kasutatakse branch strateegiaid nagu Git Flow või GitHub Flow. Iga branch'i tüübil on oma eesmärk ja oma pipeline käitumine. Feature branch'id on arendajate töölaud - kiire feedback ilma raske infrastruktuurita. Development branch on integratsioonipunkt - näitab kuidas kõik koos töötab. Main branch on production - kõik kontrollid läbitud, valmis kasutajateni jõudma.

### 1.2 Lahendus

GitHub Actions võimaldab käitumist kontrollida branch'i nime järgi. Conditional execution kasutab workflow süntaksit kus iga job saab määrata millal ta käivitub.

Näide branch-põhisest käitumisest:```yaml
name: CI/CD

on:
  push:
    branches:
      - main
      - develop
      - 'feature/**'
  pull_request:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/
      # Käivitub KÕIKIDEL branch'idel

  build:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    needs: test
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: |
          TAG=${{ github.ref == 'refs/heads/main' && 'latest' || 'develop' }}
          docker build -t myapp:$TAG .
      # Käivitub AINULT develop ja main branch'idel

  deploy-staging:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    needs: build
    environment:
      name: staging
      url: https://staging.myapp.com
    steps:
      - name: Deploy to staging
        run: echo "Deploying to staging..."
      # Käivitub AINULT develop branch'il

  deploy-production:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: build
    environment:
      name: production
      url: https://myapp.com
    steps:
      - name: Deploy to production
        run: echo "Deploying to production..."
      # Käivitub AINULT main branch'il, vajab manual approval```

Environment konfiguratsioon lisab turvalisuse kihi. Production environment saab seadistada nõudma manual approval - keegi peab GitHub UI's kinnitama enne kui deployment käivitub. Samuti saab seadistada kes võivad approve'ida - ainult senior arendajad või DevOps tiim.

Image tagging strateegia on oluline. Feature branch'idel ei builda image'i üldse. Develop branch'il tag on "develop-latest". Main branch'il on kaks tag'i - "latest" ja commit SHA, näiteks "sha-abc123". SHA tag võimaldab täpset versiooni hiljem deployda või rollback'i teha.

### 1.3 Harjutus: Branch Strategy Implementeerimine

**Nõuded:**
- [ ] Pipeline käitub erinevalt sõltuvalt branch'ist (feature → test ainult, develop → test + build + staging, main → täielik)
- [ ] Docker image'id on tagitud erinevalt (develop-latest, latest + SHA)
- [ ] Production environment nõuab manual approval
- [ ] Branch protection rules seadistatud main branch'ile (nõuab PR + review)
- [ ] README.md dokumenteerib branch strategy't ja näitab igat stsenaariumi

**Näpunäiteid:**
- Alusta lihtsamatest if condition'itest, testi iga branch'i käitumist
- GitHub environment settings asub Settings → Environments, seal saad seadistada approval'eid
- Branch protection asub Settings → Branches, seal nõua pull request review'd
- Kasuta github.ref võrdlemiseks - see on branch'i täielik nimi nagu refs/heads/main
- Tag'ide jaoks kasuta ternary operator'it workflow'des

**Testimine:**```bash
# Loo feature branch
git checkout -b feature/test-strategy
git push origin feature/test-strategy
# Vaata Actions → ainult test job käivitus

# Merge develop'i
git checkout develop
git merge feature/test-strategy
git push origin develop
# Vaata Actions → test + build + deploy-staging

# Ava PR main'i
# Vaata et nõuab review'd
# Pärast merge'i vaata et nõuab manual approval production deployment'iks```

**Boonus:**
- Lisa pull request'i jaoks eraldi workflow mis kommenteerib PR'i build statusega
- Implementeeri automatic tagging: kui merge main'i, loo Git tag
- Lisa matrix strategy: testi mitmete versioonidega, aga ainult develop ja main'il

---

## 2. Pipeline Performance Optimization

### 2.1 Probleem

Pipeline mis võtab 10-15 minutit on produktiivsuse tapja. Arendaja pushib koodi, läheb kohvi tegema, unustab konteksti. Kui ta päevas pushib 10 korda, kaotab ta 2 tundi ainult ootamisele. Meeskonnas 5 arendajat - see on 10 tundi päevas, 50 tundi nädalas.

Aeglane pipeline tekib tavaliselt samadest põhjustest. Dependencies installimine nullist iga kord - npm install laeb 500MB node_modules. Docker build käivitab kõik layer'id uuesti, kuigi muutus oli ainult ühes failis. Testid ja linting käivad järjestikku, kuigi võiksid paralleelselt. Artifact'e ei jagata job'ide vahel, build tulemus visatakse ära ja builditakse uuesti.

Tööstuses on pipeline optimiseerimine pidev protsess. Netflix optimeeris oma pipeline'i 45 minutilt 5 minutile. Google kasutab massilist paralleliseerimist ja caching'ut. Facebook buildi infrastruktuur on optimeeritud sekunditele. Mida kiirem pipeline, seda rohkem saab deployda, seda kiirem on iteratsioon.

### 2.2 Lahendus

Optimeerimise võti on caching, paralleliseerimine ja layer reuse. Alustame dependency caching'ust.

Dependencies muutuvad harva. Python'i requirements.txt või Node'i package.json muutub vahest kord nädalas. Aga me installime need iga commit'iga uuesti. Caching lahendab selle.```yaml
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-```

Cache key kasutab requirements.txt hash'i. Kui fail ei muutu, key ei muutu, cache hit. Kui fail muutub, key muutub, cache miss, uus install. Restore-keys on fallback - kui exact match puudub, kasuta kõige lähemat.

Docker layer caching on võimsam. Multi-stage build võimaldab base image'i taaskasutada.```dockerfile
# Base stage - harva muutub
FROM python:3.9-slim AS base
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip install -r requirements.txt

# App stage - sageli muutub
FROM base AS app
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]```

Base stage builditakse ainult kui requirements.txt muutub. App stage builditakse iga kord, aga see on kiire - ainult COPY ja CMD. Docker build-push-action toetab layer caching'ut built-in.```yaml
- name: Build and push
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: myapp:latest
    cache-from: type=registry,ref=myapp:buildcache
    cache-to: type=registry,ref=myapp:buildcache,mode=max```

Paralleliseerimine käivitab töö korraga. Test ja lint võivad käia samal ajal - nad ei sõltu üksteisest.```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/
  
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: flake8 .
  
  build:
    needs: [test, lint]
    runs-on: ubuntu-latest
    steps:
      - run: docker build .```

Matrix strategy testib mitmete versioonidega paralleelselt.```yaml
test:
  strategy:
    matrix:
      python-version: [3.8, 3.9, 3.10, 3.11]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - run: pytest tests/```

Artifact'id jagavad build tulemusi. Build job loob artifact'i, deploy job kasutab seda.```yaml
build:
  steps:
    - run: npm run build
    - uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

deploy:
  needs: build
  steps:
    - uses: actions/download-artifact@v3
      with:
        name: dist
    - run: deploy.sh dist/```

### 2.3 Harjutus: Pipeline Kiiruse Optimeerimine

**Nõuded:**
- [ ] Mõõda baseline - pipeline'i täielik aeg enne optimeerimist
- [ ] Implementeeri vähemalt kolm optimeerimist (caching, parallelism, Docker layers)
- [ ] Mõõda tulemused - pipeline'i aeg pärast optimeerimist
- [ ] Pipeline peab olema vähemalt 40% kiirem kui baseline
- [ ] Dokumenteeri README.md'sse kõik optimeerimised ja nende mõju

**Näpunäiteid:**
- Alusta profiling'ust - vaata GitHub Actions UI'st kus kulub kõige rohkem aega
- Dependency caching on quickest win - implementeeri see esimesena
- Multi-stage Docker build'i näide on Docker dokumentatsioonis
- actions/cache documentation näitab kõiki võimalusi
- Paralleelsed job'id on lihtsad - lihtsalt eemalda needs kui sõltuvust pole

**Testimine:**```bash
# Baseline
git tag baseline
git push origin baseline
# Vaata Actions → märgi üles igat job'i aeg

# Optimeeri ja testi
# Commit optimeerimised
git push origin main
# Vaata Actions → võrdle aegu

# Näide:
# Baseline: 8m 30s
# Optimized: 3m 45s
# Improvement: 56%```

**Boonus:**
- Kasuta BuildKit features Docker'is (cache-from, cache-to advanced options)
- Implementeeri custom cache strategy mis säilitab cache'i branch'ide vahel
- Lisa workflow dispatch trigger mis puhastab cache'i kui vaja

---

## 3. Production-Grade Security ja Monitoring

### 3.1 Probleem

Lab'i pipeline demonstreerib põhikonseptsioone, aga puudub kõik mis production'is on kritiline. Security scanning puudub - ei tea kas dependencies'tel on vulnerabilities. Deployment on fire and forget - ei tea kas rakendus tegelikult käivitus. Rollback capability puudub - kui midagi läheb valesti, pole lihtsat viisi tagasi minna. Monitoring ja alerting puudub - keegi ei tea kui deployment ebaõnnestub kell 3 öösel.

Production'i vigadel on päris tagajärjed. Security vulnerability võib tähendada data breach'i. Failed deployment tähendab downtime'i. Mitte teada et midagi on valesti tähendab et probleem jätkub tunde. Päris ettevõtetes on SLA'd - 99.9% uptime tähendab maksimum 43 minutit downtime kuus.

Production-ready pipeline hõlmab mitut kihti. Security on sisse ehitatud - iga build scannitakse. Deployment on kontrollitud - health check'id kinnitavad et rakendus töötab. Rollback on automaatne - kui midagi läheb valesti, eelmine versioon tuuakse tagasi. Monitoring on reaalajas - meeskond teab kohe kui midagi juhtub.

### 3.2 Lahendus

Security scanning peaks olema pipeline'i lahutamatu osa. Trivy on tööstustandard container ja dependency scanning'uks.```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'
    
    - name: Upload results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Fail on critical vulnerabilities
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        exit-code: '1'
        severity: 'CRITICAL'```

Container image scanning käivitub pärast build'i.```yaml
- name: Scan Docker image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:${{ github.sha }}'
    format: 'sarif'
    output: 'image-results.sarif'
    severity: 'HIGH,CRITICAL'```

Health monitoring deploymentil on kriitiline. Lihtne health check endpoint ja monitoring loop.```bash
#!/bin/bash
# health-check.sh

URL=$1
MAX_ATTEMPTS=10
ATTEMPT=0

echo "Starting health checks for $URL"

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL/health)
  
  if [ $HTTP_CODE -eq 200 ]; then
    echo "Health check passed (attempt $((ATTEMPT+1)))"
    ATTEMPT=$((ATTEMPT+1))
    
    if [ $ATTEMPT -eq 3 ]; then
      echo "Service is healthy"
      exit 0
    fi
  else
    echo "Health check failed: HTTP $HTTP_CODE"
    exit 1
  fi
  
  sleep 10
done

echo "Health checks failed after $MAX_ATTEMPTS attempts"
exit 1```

Workflow kasutab seda:```yaml
deploy:
  steps:
    - name: Deploy
      run: ./deploy.sh
    
    - name: Health check
      run: ./health-check.sh https://myapp.com
      timeout-minutes: 5
    
    - name: Rollback on failure
      if: failure()
      run: ./rollback.sh```

Rollback strateegia nõuab versiooni tracking'ut. Metadata file säilitab deployment ajalugu.```json
{
  "deployments": [
    {
      "version": "v1.2.3",
      "sha": "abc123",
      "image": "myapp:sha-abc123",
      "deployed_at": "2025-01-15T10:30:00Z",
      "deployed_by": "github-actions",
      "status": "success"
    },
    {
      "version": "v1.2.2",
      "sha": "def456",
      "image": "myapp:sha-def456",
      "deployed_at": "2025-01-14T15:20:00Z",
      "deployed_by": "github-actions",
      "status": "success"
    }
  ]
}```

Rollback workflow võimaldab manual intervention'i.```yaml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to (SHA or tag)'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Rollback to version
        run: |
          echo "Rolling back to ${{ github.event.inputs.version }}"
          docker pull myapp:${{ github.event.inputs.version }}
          ./deploy.sh ${{ github.event.inputs.version }}
      
      - name: Verify rollback
        run: ./health-check.sh https://myapp.com```

Notifications hoiavad meeskonda kursis. Slack webhook on lihtne seadistada.```yaml
- name: Notify deployment
  uses: 8398a7/action-slack@v3
  if: always()
  with:
    status: ${{ job.status }}
    text: |
      Deployment ${{ job.status }}
      Version: ${{ github.sha }}
      Deployed by: ${{ github.actor }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}```

### 3.3 Harjutus: Production Pipeline Implementeerimine

**Nõuded:**
- [ ] Security scanning - Trivy või muu tool (dependency + container)
- [ ] Health monitoring - automaatne check peale deployment'i
- [ ] Rollback capability - manual workflow või automaatne failure'il
- [ ] Notifications - Slack, Discord või email kui deployment õnnestub/ebaõnnestub
- [ ] RUNBOOK.md dokumentatsioon - kuidas süsteem töötab ja kuidas troubleshoot'ida

**Näpunäiteid:**
- Alusta security scanning'ust - Trivy action on kõige lihtsam
- Health check script kirjuta ja testi lokaalses enne kui lisad pipeline'i
- Slack webhook saad tasuta Discord või Slack workspace'iga
- Rollback workflow kasuta workflow_dispatch trigger'it
- RUNBOOK.md peab sisaldama: kuidas deployda, kuidas rollback teha, kuidas troubleshoot'ida

**Testimine:**```bash
# Security scan
git push origin main
# Vaata Actions → Security tab → peaks näitama vulnerabilities

# Health monitoring
# Lisa oma app'i /health endpoint
# Deploy ja vaata logs - peaks tegema health check'e

# Rollback
# Actions → Rollback workflow → Run workflow
# Vali eelmine versioon
# Kontrolli et rakendus tuli tagasi

# Notifications
# Iga deployment peaks saatma Slack/Discord message```

**Boonus:**
- Implementeeri canary deployment - 10% traffic uuele versioonile, siis 100%
- Lisa metrics collection - logi deployment'e Prometheus või JSON faili
- Automatic rollback kui health check ebaõnnestub 3 korda järjest
- Multi-environment support - erinevad health check URL'id staging vs production

---

## Kasulikud Ressursid

**Dokumentatsioon:**
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions Caching](https://github.com/actions/cache)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)

**Tööriistad:**
- **Trivy** - vulnerability scanning: `aquasecurity/trivy-action@master`
- **actions/cache** - dependency caching: `actions/cache@v3`
- **docker/build-push-action** - optimized Docker builds: `docker/build-push-action@v4`
- **8398a7/action-slack** - Slack notifications: `8398a7/action-slack@v3`

**Näited:**
- [GitHub Actions Examples](https://github.com/actions/starter-workflows)
- [Docker BuildKit Cache](https://docs.docker.com/engine/reference/commandline/buildx_build/#cache-from)
- [Git Flow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

Need harjutused on mõeldud süvendama teie CI/CD oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole.