# Pidev Integratsioon ja Tarnimine (CI/CD) Kodutöö: Pipeline Uues Kontekstis

**Eeldused:** Lab läbitud, git ja Docker põhitõed  
**Esitamine:** GitHub repository URL (public)  
**Tähtaeg:** Vastavalt õppejõu juhendile

See kodutöö võtab umbes poolteist tundi. Eesmärk on rakendada CI/CD kontseptsioone uues tehnoloogias, et kontrollida kas mõistad põhimõtteid, mitte ainult konkreetset implementatsiooni.

---

## Ülesande Kontekst

Lab'is ehitasid pipeline'i Python Flask rakendusele. Nüüd rakenda sama kontseptsiooni erinevale tehnoloogiale. Eesmärk ei ole kordamine, vaid mõistmine - kas saad pipeline'i loogika üle kanda?

Vali tehnoloogia, mida lab'is ei kasutanud. Kui lab oli Python, siis nüüd Go või Node.js. Kui lab oli Node.js, siis nüüd Python või Go. Kui lab oli Go, siis nüüd Python või Node.js.

---

## 1. Rakenduse Loomine

### Tehnoloogia Valimine

Siin on kolm varianti. Vali üks, mida lab'is ei kasutanud.

**Variant A: Go API**

Loo töökaust ja failid. Main.go fail sisaldab lihtsaid HTTP endpoint'e:
```go
// main.go
package main

import (
    "encoding/json"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
    Status  string `json:"status"`
}

func health(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(Response{Status: "healthy"})
}

func hello(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(Response{Message: "Hello from Go"})
}

func main() {
    http.HandleFunc("/health", health)
    http.HandleFunc("/hello", hello)
    // LISA VEEL 1 ENDPOINT (nt /info)
    http.ListenAndServe(":8080", nil)
}
```

Go.mod fail defineerib mooduli:
```go
// go.mod
module myapp

go 1.21
```

Main_test.go fail sisaldab teste:
```go
// main_test.go
package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealth(t *testing.T) {
    req := httptest.NewRequest("GET", "/health", nil)
    w := httptest.NewRecorder()
    health(w, req)
    
    if w.Code != http.StatusOK {
        t.Errorf("Expected 200, got %d", w.Code)
    }
}

// LISA TEST HELLO ENDPOINT'ILE
```

Dockerfile multi-stage build'iga:
```dockerfile
# Dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go test ./...
RUN go build -o main .

FROM alpine:latest
COPY --from=builder /app/main /main
EXPOSE 8080
CMD ["/main"]
```

**Variant B: Node.js API**

App.js fail Express rakendusega:
```javascript
// app.js
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.get('/hello', (req, res) => {
    res.json({ message: 'Hello from Node' });
});

// LISA VEEL 1 ENDPOINT

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on ${PORT}`);
});

module.exports = app;
```

Package.json fail dependencies'ga:
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "supertest": "^6.3.0"
  }
}
```

App.test.js fail testidega:
```javascript
// app.test.js
const request = require('supertest');
const app = require('./app');

test('GET /health returns healthy', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('healthy');
});

// LISA TEST HELLO ENDPOINT'ILE
```

Dockerfile:
```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm test
EXPOSE 3000
CMD ["npm", "start"]
```

**Variant C: Python FastAPI**

Main.py fail FastAPI rakendusega:
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}

# LISA VEEL 1 ENDPOINT
```

Requirements.txt fail:
```
fastapi==0.104.0
uvicorn==0.24.0
httpx==0.25.0
pytest==7.4.0
```

Test_main.py fail:
```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# LISA TEST HELLO ENDPOINT'ILE
```

Dockerfile:
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pytest test_main.py
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Testimine Lokaalselt

Go rakenduse testimine:
```bash
go run main.go
# Teises terminalis:
curl http://localhost:8080/health
go test ./...
```

Node.js rakenduse testimine:
```bash
npm install
npm start
# Teises terminalis:
curl http://localhost:3000/health
npm test
```

Python rakenduse testimine:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
# Teises terminalis:
curl http://localhost:8000/health
pytest
```

Docker testimine kõigi variantide jaoks:
```bash
docker build -t myapp .
docker run -p 8080:8080 myapp
curl http://localhost:8080/health
```

