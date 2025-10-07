# Lõpuprojekt: DevOps Integratsioon

**Eeldused:** Docker, Kubernetes, Terraform, Ansible, CI/CD põhiteadmised  
**Platvorm:** Platvormist sõltumatu (teoreetiline raamistik)

---

## Õpivälјundid

Pärast seda loengut oskate:

- Mõistab DevOps projektide arhitektuurseid põhimõtteid ja komponente
- Võrdleb erinevate tööriistakomplektide sobivust projektitüüpide jaoks
- Selgitab tehniliste otsuste tegemise protsessi ja dokumenteerimist
- Eristab projekti etappide eesmärke ja tulemusi
- Planeerib terviklikku DevOps infrastruktuuri integreerides mitut tööriista

---

## 1. Lõpuprojekti Kontseptsioon

Lõpuprojekt on integreeritav praktiline töö, kus kombineeritakse mitmeid DevOps tööriistu ühes terviklikus süsteemis. Erinevalt eraldiseisvast kodutööst või laborist demonstreerib lõpuprojekt süsteemset lähenemist, kus iga komponent täidab spetsiifilist rolli suuremas arhitektuuris.

### Integratsiooni Põhimõte

DevOps keskkond koosneb omavahel seotud tööriistadest, mis moodustavad tehnoloogiapinna (technology stack). Näiteks ei eksisteeri Kubernetes üksi - see vajab konteinerite loomist (Docker), infrastruktuuri provisioning'ut (Terraform), konfiguratsioonihaldust (Ansible) ja pidevat integreerimist (CI/CD pipeline). Lõpuprojekt peegeldab seda reaalset integratsiooni.

Projekti peamine väärtus seisneb tehniliste otsuste dokumenteerimises ja põhjendamises. Tööandjad hindavad võimet selgitada miks konkreetne lahendus valiti, millised olid alternatiivid ja millised kompromissid tehti. Seda oskust arendatakse läbi projekti dokumentatsiooni.

### Miks On See Oluline?

Professionaalses keskkonnas ei rakendata kunagi ainult ühte tööriista eraldiseisvalt. Iga DevOps lahendus on süsteem, kus komponendid peavad omavahel suhtlema, andmeid vahetama ja ühtselt toimima. Lõpuprojekt simuleerib seda reaalset keskkonda kontrollitud õppetingimuses.

---

## 2. Projekti Arhitektuurimustrid

### Komponentide Tüübid

DevOps projekti arhitektuur jaguneb tavaliselt kolmeks põhikihiks: rakenduskiht (application layer), infrastruktuurikiht (infrastructure layer) ja operatsioonikiht (operations layer).

**Rakenduskiht** sisaldab äriloogikat ja kasutajaliidest. See võib olla monoliitiline rakendus või mikroteenuste arhitektuur. Monoliitiline lähenemine on lihtsam hallata väikese meeskonna puhul, samas mikroteenused pakuvad paremat skaleeruvust ja isolatsiooni. Valik sõltub projekti suurusest ja meeskonna kogemusest.

**Infrastruktuurikiht** hõlmab servereid, võrke, andmebaase ja salvestusressursse. Kaasaegne lähenemine kasutab Infrastructure as Code (IaC) põhimõtteid, kus infrastruktuur kirjeldatakse koodina ning provisioning on automatiseeritud. Terraform ja Ansible on selle kihi peamised tööriistad.

**Operatsioonikiht** vastutab jälgimise (monitoring), logimine (logging), varundamise (backup) ja reageerimise (alerting) eest. Produktsioonikeskkonnas on see kriitiline, kuid õppeprojektis sageli alahinnatud. Prometheus ja Grafana moodustavad standardse monitoringu stack'i.

### Arhitektuursed Otsused

Iga projekti puhul tuleb teha põhilised arhitektuursed valikud, mis mõjutavad kogu edaspidist arendust.

**Konteineriseerimise vs Virtualiseerimise Valik**

