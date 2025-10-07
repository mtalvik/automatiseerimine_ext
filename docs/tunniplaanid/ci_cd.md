# Tunnikava: CI/CD – Pidev Integratsioon ja Tarnimine

**Kestus:** 4×45 min + 1.5h kodutöö  
**Tase:** Keskmine (eelteadmised: Git, Docker, YAML põhitõed)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`, `lisapraktika.md`

---

## Õpiväljundid

Pärast kursust õpilane:

- **ÕV1:** Selgitab CI/CD vajadust ja eristab Continuous Integration'it Continuous Deployment'ist
- **ÕV2:** Seadistab GitHub Actions pipeline'i põhistruktuuri (jobs, steps, triggers)
- **ÕV3:** Kirjutab YAML workflow'sid testide ja build'i automatiseerimiseks
- **ÕV4:** Automatiseerib Docker image build'i ja push'i container registry'sse
- **ÕV5:** Rakendab best practices'eid (secrets management, caching, parallel execution)

---

## Pedagoogiline raamistik

**Lähenemisviis:** Constructivist - ehita uued teadmised olemasolevatele

**Põhimõtted:**
1. **Eelteadmised:** Õpilased teavad käsitsi deployment'i - näita kuidas automatiseerimine seda asendab
2. **Progressiivne keerukus:** Alusta lihtsast (hello world) → liikudes keerulisemale (multi-stage pipeline)
3. **Metakognitsioon:** Pipeline debugging = õppimine vigadest, mitte ebaõnnestumine
4. **Authentic learning:** Kasuta päris tööriistu (GitHub Actions, Docker Hub), mitte simulatsioone

**Bloom'i taksonoomia rakendus:**

- Mäletamine: CI/CD definitsioonid
- Mõistmine: Miks automatiseerimine on vajalik
- Rakendamine: Pipeline'i kirjutamine
- Analüüs: Pipeline logide lugemine ja debugging
- Hindamine: Best practices vs bad practices

---

## Õpetamismeetodid

| Meetod | Kirjeldus | Kasutus |
|--------|-----------|---------|
| **Demonstratsioon** | Live coding - näita pipeline'i loomist | Iga bloki algus (10-15 min) |
| **Juhendatud praktika** | Õpilased järgivad samm-sammult | Lab'i esimene pool |
| **Iseseisev praktika** | Õpilased lahendavad ise | Lab'i teine pool |
| **Peer learning** | Paaristöö debugging | Kui keegi kinni jääb |
| **Refleksioon** | "Miks see ebaõnnestus?" | Iga bloki lõpp |

---

## Õpetaja ettevalmistus

### Enne esimest tundi

**Tehniline setup:**

- [ ] GitHub organisatsioon õpilastele (või public repos)
- [ ] Näidis repository valmis (Python Flask või Node.js Express)
- [ ] GitHub Actions enabled (default on)
- [ ] Docker Hub konto (demonstratsiooniks)
- [ ] Backup plan: GitLab.com kui GitHub on maas

**Materjalide kontroll:**

- [ ] `loeng.md` läbi loetud
- [ ] `labor.md` testitud (kas kõik käsud töötavad)
- [ ] `kodutoo.md` selge
- [ ] Projektoriga demo repo valmis

### Enne iga tundi

**5 minutit enne:**
- [ ] Ava demo repo browseris
- [ ] Ava GitHub Actions tab
- [ ] Terminal valmis
- [ ] Code editor avatud

---

## Tüüpilised probleemid ja lahendused

### "Pipeline ei käivitu"

**Probleem:** `.github/workflows/` kaust puudub või vale nimi

**Lahendus:**
```bash
mkdir -p .github/workflows
# NB! Täpselt see path, mitte .github/workflow
```

### "Syntax error in YAML"

**Probleem:** Indentation vale (YAML on range!)

**Lahendus:**

- Näita https://www.yamllint.com/
- Selgita: YAML kasutab spaces, mitte tabs
- Tipp: VS Code YAML extension

### "Permission denied - Docker Hub"

**Probleem:** Secrets pole seadistatud või vale nimi

**Lahendus:**
1. Settings → Secrets and variables → Actions
2. New repository secret
3. Nimi TÄPSELT nagu workflow'is: `DOCKER_USERNAME`

### "Tests fail"

**Probleem:** Dependency puudub või test on vale

**Lahendus:**

- Loe logs tähelepanelikult (scroll to error)
- "Kas see töötab lokaalses?"
- Dependencies install before test

### "Image not found on Docker Hub"

**Probleem:** Vale repository nimi või pole push'inud

**Lahendus:**

- Docker Hub repo nimi: `username/reponame` (lowercase!)
- Kontrolli kas push job õnnestus

---

## Blokk 1: CI/CD põhitõed ja esimene pipeline (45 min)

### Eesmärk
Õpilane mõistab CI/CD vajadust ja loob esimese toimiva GitHub Actions workflow'i.

### Minutiplaan

**0-10 min: Motivatsioon ja kontekst**

Alusta küsimusega (vastuseid ei vaja, mõtlema panna):
> "Kes on deploy'inud koodi production'i? Kuidas see käis?"

Näita probleemi:
```
Käsitsi deploy:
1. SSH serverisse
2. git pull
3. Install dependencies
4. Restart service
5. Kontrolli kas töötab
6. Kui ei tööta → debug
Aeg: 15-30 min
Vigu: palju
```

vs
```
CI/CD:
1. git push
Pipeline teeb automaatselt kõik
Aeg: 5 min
Vigu: vähem (testid püüavad kinni)
```

**10-15 min: CI/CD kontseptsioonid**

Selgita lühidalt (kasuta `loeng.md` slaide):

- **Continuous Integration:** Merge tihti, testi automaatselt
- **Continuous Deployment:** Kui testid OK → production automaatselt
- **Pipeline:** Sammud mida iga commit läbib

**NB:** Ära uppuge detailidesse! See on ülevaade, detailid tulevad lab'is.

**15-25 min: Live demo - Hello World pipeline**

Screen share + live coding:

1. Ava GitHub repo
2. Loo fail `.github/workflows/hello.yml`
```yaml
name: Hello World