Kontrolli et rakendus töötab kohalikult, kõik testid läbivad ja Docker image ehitub ning töötab korrektselt.

---

## 2. Pipeline'i Disain

Enne koodi kirjutamist vasta järgmistele küsimustele. See on osa hindamisest - vastused näitavad, kas mõistad pipeline'i struktuuri, mitte ainult kopeerid lab'ist.

Loo fail nimega PIPELINE.md:

### Stage'ide Järjekord

Sul on kolm stage'i: test, build, deploy.

Küsimus: Millises järjekorras neid käivitad?

Järjekord: _____ → _____ → _____

Põhjendus (üks kuni kaks lauset):

Näide heast vastusest: "test → build → deploy, sest testid on kiired (umbes kakskümmend sekundit) ja kui need failivad, pole mõtet build'ida (kaks minutit). Leiame vead kiiresti ja säästame aega."

Näide halvast vastusest: "Test on esimene." (miks?) või "Nii oli lab'is." (ei ole põhjendus)

### Deploy Tüüp

Küsimus: Kas deploy käivitub automaatselt või manuaalselt?

Vali üks:

- Automaatselt (kui test ja build õnnestuvad)
- Manuaalselt (nupuvajutusega)

Põhjendus (üks kuni kaks lauset):

Mõtle: Mis on erinevus? Millal kasutada kumbagi?

### Image Tagimine

Küsimus: Kuidas tagid Docker image'id?

Vali üks:

- Ainult latest
- Latest ja commit SHA
- Muu strateegia

Põhjendus (üks kuni kaks lauset): Kuidas see aitab rollback'i teha?

---

## 3. Pipeline'i Implementeerimine