Konteinerid (Docker) ja virtuaalmasinad (VMs) lahendavad sarnast probleemi erinevalt. Konteinerid jagavad host operatsioonisüsteemi kerneli, mis teeb nad kergemaks ja kiiremaks käivituda. Virtuaalmasinad sisaldavad täielikku OS'i, pakkudes tugevamat isolatsiooni aga suurema ressursikasutuse hinnaga.

| Aspekt | Konteinerid (Docker) | Virtuaalmasinad |
|--------|---------------------|-----------------|
| Käivitusaeg | Sekundid | Minutid |
| Ressursikasutus | Madal (MB-d) | Kõrge (GB-d) |
| Isolatsioon | OS-level | Hardware-level |
| Kasutusjuht | Mikroteenused, CI/CD | Legacy rakendused, täielik OS vajalik |

**Orkestreerimise Valik**

Kui konteinerid on valitud, tekib küsimus nende haldamisest suuremas mahus. Kubernetes on industry standard, pakkudes automaatset scaling'ut, self-healing võimekust ja deklaratiivset konfiguratsiooni. Docker Swarm on lihtsam alternatiiv väiksematele projektidele, kuid piiratud funktsionaalsusega.

**Infrastruktuuri Halduse Valik**

Terraform ja Ansible täidavad erinevaid rolle, kuigi mõlemat võib kasutada infrastruktuuri haldamiseks. Terraform on spetsialiseerunud infrastruktuuri provisioning'ule - ressursside loomisele pilves või andmekeskuses. Ansible fookuseb konfiguratsioonihaldusele - olemasolevate serverite seadistamisele ja rakenduste deploy'imisele.

| Aspekt | Terraform | Ansible |
|--------|-----------|---------|
| Peamine eesmärk | Infrastruktuuri provisioning | Konfiguratsioonihaldus |
| Lähenemisviis | Deklaratiivne (HCL) | Protseduuriline (YAML) |
| State management | Keskne state fail | Stateless |
| Idempotentsus | Sisseehitatud | Playbook disaini küsimus |
| Kasutusjuht | Cloud ressursside loomine | Serverite konfigureerimine |

Professionaalses keskkonnas kasutatakse neid sageli koos: Terraform loob infrastruktuuri (VMs, võrgud, load balancers), Ansible konfigreerib neid servereid (installib software, seadistab teenuseid).

---

## 3. Tööriistakomplektide Valik

Lõpuprojekti jaoks valitakse 2-3 tööriista, mis moodustavad koherentse stack'i. Järgnevad kombinatsioonid on tööstuses levinud ja hästi dokumenteeritud.

### Kombinatsioon A: Konteinerite Orkestreerimise Stack

**Tööriistad:** Docker + Kubernetes + CI/CD

See kombinatsioon esindab kaasaegset cloud-native lähenemist. Docker pakub konteinerite standardit, Kubernetes haldab nende elutsüklit produktsioonis, CI/CD automatiseerib build ja deploy protsessi.

**Arhitektuurne Ülevaade:**
1. Arendaja pushib koodi Git repository'sse
2. CI/CD pipeline (GitHub Actions, GitLab CI) käivitub automaatselt
3. Pipeline ehitab Docker image'i ja pushib registry'sse
4. Kubernetes tõmbab uue image'i ja deploy'ib see
5. Kubernetes jälgib pod'ide tervist ja taaskäivitab vajadusel

**Sobivus:** Mikroteenuste arhitektuurid, cloud deployment, meeskonnad kellel on Kubernetes kogemus.

**Väljakutsed:** Kubernetes'el on järsk õppimiskõver. YAML konfiguratsiooni keerukus kasvab kiiresti. Local development erineb production keskkonnast.

### Kombinatsioon B: Infrastruktuuri Automatiseerimise Stack

**Tööriistad:** Terraform + Ansible + CI/CD

See kombinatsioon fookuseerub infrastruktuuri kui koodi (IaC) põhimõtetele. Terraform loob ja haldab cloud ressursse, Ansible konfigreerib servereid, CI/CD automatiseerib deployment'i.