on: [push]

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:

      - run: echo "Hello from CI/CD!"
```
3. Commit ja push
4. Mine Actions tab → näita kui see jookseb
5. Ava job logs → näita output

**Rõhuta:**

- `.github/workflows/`
- täpne path
- YAML süntaks
- indentation oluline
- Actions tab
- kus näed pipeline'e

**25-45 min: Juhendatud praktika**

Õpilased teevad sama:
1. Fork või loo uus repo
2. Loo `.github/workflows/hello.yml`
3. Push ja vaata Actions tab'is

**Kõnni ringi, aita:**

- YAML syntax errorid
- Kas Actions tab avaneb
- Kas näevad logs

**Lõpp-refleksioon (viimased 2 min):**
> "Mis oli kõige keerulisem?" (lase 2-3 õpilasel vastata)

### Kontrollpunktid

Bloki lõpuks:

- [ ] Iga õpilane on loonud esimese workflow'i
- [ ] Pipeline on käivitunud edukalt
- [ ] Õpilased teavad kus Actions tab on

---

## Blokk 2: Testide ja build'i automatiseerimine (45 min)

### Eesmärk
Õpilane lisab pipeline'i automaatsed testid ja build stage.

### Minutiplaan

**0-5 min: Recap**

> "Mida me eelmine kord tegime?" (lase õpilastel vastata)

**5-15 min: Demo - Tests in pipeline**

Live coding: Lisa testid pipeline'i
```yaml
name: CI

on: [push]

jobs:
  test:
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
        run: pytest tests/
