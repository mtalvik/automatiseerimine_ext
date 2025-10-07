# Automatiseerimine

> Praktiline kutsekeskhariduse kursus DevOps tööriistade ja automatiseerimise õppimiseks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Course Level](https://img.shields.io/badge/Level-Intermediate-orange.svg)]()
[![Duration](https://img.shields.io/badge/Duration-14%20weeks-blue.svg)]()
[![Language](https://img.shields.io/badge/Language-Estonian-green.svg)]()

---

## Kursuse kirjeldus

Õpi kuidas automatiseerida servereid, hallata kontainereid ja luua CI/CD pipeline'e nagu päris DevOps insenerid. Kursus on 70% praktika, 30% teooria - õpid tehes!

### Mida õpid?

```
Git → Ansible → Docker → Terraform → Kubernetes → CI/CD → Lõpuprojekt
```

- ✅ **Git & GitHub** - versioonihaldus ja meeskonnatöö
- ✅ **Docker** - konteinerite loomine ja orkestratsioon
- ✅ **Ansible** - serverite automatiseerimine ja konfiguratsioonihaldus
- ✅ **Terraform** - infrastruktuur koodina (IaC)
- ✅ **Kubernetes** - konteinerite orkestratsioon suuremas mahus
- ✅ **CI/CD** - automaatne testimine ja deployment

### Kursuse lõpuks oskad:

- 🐳 Dockeriseerida rakendusi ja hallata multi-container süsteeme
- 🤖 Automatiseerida serverite seadistamist Ansible'iga
- ☁️ Luua cloud infrastruktuuri Terraform'iga
- 🎯 Seadistada Kubernetes klastrit ja deploy'ida rakendusi
- 🔄 Ehitada CI/CD pipeline'e GitHub Actions'iga
- 📦 Integreerida kõiki tööriistu ühes produktsioonikeskkonnas

---

## Kellele see kursus on?

### ✅ Ideaalne kui:
- Õpid kutsekeskhariduses IT erialal
- Tunned Linux põhikäske (`cd`, `ls`, `mkdir`)
- Tahad saada DevOps/SRE tööle
- Soovid automatiseerida igavad käsitsitööd

### ❌ Ei sobi kui:
- Pole kunagi terminali näinud
- Otsid ainult teoreetilist kursust
- Ei ole valmis praktilisi ülesandeid tegema

---

## 📖 Kursuse sisu

| Nädal | Moodul | Teemad | Projekt |
|-------|--------|--------|---------|
| 1 | Git | Version control, branching, GitHub | Portfolio repo |
| 2 | Ansible Basics | Playbooks, inventory, modules | Web server setup |
| 3 | Docker Basics | Dockerfile, images, containers | Containerize app |
| 4 | Docker Compose | Multi-container, networks | Full stack app |
| 5 | Ansible Advanced | Vault, templates, handlers | Secure deployment |
| 6 | Ansible Roles | Role structure, Galaxy | Reusable configs |
| 7 | Terraform Basics | HCL, resources, state | Infrastructure setup |
| 8 | Terraform Advanced | Modules, providers, cloud | Cloud deployment |
| 9-10 | Kubernetes | Pods, services, deployments | K8s cluster |
| 11 | CI/CD | GitHub Actions, pipelines | Auto deployment |
| 12-14 | Lõpuprojekt | **Integreeri kõik tööriistad** | Production app |

---

## 🛠️ Vajalikud tööriistad

Paigalda need enne kursuse algust:

```bash
# Kontrolli kas on installitud
git --version
docker --version
# VÕI
podman --version
```

**Kohustuslikud:**
- [Git](https://git-scm.com/) - versioonihaldus
- [Docker](https://www.docker.com/) või [Podman](https://podman.io/) - konteinerid
- [VS Code](https://code.visualstudio.com/) - redaktor (või Vim/Nano)

**Installitakse kursuse käigus:**
- Ansible
- Terraform
- kubectl
- Minikube

**Soovituslikud VS Code laiendused:**
- Docker
- YAML
- GitLens
- Ansible

---

## 📂 Projekti struktuur

```
automatiseerimine_ext/
│
├── git/                    # Moodul 1: Git versioonihaldus
│   ├── loeng.md           # Teooria
│   ├── labor.md           # Praktika tunnis
│   ├── kodutoo.md         # Iseseisev töö
│   └── lisapraktika.md    # Lisaülesanded
│
├── ansible_basics/         # Moodul 2: Ansible alused
├── docker_basics/          # Moodul 3: Docker alused
├── docker_orchestration/   # Moodul 4: Docker Compose
├── ansible_advanced/       # Moodul 5: Ansible edasijõudnud
├── ansible_roles/          # Moodul 6: Ansible rollid
├── terraform_basics/       # Moodul 7: Terraform alused
├── terraform_advanced/     # Moodul 8: Terraform edasijõudnud
├── kubernetes/             # Moodul 9: Kubernetes
├── ci_cd/                  # Moodul 10: CI/CD pipeline'id
└── lopuprojekt/            # Moodul 11: Lõpuprojekt
```

---

## Hindamine

| Komponent | Kaal | Kirjeldus |
|-----------|------|-----------|
| **Praktilised tööd** | 50% | Labor + kodutööd (10 moodulit × 5%) |
| **Lõpuprojekt** | 40% | Integreerib kõik õpitud tööriistad |
| **GitHub portfoolio** | 10% | Repository kvaliteet ja dokumentatsioon |

### Praktiliste tööde nõuded:
- ✅ Labor tehtud tunnis või nädalaga
- ✅ Kodutöö push'itud GitHub'i tähtajaks
- ✅ Kood töötab ja on dokumenteeritud
- ✅ Commit history näitab tööprotsessi

### Lõpuprojekti nõuded:
- ✅ Kasutab vähemalt 3 erinevat tööriista
- ✅ Töötav CI/CD pipeline
- ✅ Deployitav produktsioonikeskkonda
- ✅ Täielik dokumentatsioon

---

## Kuidas alustada?

### 1. Klooni repositoorium

```bash
git clone https://github.com/mtalvik/automatiseerimine-2025
cd automatiseerimine-2025
```

### 2. Alusta esimesest moodulist

```bash
cd git
cat loeng.md  # Loe teooria
cat labor.md  # Tee praktika
```

### 3. Tee oma repositoorium

```bash
# Loo oma kursuse repositoorium
mkdir automatiseerimine-[sinu-nimi]
cd automatiseerimine-[sinu-nimi]
git init

# Lisa esimene commit
echo "# Automatiseerimine - Minu Portfoolio" > README.md
git add README.md
git commit -m "Initial commit"

# Loo GitHub'is repo ja push
git remote add origin https://github.com/[sinu-kasutaja]/automatiseerimine-[nimi].git
git push -u origin main
```

### 4. Tee nädala töö

```
Esmaspäev   → Loe loeng.md
Kolmapäev   → Tee labor.md klassis
Reede       → Esita kodutoo.md
Nädalavahetus → (Valikuline) lisapraktika.md
```

---

## 💡 Õppenõuanded

### ✅ Tee:
- Commit'i tööd regulaarselt (iga päev vähemalt 1 commit)
- Kirjuta commit message'id eesti keeles ja selgelt
- Tee branch'e suurematele featuredele
- Küsi küsimusi kohe kui kinni jääd
- Aita klassikaaslasi (õpetades õpid ise kõige paremini)

### ❌ Ära tee:
- Ära kopeeri teiste koodi (õpid palju vähem)
- Ära jäta kodutöid viimasele minutile
- Ära push'i GitHub'i paroole või API võtmeid
- Ära jäta vahele mooduleid (iga järgmine eeldab eelmist)

---

## Abi ja suhtlus

### 📧 Kontakt
- **Õpetaja:** Maria Talvik
- **GitHub:** [@mtalvik](https://github.com/mtalvik)

### 💬 Küsimused?
1. Kontrolli kas vastus on `loeng.md` failis
2. Google'da error message't
3. Küsi klassikaaslastelt
4. Küsi tunnis õpetajalt

### 🐛 Leidsin vea materjalides
Loo [GitHub Issue](https://github.com/mtalvik/automatiseerimine-2025/issues) või tee Pull Request!

---

## 📜 Litsents

See kursus on avatud lähtekoodiga ja kasutatav õppeotstarbel.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Projekti näited

Vaata eelmiste õpilaste lõpuprojekte inspiratsiooni saamiseks:

- [E-pood Kubernetes'es](https://github.com/example/eshop-k8s) - Full-stack app K8s'is
- [Terraform AWS Infrastructure](https://github.com/example/aws-terraform) - Production-ready AWS
- [CI/CD Pipeline](https://github.com/example/cicd-demo) - GitHub Actions demo

*(Lisa siia päris õpilaste projekte kui on)*

---

<div align="center">

**[Git Versioonihaldus →](git/loeng.md)**

---

*"The best way to learn is by doing."*

</div># Trigger deployment Tue Oct  7 17:09:31 EEST 2025