**Arhitektuurne Ülevaade:**
1. Terraform moodulid defineerivad infrastruktuuri (VMs, võrgud, turvalisus)
2. Terraform apply käsk provisioning'ub ressursid cloud'is
3. Ansible playbook'id konfigreerivad servereid (installivad software, seadistavad teenuseid)
4. CI/CD pipeline käivitab Terraform ja Ansible automaatselt
5. Rakendus deploy'itakse Ansible kaudu

**Sobivus:** Traditsiooniline server-based arhitektuur, infrastruktuuri haldamise rõhk, multi-cloud projektid.

**Väljakutsed:** State management Terraform'is vajab hoolikat planeerimist. Ansible playbook'ide idempotentsus vajab testimist. Infrastruktuuri muudatused võivad olla destruktiivsed.

### Kombinatsioon C: Konteinerite Arenduse Stack

**Tööriistad:** Docker + CI/CD + Testing

See on lihtsustatud stack neile, kes soovivad fokuseeruda konteinerite arendusele ja CI/CD praktikatele ilma orkestreerimise keerukuseta.

**Arhitektuurne Ülevaade:**
1. Rakendus arendatakse Docker konteinerites (consistency dev ja prod vahel)
2. CI/CD pipeline ehitab ja testib image'eid
3. Automatiseeritud testid käitatakse konteinerites
4. Edukad build'id push'itakse registry'sse
5. Deploy võib olla lihtne (Docker Compose) või managed (AWS ECS, Azure Container Instances)

**Sobivus:** Ühe rakenduse projektid, arendusprotsessi automatiseerimine, meeskonnad kes ei vaja täielikku orkestreerimist.

**Väljakutsed:** Piiratud scaling võimalused ilma orkestreerijata. Production deployment nõuab lisatööriistu. Networking võib olla keeruline multi-container setup'is.

### Kombinatsioon D: Observability Stack

**Tööriistad:** Kubernetes + Prometheus + Grafana

See kombinatsioon rõhutab operatsioonide poolt - kuidas jälgida, et süsteem töötab. Prometheus kogub meetrikaid, Grafana visualiseerib neid, Kubernetes on platvorm mida monitoritakse.

**Arhitektuurne Ülevaade:**
1. Kubernetes töötab rakenduste platvormina
2. Prometheus scrape'ib meetrikaid Kubernetes pod'idest
3. Grafana dashboard'id visualiseerivad meetrikaid
4. Alertmanager saadab hoiatusi probleemide korral
5. Rakendused ekspordiivad custom meetrikaid

**Sobivus:** Operations-focused projektid, site reliability engineering (SRE), meeskonnad kes soovivad süvendada jälgimise oskusi.

**Väljakutsed:** Prometheus query language (PromQL) õppimine. Grafana dashboard'ide disain. Alert'ide häälestamine false positive'te vältimiseks.

---

## 4. Projekti Tüübid ja Sobivus

### Veebirakenduse Projekt

Traditsiooniline veebirakendus koosneb kolmest põhikihist: frontend (kasutajaliides), backend (äriloogika ja API) ning andmebaas (andmete püsivus). See arhitektuur on hästi mõistetav ja dokumenteeritud.

**Tehnilised Aspektid:**
- Frontend võib olla staatiline (HTML/CSS/JS) või raamistiku-põhine (React, Vue)
- Backend pakub REST või GraphQL API't
- Andmebaas võib olla relatsioonne (PostgreSQL, MySQL) või NoSQL (MongoDB)
- Session management ja autentimine on vajalikud

**DevOps Integratsioon:**
- Iga komponent on eraldi Docker konteiner
- Kubernetes deploy'ib ja skaleerib komponente sõltumatult
- CI/CD pipeline testib ja deploy'ib automaatselt
- Monitoring jälgib latency't ja error rate'e