```

**Selgita iga rida:**

- `actions/checkout`
- clone repo
- `actions/setup-python`
- install Python
- `run:`
- käivita käsud

**Näita kui see faili'b:**

- Loo tahtlikult failing test
- Näita punast X Actions tab'is
- Näita error logs

**Õpetuslik moment:** "Pipeline'i ebaõnnestumine EI OLE PROBLEEM - see on feature! See leidis vea enne kui production'i läks."

**15-35 min: Lab praktika**

Õpilased (`labor.md` harjutused 1-3):
1. Loo lihtne rakendus (Flask/Express)
2. Lisa testid
3. Lisa test job pipeline'i
4. Push ja vaata kas läbib

**Aita troubleshoot:**

- Dependencies install
- Test framework setup
- YAML süntaks

**35-45 min: Paaristöö + refleksioon**

Paarides:

- Üks inimene selgitab teisele oma pipeline'i
- Teine küsib: "Miks sa seda teed?"

**Lõpp-küsimus:**
> "Miks testid pipeline'is, mitte käsitsi?"

### Kontrollpunktid

- [ ] Pipeline sisaldab test job'i
- [ ] Testid jooksevad automaatselt
- [ ] Õpilased mõistavad MIKS testid on olulised

---

## Blokk 3: Docker image build ja registry push (45 min)

### Eesmärk
Õpilane automatiseerib Docker image build'i ja push'i Docker Hub'i.

### Minutiplaan

**0-5 min: Motivatsioon**

> "Kui teil on Docker image, kuidas te praegu seda build'ite ja push'ite?" (käsitsi)

Näita probleemi:
```bash
docker build -t myapp:v1.2.3 .
docker push myapp:v1.2.3
# Iga kord käsitsi
# Unustame versiooni number
# Vale tag
```

**5-15 min: Demo - Docker build in CI**

**OLULINE:** Enne demo, näita secrets setup:
1. GitHub Settings → Secrets
2. Lisa `DOCKERHUB_USERNAME` ja `DOCKERHUB_TOKEN`

Live coding:
```yaml
build:
  needs: test
  runs-on: ubuntu-latest
  steps:

    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push
      run: |
        docker build -t username/myapp:${{ github.sha }} .
        docker push username/myapp:${{ github.sha }}
```

**Selgita:**

- `needs: test`
- jookseb alles kui test õnnestub
- `secrets.*`
- turvaline viis paroole kasutada
- `github.sha`
- unikaalne commit hash

**15-40 min: Lab praktika**

Õpilased (labor.md):
1. Loo Dockerfile
2. Seadista Docker Hub secrets
3. Lisa build job
4. Push ja kontrolli Docker Hub'is

**Tüüpilised probleemid:**

- Secrets vale nimi
- Docker Hub repo pole public
- Image tag lowercase

**40-45 min: Refleksioon**

**Küsimus:**
> "Miks me kasutame secrets, mitte ei pane parooli otse koodi?"

Oodatav vastus: Turvalisus, kui repo on public

### Kontrollpunktid

- [ ] Docker image build'ib automaatselt
- [ ] Image push'ib Docker Hub'i
- [ ] Õpilased mõistavad secrets'ite vajadust

---

## Blokk 4: Best practices ja troubleshooting (45 min)

### Eesmärk
Õpilane optimeerib pipeline'i ja õpib debugima probleeme.

### Minutiplaan

**0-10 min: Pipeline optimeerimine**

Demo - näita aeglast vs kiiret pipeline'i:

**Aeglane:**
```yaml
- run: pip install -r requirements.txt  # 30 sek iga kord
```

**Kiire (cache'iga):**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

- run: pip install -r requirements.txt  # 5 sek
```

**Parallel jobs:**
```yaml
jobs:
  test:
    # ...
  
  lint:
    # Jookseb samaaegselt testidega
```

**10-20 min: Debugging techniques**

Näita reaalseid error log'e ja kuidas neid lugeda:

1. **YAML syntax error:**
```
Error: Unable to process file: .github/workflows/ci.yml
unexpected character
```
Lahendus: Kontrolli indentation

2. **Test failure:**
```
FAILED tests/test_app.py:

- :test_home
- assert 404 == 200
```
Lahendus: Loe mida assert ootab vs mis sai

3. **Permission denied:**
```
denied: requested access to the resource is denied
```
Lahendus: Secrets või login

**20-40 min: Lab - Optimeeri pipeline**

Õpilased:
1. Lisa caching
2. Tee 2 job'i parallel
3. Lisa badge README'sse

**40-45 min: Mini-quiz + kodutöö tutvustus**

**Quiz (suuliselt):**
1. "Mis on CI vs CD?"
2. "Miks testid enne build'i?"
3. "Kuidas debugid YAML syntax errori?"

**Kodutöö tutvustus:**

- Loo täielik pipeline uuele projektile
- Details `kodutoo.md`'is
- Tähtaeg: 1 nädal

### Kontrollpunktid

