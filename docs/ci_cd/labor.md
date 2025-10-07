# Pidev Integratsioon ja Tarnimine (CI/CD) Labor

**Eeldused:** Git põhitõed, Docker, käsurida  
**Platvorm:** GitHub Actions

---

## Õpiväljundid

Pärast seda labor'it oskad:
- **Loob** GitHub Actions pipeline'i põhistruktuuri stage'idega
- **Seadistab** automaatse testimise ja Docker build'i
- **Debugib** pipeline vigu logide abil
- **Rakendab** manual approval'i production deployment'iks
- **Selgitab** miks CI/CD vähendab vigu ja säästab aega

---

## Enne kui alustad

See labor võtab umbes 90 minutit. Lab'i lõpuks on sul töötav automatiseeritud süsteem: sina kirjutad koodi, teed git push, ja automaatne masin kontrollib koodi, käivitab testid, ehitab Docker image ja deploy'ib rakenduse pärast sinu kinnitust.

### Miks see oluline?

Vaatame kahte stsenaariumi. Ilma CI/CD'ta peab arendaja käsitsi testid jooksutama, mis võtab kakskümmend minutit ja mida vahel unustatakse. Seejärel käsitsi Docker build, mis võtab kümme minutit. Siis käsitsi deployment, veel viisteist minutit. Kui midagi läheb valesti, võtab rollback pool tundi. Kokku üle seitsmekümne minuti ja kolmekümne protsendine vigade risk.

CI/CD'ga arendaja kirjutab koodi ja teeb git push. Pipeline käivitub automaatselt. Viis minutit hiljem on kõik testid läbitud ja süsteem on valmis deployment'iks. Üks klikk ja valmis. Kokku viis minutit pluss üks klikk, viis protsenti vigade risk.

---

## 1. Rakenduse ja Git Setup

Selles jaotises loome lihtsa API, mida hiljem automatiseerime. Me kasutame lihtsat rakendust, et fookus oleks automatiseerimisel, mitte rakenduse keerukusel. Kui rakendus on keerukas, on raske eristada kas probleem on rakenduses või pipeline'is.

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

Health endpoint on oluline, sest pipeline kasutab seda pärast deployment'i kontrollimaks kas rakendus töötab. Kui health endpoint ei vasta, siis deployment on ebaõnnestunud.

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

Ava teine terminal ja testi endpoint'e:
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/products
```

Kõik kolm endpoint'i peaksid tagastama JSON vastuse.

### Loo Git repository
```bash
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore

git add .
git commit -m "Initial: Flask app"
```

### GitHub setup

Mine GitHub'i lehele ja loo uus repository nimega cicd-demo. Vali Public visibility, et GitHub Actions töötaks tasuta.
```bash
# Asenda USERNAME oma GitHub kasutajanimega
git remote add origin https://github.com/USERNAME/cicd-demo.git
git push -u origin main
```

### Kontrolli

Veendu et rakendus töötab kohalikult, kõik endpoint'id vastavad korrektselt ja kood on GitHub'is nähtav.

---

## 2. Validate Stage

Selles jaotises loome esimese pipeline stage'i, mis kontrollib koodi süntaksit. Pipeline'id on jagatud stage'ideks hierarhilises järjekorras. Validate stage võtab umbes kümme sekundit, test stage kolmkümmend sekundit, build kaks minutit ja deploy ühe minuti. Põhimõte on leida vigu võimalikult vara ja odavalt.

Kui koodis on süntaksi viga, siis validate stage fail'ib kümne sekundi pärast. Ilma validate'ita jookseks build kaks minutit ja alles siis fail'iks. See tähendab et kaks minutit aega läks raisku.

### Validate stage eesmärk

Validate stage kontrollib ainult süntaksi vigu. See ei kontrolli loogikat ega ärireegleid. Näiteks validate leiab kui kooloni ei ole funktsioonideklaratsioonis, aga ei leia kui if-lause kasutab vale võrdlusmärki.

Validate on esimene stage, kuna see on kõige kiirem ja odavam viis vigade leidmiseks. Kui valideerimine fail'ib, pole mõtet teste ega build'i käivitada.

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
          echo "Alustan valideerimist..."
          python -m py_compile app.py
          echo "Kood on korrektne"
```

Workflow käivitub automaatselt kui keegi pushib või avab pull request'i main branch'i. Validate job käivitub Ubuntu masinal, tõmbab koodi, seadistab Python'i ja kontrollib app.py süntaksit.

### Push ja vaata
```bash
git add .github/
git commit -m "Add pipeline: validate stage"
git push origin main
```

Mine GitHub'is Actions tab'i alla. Kliki pipeline'i nimel ja vaata validate job'i logi. Pipeline peaks käivituma automaatselt, job peaks olema roheline ja logis peaksid nägema echo käskude väljundit.

