# Haapsalu Kutsehariduskeskus

**IT-süsteemide nooremspetsialist (441 Neljanda taseme kutseõppe esmaõpe (kutsekeskharidusõpe)) mooduli rakenduskava**

---

## Mooduli Üldandmed

| Parameeter | Väärtus |
|---|---|
| **Sihtrühm** | Põhiharidusega noor |
| **Õppevorm** | Statsionaarne õpe - koolipõhine õpe |

| Parameeter | Väärtus |
|---|---|
| **Mooduli nr** | 1 |
| **Mooduli nimetus** | Automatiseerimine |
| **Mooduli maht (EKAP)** | 2,5 EKAP |
| **Õpetajad** | Rain Koor, Maria Talvik |
| **Nõuded mooduli alustamiseks** | Puuduvad. Moodul õpetatakse III kursusel |
| **Mooduli eesmärk** | Õpetusega taotletakse, et õppija oskab kasutada kaasaegseid DevOps automatiseerimise tööriistu eesmärgiga teha tarkvara arendamist, testimist ning juurutamist kiiremini ja sagedamini |
| **Auditoorne õpe** | 50 tundi |
| **Iseseisev õpe** | 15 tundi |

## Õpiväljundid ja Hindamine

| Õpiväljundid | Hindamiskriteeriumid | Hindamine |
|---|---|---|
| Oskab kasutada Git versioonihaldust meeskonnatöös | • Loob Git repositooriumi ja seadistab remote'i<br>• Teostab branch'ide loomist ja merge'imist<br>• Lahendab merge konflikte<br>• Teostab pull request'e ja koodireview'd<br>• Kasutab Git Flow workflow'i | Eristav hindamine |
| Oskab luua ja seadistada konteinereid ja virtuaalmasinaid | • Loob ja käivitab Docker konteinereid<br>• Kirjutab Dockerfile'e järgides best practices<br>• Seadistab Docker Compose mitme-konteineriga rakenduste jaoks<br>• Haldab Docker võrgustikku ja volumes'e<br>• Optimeerib konteinerite turvalisust | Eristav hindamine |
| Oskab koostada Ansible PlayBooki ja hallatavate masinate loendit | • Kirjutab YAML süntaksiga Ansible playbook'e<br>• Loob ja haldab inventory faile<br>• Kasutab Ansible mooduleid ja rolle<br>• Rakendab Jinja2 template'id ja muutujaid<br>• Kasutab Ansible Vault'i secrets haldamiseks | Eristav hindamine |
| Automatiseerib operatsioonisüsteemide haldustegevused kasutades Ansible tarkvara | • Loob taaskasutatavaid Ansible rolle<br>• Optimeerib playbook'ide jõudlust<br>• Rakendab error handling'ut<br>• Kasutab conditional execution'it | Eristav hindamine |
| Automatiseerib operatsioonisüsteemides tarkvarapakettide paigalduse ja seadistuste rakendamise kasutades Ansible tarkvara ja GitLabi keskkonda | • Rakendab Infrastructure as Code põhimõtteid Terraform'iga<br>• Kirjutab Terraform HCL koodi<br>• Haldab Terraform state'i lokaalselt ja remote'lt<br>• Paigaldab infrastruktuuri pilves (AWS/Azure)<br>• Kasutab Terraform mooduleid ja workspaces'eid | Eristav hindamine |
| Oskab läbi Ansible AWX rakenduse käivitada playbooke | • Orkestreerib konteineriseeritud rakendusi Kubernetes'es<br>• Haldab Kubernetes klastreid (Minikube/Kind)<br>• Loob Kubernetes ressursse (Deployments, Services, Ingress)<br>• Skaleerib rakendusi Kubernetes'es<br>• Kasutab kubectl käsurida | Eristav hindamine |
| Automatiseerib tarkvara arenduse ja juurutamise CI/CD'ga | • Loob GitLab CI/CD pipeline'e<br>• Seadistab .gitlab-ci.yml konfiguratsiooni<br>• Lõimib testimist ja deployment'i<br>• Automatiseerib konteinerite ehitamist ja paigaldamist<br>• Rakendab CI/CD best practices'eid | Eristav hindamine |
| Integreerib kõiki DevOps tööriistu lõpuprojektis | • Projekteerib täieliku DevOps infrastruktuuri<br>• Lõimib Git, Docker, Ansible, Terraform, Kubernetes ja CI/CD<br>• Dokumenteerib arhitektuuri ja tehnilisi otsuseid<br>• Esitleb projekti professionaalselt<br>• Teostab koodireview'd teiste projektidele | Eristav hindamine |

