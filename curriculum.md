# Haapsalu Kutsehariduskeskus

**IT-süsteemide nooremspetsialist (441 Neljanda taseme kutseõppe esmaõpe (kutsekeskharidusõpe)) mooduli rakenduskava**

---

## Põhiandmed

| | |
|---|---|
| **Sihtrühm** | Põhiharidusega noor |
| **Õppevorm** | statsionaarne õpe - koolipõhine õpe |

| Mooduli nr | Mooduli nimetus | Mooduli maht (EKAP) | Õpetajad |
|---|---|---|---|
| 1 | Automatiseerimine | 2,5 EKAP | Rain Koor, Maria Talvik |

**Nõuded mooduli alustamiseks:**

Puuduvad. Moodul õpetatakse III kursusel.

Soovituslikud eelteadmised:
- Põhilised Linux süsteemihalduse oskused
- Bash skriptimise alused
- TCP/IP võrkude põhiteadmised

**Mooduli eesmärk:**

Õpetusega taotletakse, et õppija omandab kaasaegsed DevOps automatiseerimise tööriistad ja meetodid. Õppija oskab kasutada Git, Docker, Ansible, Terraform, Kubernetes ja GitLab CI/CD tööriistu tarkvara arendamise, testimise ning juurutamise automatiseerimiseks ning infrastruktuuri kui koodi (Infrastructure as Code) põhimõtete rakendamiseks.

Õppija omandab:
- Git versioonihalduse meeskonnatöös
- Konteinerite loomise ja haldamise (Docker)
- Ansible automatiseerimise tarkvara kasutamise
- Infrastructure as Code põhimõtted (Terraform)
- Kubernetes orkestreerimise
- CI/CD pipeline'ide loomise GitLabis

| Auditoorne õpe | Iseseisev õpe | Kokku |
|---|---|---|
| 50 tundi | 15 tundi | 65 tundi |

---

## Õpiväljundid ja hindamiskriteeriumid

| Õpiväljundid | Hindamiskriteeriumid | Hindamine |
|---|---|---|
| Kasutab Git versioonihaldust meeskonnatöös | • Loob Git repositooriumi ja seadistab remote'i<br>• Teostab branch'ide loomist ja merge'imist<br>• Lahendab merge konflikte<br>• Teostab pull request'e ja koodireview'd<br>• Kasutab Git Flow workflow'i | Eristav hindamine |
| Konteineriseerib rakendusi ja haldab konteinereid | • Loob ja käivitab Docker konteinereid<br>• Kirjutab Dockerfile'e järgides best practices<br>• Seadistab Docker Compose mitme-konteineriga rakenduste jaoks<br>• Haldab Docker võrgustikku ja volumes'e<br>• Optimeerib konteinerite turvalisust | Eristav hindamine |
| Automatiseerib infrastruktuuri haldust Ansible'iga | • Kirjutab YAML süntaksiga Ansible playbook'e<br>• Loob ja haldab inventory faile<br>• Kasutab Ansible mooduleid ja rolle<br>• Rakendab Jinja2 template'id ja muutujaid<br>• Kasutab Ansible Vault'i secrets haldamiseks<br>• Loob taaskasutatavaid Ansible rolle | Eristav hindamine |
| Rakendab Infrastructure as Code põhimõtteid Terraform'iga | • Kirjutab Terraform HCL koodi<br>• Haldab Terraform state'i lokaalselt ja remote'lt<br>• Paigaldab infrastruktuuri pilves (AWS/Azure)<br>• Kasutab Terraform mooduleid ja workspaces'eid<br>• Rakendab IaC best practices'eid | Eristav hindamine |
| Orkestreerib konteineriseeritud rakendusi Kubernetes'es | • Haldab Kubernetes klastreid (Minikube/Kind)<br>• Loob Kubernetes ressursse (Deployments, Services, Ingress)<br>• Skaleerib rakendusi Kubernetes'es<br>• Kasutab kubectl käsurida<br>• Rakendab Kubernetes best practices'eid | Eristav hindamine |
| Automatiseerib tarkvara arenduse ja juurutamise CI/CD'ga | • Loob GitLab CI/CD pipeline'e<br>• Seadistab .gitlab-ci.yml konfiguratsiooni<br>• Lõimib testimist ja deployment'i<br>• Automatiseerib konteinerite ehitamist ja paigaldamist<br>• Rakendab CI/CD best practices'eid | Eristav hindamine |
| Integreerib kõiki DevOps tööriistu lõpuprojektis | • Projekteerib täieliku DevOps infrastruktuuri<br>• Lõimib Git, Docker, Ansible, Terraform, Kubernetes ja CI/CD<br>• Dokumenteerib arhitektuuri ja tehnilisi otsuseid<br>• Esitleb projekti professionaalselt<br>• Teostab koodireview'd teiste projektidele | Eristav hindamine |

