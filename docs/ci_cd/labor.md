# Pidev Integratsioon ja Tarnimine (CI/CD) Labor

**Eeldused:** Git põhitõed, Docker, käsurida  
**Platvorm:** GitHub Actions  
**Oluline:** See labor sisaldab tahtlikke vigu! Sinu ülesanne on need leida ja parandada.

---

## Õpiväljundid

Pärast seda labor'it oskad:

- **Loob** GitHub Actions pipeline'i põhistruktuuri stage'idega
- **Debugib** pipeline vigu logide abil (praktiliselt!)
- **Leiab ja parandab** vigu mida CI/CD süsteem avastab
- **Seadistab** automaatse testimise ja Docker build'i
- **Rakendab** manual approval'i production deployment'iks

---

## Enne kui alustad

See labor võtab umbes 90 minutit. Lab'i lõpuks on sul töötav automatiseeritud süsteem mis leiab vigasid sinu eest.

⚠️ **TÄHTIS:** Selles lab'is on tahtlikke vigu! Need on seal õppimise eesmärgil. Sinu ülesanne on:
1. Järgida juhiseid
2. Push'ida koodi GitHubi
3. Vaadata mis GitHub Actions ütleb
4. Leida ja parandada vead
5. Push'ida uuesti

See on päris maailm - CI/CD leiab vigu ja sina pead need parandama!

---

## 1. Rakenduse ja Git Setup

### Loo projekt
```bash
mkdir cicd-demo
cd cicd-demo
git init
git branch -M main
```

### Loo Flask rakendus

Loo fail nimega app.py:
```python
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'CI/CD Demo API',
        'version': '1.0.0',
        'timestamp': str(datetime.now())
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/products')
def products():
    return jsonify([
        {'id': 1, 'name': 'Laptop', 'price': 999},
        {'id': 2, 'name': 'Phone', 'price': 599}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Loo fail nimega requirements.txt:
```
Flask==3.0.0
pytest==7.4.3
```

### Testi kohalikult
```bash
pip install -r requirements.txt
python app.py
```

Ava teine terminal:
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/products
```

### Loo Git repository
```bash
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore

git add .
git commit -m "Initial: Flask app"
```

### GitHub setup

Mine GitHub'i ja loo uus repository nimega cicd-demo (Public).
```bash
# Asenda USERNAME oma GitHub kasutajanimega
git remote add origin https://github.com/USERNAME/cicd-demo.git
git push -u origin main
```

---

## 2. Validate Stage

### Loo workflow fail

Loo kataloog ja fail: .github/workflows/ci.yml
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Validate Python syntax
        run: |
          python -m py_compile app.py
          echo "✅ Süntaks on korrektne"
```

### Push ja vaata
```bash
git add .github/
git commit -m "Add pipeline: validate stage"
git push origin main
```

Mine GitHub'is Actions tab'i alla. Pipeline peaks olema roheline ✅.

### 🎯 Ülesanne 2.1: Süntaksi viga

**SINU ÜLESANNE:** Tee tahtlik süntaksi viga ja vaata kuidas pipeline selle leiab!

1. Muuda `app.py` real 8: eemalda koolon `def home():` lõpust → `def home()`
2. Push GitHubi:
```bash
git add app.py
git commit -m "Test: intentional error"
git push origin main
```
3. Mine GitHub Actions'i → Vaata: ❌ PUNANE!
4. Kliki pipeline'i peale → Loe error message'it
5. **Küsimus:** Mis real viga on? Mida error ütleb?
6. Paranda viga (lisa koolon tagasi)
7. Push uuesti → Peaks olema ✅ roheline

**Refleksioon:** Kui kiiresti said teada et midagi oli valesti? See on validate stage'i väärtus!

---

## 3. Test Stage

### Loo testid

Loo fail nimega test_app.py:
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['version'] == '1.0.0'
    assert 'message' in data

def test_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 2
    
    # Kontrolli et kõik hinnad on positiivsed
    for product in products:
        assert product['price'] > 0, f"Hind peab olema positiivne! Leitud: {product['price']}"
```

Viimane test kontrollib ärireegleid - hinnad peavad olema positiivsed!

### Testi kohalikult
```bash
pytest test_app.py -v
```

Kõik testid peaksid läbima ✅.

### Lisa test stage

Uuenda .github/workflows/ci.yml:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Validate Python syntax
        run: |
          python -m py_compile app.py

  test:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest test_app.py -v