### Eksperiment - süntaksi viga

Nüüd õpime kuidas pipeline vigu leiab. Lisa app.py faili tahtlik süntaksi viga. Muuda real kuus def home(): nii, et eemaldad kooloni: def home(). Commit ja push.
```bash
git add app.py
git commit -m "Test: syntax error"
git push origin main
```

Mine GitHub Actions'i ja vaata mis juhtub. Pipeline fail'ib kiiresti. Vaata error message'it logis. See näitab täpselt kus viga on. Paranda viga ja push uuesti.
```bash
# Paranda app.py - lisa koolon tagasi
git add app.py
git commit -m "Fix: syntax error"
git push origin main
```

### Refleksioon

Mõtle kui kiiresti said teada, et midagi oli valesti. Kümme sekundit versus minutid või tunnid hiljem. See on validate stage'i väärtus.

---

## 3. Test Stage

Selles jaotises lisame automaatsed testid, mis kontrollivad kas rakendus töötab õigesti. Validate kontrollib süntaksit, test kontrollib loogikat. Validate leiab kui koolon puudub. Test leiab kui rakendus tagastab vale andmeid.

### Validate versus Test

Validate kontrollib kas kood kompileerub. Test kontrollib kas kood teeb õiget asja. Validate võtab kümme sekundit. Test võtab kolmkümmend kuni kuuskümmend sekundit. Validate leiab vigu mida compiler näeks. Test leiab vigu mida kasutaja näeks. Mõlemad on vajalikud.

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

def test_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.get_json()) == 2
```

Esimene test kontrollib health endpoint'i - see peab tagastama status code 200 ja status healthy. Teine test kontrollib home endpoint'i - versioon peab olema 1.0.0. Kolmas test kontrollib products endpoint'i - peab olema kaks toodet.

### Testi kohalikult
```bash
pytest test_app.py -v
```

Kõik kolm testi peaksid läbima rohelisega. Kui mõni test fail'ib, loe error message'it. Vaata milline assert fail'is. Paranda test või rakendus.

### Lisa test stage workflow'sse

Uuenda .github/workflows/ci.yml faili. Lisa uus job nimega test, mis jookseb pärast validate'i:
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
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest test_app.py -v
          echo "Testid läbisid edukalt"
```

Test job kasutab needs: validate, mis tähendab et test jookseb ainult kui validate õnnestub. Kui validate fail'ib, siis test ei käivitu üldse. See hoiab kokku aega ja ressursse.

### Push ja kontrolli
```bash
git add test_app.py .github/workflows/ci.yml
git commit -m "Add tests and test stage"
git push origin main
```

Mine GitHub Actions'i. Vaata et validate job jookseb esimesena. Test job jookseb teisena. Mõlemad peaksid olema rohelised.

### Eksperiment - testide failure

Nüüd vaatame mis juhtub kui test fail'ib. Muuda app.py's versiooni 2.0.0 aga ära muuda test'i. Test ootab endiselt versiooni 1.0.0.
```bash
# Muuda app.py's version: '2.0.0'
git add app.py
git commit -m "Update version"
git push origin main
```

Vaata GitHub Actions'is mis juhtub. Validate läbib edukalt. Test fail'ib. Loe error message'it - see näitab et oodati 1.0.0 aga sai 2.0.0. Paranda test nii, et see ootab 2.0.0 ja push uuesti.

---

## 4. Build Stage

Selles jaotises pakime rakenduse Docker image'iks. Docker image sisaldab rakendust, kõiki dependencies'eid, operatsioonisüsteemi ja runtime'i. See tähendab et kui image töötab meie masinas, töötab see ka igal pool mujal.

### Miks Docker?

Klassikaline probleem: arendaja ütleb et rakendus töötab tema masinas. Server ütleb et ei tööta. Põhjused on erinevad Python versioonid, puuduvad teegid või erinev operatsioonisüsteem. Docker lahendab selle pakendades kõik kokku ühte image'isse.

### Loo Dockerfile

Loo fail nimega Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app

# Kopeeri ja installi dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopeeri rakendus
COPY app.py .

# Port
EXPOSE 5000

# Käivita
CMD ["python", "app.py"]
```

Dockerfile algab Python 3.9 slim base image'iga. Töökaust on app. Esimesena kopeerime requirements.txt ja installime dependencies. Alles seejärel kopeerime app.py. See järjekord on oluline Docker layer caching'u jaoks. Dependencies muutuvad harva, app.py muutub tihti. Kui kopeerime requirements eraldi, siis Docker cacheb dependency installatsiooni.

### Testi Docker kohalikult
```bash
# Ehita image
docker build -t cicd-demo:test .

# Käivita container
docker run -d -p 5000:5000 --name test-app cicd-demo:test