---

## Mooduli sisu ja jaotus

**Automatiseerimine**

Auditoorne õpe: 50h  
Iseseisev õpe: 15h  
Kokku: 65h

### Tunniplaan:

Kursus koosneb 10 teemaloengust + lõpuprojekt:
- **10 teemaloengut** × 4h auditoorset tööd = 40h
- **Iseseisev töö** moodulite kaupa = 15h (kodutööd, harjutused, lugemine)
- **Lõpunädal/Intensiiv** = 10h (projekti juhendamine, esitlused, hindamine)

### Alateemad:

**1. Git Versioonihaldus (Loeng 1: 4h auditoorset + 1.5h iseseisev)**
- Git kontseptsioonid ja töövoog
- Põhilised käsud praktikas (clone, commit, push, pull, branch, merge)
- GitHub/GitLab koostöö ja Pull Request'id
- Harude loomine ja ühendamine
- Konfliktide lahendamine
- Git Flow branching strategy

**2. Ansible Alused (Loeng 2: 4h auditoorset + 1.5h iseseisev)**
- Ansible arhitektuuri ülevaade
- Kohalik VM seadistus Vagrant'iga
- SSH seadistus ja inventory
- Ad-hoc käskude praktika
- YAML süntaks
- Esimeste playbook'ide loomine

**3. Docker Alused (Loeng 3: 4h auditoorset + 1.5h iseseisev)**
- Konteinerite kontseptsioonid vs VM'id
- Docker'i installimine ja põhikäsud
- Dockerfile'i loomine ja best practices
- Docker'i võrgustik ja volumes
- Docker Hub ja registrid
- Konteinerite turvalisus

**4. Docker Orkestratsioon (Loeng 4: 4h auditoorset + 1.5h iseseisev)**
- Docker Compose süntaks
- Mitme-konteineriga rakendused
- Keskkonna-spetsiifilised konfiguratsioonid
- Kohalikud arenduse töövood
- Docker Swarm tutvustus
- Orkestreerimise mustrid

**5. Ansible Edasijõudnud (Loeng 5: 4h auditoorset + 1.5h iseseisev)**
- Muutujad ja Jinja2 mallid
- Käsitlejad (handlers) ja veakäsitlus
- Ansible Vault turvalisuse labor
- Ansible Galaxy kogukond
- Edasijõudnud playbook'id
- Jõudluse optimeerimine

**6. Ansible Rollid (Loeng 6: 4h auditoorset + 1.5h iseseisev)**
- Rolli struktuur ja best practices
- Rolli loomine samm-sammult
- Rolli muutujad ja sõltuvused
- Galaxy rollide kasutamine
- Rollide testimine
- Rollide versioneerimine

**7. Terraform Alused (Loeng 7: 4h auditoorset + 1.5h iseseisev)**
- Infrastructure as Code ülevaade
- Terraform alused ja HCL keel
- Kohalikud providerid
- State'i haldamise kontseptsioonid
- Terraform Cloud tutvustus
- Moodulid ja tööruumid

**8. Terraform Edasijõudnud (Loeng 8: 4h auditoorset + 1.5h iseseisev)**
- Pilve ressursid ja providerid
- AWS/Azure põhilised ressursid
- Terraform Workspaces ja keskkonnad
- Turvalisus ja IAM
- Edasijõudnud Terraform mustrid
- Optimeerimine ja best practices

