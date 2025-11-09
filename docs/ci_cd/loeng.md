# CI/CD Alused

**Eeldused:** Git, Docker, Ansible, Terraform, Kubernetes  
**Platvorm:** GitHub Actions  
**Kestus:** 20 minutit

---

## Õpiväljundid

- Selgitad miks CI/CD on vajalik ja millist probleemi see lahendab
- Eristad Continuous Integration ja Continuous Deployment kontseptsioone
- Mõistad GitHub Actions arhitektuuri ja põhikomponente
- Seod CI/CD eelnevate automatiseerimise tööriistadega (Docker, Kubernetes, Terraform)

---

## 1. Suur Pilt: Kõik Kokku (4 min)

### Meie Automatiseerimise Teekond

Selle kursuse jooksul oleme õppinud palju automatiseerimise tööriistu. Iga tööriist lahendas konkreetset probleemi. Git haldab koodi versioone. Docker pakendab rakenduse. Ansible seadistab servereid. Terraform loob infrastruktuuri. Kubernetes orkestreerib konteinereid.

Aga kuidas need kõik koos töötavad? Kes käivitab need protsessid? Kes otsustab millal buildida Docker image? Millal jooksutada Ansible playbook'i? Millal Terraform apply teha?

Vastus on CI/CD.

![Git → CI/CD → Docker → K8s → Production](https://www.container-solutions.com/hs-fs/hubfs/CICD%20Diagram@2x.png?width=1334&name=CICD%20Diagram@2x.png)

### CI/CD Ühendab Kõik

CI/CD on liim mis ühendab kõik meie tööriistad automatiseeritud protsessiks. Vaatame kuidas klassikaline workflow näeb välja:

Arendaja kirjutab koodi ja teeb `git push`. See käivitab GitHub Actions workflow'i. Workflow buildib Docker image'i kasutades Dockerfile'i mida te õppisite. Jooksutab automaatsed testid. Kui testid läbivad, push'ib image Docker Registry'sse. Siis kasutab Terraform'i et veenduda infrastruktuur on õige. Käivitab Ansible playbook'i et seadistada servereid. Lõpuks deploy'ib Kubernetes'iga kasutades kubectl või Helm'i. Kõik see juhtub automaatselt 5-10 minutiga.

Ilma CI/CD-ta peaksite te kõik need sammud käsitsi tegema. Iga kord. Iga deployment'iga. See võtaks tunde ja oleks vigane.

**Kontrollküsimus:** Millised tööriistad meie kursusest CI/CD kasutab?

### Käsitsi vs Automaatne

Vaatame konkreetset näidet. Teil on veebirakendus. Te muudate koodi. Kuidas see jõuab production'i?

**Käsitsi (traditsiooniline):** Arendaja lõpetab koodi. Testib lokaalselt. Teeb `git push`. Siis logib SSH'iga serverisse. Teeb `git pull`. Installib dependencies käsitsi. Buildib rakenduse. Restartib teenuse. Kontrollib kas töötab. Kui midagi valesti, debugib. Proovib uuesti. See võtab 1-3 tundi. Järgmine kord võib protsess olla natuke erinev, sest inimesed unustavad samme või teevad vigu.

**Automaatne (CI/CD):** Arendaja teeb `git push`. GitHub Actions workflow käivitub automaatselt. Buildib, testib, deploy'ib. 10 minutit hiljem on production'is uus versioon. Sama protsess iga kord. Dokumenteeritud YAML failina. Reprodutseeritav. Usaldusväärne.

Kaasaegsed ettevõtted nagu Amazon deploy'ivad 23,000 korda päevas. Netflix 1000 korda päevas. Eestis Bolt ja Wise kasutavad samuti intensiivset CI/CD't. See on võimalik ainult täieliku automatiseerimisega.

**Kontrollküsimus:** Miks käsitsi deployment ei skaleeru kui meeskond kasvab?

### Integration Hell

Teine probleem on "integration hell". Kaks arendajat töötavad eraldi branch'ides kaks nädalat. Mõlemad muudavad koodi, lisavad feature'eid. Siis proovivad merge'ida. Tekivad konfliktid. Kood ei kompileeru. Testid failivad. API'd on muutunud. Docker image'id on erinevad. Kubernetes manifest'id ei ole sünkroonis. Kulub päevi et parandada.

CI/CD lahendab selle: integreeri sageli (iga päev või mitu korda päevas) ja kontrolli automaatselt. Väikesed muudatused on lihtne debugida.

---

## 2. Mis on CI ja CD? (4 min)

### Continuous Integration

Continuous Integration tähendab et iga kord kui arendaja push'ib koodi, süsteem automaatselt buildib ja testib selle. Developer teeb `git push`. GitHub Actions workflow käivitub. Kood buildib automaatselt. Testid jooksevad automaatselt. Kui midagi ebaõnnestub, developer saab teada 5 minutit hiljem. Mitte homme. Mitte järgmisel nädalal. Kohe, kui kontekst on veel meeles.

![ByteByteGo CI/CD Pipeline](https://substackcdn.com/image/fetch/$s_!X8eQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0392cd2-a9b4-4c12-8c12-5250127d7df2_1280x1679.jpeg)

*Allikas: [ByteByteGo - CI/CD Pipeline](https://blog.bytebytego.com/p/ep71-cicd-pipeline-explained-in-simple)*

Vaadake seda diagrammi. See näitab täielikku development lifecycle'i. Developer commits code GitHubi. CI server detekteerib muudatuse. Buildib ja testib automaatselt. Kui testid läbivad, deploy'ib staging keskkonda. Sealt edasi production'i. Kui midagi ebaõnnestub, läheb tagasi developer'ile parandamiseks.

**Kontrollküsimus:** Mis juhtub kui testid failivad CI's?

### Continuous Deployment

Continuous Deployment läheb sammu edasi. Kui kood läbis kõik testid ja kvaliteedikontrollid, deploy automaatselt. Praktikas on kaks varianti mis erinevad viimases sammus.

| Aspekt | Continuous Delivery | Continuous Deployment |
|--------|--------------------|-----------------------|
| **Automatiseerimine** | Kõik peale viimase sammu | Täiesti automaatne |
| **Production deploy** | Inimene vajutab nuppu | Automaatne |
| **Kontroll** | Manual approval | Testide põhjal |
| **Sobib** | Regulated industries, algajad | Mature teams, SaaS |

Enamik ettevõtteid alustab Continuous Delivery'ga kus inimene vaatab üle ja vajutab "deploy" nuppu. Järk-järgult kui usaldus kasvab, liigutakse Continuous Deployment'i poole kus kõik on täiesti automaatne.

### Pipeline Samm-Sammult

ByteByteGo diagramm näitab klassikalist pipeline'i. Developer commits code GitHubi. CI server (meie puhul GitHub Actions) detekteerib muudatuse. Käivitab build'i - kompileerib koodi, loob Docker image'i. Jooksutab testid - unit testid, integration testid. Teatab tulemused developer'ile. Kui kõik OK, deploy'ib artifacts staging keskkonda. Selles keskkonnas jooksevad täiendavad testid - end-to-end testid, performance testid. Kui staging'us kõik töötab, CD süsteem deploy'ib production'i.

Oluline on mõista et kui üks samm ebaõnnestub, järgmised ei käivitu. Kui build fallib, teste ei jooksutata. Kui testid failivad, deployment'i ei toimu. See tagab et ainult töötav kood jõuab production'i.

---

## 3. GitHub Actions (10 min)

### Miks GitHub Actions?

CI/CD platvorme on palju. Jenkins on vanim ja enim kasutatud. GitLab CI on võimas täielik DevOps platvorm. CircleCI on kiire aga kallis. Me õpime GitHub Actions'i mitmel põhjusel.

Esiteks, see on sisse-ehitatud. Kui teil on GitHub repository, teil on GitHub Actions. Zero setup. Ei pea midagi installima, konfigureerima, servereid üles seadma. Teiseks, see on tasuta avalikele projektidele ja piisavalt tasuta privaatsetele (2000 minutit kuus). Kolmandaks, see on lihtne õppida - YAML konfiguratsioon on loetav, dokumentatsioon on hea, näiteid on palju. Neljandaks, suur kogukond - GitHub Marketplace'is on üle 13,000 valmis action'eid. Viies, täielik integratsioon GitHub'iga - saab käivitada workflow'i igal GitHub event'il.

**Kontrollküsimus:** Miks me valime GitHub Actions'i mitte Jenkins'i?

### Kuidas See Töötab?

![GitHub Actions architecture](https://miro.medium.com/v2/resize:fit:720/format:webp/1*OYmkVffRgQ1bioPm0EhNOw.png)

Kui te push'ite koodi GitHubi ja teil on workflow defineeritud, toimub järgmine. GitHub detekteerib et repositooriumis on `.github/workflows/` kaustas YAML fail. Allocate'ib runner'i - loob virtuaalserveri (Ubuntu, Windows või macOS). Execute'ib workflow'i selles serveris - jooksutab kõik job'id ja step'id. Report'ib tulemused - näitab GitHubis kas õnnestus või ebaõnnestus. Clean up - kustutab serveri ära. Te ei pea muretsema serveri haldamise pärast. GitHub teeb kõik.

**Kontrollküsimus:** Mis juhtub pärast seda kui workflow lõpeb?

### Põhikontseptsioonid

GitHub Actions koosneb neljast põhikomponendist mida on oluline eristada.

| Komponent | Kirjeldus | Näide | Jookseb |
|-----------|-----------|-------|---------|
| **Workflow** | Terve protsess | `ci.yml` fail | - |
| **Job** | Üks suur tükk tööd | `build`, `test`, `deploy` | Eraldi serveris |
| **Step** | Üks väike operatsioon | "Checkout code", "Run tests" | Job'i sees järjestikku |
| **Action** | Taaskasutav komponent | `actions/checkout@v3` | Step'i sees |

**Workflow** on kirjeldatud YAML failina `.github/workflows/` kaustas. Iga fail on üks workflow. Repositooriumis võib olla mitu workflow'i - näiteks `ci.yml` testideks, `deploy.yml` deployment'iks, `cron.yml` scheduled task'ideks. Workflow defineerib millal see käivitub (events) ja mida see teeb (jobs).

**Job** on üks suur tükk tööd. Näiteks workflow'is võib olla kolm job'i: `build` kompileerib rakenduse, `test` jooksutab testid, `deploy` paigaldab production'i. Job'id võivad jooksda paralleelselt (kõik samal ajal, kiire) või järjestikku (kui määrad `needs: build`). Oluline on mõista et iga job jookseb eraldi runner'is ehk eraldi serveris. Job'id ei jaga faile ega state'i automaatselt.

**Step** on üks konkreetne operatsioon job'i sees. Step'id jooksevad järjestikku. Kui üks step ebaõnnestub, järgmised ei käivitu. Näiteks `test` job'is võivad olla step'id: lae kood alla, installi Python, installi dependencies, jooksuta testid. Step võib olla kas valmis action (keegi teine kirjutas) või käsurea käsk (`run:`).

**Action** on taaskasutav komponent. Mõelge sellele nagu funktsioonile programmeerimises. Keegi on kirjutanud, testinud, dokumenteerinud, üles laadinud GitHub Marketplace'i. Sina lihtsalt kasutad. Näiteks `actions/checkout@v3` laeb koodi alla, `actions/setup-python@v4` installib Python'i, `docker/build-push-action@v4` buildib ja push'ib Docker image'i.

**Kontrollküsimus:** Mis vahe on job'il ja step'il?

### Runner

Runner on virtuaalserver kus workflow jookseb. GitHub pakub kolme tüüpi runner'eid: Ubuntu Linux (kõige levinum, kiire), Windows (kui vajad Windows'i keskkonda) ja macOS (kui vajad macOS'i, näiteks iOS app build). Runner'is on juba palju tööriistu installitud - Git, Docker, Node.js, Python, Ruby, Java, AWS CLI, Azure CLI ja palju muud. See tähendab et enamasti ei pea te midagi installima, saate kohe kasutada.

### Events ja Triggers

Workflow peab teadma millal käivituda. Kaks kõige tavalisem event'i on `push` ja `pull_request`.

**push event** käivitub kui keegi push'ib koodi. Saate määrata konkreetseid branch'e: `branches: [ main, develop ]`. See tähendab et workflow jookseb ainult kui push'itakse nendesse branch'idesse, mitte teistesse.

**pull_request event** käivitub kui keegi teeb pull request'i. See on väga oluline. Enne kui kood merge'itakse main'i, jooksevad testid automaatselt. Kui testid failivad, ei saa merge'ida. See tagab et ainult testitud kood läheb main branch'i.

### Lihtne Näide

Vaatame ühte väga lihtsat näidet et mõista struktuuri:

```yaml
name: CI

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

Selles näites on workflow nimega CI mis käivitub kui keegi push'ib main branch'i. On üks job nimega test mis jookseb Ubuntu serveris. Job koosneb neljast step'ist. Esimene step kasutab valmis action'i `checkout` et laadida kood alla. Teine step kasutab action'i `setup-python` et installida Python 3.9. Kolmas step käivitab käsu et installida dependencies. Neljas step jooksutab testid pytest'iga. Kui mõni step ebaõnnestub, workflow stopib ja GitHub näitab punast X'i.

See on kõik! 12 rida YAML'i ja teil on töötav CI pipeline.

**Kontrollküsimus:** Kus see fail peab repositooriumis olema?

### GitHub Actions Kasutajaliides

![GitHub Actions workflow](https://docs.github.com/assets/cb-34427/images/help/actions/reusable-workflows-ci-cd.png)

GitHubis iga repositooriumi üleval on "Actions" tab. Kui klõpsate sinna, näete kõiki workflow'e. Näete millised on jooksmas (kollane ring), millised õnnestusid (roheline checkmark), millised ebaõnnestusid (punane X). Kui klõpsate workflow'i peale, näete detaile - kõiki job'e, iga job'i kõiki step'e, iga step'i output'i ja loge. Kui midagi ebaõnnestus, näete täpset error message'it ja saate debugida.

Pull request'i juures näete check'e. Kas "All checks have passed" rohelisega või "Some checks failed" punasega. Kui branch protection on seadistatud, ei saa merge'ida enne kui kõik check'id on rohelised. See tagab et ainult testitud kood läheb main branch'i.

---

## 4. Teised CI/CD Platvormid (2 min)

GitHub Actions pole ainus. Lühike ülevaade alternatiividest.

**GitLab CI/CD** sobib kui kasutate GitLab'i või vajate self-hosted lahendust. See on täielik DevOps platvorm mis sisaldab Git'i, CI/CD'd, Container Registry'd, monitoring'u. Tasuta self-hosted variant. Väga võimas. Kasutavad CERN, Siemens, paljud Euroopa ettevõtted.

**Jenkins** on vanim (2011) ja enim kasutatud CI/CD tööriist. Üle 1800 plugina. Täielik kontroll. Tasuta. Aga vana kasutajaliides ja raske setup. Ainult self-hosted. Kasutavad pangad ja suured enterprise ettevõtted legacy süsteemidega.

**Bitbucket Pipelines** sobib kui kasutate Atlassian'i tooteid (Jira, Confluence). Hea integratsioon nendega.

**CircleCI** on kiire SaaS platvorm. Väga hea parallelism. Aga kallis. Sobib kui kiirus on kriitiline ja saate tasuda.

| Platvorm | Kasuta Kui | Hind | Setup |
|----------|-----------|------|-------|
| **GitHub Actions** | Kasutad GitHub'i | Tasuta/Odav | Zero |
| **GitLab CI** | Vajad self-hosted | Tasuta/Kallis | Keskmine |
| **Jenkins** | Enterprise, kontroll | Tasuta | Raske |
| **Bitbucket** | Atlassian stack | Kallis | Lihtne |
| **CircleCI** | Kiirus kriitiline | Kallis | Lihtne |

Praktikas 90% juhtudest: kui kasutate GitHub'i, valige GitHub Actions. Kui kasutate GitLab'i, valige GitLab CI. Valik on lihtne.

---

## Kokkuvõte

### Põhipunktid

CI/CD ühendab kõik meie kursuse tööriistad automatiseeritud protsessiks. Git haldab versioone. Docker pakendab rakenduse. CI/CD orkestreerib kogu workflow'i automaatselt. Käsitsi deployment mis võtab 2-3 tundi muutub automaatseks protsessiks mis võtab 10 minutit. Deployment 1 kord kuus muutub deployment'iks 10-100 korda päevas.

GitHub Actions koosneb neljast komponendist. Workflow on terve protsess kirjeldatud YAML failina. Job on üks suur tükk tööd mis jookseb eraldi serveris. Step on üks väike operatsioon job'i sees. Action on taaskasutav komponent mida keegi teine kirjutas. Runner on GitHub'i virtuaalserver kus kõik see jookseb.

Klassikaline pipeline näeb välja nii: Developer push'ib koodi. Build käivitub automaatselt. Testid jooksevad automaatselt. Kui testid läbivad, deploy'ib staging'u. Sealt edasi production'i. Kogu protsess dokumenteeritud, reprodutseeritav, usaldusväärne.

### Järgmised Sammud

Järgmine kord on labor. Loome oma projekti CI/CD pipeline'i. Seadistame GitHub Actions'i. Kirjutame workflow faili. Ühendame Docker, testid, deployment. Vaatame Actions tab'is tulemust. Õpime debugima kui midagi läheb valesti.

---

## Kontrollküsimused

1. Millised tööriistad meie kursusest CI/CD kasutab?
2. Miks käsitsi deployment ei skaleeru?
3. Mis juhtub kui testid failivad CI's?
4. Miks me valime GitHub Actions'i?
5. Mis juhtub pärast seda kui workflow lõpeb?
6. Mis vahe on job'il ja step'il?
7. Kus workflow fail peab olema?

---

## Ressursid

**Dokumentatsioon:**
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [ByteByteGo - CI/CD Pipeline](https://blog.bytebytego.com/p/ep71-cicd-pipeline-explained-in-simple)

**Õppematerjalid:**
- [GitHub Skills](https://skills.github.com/)
- [GitHub Beginner's Guide](https://github.blog/developer-skills/github/a-beginners-guide-to-ci-cd-and-automation-on-github/)

---

**Järgmine kord:** Labor - seome kokku Git + Docker + Kubernetes + CI/CD
