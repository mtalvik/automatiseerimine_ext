# Automatiseerimise Kursus

**IT-süsteemide nooremspetsialist - Automatiseerimise moodul**

---

## Kursuse Ülevaade

| | |
|---|---|
| **Sihtrühm** | IT-süsteemide nooremspetsialist |
| **Kestus** | 65 tundi (50h auditoorset + 15h iseseisvat) |
| **Õppevorm** | Statsionaarne õpe |
| **Õpetajad** | Rain Koor, Maria Talvik |

### Eeltingimused

**Nõuded mooduli alustamiseks:**
- Puuduvad. Moodul õpetatakse III kursusel.

**Soovituslikud eelteadmised:**
- Põhilised Linux süsteemihalduse oskused
- Bash skriptimise alused
- TCP/IP võrkude põhiteadmised

### Kursuse Eesmärk

Õppija omandab kaasaegsed DevOps automatiseerimise tööriistad ja meetodid. Õppija oskab kasutada Git, Docker, Ansible, Terraform, Kubernetes ja GitLab CI/CD tööriistu tarkvara arendamise, testimise ning juurutamise automatiseerimiseks ning infrastruktuuri kui koodi (Infrastructure as Code) põhimõtete rakendamiseks.

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

| | |
|---|---|
| **Auditoorne õpe** | 50h |
| **Iseseisev õpe** | 15h |
| **Kokku** | 65h |

### Tunniplaan

| Komponent | Kestus | Kirjeldus |
|-----------|--------|-----------|
| **10 teemaloengut** | 40h | 4h auditoorset tööd per loeng |
| **Iseseisev töö** | 15h | Kodutööd, harjutused, lugemine |
| **Lõpunädal** | 10h | Projekti juhendamine, esitlused, hindamine |

### Moodulid

| Nr | Moodul | Kestus | Põhiteemad |
|----|--------|--------|------------|
| 1 | **Git** | 4h + 1.5h | Versioonihaldus, GitHub koostöö, Git Flow |
| 2 | **Ansible Alused** | 4h + 1.5h | Arhitektuur, YAML, playbook'id, Vagrant |
| 3 | **Docker Basics** | 4h + 1.5h | Konteinerid, Dockerfile, võrgustik, turvalisus |
| 4 | **Docker Orkestratsioon** | 4h + 1.5h | Docker Compose, multi-container, Swarm |
| 5 | **Ansible Edasijõudnud** | 4h + 1.5h | Muutujad, Jinja2, Vault, Galaxy |
| 6 | **Ansible Rollid** | 4h + 1.5h | Rolli struktuur, best practices, testimine |
| 7 | **Terraform Alused** | 4h + 1.5h | IaC, HCL, state haldamine, moodulid |
| 8 | **Terraform Edasijõudnud** | 4h + 1.5h | Pilve ressursid, workspaces, turvalisus |
| 9 | **Kubernetes** | 4h + 1.5h | Arhitektuur, Minikube, ressursid, Helm |
| 10 | **CI/CD** | 4h + 1.5h | Pipeline'id, GitLab, testimine, GitOps |
| 11 | **Lõpuprojekt** | 10h | Integratsioon, esitlused, hindamine |

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
| **1. Git** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git/kodutoo.md) | [lisamaterjalid.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/git/lisamaterjalid.md) |
| **2. Ansible Basics** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/kodutoo.md) | [seadistus.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_basics/seadistus.md) |
| **3. Docker Basics** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_basics/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_basics/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_basics/kodutoo.md) | - |
| **4. Docker Orchestration** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/kodutoo.md) | [seadistus.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/docker_orchestration/seadistus.md) |
| **5. Ansible Advanced** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_advanced/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_advanced/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_advanced/kodutoo.md) | - |
| **6. Ansible Roles** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_roles/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_roles/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ansible_roles/kodutoo.md) | - |
| **7. Terraform Basics** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_basics/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_basics/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_basics/kodutoo.md) | - |
| **8. Terraform Advanced** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_advanced/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_advanced/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/terraform_advanced/kodutoo.md) | - |
| **9. Kubernetes** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes/kodutoo.md) | [lisa_labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/kubernetes/lisa_labor.md) |
| **10. CI/CD** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ci_cd/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ci_cd/labor.md) | [kodutoo.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/ci_cd/kodutoo.md) | - |
| **11. Lõpuprojekt** | [loeng.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/lopuprojekt/loeng.md) | [labor.md](https://github.com/mtalvik/automatiseerimine_ext/blob/main/lopuprojekt/labor.md) | - | - |

### Tehniline keskkond:
- Arvuti vähemalt 8GB RAM ja 50GB vaba ruumi
- VirtualBox või Docker Desktop
- Git, Ansible, Terraform, kubectl installeeritud
- Juurdepääs GitHub/GitLab kontole
- Ligipääs AWS/Azure free tier kontole (soovituslik)