**9. Kubernetes Sügavõte (Loeng 9: 4h auditoorset + 1.5h iseseisev)**
- Kubernetes arhitektuur ja kontseptsioonid
- Kohalik klastri haldamine (Minikube/Kind)
- Ressursside haldamine (Deployments, Services, Ingress)
- Skaleerimine ja jõudlus
- Helm charts tutvustus
- Kubernetes best practices

**10. CI/CD Pipeline'id (Loeng 10: 4h auditoorset + 1.5h iseseisev)**
- CI/CD kontseptsioonid ja töövood
- GitLab CI/CD ja .gitlab-ci.yml
- Pipeline'ide loomine ja optimeerimine
- Automatiseeritud testimine
- Automatiseeritud deployment
- GitOps põhimõtted

**11. Lõpuprojekt ja Integratsioon (Intensiivnädal/Eksamiperiood: 10h)**
- Projekti esitlused ja demo'd (auditoorset)
- Koodireview sessioonid (auditoorset)
- Projekti dokumentatsiooni viimistlemine (iseseisev)
- Hindamine ja tagasiside (auditoorset)

---

## Hindamine

**Hindamise vorm:** Eristav hindamine (hinnetega 3, 4, 5)

### Mooduli kokkuvõtva hinde kujunemine:

**1. Praktilised tööd - 10 moodulit (50%)**
- Iga mooduli lab ja homework hindamine
- Funktsionaalsus ja koodikvaliteet
- Dokumentatsiooni kvaliteet
- Õigeaegne esitamine

**2. Lõpuprojekt (40%)**
- Kõigi tööriistade integratsioon
- Arhitektuuri kvaliteet
- Dokumentatsioon ja tehniliste otsuste põhjendamine
- Esitlus ja demo
- Innovatiivsus

**3. Portfoolio ja koostöö (10%)**
- GitHub repositooriumi korrashoid
- Commit'ide kvaliteet ja ajalugu
- Koodireview teiste õppijatele
- README ja dokumentatsiooni kvaliteet

**Nõue läbimiseks:** Kõik 10 mooduli praktilised tööd peavad olema esitatud ja funktsionaalsed. Lõpuprojekt peab olema esitatud ja töötav.

### Hindamiskriteeriumid (lävend):

**"3" (rahuldav) saamise tingimus:**
- Kõik 10 mooduli praktilised tööd on esitatud ja põhifunktsionaalsus töötab
- Git: oskab teha põhilisi operatsioone (clone, commit, push, pull, branch, merge)
- Docker: oskab luua lihtsaid Dockerfile'e ja käivitada konteinereid
- Ansible: oskab kirjutada põhilisi playbook'e ja kasutada levinumaid mooduleid
- Terraform: oskab kirjutada lihtsat HCL koodi ja hallata state'i
- Kubernetes: oskab paigaldada rakendusi Minikube'is
- CI/CD: oskab luua lihtsa GitLab pipeline'i
- Dokumentatsioon on minimaalne, kuid olemas
- Lõpuprojekt töötab ja integreerib vähemalt 4 tööriista, kuid võib sisaldada vigu

**"4" (hea) saamise tingimus:**
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

**"5" (väga hea) saamise tingimus:**
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

---

## Õppemeetodid

- Praktiline töö (hands-on lab harjutused)
- Juhendatud praktika ja demostratsioon
- Meeskonnatöö ja peer programming
- Projektipõhine õppimine
- Iseseisev töö ja uurimine
- Probleemilahendus ja debugging
- Koodireview ja tagasiside

---

## Hindamismeetodid

- Praktiliste tööde hindamine (funktsionaalsus, koodikvaliteet, dokumentatsioon)
- Lõpuprojekti hindamine (integratsioon, arhitektuur, esitlus)
- Portfoolio hindamine (GitHub repository kvaliteet)
- Enesehindamine ja eesmärkide refleksioon
- Jookev tagasiside lab'ide ja harjutuste käigus

---

## Lõimitud teemad