**Näide Arhitektuurist:**
```
[Kasutaja] → [Load Balancer] → [Frontend Pod'id]
                                      ↓
                            [Backend API Pod'id]
                                      ↓
                            [Database Service]
                                      ↓
                            [Persistent Volume]
```

Frontend pod'id serveerivad staatilist sisu, backend pod'id töötlevad API päringuid, database service pakub püsivat salvestust läbi persistent volume'i.

### API Teenuse Projekt

REST API teenus on backend-focused projekt, mis eksponeerib andmeid ja funktsionaalsust HTTP endpoint'ide kaudu. Frontend puudub, fookus on API disainil ja dokumentatsioonil.

**Tehnilised Aspektid:**
- RESTful endpoint'id CRUD operatsioonide jaoks
- OpenAPI/Swagger dokumentatsioon
- Autentimine läbi API key'de või JWT
- Rate limiting ja throttling
- Versioonimine (v1, v2 endpoint'id)

**DevOps Integratsioon:**
- API konteinerid deploy'itakse Kubernetes'es
- API Gateway haldab routing'ut ja rate limiting'ut
- Andmebaas on HA (High Availability) konfiguratsioonis
- Monitoring mõõdab latency't endpoint'ide kaupa

**API Versioonimine:**

API versioonimise strateegiad võimaldavad muudatusi ilma olemasolevaid kliente rikkumata:

| Strateegia | Näide | Plussid | Miinused |
|-----------|-------|---------|----------|
| URL path | `/v1/users`, `/v2/users` | Selge, lihtne routida | URL'id muutuvad |
| Query parameter | `/users?version=1` | URL stable | Vähem nähtav |
| Header | `Accept: application/vnd.api.v1` | REST'ile truuem | Keerulisem testida |

### Monitoring Dashboard Projekt

Monitoring dashboard visualiseerib süsteemi meetrikaid reaalajas. See projekt on operations-focused, rõhutades observability't ja alerting'ut.

**Tehnilised Aspektid:**
- Prometheus kogub meetrikaid exporteritelt
- Grafana dashboard'id visualiseerivad andmeid
- Alertmanager haldab hoiatusi
- Time-series andmebaas (Prometheus built-in)

**DevOps Integratsioon:**
- Prometheus deploy'itakse Kubernetes'es
- Service discovery leiab automaatselt target'id
- Grafana import'ib eelseadistatud dashboard'e
- Alert'id saadetakse Slack'i või email'i

**Meetrikate Tüübid:**

| Tüüp | Näide | Kasutusjuht |
|------|-------|-------------|
| Counter | HTTP requests kokku | Kasvav väärtus, resetitakse restart'il |
| Gauge | CPU kasutus % | Hetke väärtus, võib kasvada või kahaneda |
| Histogram | Request latency distribution | Väärtuste jaotus buckets'is |
| Summary | Request latency percentiles | Kvantiiilid (p50, p95, p99) |

---

## 5. Projekti Elutsükkel

### Planeerimise Faas

Planeerimise käigus defineeritakse projekti ulatus (scope), arhitektuur ja tehnilised otsused. Puudulik planeerimine toob kaasa hilisemaid refaktorimisi ja ajakulu.

**Arhitektuuri Dokumenteerimine:**

Arhitektuuridiagramm visualiseerib süsteemi komponente ja nende vahelisi suhteid. See ei pea olema professionaalne diagramm - lihtne kastide-ja-nooltega visand on piisav kui see kommunikeerib struktuuri.

Komponentide kirjeldus peaks sisaldama:

- Komponendi eesmärk ja vastutus
- Kasutatavad tehnoloogiad ja versioonid
- Sõltuvused teistest komponentidest
- Kommunikatsiooni protokollid (HTTP, gRPC, message queue)
- Ressursinõuded (CPU, RAM, storage)

**Tehniliste Otsuste Dokumenteerimine:**

Iga oluline tehniline valik vajab dokumenteerimist Architecture Decision Record (ADR) formaadis:
```
## Otsus: PostgreSQL kui Primaarset Andmebaas

**Kontekst:**
Rakendus vajab relatsioonset andmebaasi ACID garantiidega.
Peamised kasutusjuhtumid on kasutajate ja tellimuste haldamine.

**Valikud:**
1. PostgreSQL - avatud lähtekoodiga, ACID, JSON tugi
2. MySQL - laialdaselt kasutatud, lihtsam
3. MongoDB - NoSQL, paindlik skeem

**Otsus:**
Valime PostgreSQL'i.

**Põhjendus:**
- ACID garantii on kriitiline tellimuste jaoks
- JSON tugi võimaldab paindlikkust ilma NoSQL'i liikumata
- Parem full-text search kui MySQL'il
- Rikkalikkud data tüübid (arrays, hstore)

**Tagajärjed:**
- Vajame PostgreSQL ekspertiisi meeskonnas
- Backup strateegia peab arvestama WAL'iga
- Replication seadistamine on keerulisem kui MongoDB'l
```

### Arenduse Faas

Arendus toimub iteratiivselt, alustades lihtsaimast komponendist ja liikudes järk-järgult keerukamate poole. Iga iteratsioon peaks lõppema working state'iga, mida saab demonstreerida.

**Iteratiivne Lähenemine:**

Esimene iteratsioon loob minimaalse toimiva süsteemi (MVP - Minimum Viable Product). See võib olla lihtsalt Docker konteiner, mis töötab lokaalselt. Järgmised iteratsioonid lisavad kihte: andmebaas, CI/CD, Kubernetes, monitoring.

**Versioonikontrolli Praktikad:**

Git workflow peaks olema struktureeritud:

- `main` branch on alati deploy'itav
- `develop` branch on aktiivse arenduse baas
- Feature branch'id arendatakse `develop`'ist
- Pull request'id läbivad code review'
- Merge toimub alles peale testide läbimist

Commit messages peaksid olema kirjeldavad:
```
feat: Lisa Prometheus monitoring support

- Configura /metrics endpoint
- Ekspordib HTTP request counter'id
- Lisab custom business metrics
- Dokumenteerib saadaolevad metrics README's

Closes #42
```

**Testimise Strateegiad:**

Testide püramiid näitab, kui palju milliseid teste peaks olema:
```
        /\
       /E2E\          Vähe - aeglased, haaravad
      /------\
     /Integr.\       Mõõdukalt - komponendid koos
    /----------\
   /Unit Tests \     Palju - kiired, isoleeritud
  /--------------\
```

Unit testid kontrollivad üksikuid funktsioone, integration testid kontrollivad komponentide koostööd, end-to-end testid kontrollivad tervet süsteemi kasutaja perspektiivist.

### Viimistlemise Faas

Viimistlemine hõlmab testimist, dokumentatsiooni täiendamist ja demo ettevalmistamist. See ei ole "optional" faas, vaid oluline osa professionaalsest projektist.

**Dokumentatsiooni Viimistlemine:**

README.md peaks vastama kolmele põhiküsimusele:

1. Mis see projekt on? (kirjeldus, eesmärk)
2. Kuidas seda käivitada? (sammud nullist töötava süsteemini)
3. Kuidas seda kasutada? (API dokumentatsioon, UI juhend)

Deployment guide peaks olema reprodutseeritav - keegi teine peaks seda järgides saama identsed tulemused. Serteerimata eeldused (nt "sul peab olema kubectl seadistatud") on levinud viga.

**Demo Ettevalmistus:**

Efektiivne demo järgib struktuuri:

1. Kontekst (mis probleem lahendatakse)
2. Arhitektuuri ülevaade (slide'id või diagramm)
3. Live demo (töötav süsteem)
4. Koodielementide selgitus (huvitavad lahendused)
5. Lessons learned (mida õppisite, mis oli keeruline)

Demo ajal võib tekkida tehnilisi probleeme. Varuplaan:

- Salvestatud video backup kui live demo failib
- Screenshot'id kriitilisest funktionaalsusest
- Kohalik versioon kui cloud access failib

---

## 6. Dokumentatsiooni Standardid

### README Struktuuri Standard

README on projekti esimene kontaktpunkt. Selle kvaliteet mõjutab kogu projekti tajutavat professionaalsust.

**Minimaalselt Vajalik Sisu:**
```markdown
# Projekti Nimi

Ühe lause kirjeldus, mis selgitab projekti eesmärki.

## Ülevaade

2-3 lõiku, mis kirjeldab:

- Mis probleem see lahendab
- Kes on sihtkasutajad
- Millised on põhilised featured

## Arhitektuur

Diagramm ja kirjeldus põhikomponentidest.

## Kiire Alustamine

### Eeltingimused
- Docker 24.0+
- kubectl 1.28+
- Terraform 1.6+

### Installimine
\`\`\`bash
git clone [repo-url]
cd project
./scripts/setup.sh
\`\`\`

### Käivitamine
\`\`\`bash
docker-compose up
\`\`\`

Rakendus on kättesaadav: http://localhost:3000

## Dokumentatsioon

- [Arhitektuur](docs/architecture.md)
- [API Dokumentatsioon](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## Arendamine

### Koodi Struktuur
[Koodipuu selgitus]

### Testide Käivitamine
\`\`\`bash
npm test
\`\`\`

## License
[License info]
```

### Arhitektuuri Dokumentatsiooni Standard

Arhitektuuridokument selgitab süsteemi struktuuri ja põhjendab disainiotsuseid. See on tehnilisem dokument kui README.

**Komponendid Üksikasjad:**

Iga suurem komponent vajab kirjeldust:
```markdown
### Frontend Service

**Tehnoloogiad:** React 18, TypeScript, Vite
**Vastutus:** Kasutajaliidese renderdamine, state management
**API Suhtlus:** REST API backend'iga
**Deployment:** Nginx container Kubernetes'es

**Environment Variables:**
- `API_URL` - Backend API endpoint
- `AUTH_DOMAIN` - Autentimise provider

**Ressursinõuded:**
- CPU: 100m request, 500m limit
- Memory: 128Mi request, 512Mi limit

**Health Check:**
- Readiness: `GET /health`
- Liveness: `GET /`
```

**Andmevoo Dokumenteerimine:**

Andmevoo diagramm näitab kuidas info liigub läbi süsteemi:
```
User Request
    ↓
[Load Balancer]
    ↓
[Frontend Pod] → [Static Assets Cache]
    ↓
[API Gateway]
    ↓ (Authentication)
[Auth Service]
    ↓ (Authorized)
[Backend API Pod]
    ↓ (Query)
[Database Master]
    ↓ (Replication)
[Database Replica]
```

Iga noole juurde peaks kirjeldama:

- Protokoll (HTTP, gRPC, SQL)
- Autentimine (JWT, API key, cert)
- Error handling (retry, fallback, circuit breaker)

### Deployment Juhendi Standard

Deployment guide peab võimaldama reprodutseeritavat deployment'i nullist working state'ini.

**Keskkonna Ettevalmistus:**
```markdown
## Keskkonna Seadistamine

### 1. Cloud Provider Setup

AWS näitel:
\`\`\`bash
# Loo IAM kasutaja Terraform jaoks
aws iam create-user --user-name terraform-deployer

# Anna vajalikud õigused
aws iam attach-user-policy \
  --user-name terraform-deployer \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Genereeri access key
aws iam create-access-key --user-name terraform-deployer
\`\`\`

Salvesta access key ja secret key keskkonna muutujatesse:
\`\`\`bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
\`\`\`

### 2. Kubernetes Cluster Loomine

\`\`\`bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
\`\`\`

Oodatav tulemus:

- EKS cluster 3 node'iga
- VPC koos subnet'idega
- Security group'id
- IAM role'id

Keskkonna konfiguratsioon kubectl jaoks:
\`\`\`bash
aws eks update-kubeconfig --name production-cluster
kubectl get nodes
\`\`\`

Peaks näitama 3 node'i Ready state'is.
```

---

## 7. Kvaliteedi Kriteeriumid

### Koodi Kvaliteedi Mõõtmine

Koodi kvaliteet ei ole subjektiivne tunne - seda saab mõõta konkreetsete kriteeriumidega.

**Testimise Katvus:**

Test coverage näitab, kui palju koodist on testidega kaetud. Industry standard on minimaalselt 80% statement coverage, aga see ei garanteeri kvaliteeti - saab kirjutada kasutuid teste mis lihtsalt käivitavad koodi.

Tähtsam on test coverage kvaliteet:

- Critical path'id on kaetud (happy path ja error case'id)
- Edge case'id on testitud (null, empty, max values)
- Integration point'id on kaetud (API calls, database queries)

**Linting ja Code Style:**

Automaatne linting tagab ühtse code style'i:
```yaml
# .eslintrc.yml näide
rules:
  indent: [error, 2]
  quotes: [error, single]
  semi: [error, always]
  no-unused-vars: error
  no-console: warn
```

Pre-commit hook'id jõustavad neid reegleid:
```bash
# .git/hooks/pre-commit
#!/bin/sh
npm run lint
npm run test
```

**Dependency Management:**

Dependency vulnerabilities on tõsine turvaoht. Automaatne skaneerimine:
```yaml
# Dependabot config
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
```

### Infrastruktuuri Kvaliteedi Mõõtmine

**Terraform Kvaliteedikontroll:**

Terraform kood peaks järgima best practices:
```hcl
# Hea: Kasuta module'eid reusability jaoks
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = var.vpc_name
  cidr = var.vpc_cidr
}

# Halb: Kõik otse main.tf'is
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  # ... 50 rida konfiguratsioon
}
```

Terraform validation:
```bash
terraform fmt -check     # Kontrolli formatting
terraform validate       # Kontrolli syntax
tflint                   # Linting
tfsec                    # Security scanning
```

**Kubernetes Manifest'ide Kvaliteet:**
```yaml
# Hea: Resource limits määratud
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "512Mi"
        cpu: "500m"

# Halb: Limitid puuduvad (võib consumeerida kogu node)
```

Kubernetes manifest validation:
```bash
kubectl apply --dry-run=client -f manifest.yaml
kubeval manifest.yaml
kube-score manifest.yaml
```

### Dokumentatsiooni Kvaliteedi Mõõtmine

**README Täielikkus:**

Checklist hea README jaoks:
- [ ] Projekti kirjeldus esimeses lõigus
- [ ] Installimise sammud nullist working state'ini
- [ ] Prerequisite'id versiooni numbritega
- [ ] Troubleshooting sektsioon common errors jaoks
- [ ] Architecture diagram või link architecture.md'ile
- [ ] Contributing guidelines kui open-source

**API Dokumentatsiooni Standard:**

OpenAPI/Swagger spetsifikatsioon peaks olema genereeritud koodist, mitte käsitsi kirjutatud:
```javascript
// Code comment becomes API documentation
/**
 * @swagger
 * /users:
 *   get:
 *     summary: Returns list of users
 *     responses:
 *       200:
 *         description: Successful response
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/User'
 */
app.get('/users', getUsers);
```

---

## 8. Levinud Väljakutsed ja Lahendused

### Projekti Scope Creep

Scope creep on nähtus, kus projekti ulatus kasvab planeeritust suuremaks. See on üks peamisi põhjuseid, miks projektid hilinevad või jäävad poolikuks.

**Ennetamine:**

Defineeri selgelt Minimum Viable Product (MVP):
- Millised featured on absolutely essential?
- Millised on nice-to-have?
- Millised on future enhancements?

Kirjuta MVP nõuded enne kodeerimist. Iga uus feature idee küsimusega: "Kas see on vajalik MVP jaoks?"

**Ravi:**

Kui scope juba kasvanud:
1. Prioritiseeri featured MoSCoW meetodil (Must have, Should have, Could have, Won't have)
2. Freezie scope konkreetsel kuupäeval
3. Liiguta nice-to-have featured "Phase 2" listi

### Integration Issues

Komponentide integreerimine on sage pain point. Lokaalselt töötab kõik, aga koos panemine on keeruline.

**API Contract Testing:**

Consumer-driven contract testing tagab, et provider ja consumer on sync'is:
```javascript
// Consumer defineerib mida ta ootab
describe('User API contract', () => {
  it('returns user with expected fields', async () => {
    const response = await api.getUser(1);
    expect(response).toHaveProperty('id');
    expect(response).toHaveProperty('email');
    expect(response).toHaveProperty('name');
  });
});
```

Provider käivitab need testid oma koodis veendumaks, et ta täidab contract'i.

**Service Mesh'id:**

Service mesh (nt Istio, Linkerd) abstraheerib networking'u service-to-service communication jaoks:
```yaml
# Istio VirtualService - traffic routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        user-type:
          exact: tester
    route:
    - destination:
        host: reviews
        subset: v2  # Testers näevad v2
  - route:
    - destination:
        host: reviews
        subset: v1  # Teised näevad v1
```

### State Management Issues

Terraform state on critiline - selle kaotamine või corruption tähendab, et Terraform ei tea enam mis infrastruktuur on deployed.

**Remote State Backend:**

Kasuta remote state backend'i alati:
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-locks"  # State locking
    encrypt        = true
  }
}
```

DynamoDB table state locking jaoks ennetab concurrent modifications:
```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