# Testi
curl http://localhost:5000/health

# Peata ja eemalda
docker stop test-app
docker rm test-app
```

Kontrolli et Docker build õnnestub, container käivitub ja rakendus vastab korrektselt.

### Lisa build stage

Uuenda .github/workflows/ci.yml faili. Lisa build job mis jookseb pärast test'i:
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
      
      - name: Build and push Docker image
        run: |
          IMAGE_NAME=ghcr.io/${{ github.repository }}
          docker build -t $IMAGE_NAME:${{ github.sha }} .
          docker build -t $IMAGE_NAME:latest .
          docker push $IMAGE_NAME:${{ github.sha }}
          docker push $IMAGE_NAME:latest
          echo "Image pushed successfully"
```

Build job kasutab if tingimust, et jooksda ainult main branch'il. See hoiab ära et iga feature branch push'iga ehitataks Docker image. Job logib sisse GitHub Container Registry'sse, ehitab image'i kahe tag'iga ja pushib registry'sse.

Kaks tag'i on vajalikud erinevatel põhjustel. Latest tag on lihtsam development'is - see annab alati uusima versiooni. Commit hash tag on täpne versioon, mida saab kasutada rollback'iks või audit'iks.

### Seadista permissions

GitHub vajab luba registry'sse kirjutamiseks. Mine repo Settings'i. Vali Actions alt General. Workflow permissions alt vali Read and write permissions. Salvesta.

### Push ja kontrolli
```bash
git add Dockerfile .github/workflows/ci.yml
git commit -m "Add Docker build stage"
git push origin main
```

Mine GitHub Actions'i ja vaata pipeline'i. Validate, test ja build peaksid kõik edukalt läbima. Mine repo põhilehele ja vaata Packages sektsiooni paremal. Seal peaks nähtav olema sinu image koos kahe tag'iga.

---

## 5. Deploy Stage

Selles jaotises lisame deployment'i, mis viib rakenduse live keskkonda. Deploy võib olla automaatne või nõuda manuaalset kinnitust. Development ja staging keskkonnad kasutavad tavaliselt automaatset deployment'i, kuna risk on madal ja kiire feedback on oluline. Production kasutab manuaalset deployment'i, kuna risk on kõrge ja vajame kontrolli.

### Automaatne versus manuaalne

Otsustuspunkt on keskkond. Development'is on automaatne deploy hea, sest kiire feedback ja madal risk. Staging'us samuti automaatne, et testida enne production'i. Production'is manuaalne, sest kõrge risk ja vajame kinnitust.

Mõned ettevõtted kasutavad täielikult automaatset production deployment'i, aga see nõuab väga häid teste, kõrget coverage'it, madalat riski ja lihtsat rollback'i. Enamik ettevõtteid kasutab manuaalset production deployment'i.

### Lisa deploy stage

Uuenda .github/workflows/ci.yml faili. Lisa deploy job:
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
          echo "Deploying $IMAGE_NAME"
          echo "SIMULATED: docker pull $IMAGE_NAME"
          echo "SIMULATED: docker stop cicd-demo || true"
          echo "SIMULATED: docker rm cicd-demo || true"
          echo "SIMULATED: docker run -d --name cicd-demo -p 5000:5000 $IMAGE_NAME"
          echo "SIMULATED: Health check would run here"
          echo "Deploy successful"
```

Deploy job kasutab environment konfiguratsiooni. See võimaldab meil seadistada manual approval'i ja näha deployment ajalugu.

### Seadista manual approval

Mine GitHub repo Settings'i. Vali Environments. Loo uus environment nimega production. Deployment protection rules alt vali Required reviewers. Lisa ennast vähemalt üheks reviewer'iks. Salvesta.

### Testi deployment workflow

Muuda app.py's versiooni 2.0.0. Uuenda test_app.py's oodatavat versiooni 2.0.0. Commit ja push.
```bash
git add app.py test_app.py .github/workflows/ci.yml
git commit -m "Version 2.0.0 + deploy stage"
git push origin main
```

Mine GitHub Actions'i ja vaata pipeline'i. Validate, test ja build jooksevad läbi. Deploy job jääb ootama kollase Waiting staatusega. Kliki deploy job'il. Vajuta Review deployments. Märgi production ja vajuta Approve and deploy. Vaata kuidas deploy job käivitub ja logis näed deployment samme.

### Deployment ajalugu

Pärast deployment'i mine repo Settings'i ja vaata Environments lehte. Seal näed production environment'i ja deployment ajalugu. Iga deployment on logitud koos ajaga, kasutajaga ja commit'iga.

---

## 6. Pipeline Optimeerimine

Selles jaotises õpime kuidas pipeline'i kiiremaks teha. Põhiline tehnika on caching, mis võimaldab meil salvestada ja taaskasutada andmeid pipeline run'ide vahel.

### Caching kontseptsioon

Probleem on see, et iga pipeline run installib dependencies nullist. Kui dependencies ei muutu, siis see on sama töö kordamine. Esimene run võtab kolmkümmend sekundit dependency installatsiooni. Teine run võtab jälle kolmkümmend sekundit. Kolmas run samuti.

Caching lahendab selle. Esimene run installib dependencies ja salvestab cache'sse. Teine run laeb cache'st, mis võtab ainult viis sekundit. See on kuus korda kiirem.

### Lisa caching test job'i

Uuenda test job'i .github/workflows/ci.yml failis:
```yaml
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
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest test_app.py -v
```

Setup-python action toetab built-in caching'ut. Lisa lihtsalt cache: pip parameeter ja see hakkab automaatselt cachima pip dependencies'eid.

### Lisa README badge

Loo README.md fail:
```markdown
# CI/CD Demo