| Auditoorne õpe | Iseseisev õpe | Kokku |
|---|---|---|
| 50 tundi | 15 tundi | 65 tundi |

---

## Hindamine

| Parameeter | Väärtus |
|---|---|
| **Hindamine** | Eristav hindamine |

### Mooduli kokkuvõtva hinde kujunemine

| Parameeter | Väärtus |
|---|---|
| **sh kokkuvõtva hinde kujunemine** | Esitatud praktilised tööd koos dokumentatsiooniga |
| **sh hindamiskriteeriumid** | (hea, kui õpetaja kohe alguses need kirjeldab, siis hiljem selgem ja üheselt arusaadav) |

**"3" saamise tingimus:**
- Kõik 10 mooduli praktilised tööd on esitatud ja põhifunktsionaalsus töötab
- Git: oskab teha põhilisi operatsioone (clone, commit, push, pull, branch, merge)
- Docker: oskab luua lihtsaid Dockerfile'e ja käivitada konteinereid
- Ansible: oskab kirjutada põhilisi playbook'e ja kasutada levinumaid mooduleid
- Terraform: oskab kirjutada lihtsat HCL koodi ja hallata state'i
- Kubernetes: oskab paigaldada rakendusi Minikube'is
- CI/CD: oskab luua lihtsa GitLab pipeline'i
- Dokumentatsioon on minimaalne, kuid olemas
- Lõpuprojekt töötab ja integreerib vähemalt 4 tööriista, kuid võib sisaldada vigu

**"4" saamise tingimus:**
- Kõik "3" kriteeriumid on täidetud
- Kood järgib enamasti best practices'eid ja on loetav
- Git: oskab lahendada merge konflikte ja kasutada Git Flow
- Docker: oskab kirjutada multi-stage Dockerfile'e ja kasutada Docker Compose
- Ansible: oskab kasutada rolle, muutujaid, Jinja2 template'id ja Vault'i
- Terraform: oskab kasutada mooduleid ja workspaces'eid
- Kubernetes: oskab hallata Deployments, Services ja Ingress ressursse
- CI/CD: pipeline sisaldab testimist ja mitut stage'i
- Dokumentatsioon on hea ja selgitab lahendusi
- Lõpuprojekt on hästi struktureeritud, integreerib 5+ tööriista ja on funktsionaalne

**"5" saamise tingimus:**
- Kõik "4" kriteeriumid on täidetud
- Kood on optimeeritud, järgib best practices'eid ja on täielikult dokumenteeritud
- Git: kasutab Git Flow professionaalselt, teeb kvaliteetseid commit'e
- Docker: rakendab turvalisuse best practices'eid, optimeerib image'ide suurust
- Ansible: kirjutab modulaarseid, taaskasutatavaid rolle, optimeerib jõudlust
- Terraform: rakendab IaC best practices'eid, kirjutab taaskasutatavaid mooduleid
- Kubernetes: rakendab skaaleerimist, jõudluse optimeerimist
- CI/CD: pipeline on optimeeritud, sisaldab security scanning'ut, automatiseeritud deployment'i
- Dokumentatsioon on professionaalne (README, arhitektuuridiagrammid, API docs)
- Lõpuprojekt demonstreerib sügavat mõistmist, innovaatilist lähenemist, integreerib kõik tööristad
- Lisafunktsioonid ja boonus ülesanded on tehtud

## Õppemeetodid

| Parameeter | Väärtus |
|---|---|
| **Õppemeetodid** | Praktiline töö (harjutused ja ülesanded), meeskonnatöö, iseseisev töö |

## Hindamismeetodid

| Parameeter | Väärtus |
|---|---|
| **Hindamismeetodid** | Praktiliste tööde hindamine (funktsionaalsus, koodikvaliteet, dokumentatsioon), lõpuprojekti hindamine (integratsioon, arhitektuur, esitlus), portfoolio hindamine (GitHub repository kvaliteet) |

## Lõimitud teemad