```

### Push ja kontrolli
```bash
git add test_app.py .github/workflows/ci.yml
git commit -m "Add tests and test stage"
git push origin main
```

Validate ✅ → Test ✅

### 🎯 Ülesanne 3.1: Negatiivne hind

**SINU ÜLESANNE:** Lisa negatiivne hind ja vaata kuidas test selle leiab!

1. Muuda `app.py` products funktsioonis Phone hind: `'price': 599` → `'price': -599`
2. Push:
```bash
git add app.py
git commit -m "Negative price bug"
git push origin main
```
3. Vaata GitHub Actions'is:
   - Validate ✅ (süntaks on õige)
   - Test ❌ (äriloogika on vale!)
4. Loe error message'it - mis test fail'is?
5. Paranda hind positiivseks
6. Push uuesti → ✅

**Küsimus:** Miks validate ei leidnud seda viga aga test leidis?

### 🎯 Ülesanne 3.2: Versiooni uuendus

**SINU ÜLESANNE:** Uuenda versiooni aga unusta test'i uuendada!

1. Muuda `app.py`-s: `'version': '1.0.0'` → `'version': '2.0.0'`
2. ÄRA muuda test'i!
3. Push:
```bash
git add app.py
git commit -m "Update to version 2.0.0"
git push origin main
```
4. Vaata: Test ❌ fail'ib!
5. Loe error'it - test ootab 1.0.0 aga saab 2.0.0
6. Uuenda `test_app.py` test'is: `assert data['version'] == '2.0.0'`
7. Push uuesti → ✅

**Õppetund:** Kui muudad koodi, pead muutma ka teste!

---

## 4. Build Stage

### Loo Dockerfile

⚠️ **TÄHELEPANU:** Selles Dockerfile'is on tahtlik viga!

Loo fail nimega Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Tahtlik viga - vale port!
EXPOSE 8080

CMD ["python", "app.py"]
```

### Testi Docker kohalikult
```bash
docker build -t cicd-demo:test .
docker run -d -p 5000:5000 --name test-app cicd-demo:test
curl http://localhost:5000/health
docker stop test-app && docker rm test-app
```

### Lisa build stage

Uuenda .github/workflows/ci.yml (lisa build job):
```yaml
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
      
      - name: Build Docker image
        run: |
          IMAGE_NAME=ghcr.io/${{ github.repository }}
          docker build -t $IMAGE_NAME:${{ github.sha }} .
          docker build -t $IMAGE_NAME:latest .
      
      - name: Test Docker image
        run: |
          IMAGE_NAME=ghcr.io/${{ github.repository }}:${{ github.sha }}
          docker run -d -p 5000:5000 --name test-container $IMAGE_NAME
          sleep 5
          
          # Health check
          if curl -f http://localhost:5000/health; then
            echo "✅ Health check passed"
          else
            echo "❌ Health check failed"
            docker logs test-container
            exit 1
          fi
          
          docker stop test-container
          docker rm test-container
      
      - name: Push Docker image
        run: |
          IMAGE_NAME=ghcr.io/${{ github.repository }}
          docker push $IMAGE_NAME:${{ github.sha }}
          docker push $IMAGE_NAME:latest
```

### Seadista permissions

Mine repo Settings → Actions → General → Workflow permissions → **Read and write permissions** → Save.

### 🎯 Ülesanne 4.1: Paranda Dockerfile

1. Push praegune kood:
```bash
git add Dockerfile .github/workflows/ci.yml
git commit -m "Add Docker build"
git push origin main
```
2. Validate ✅, Test ✅, Build... oodake...
3. Build jookseb aga kas health check õnnestub? Vaata logi!
4. **SINU ÜLESANNE:** 
   - Kui health check fail'ib, loe error'it
   - Mõtle: mis Dockerfile'is on valesti?
   - Vihje: Vaata EXPOSE rida ja võrdle rakenduse pordiga
5. Paranda Dockerfile: `EXPOSE 5000`
6. Push uuesti → ✅

**Küsimus:** Miks on health check oluline pärast build'i?

---

## 5. Deploy Stage

### Lisa deploy stage

Uuenda .github/workflows/ci.yml (lisa deploy job):
```yaml
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: http://localhost:5000
    steps:
      - name: Deploy application
        run: |
          IMAGE_NAME=ghcr.io/${{ github.repository }}:${{ github.sha }}
          echo "🚀 Deploying $IMAGE_NAME"
          echo "SIMULATED: docker pull $IMAGE_NAME"
          echo "SIMULATED: docker stop cicd-demo || true"
          echo "SIMULATED: docker rm cicd-demo || true"
          echo "SIMULATED: docker run -d --name cicd-demo -p 5000:5000 $IMAGE_NAME"
          echo "SIMULATED: Health check..."
          echo "✅ Deploy successful"
```

### Seadista manual approval

1. Mine Settings → Environments
2. Loo "production" environment
3. Deployment protection rules → ✅ Required reviewers
4. Lisa enda nimi
5. Save

### 🎯 Ülesanne 5.1: Manual deployment

1. Lisa uus feature - endpoint /api/version:
```python
@app.route('/api/version')
def version():
    return jsonify({'version': '2.0.0', 'build': 'stable'})
```