[![CI/CD](https://github.com/USERNAME/cicd-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/cicd-demo/actions/workflows/ci.yml)

Automaatse CI/CD pipeline'iga Flask API.

## Pipeline

Pipeline koosneb neljast stage'ist:

1. Validate - Python syntax check
2. Test - Automated tests
3. Build - Docker image
4. Deploy - Manual production deployment

## Endpoints

Rakendus pakub kolme endpoint'i:

- GET / - API info
- GET /health
- Health check
- GET /products
- Products list

## Käivitamine
```

Lokaalselt:

```bash
pip install -r requirements.txt
python app.py
```

Docker'iga:
```bash
docker build -t cicd-demo .
docker run -p 5000:5000 cicd-demo
```

Testid:
```bash
pytest test_app.py -v
```

Asenda USERNAME oma GitHub kasutajanimega. Badge näitab pipeline'i staatust - roheline kui kõik töötab, punane kui midagi on katki.

### Viimane push
```bash
git add README.md .github/workflows/ci.yml
git commit -m "Add caching and README"
git push origin main
```

Vaata GitHub'is et pipeline jookseb läbi ja README näitab badge'i.

---

## Kontrollnimekiri

Kontrolli et oled kõik sammud läbinud:

**Rakendus:**
- [ ] Flask app töötab kohalikult
- [ ] Kõik kolm endpoint'i vastavad korrektselt
- [ ] Testid läbivad kohalikult

**Pipeline:**
- [ ] Validate stage kontrollib süntaksit
- [ ] Test stage jooksutab automaatseid teste
- [ ] Build stage ehitab Docker image'i
- [ ] Deploy stage nõuab manual approval'i

**GitHub:**
- [ ] Repository on public
- [ ] Actions permissions on seadistatud
- [ ] Production environment on loodud
- [ ] Image on nähtav Packages'is

**Mõistmine:**
- [ ] Tead miks validate on esimene stage
- [ ] Mõistad erinevust validate ja test vahel
- [ ] Oskad selgitada miks kasutame Docker'it
- [ ] Tead millal kasutada manual deployment'i

---

## Refleksioon

Vasta ausalt järgmistele küsimustele. See aitab sul õppida ja mõista mida õppisid.

**Mis oli kõige raskem?**

Kirjuta paar lauset selle kohta, mis osa lab'ist oli kõige keerulisem. Kas see oli YAML süntaks, Docker mõistmine, pipeline'i debugimine või kontseptsioonide mõistmine?

**Mis oli ahaa moment?**

Kirjuta millal läks lambike põlema. Millist kontseptsiooni sa nüüd mõistad, mis varem oli ebaselge? Kas see oli kui nägid kuidas automaatne testimine töötab? Või kui mõistsid miks validate peab olema esimene?

**Kas oskad selgitada?**

Kontrolli et oskad sõnastada:
- Miks validate on esimene stage? (Kõige kiirem viis vigade leidmiseks)
- Miks production deploy on manual? (Kõrge risk, vajame kontrolli)
- Kuidas Docker aitab? (Garanteerib sama keskkonna igal pool)

**Mida teeksid järgmine kord teisiti?**

Kirjuta paar lauset selle kohta, mida sa järgmine kord teisiti teeksid. Kas alustaksid teisest kohast? Kas kasutaksid rohkem dokumentatsiooni? Kas võtaksid rohkem aega mõistmiseks?

**Järgmised sammud:**

Nüüd oskad luua põhilist CI/CD pipeline'i, automatiseerida build-test-deploy protsessi ja kasutada Docker'it CI/CD kontekstis. Järgmised võimalused on kodutöö kus lood sarnase pipeline'i erineva rakendusega, lisapraktika kus lisad notifications'eid ja rollback'i või uurid GitLab CI'd kui alternatiivi GitHub Actions'ile.