# IT-süsteemide nooremspetsialist (441 Neljanda taseme kutseõppe esmaõpe (kutsekeskharidusõpe)) mooduli töökava

**Automatiseerimine**

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
| Orkestreerib konteineriseeritud rakendusi Kubernetes'es | • Haldab Kubernetes klastreid (Minikube/Kind)<br>• Loob Kubernetes ressursse (Deployments, Services, Ingress)<br>• Skaleerib rakendusi Kubernetes'es<br>• Kasutab kubectl käsurida<br>• Rakendab Kubernetes best practices'eid | Eristav hindamine |
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
| **sh hindamiskriteeriumid** | Praktilised tööd (50%), Lõpuprojekt (40%), Portfoolio (10%) |

| Hinne | Nõuded |
|---|---|
| **"3" (rahuldav)** | • Kõik praktilised tööd on esitatud<br>• Põhifunktsionaalsus töötab<br>• Git: põhilised käsud (clone, commit, push, pull)<br>• Docker: lihtsad Dockerfile'id<br>• Ansible: põhilised playbook'id<br>• Terraform: lihtne HCL kood<br>• Kubernetes: rakenduste paigaldamine<br>• CI/CD: lihtne pipeline<br>• Lõpuprojekt: 2-3 tööriista kasutatud |
| **"4" (hea)** | • Kõik "3" nõuded täidetud<br>• Kood on loetav ja kommenteeritud<br>• Git: branch'ide haldamine<br>• Docker: Docker Compose kasutamine<br>• Ansible: muutujate ja rolle kasutamine<br>• Terraform: moodulite kasutamine<br>• Kubernetes: Services ja Deployments<br>• CI/CD: testimise integratsioon<br>• Lõpuprojekt: 3-4 tööriista hästi integreeritud |
| **"5" (väga hea)** | • Kõik "4" nõuded täidetud<br>• Kood järgib best practices'eid<br>• Git: Git Flow kasutamine<br>• Docker: multi-stage builds<br>• Ansible: Vault ja template'id<br>• Terraform: workspaces ja remote state<br>• Kubernetes: Ingress ja scaling<br>• CI/CD: mitme stage'i pipeline<br>• Lõpuprojekt: 4+ tööriista professionaalselt integreeritud |

## Õppemeetodid

| Parameeter | Väärtus |
|---|---|
| **Õppemeetodid** | Praktiline töö (harjutused ja ülesanded), meeskonnatöö, iseseisev töö |

## Hindamismeetodid

| Meetod | Kirjeldus |
|---|---|
| **Praktiliste tööde hindamine** | Funktsionaalsus, koodikvaliteet, dokumentatsioon |
| **Lõpuprojekti hindamine** | Integratsioon, arhitektuur, esitlus |
| **Portfoolio hindamine** | GitHub repository kvaliteet |

## Lõimitud teemad

| Teema | Seosed |
|---|---|
| **Programmeerimine** | Bash skriptimine, YAML, HCL, Python |
| **Võrgud** | TCP/IP, SSH, DNS, load balancing |
| **Andmebaasid** | PostgreSQL, MySQL |
| **Turvalisus** | SSL/TLS, SSH key management, secrets handling |
| **Operatsioonisüsteemid** | Linux süsteemihaldus |
| **Pilvetehnoloogiad** | AWS, Azure |

## Mooduli hindamine

| Parameeter | Väärtus |
|---|---|
| **Mooduli hindamine** | Eristav hindamine |

## Mooduli sisu ja teemad

| Teema | Kestus | Õpiväljund |
|---|---|---|
| **Git versioonihaldus** | 5.5h | ÕV1: Git versioonihaldus meeskonnatöös |
| **Ansible alused** | 5.5h | ÕV3: PlayBook ja automatiseerimine |
| **Docker alused** | 5.5h | ÕV2: Konteinerite loomine ja seadistamine |
| **Docker orkestratsioon** | 5.5h | ÕV2: Multi-container rakendused |
| **Ansible edasijõudnud** | 5.5h | ÕV4: Edasijõudnud automatiseerimine |
| **Ansible rollid** | 5.5h | ÕV4: Rollide loomine ja haldamine |
| **Terraform alused** | 5.5h | ÕV5: IaC põhimõtted |
| **Terraform edasijõudnud** | 5.5h | ÕV5: Pilve ressursid ja workspaces |
| **Kubernetes** | 5.5h | ÕV6: Konteinerite orkestreerimine |
| **CI/CD** | 5.5h | ÕV7: Automatiseeritud arendus |
| **Lõpuprojekt** | 10h | ÕV8: Tööriistade integratsioon |
| **KOKKU** | **65h** | **Kõik õpiväljundid** |

## Õppematerjalid

| Materjal | Kirjeldus |
|---|---|
| **GitHub repositoorium** | https://github.com/mtalvik/automatiseerimine_ext (11 moodulit) |
| **Ametlik dokumentatsioon** | Git, Ansible, Docker, Terraform, Kubernetes, GitLab CI/CD |
| **Kursuse moodulid** | Git, Ansible (alused/edasijõudnud/rollid), Docker (alused/orkestratsioon), Terraform (alused/edasijõudnud), Kubernetes, CI/CD, Lõpuprojekt |