2. Lisa test sellele:
```python
def test_version_endpoint(client):
    response = client.get('/api/version')
    assert response.status_code == 200
    data = response.get_json()
    assert data['version'] == '2.0.0'
```

3. Push:
```bash
git add app.py test_app.py .github/workflows/ci.yml
git commit -m "Add version endpoint + deploy stage"
git push origin main
```

4. GitHub Actions'is:
   - Validate ✅
   - Test ✅
   - Build ✅
   - Deploy 🟡 **Waiting for approval**

5. Kliki deploy job'il → **Review deployments** → Approve → Vaata kuidas deployb!

**Küsimus:** Miks production vajab manual approval'i aga test/build mitte?

---

## 6. Täiendavad Väljakutsed

### 🎯 Väljakutse 6.1: Lisa uus endpoint

**SINU ÜLESANNE:** Lisa täiesti uus endpoint koos testiga!

1. Lisa `app.py`-sse:
```python
@app.route('/api/status')
def status():
    return jsonify({
        'api': 'running',
        'version': '2.0.0',
        'endpoints': ['/', '/health', '/products', '/api/version', '/api/status']
    })
```

2. Kirjuta test `test_app.py`-sse (sina kirjuta ise!)
3. Push ja kontrolli et pipeline läbib ✅

### 🎯 Väljakutse 6.2: Badge README'sse

1. Loo README.md:
```markdown
# CI/CD Demo

![CI/CD](https://github.com/USERNAME/cicd-demo/actions/workflows/ci.yml/badge.svg)

Automaatse CI/CD pipeline'iga Flask API.

## Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /products` - Products list
- `GET /api/version` - Version info
- `GET /api/status` - API status

## Pipeline

Pipeline koosneb 4 stage'ist:

1. **Validate** - Python syntax check
2. **Test** - Automated tests (pytest)
3. **Build** - Docker image + health check
4. **Deploy** - Manual production deployment

## Features

✅ Automaatne testimine  
✅ Docker containerization  
✅ Manual production approval  
✅ Health checks  
✅ Negatiivse hinna kontroll  
```

2. Asenda USERNAME oma kasutajanimega
3. Push → Mine GitHubi ja vaata badge'i!

### 🎯 Väljakutse 6.3: Rollback

**Stsenaarium:** Version 2.0.0 on production'is aga on bug!

1. Vaata GitHub Packages lehte
2. Leia varasem image (commit hash)
3. Kuidas deployda vana versiooni tagasi?
4. Vihje: Muuda deploy stage'is image tag'i

---

## Kontrollnimekiri

**Rakendus:**
- [ ] Flask app töötab kohalikult
- [ ] Kõik endpoint'id vastavad
- [ ] Testid läbivad kohalikult

**Pipeline:**
- [ ] Validate leidis süntaksi vea (ülesanne 2.1)
- [ ] Test leidis negatiivse hinna (ülesanne 3.1)
- [ ] Test leidis versiooni mittevastavuse (ülesanne 3.2)
- [ ] Dockerfile port viga parandatud (ülesanne 4.1)
- [ ] Manual approval production'i töötab (ülesanne 5.1)

**Mõistmine:**
- [ ] Tead miks validate on esimene (kiireim vigade leidmine)
- [ ] Mõistad erinevust validate ja test vahel
- [ ] Oskad selgitada miks Docker health check vajalik
- [ ] Tead millal kasutada manual deployment'i

**Boonus:**
- [ ] Lisasid uue endpoint'i (väljakutse 6.1)
- [ ] README koos badge'iga (väljakutse 6.2)

---

## Refleksioon

**Mis oli kõige raskem?**

Kirjuta paar lauset: Mis osa oli keerulisem? Kas debug logide lugemine? YAML süntaks? Docker?

**Ahaa moment?**

Mis hetkel läks lambike põlema? Millal mõistsid kuidas CI/CD päriselt töötab?

**Kas oskad selgitada:**

- Miks validate on esimene stage? *(Vastus: Kõige kiirem viis vigade leidmiseks - võtab 10s, mitte 2min)*
- Miks test leidis negatiivse hinna aga validate mitte? *(Vastus: Validate kontrollib süntaksit, test kontrollib loogikat)*
- Miks production vajab manual approval'i? *(Vastus: Kõrge risk, vajame kontrolli)*

**Järgmised sammud:**

Nüüd oskad:
- Luua CI/CD pipeline'i GitHubis
- Debugida pipeline vigu praktiliselt
- Lisada automaatseid teste
- Kasutada Docker'it CI/CD's
- Seadistada manual approval'i

**Edasi:**
- Kodutöö: Lisa CI/CD oma projektile
- Lisapraktika: GitLab CI alternatiiv
- Advanced: Multi-environment deployment (dev/staging/prod)