**Seosed teiste ainetega:**
- **Programmeerimine:** Bash skriptimine, YAML, HCL, Python
- **Võrgud:** TCP/IP, SSH, DNS, load balancing, Ingress
- **Andmebaasid:** PostgreSQL/MySQL paigaldamine ja konfigureerimine
- **Turvalisus:** SSL/TLS, SSH key management, secrets handling, RBAC
- **Operatsioonisüsteemid:** Linux süsteemihaldus (Ubuntu, CentOS/RHEL)
- **Pilvetehnoloogiad:** AWS, Azure ressursside haldamine

**Üldpädevused:**
- **Õpipädevus:** iseseisev uute tööriistade õppimine, dokumentatsiooni kasutamine, probleemide uurimine
- **Suhtluspädevus:** tehniline dokumenteerimine, esitlused, koodireview, meeskonnas suhtlemine
- **Meeskonnatöö:** Git koostöö, projektihaldus, feedback andmine ja vastuvõtmine, paaristöö
- **Probleemilahendus:** debugging, arhitektuurilahendused, optimeerimine, kriitilise mõtlemise
- **Digipädevus:** CLI tööriistad, cloud services, DevOps toolchain, automatiseerimine

---

## Mooduli hindamine

Eristav hindamine (3, 4, 5)

---

## Mooduli kokkuvõtva hinde kujunemine

Praktilised tööd 50% + Lõpuprojekt 40% + Portfoolio 10%

Nõue: Kõik 10 mooduli tööd ja lõpuprojekt peavad olema esitatud ja funktsionaalsed.

---

## Õppematerjalid

### Veebiallikad ja dokumentatsioon:

| Tööriist | Dokumentatsioon | URL |
|----------|----------------|-----|
| **Git** | Ametlik dokumentatsioon | https://git-scm.com/doc |
| **Ansible** | Ametlik dokumentatsioon | https://docs.ansible.com |
| **Docker** | Ametlik dokumentatsioon | https://docs.docker.com |
| **Terraform** | Ametlik dokumentatsioon | https://terraform.io/docs |
| **Kubernetes** | Ametlik dokumentatsioon | https://kubernetes.io/docs |
| **GitLab CI/CD** | Ametlik dokumentatsioon | https://docs.gitlab.com/ee/ci/ |

### Soovituslik kirjandus:
1. **The Phoenix Project** (Gene Kim) - DevOps filosoofia ja kultuur
2. **Infrastructure as Code** (Kief Morris) - IaC põhimõtted ja mustrid
3. **Continuous Delivery** (Jez Humble, David Farley) - CI/CD best practices

### Kursuse materjalid:

**📦 GitHub repositoorium:** https://github.com/mtalvik/automatiseerimine_ext

| Moodul | Loeng | Lab | Kodutöö | Lisad |
|--------|-------|-----|---------|-------|
| **1. Git** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git_version_control/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git_version_control/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git_version_control/homework.md) | [reading](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git_version_control/reading_materials.md) |
| **2. Ansible Basics** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/homework.md) | [vagrant.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/vagrant.md) |
| **3. Docker Fundamentals** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_fundamentals/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_fundamentals/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_fundamentals/homework.md) | - |
| **4. Docker Orchestration** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/homework.md) | [setup guide](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/kodu_masina_ehitus_juhend.md) |
| **5. Ansible Advanced** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_advanced/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_advanced/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_advanced/homework.md) | - |
| **6. Ansible Roles** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_roles/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_roles/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_roles/homework.md) | - |
| **7. Terraform Basics** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_basics/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_basics/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_basics/homework.md) | - |
| **8. Terraform Advanced** | - | - | - | [additional_modules](https://github.com/mtalvik/automatiseerimine_ext/tree/main/additional_modules) |
| **9. Kubernetes** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes_overview/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes_overview/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes_overview/homework.md) | [lisa_lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes_overview/lisa_lab.md) |
| **10. CI/CD** | [lecture.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ci_cd_advanced/lecture.md) | [lab.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ci_cd_advanced/lab.md) | [homework.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ci_cd_advanced/homework.md) | - |

### Tehniline keskkond:
- Arvuti vähemalt 8GB RAM ja 50GB vaba ruumi
- VirtualBox või Docker Desktop
- Git, Ansible, Terraform, kubectl installeeritud
- Juurdepääs GitHub/GitLab kontole
- Ligipääs AWS/Azure free tier kontole (soovituslik)