| Parameeter | Väärtus |
|---|---|
| **Lõimitud teemad** | Programmeerimine (Bash skriptimine, YAML, HCL, Python), võrgud (TCP/IP, SSH, DNS, load balancing), andmebaasid (PostgreSQL/MySQL), turvalisus (SSL/TLS, SSH key management, secrets handling), operatsioonisüsteemid (Linux süsteemihaldus), pilvetehnoloogiad (AWS, Azure) |

## Mooduli hindamine

| Parameeter | Väärtus |
|---|---|
| **Mooduli hindamine** | Eristav hindamine |

## Mooduli kokkuvõtva hinde kujunemine

| Parameeter | Väärtus |
|---|---|
| **Mooduli kokkuvõtva hinde kujunemine** | Esitatud praktilised tööd koos dokumentatsiooniga |

### sh lävend

**"3" saamise tingimus:**
- Kõik 10 mooduli praktilised tööd on esitatud ja põhifunktsionaalsus töötab
- Git: oskab teha põhilisi operatsioone (clone, commit, push, pull, branch, merge)
- Docker: oskab luua lihtsaid Dockerfile'e ja käivitada konteinereid
- Ansible: oskab kirjutada põhilisi playbook'e ja kasutada levinumaid mooduleid
- Terraform: oskab kirjutada lihtsat HCL koodi ja hallata state'i
- Kubernetes: oskab paigaldada rakendusi Minikube'is
- CI/CD: oskab luua lihtsa GitLab pipeline'i
- Dokumentatsioon on minimaalne, kuid olemas
- Lõpuprojekt töötab ja integreerib vähemalt 4 tööriista, kuid võib sisaldada vigu

**"4" saamise tingimus:**
- Kõik "3" kriteeriumid on täidetud
- Kood järgib enamasti best practices'eid ja on loetav
- Git: oskab lahendada merge konflikte ja kasutada Git Flow
- Docker: oskab kirjutada multi-stage Dockerfile'e ja kasutada Docker Compose
- Ansible: oskab kasutada rolle, muutujaid, Jinja2 template'id ja Vault'i
- Terraform: oskab kasutada mooduleid ja workspaces'eid
- Kubernetes: oskab hallata Deployments, Services ja Ingress ressursse
- CI/CD: pipeline sisaldab testimist ja mitut stage'i
- Dokumentatsioon on hea ja selgitab lahendusi
- Lõpuprojekt on hästi struktureeritud, integreerib 5+ tööriista ja on funktsionaalne

**"5" saamise tingimus:**
- Kõik "4" kriteeriumid on täidetud
- Kood on optimeeritud, järgib best practices'eid ja on täielikult dokumenteeritud
- Git: kasutab Git Flow professionaalselt, teeb kvaliteetseid commit'e
- Docker: rakendab turvalisuse best practices'eid, optimeerib image'ide suurust
- Ansible: kirjutab modulaarseid, taaskasutatavaid rolle, optimeerib jõudlust
- Terraform: rakendab IaC best practices'eid, kirjutab taaskasutatavaid mooduleid
- Kubernetes: rakendab skaaleerimist, jõudluse optimeerimist
- CI/CD: pipeline on optimeeritud, sisaldab security scanning'ut, automatiseeritud deployment'i
- Dokumentatsioon on professionaalne (README, arhitektuuridiagrammid, API docs)
- Lõpuprojekt demonstreerib sügavat mõistmist, innovaatilist lähenemist, integreerib kõik tööristad
- Lisafunktsioonid ja boonus ülesanded on tehtud

## Mooduli jagunemine - soovi ja vajaduse korral kirjeldage teemasid/alateemasid

| Parameeter | Väärtus |
|---|---|
| **Automatiseerimine** | Auditoorne õpe 50, Iseseisev õpe 15 |
| **Alateemad** | Git versioonihaldus, Docker konteineriseerimine, Ansible automatiseerimine, Terraform Infrastructure as Code, Kubernetes orkestreerimine, CI/CD pipeline'id, Lõpuprojekt |
| **Seos õpiväljundiga (pole vaja täita)** | |

## Õppematerjalid

| Parameeter | Väärtus |
|---|---|
| **Õppematerjalid** | Kohustuslik kirjandus: 1. GitHub repositoorium: https://github.com/mtalvik/automatiseerimine_ext 2. Ametlik dokumentatsioon: Git, Ansible, Docker, Terraform, Kubernetes, GitLab CI/CD |