Loo fail .github/workflows/ci.yml:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  IMAGE_NAME: ghcr.io/${{ github.repository }}:${{ github.sha }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v3
      
      - name: Run tests
        run: |
          echo "Running tests..."
          # VALI ÕIGE:
          # Go: go test ./...
          # Node: npm ci && npm test
          # Python: pip install -r requirements.txt && pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:

      - uses: actions/checkout@v3
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        run: |
          docker build -t $IMAGE_NAME .
          docker tag $IMAGE_NAME ghcr.io/${{ github.repository }}:latest
          docker push $IMAGE_NAME
          docker push ghcr.io/${{ github.repository }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
    steps:

      - name: Deploy
        run: |
          echo "Deploying $IMAGE_NAME"
          echo "SIMULATED DEPLOY - would run: docker pull $IMAGE_NAME"
          echo "Deploy complete"
```

Oluline on asendada test käsud õigega vastavalt tehnoloogiale. Pipeline peab vastama sinu PIPELINE.md disainile. Kui valisid manual deploy, siis GitHub manual approve vajab environment protection rule'i Settings'is.

---

## 4. Dokumentatsioon

Loo README.md fail:
```markdown
# [Projekti Nimi]

[![CI/CD](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/ci.yml)

## Rakendus
[Üks kuni kaks lauset: mis tehnoloogia, millised endpoint'id]

## Pipeline Disain

### Stage'ide Järjekord
[Kopeeri PIPELINE.md'st su vastus]

### Deploy Strateegia
- Deploy tüüp: [manual/automatic]
- Tagimine: [strateegia]
- Rollback: [kuidas teed rollback'i - üks kuni kaks lauset]

## Käivitamine

### Lokaalselt
```bash
# Tehnoloogiast sõltuvalt:
# Go: go run main.go
# Node: npm start  
# Python: uvicorn main:app --reload

curl http://localhost:PORT/health
```

### Docker'iga
```bash
docker build -t myapp .
docker run -p 8080:8080 myapp
curl http://localhost:8080/health
```

### Testid
```bash
# Go: go test ./...
# Node: npm test
# Python: pytest
```

## Refleksioon

### 1. Disaini Muudatused
Küsimus: Kas muutsid pipeline'i struktuuris midagi pärast algset PIPELINE.md disaini? Miks?

[SINU VASTUS - konkreetne näide, mitte "ei muutnud midagi"]

### 2. Debugging
Küsimus: Kirjelda üht probleemi, mis pipeline'iga tekkis. Kuidas lahendasid?

Probleem: [Mis fail'is, mida nägid log'ides]
Põhjus: [Miks see juhtus]
Lahendus: [Kuidas fiksisid]

[Kui probleeme ei olnud, kirjelda probleemi, mis võiks tekkida ja kuidas seda debugida]

### 3. Erinevused Lab'ist
Küsimus: Mis oli kõige suurem erinevus selle pipeline'i ja lab'i pipeline'i vahel?

[SINU VASTUS - tehnoloogia, konfiguratsioon, või muu? Põhjenda]
```

---

## 5. Esitamine

### Kontroll Enne Esitamist

Kohustuslik kontrollnimekiri:

- Repository on public GitHub'is
- PIPELINE.md olemas (kolm küsimust vastatud)
- Rakendus töötab kohalikult
- Testid läbivad lokaalses
- Pipeline fail olemas ja käivitatud (screenshot Actions tab'ist)
- README.md täielik (kõik kolm refleksiooni küsimust vastatud)

### Esita

Esita Moodle'sse repository URL (public link).

---

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| Pipeline Disain | 20% | PIPELINE.md vastused konkreetsed ja põhjendatud |
| Implementation | 35% | Pipeline töötab, järgib disaini, õige tehnoloogia |
| Testid | 15% | Vähemalt kaks testi, läbivad |
| Dokumentatsioon | 15% | README selge, juhised töötavad |
| Refleksioon | 15% | Konkreetsed vastused |

Kokku: 100%  
Läbimiseks: 50%

### Hindamise Reeglid

Täispunktide saamiseks:

- Põhjendused on konkreetsed (näiteks "test → build, sest testid võtavad kakskümmend sekundit versus build kaks minutit")
- Refleksioon näitab mõistmist (kirjeldad debugging'u protsessi)
- Pipeline järgib sinu disaini (mitte lihtsalt kopeeritud lab'ist)

Ei sobi:

- "Nii oli lab'is"
- see ei ole põhjendus
- "Õppisin CI/CD'd"
- liiga üldine
- Pipeline töötab, aga ei vasta PIPELINE.md disainile

---

## Boonus

Vali üks variant boonuspunktide saamiseks (pluss kümme protsenti):


### Variant 1: Caching

Lisa dependency caching pipeline'i:
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: # oleneb tehnoloogiast
    key: ${{ runner.os }}-deps-${{ hashFiles('**/lockfile') }}
```

Põhjenda README's: Mida caching teeb ja miks aitab? Näita enne ja pärast aegasid.

### Variant 2: Build Badge

Lisa README.md algusesse pipeline status badge. See peab päriselt töötama ja näitama pipeline staatust.

### Variant 3: Multi-Stage Dockerfile

Optimeeri Dockerfile kasutades multi-stage build'i:

- Builder stage
- Runtime stage
- Väiksem image size

Näita README's: Mõõda image size enne ja pärast optimeerimist.

---

## Troubleshooting

### Pipeline Failib Kohe

Kontrolli järgmist:

- YAML syntax
- kasuta https://www.yamllint.com/
- Test käsud
- kas töötavad lokaalses?
- GitHub Actions tab
- loe error message'it

### Test Stage Failib

Debug järgmiselt:
```bash
# Testi lokaalses samas image'is
docker run -it [IMAGE] bash
# Käivita samad käsud mis pipeline'is
```

### Build Stage Failib

Kontrolli järgmist:

- Kas Dockerfile töötab lokaalses?
- Kas kõik failid on commit'itud?
- Kas on permissions GitHub Container Registry'sse? (Settings → Actions → General → Workflow permissions → Read and write)

### Deploy ei Käivitu

Kui manual deploy:

- GitHub'is Settings → Environments → Create environment "production"
- Seal saad seadistada manual approval

Kui automatic deploy:

- Kontrolli if ja needs tingimusi workflow failis

---

## Õppematerjalid

Kasulikud ressursid:

- Lab materjalid
- GitHub Actions dokumentatsioon: https://docs.github.com/actions
- Docker dokumentatsioon: https://docs.docker.com/

Edu kodutöö tegemisel!