- [ ] Õpilased teavad caching'ut
- [ ] Oskavad pipeline log'e lugeda
- [ ] Mõistavad kodutöö ülesannet

---

## Kodutöö (1.5h)

Detailid failis `kodutoo.md`.

**Eesmärk:** Rakenda õpitud kontsepte uuele projektile (mitte lab'i kordamine).

**Struktuur:**
1. Vali erinev tehnoloogia kui lab'is
2. Disaini pipeline (`PIPELINE.md` - põhjendused)
3. Implementeeri
4. Dokumenteeri (`README.md` - refleksioon)

**Hindamine:**

- 20%
- Pipeline disain (põhjendused)
- 35%
- Implementation (töötab, järgib disaini)
- 15% - Testid
- 15%
- Dokumentatsioon
- 15%
- Refleksioon (konkreetsed vastused)

---

## Lisapraktika (boonus)

Failis `lisapraktika.md` - 3 advanced harjutust:
1. Multi-branch strategy
2. Performance optimization
3. Production-ready pipeline

**Kasutamine:**

- Kiired õpilased kes lab'i varakult lõpetavad
- Boonus punktid
- Portfolio materjal

---

## Hindamiskriteeriumid (lab + kodutöö)

### Lab (formatiivne)

**Eesmärk:** Õppimine, mitte hindamine

**Kontroll:**

- [ ] Pipeline eksisteerib ja käivitub
- [ ] Vähemalt 2 job'i (test + build)
- [ ] Testid läbivad

**Punktid ei ole olulised** - fookus on mõistmisel.

### Kodutöö (summatiivne)

**Detailid `kodutoo.md`'is**

**Läbimiseks (50%):**

- Pipeline töötab
- Testid läbivad
- README olemas

**Täispunktideks (100%):**

- Põhjendused konkreetsed
- Pipeline optimeeritud
- Refleksioon näitab mõistmist

---

## Pedagoogilised märkmed

### Mis töötab hästi

**1. Alusta käsitsi deployment'i näitamisest**
- Õpilased tunnevad seda
- Automatiseerimine on selge lahendus

**2. Lase pipeline'il faili'da**
- See on õpetuslik moment
- "Error = õppimise võimalus"

**3. Live coding, mitte slide'id**
- Näita täpset protsessi
- Tee vigu (tahtlikult)

**4. Peer learning**
- Õpilased õpetavad üksteisele
- Debugging koos

### Väldi neid vigu

**1. Liiga kiiresti kontseptsioonidest**
- Võta aega selgitada MIKS
- Mitte ainult KUIDAS

**2. "See peaks töötama"**
- Pipeline'id failivad PALJU
- See on normaalne
- Debugimine on skill

**3. Production deployment lab'is**
- Liiga riskantne
- Piisab simulatsioonist

**4. Jenkins esimese platvormina**
- Liiga keeruline algajatele
- Alusta GitHub Actions'iga

---

## Viited ja ressursid

### Dokumentatsioon
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitLab CI Docs](https://docs.gitlab.com/ee/ci/) (alternatiiv)
- [Docker Docs](https://docs.docker.com/)

### Pedagoogiline kirjandus
- National Research Council (2000). *How People Learn*
- Vygotsky, L. S. (1978). *Zone of Proximal Development*
- Bloom, B. S. (1956). *Taxonomy of Educational Objectives*

### Industry best practices
- [Martin Fowler - Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
- [The Phoenix Project](https://itrevolution.com/the-phoenix-project/) (DevOps kultuurist)

---

## Kokkuvõte

### Teha

- Alusta lihtsast (hello world)
- Näita reaalseid probleeme (käsitsi deploy)
- Lase õppida vigadest (pipeline fails)
- Kasuta päris tööriistu (GitHub Actions, Docker Hub)
- Fookus mõistmisel, mitte punktidel

### Mitte teha

- Jenkins esimesena (liiga keeruline)
- 10-stage pipeline kohe
- Production deployment (risk)
- Ignoreerida YAML süntaksi (see on raske)

### Võtmesõnum õpilastele

> "CI/CD ei ole lihtsalt tööriist. See on viis mõelda: kuidas tuua kood kasutajateni kiiremini, turvalisemalt ja vähem stressiga."