**State Backup:**

Automatiseeri state backup:
```bash
#!/bin/bash
# backup-terraform-state.sh
DATE=$(date +%Y%m%d-%H%M%S)
aws s3 cp \
  s3://my-terraform-state/production/terraform.tfstate \
  s3://my-terraform-state-backups/production/terraform.tfstate.$DATE
```

### Monitoring Blind Spots

Monitoring on sageli afterthought, aga produktsioonis see on kriitilise tähtsusega.

**Golden Signals:**

Google SRE raamat defineerib 4 golden signals:

1. **Latency** - Kui kaua võtab request?
2. **Traffic** - Kui palju request'e tulebüsteemile?
3. **Errors** - Kui palju request'e failib?
4. **Saturation** - Kui täis on süsteemi ressursid?

Prometheus queries nende jaoks:
```promql
# Latency (95th percentile)
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[5m]))

# Traffic (requests per second)
rate(http_requests_total[1m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) /
rate(http_requests_total[5m])

# Saturation (CPU usage)
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Alert Fatigue:**

Liiga palju alert'e on sama halb kui mitte ühtegi - inimesed hakkavad ignoreerima.

Alert'ide põhimõtted:
- Alert ainult actionable problems korral
- Alert severity järgi urgency't (critical, warning, info)
- Dokumenteeri iga alert'i runbook'is "mida teha?"
```yaml
# Prometheus AlertManager rule
groups:
- name: example
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 10m  # Ainult kui kestab 10+ minutit
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }}%"
      runbook: "https://wiki.company.com/runbooks/high-error-rate"
```

---

## Kokkuvõte

Lõpuprojekt on DevOps teadmiste integreerimise praktiline demonstratsioon. Projekti väärtus seisneb mitte ainult töötavas süsteemis, vaid tehniliste otsuste dokumenteerimises ja põhjendamises. Iga arhitektuurne valik, tööriista valik ja design decision peaks olema argumenteeritud alternatiivide võrdluse ja konteksti alusel.

Professionaalses keskkonnas hinnatakse võimet selgitada miks konkreetne lahendus valiti, millised olid trade-off'id ja millised olid alternatiivid. Lõpuprojekti dokumentatsioon on see, mis demonstreerib seda mõtlemisprotsessi.

Projekti käigus kohatud väljakutsed ja nende lahendused on sama väärtuslikud kui lõpptulemus. Refleksioon "mis läks hästi" ja "mida teeks järgmine kord teisiti" on osa professionaalsest engineer'i mindset'ist.