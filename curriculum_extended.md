# 📚 Automatiseerimise Kursuse Laiendatud Õppekava

**ITS-24 - Täiskasvanute klass (60 tundi, 12 moodulit)**

---

## 📋 Kursuse Ülevaade

See laiendatud kursus pakub põhjalikku automatiseerimise koolitust, mis katab kõik olulised DevOps tööriistad ja praktikad. Iga moodul sisaldab 5 tundi kontaktõpet ning struktureeritud kodutöid. Lisaks on lisatud uued moodulid ja praktilised projektid.

---

## 📊 Kursuse Struktuur

| Moodul | Teema | Kontaktaeg | Kodutöö Ülesanne 1 | Kodutöö Ülesanne 2 | Lisapraktika |
|--------|-------|------------|-------------------|-------------------|--------------|
| 1 | **Git Versioonihaldus** | 5h | Git projekti portfoolio näidetega | Lugemine: Git ajalugu, sisemused | GitHub Actions tutvustus |
| 2 | **Ansible Alused** | 5h | Kohalik LAMP stack (VirtualBox/Vagrant) | Lugemine: Ansible arhitektuur, YAML | Ansible Tower demo |
| 3 | **Docker Alused** | 5h | Mitme-rakendusega konteineriseerimise projekt | Lugemine: Docker arhitektuur, turvalisus | Docker Hub ja registrid |
| 4 | **Docker Orkestratsioon** | 5h | Täispinu kohalik paigaldus | Lugemine: Konteinerite orkestreerimise mustrid | Docker Swarm tutvustus |
| 5 | **Ansible Edasijõudnud** | 5h | Edasijõudnud funktsioonide laboriharjutused | Lugemine: Jinja2, muutujad, Ansible Vault | Ansible Galaxy projekt |
| 6 | **Ansible Rollid** | 5h | Rolli loomise labor + Puppet võrdlus | Lugemine: Rollide parimad praktikad, Galaxy | Rolli testimine ja valideerimine |
| 7 | **Terraform Alused** | 5h | Kohalik infrastruktuur (failid, konfiguratsioon) | Lugemine: IaC põhimõtted, Terraform mustrid | Terraform Cloud demo |
| 8 | **Terraform Edasijõudnud** | 5h | AWS/Azure pilve infrastruktuur | Lugemine: Pilve ressursid ja turvalisus | Terraform Workspaces |
| 9 | **Kubernetes Sügavõte** | 5h | Kohalik K8s klastri haldamine | Lugemine: K8s arhitektuur ja ressursid | Helm charts tutvustus |
| 10 | **CI/CD Pipeline'id** | 5h | Täielik automatiseerimise pipeline | Lugemine: GitOps ja DevOps praktikad | Jenkins vs GitHub Actions |
| 11 | **Turvalisus ja Jälgimine** | 5h | Turvalisuse skaneerimine ja logide analüüs | Lugemine: DevSecOps ja observability | Prometheus ja Grafana |
| 12 | **Lõpuprojekt ja Integratsioon** | 5h | Kõigi tööriistade integratsioon | Projekti dokumentatsioon ja esitlemine | Meeskonnatöö ja koodireview |

---

## 🎯 Moodulite Detailid

### **Moodul 1: Git Versioonihaldus (5h)**

**Kontaktaja Struktuur:**
- Git kontseptsioonid ja töövoog (1.5h)
- Põhilised käsud praktikas (1.5h)
- GitHub koostöö ja Pull Request'id (1h)
- Harude loomine ja ühendamine praktikas (1h)
- **Boonus:** GitHub Actions tutvustus ja põhilised workflow'id

**Käsitletud Teemad:**
- Git alused ja versioonihalduse põhimõtted
- Kohalik Git kasutamine ja põhilised käsud
- GitHub ja kaugrepositooriumid
- Meeskonnatöö ja Pull Request'id
- GitHub Actions ja automatiseerimine

**Kodutööd:**
- **Ülesanne 1:** Täielik Git projekti portfoolio harude töövooga
- **Ülesanne 2:** Loe Git ajalugu, sisemusi ja edasijõudnud kontseptsioone (3-4 tundi)
- **Lisapraktika:** Loo lihtne GitHub Actions workflow

---

### **Moodul 2: Ansible Alused (5h)**

**Kontaktaja Struktuur:**
- Ansible arhitektuuri ülevaade (1h)
- Kohalik VM seadistus Vagrant'iga (1h)
- SSH seadistus ja inventory (1h)
- Ad-hoc käskude praktika (1h)
- Esimese playbook'i loomine (1h)
- **Boonus:** Ansible Tower/AWX demo ja kasutamine

**Käsitletud Teemad:**
- Ansible arhitektuur ja SSH konfiguratsioon
- Kohalik testimine Vagrant/VirtualBox'iga
- Inventory haldamine ja ad-hoc käsud
- YAML süntaks ja põhilised playbook'id
- Esimesed automatiseerimise töövood
- Ansible Tower kasutajaliides

**Kodutööd:**
- **Ülesanne 1:** Paigalda LAMP stack kohalikult Vagrant VM'idega + palju näiteid
- **Ülesanne 2:** Loe Ansible arhitektuur, YAML ja moodulite ökosüsteem (3-4 tundi)
- **Lisapraktika:** Loo Ansible Tower projekt ja käivita playbook

---

### **Moodul 3: Docker Alused (5h)**

**Kontaktaja Struktuur:**
- Konteinerite kontseptsioonid vs VM'id (1h)
- Docker'i installimine ja esimene konteiner (1h)
- Dockerfile'i loomise töötuba (1.5h)
- Põhiline võrgustik ja helitugevused (1h)
- Docker Hub ja registrid (30 min)
- **Boonus:** Mitme-etapiline ehitus, turvalisus, edasijõudnud võrgustik

**Käsitletud Teemad:**
- Konteineritehnoloogia ülevaade
- Docker'i installimine ja põhilised käsud
- Dockerfile'i loomine ja parimad praktikad
- Docker'i võrgustik ja helitugevused
- Docker Hub ja privaatsed registrid
- Konteinerite turvalisus ja optimeerimine

**Kodutööd:**
- **Ülesanne 1:** Konteineriseeri mitu rakendust paljude näidetega
- **Ülesanne 2:** Loe Docker'i arhitektuur, turvalisus ja parimad praktikad (3-4 tundi)
- **Lisapraktika:** Loo privaatne Docker registry ja jagage konteinereid

---

### **Moodul 4: Docker Orkestratsioon (5h)**

**Kontaktaja Struktuur:**
- Mitme-konteineriga kontseptsioonid (1h)
- Compose faili loomine (1.5h)
- Mitme-teenusega rakenduse seadistus (1.5h)
- Kohalik orkestratsioon näidetega (1h)
- **Boonus:** Docker Swarm tutvustus ja põhilised kontseptsioonid

**Käsitletud Teemad:**
- Docker Compose süntaks ja kasutamine
- Mitme-konteineriga rakendused
- Keskkonna-spetsiifilised konfiguratsioonid
- Kohalikud arenduse töövood
- Docker Swarm ja klastri haldamine
- Orkestreerimise mustrid ja strateegiad

**Kodutööd:**
- **Ülesanne 1:** Paigalda full-stack rakendus kohalikult paljude teenuste näidetega
- **Ülesanne 2:** Loe konteinerite orkestreerimise mustreid ja strateegiaid (3-4 tundi)
- **Lisapraktika:** Loo lihtne Docker Swarm klastri ja käivita teenused

---

### **Moodul 5: Ansible Edasijõudnud (5h)**

**Kontaktaja Struktuur:**
- Muutujad ja Jinja2 mallid (1.5h)
- Käsitlejad ja veakäsitlemise strateegiad (1.5h)
- Ansible Vault turvalisuse labor (1h)
- Ansible Galaxy ja kogukond (1h)
- **Boonus:** Edasijõudnud playbook'id ja optimeerimine

**Käsitletud Teemad:**
- Muutujad ja Jinja2 mallid
- Käsitlejad ja veakäsitlemise strateegiad
- Ansible Vault saladuste haldamiseks
- Parimad praktikad ja optimeerimine
- Ansible Galaxy ja kogukonna rollid
- Edasijõudnud playbook'id ja mustrid

**Kodutööd:**
- **Ülesanne 1:** Lõpeta kõik iseseisva labori harjutused näidetega
- **Ülesanne 2:** Loe Jinja2 mallid, muutujad ja Vault turvalisus (3-4 tundi)
- **Lisapraktika:** Loo ja jagage oma Ansible Galaxy roll

---

### **Moodul 6: Ansible Rollid (5h)**

**Kontaktaja Struktuur:**
- Rolli loomise samm-sammuline juhend (1.5h)
- Rolli muutujate ja sõltuvuste labor (1.5h)
- Ansible Galaxy uurimine (1h)
- Puppet vs Ansible võrdlusharjutus (1h)
- **Boonus:** Rolli testimine ja valideerimine

**Käsitletud Teemad:**
- Ansible rollide struktuur ja parimad praktikad
- Rolli muutujad ja sõltuvused
- Ansible Galaxy kogukond
- Konfiguratsiooni haldamise võrdlus
- Rolli testimine ja valideerimine
- Rollide haldamine ja versioneerimine

**Kodutööd:**
- **Ülesanne 1:** Loo roll + Puppet võrdlus paljude näidetega
- **Ülesanne 2:** Loe rolli parimaid praktikaid ja Galaxy ökosüsteemi (3-4 tundi)
- **Lisapraktika:** Loo testid oma rollile ja valideeri seda

---

### **Moodul 7: Terraform Alused (5h)**

**Kontaktaja Struktuur:**
- Infrastructure as Code ülevaade (1h)
- Kohalik Terraform demo (failisüsteemi haldamine) (1.5h)
- Praktiline: Loo kohalik infrastruktuur (1.5h)
- Terraform Cloud demo (1h)
- **Boonus:** Moodulid, tööruumid, edasijõudnud mallid

**Käsitletud Teemad:**
- Terraform alused ja HCL keel
- Kohalikud providerid (failisüsteemi haldamine)
- State'i haldamise kontseptsioonid
- Infrastructure as Code põhimõtted
- Terraform Cloud ja remote state
- Moodulid ja tööruumid

**Kodutööd:**
- **Ülesanne 1:** Kohalik infrastruktuuriprojekt (failid, konfiguratsioon, skriptid) paljude näidetega
- **Ülesanne 2:** Loe IaC põhimõtteid ja Terraform mustreid (3-4 tundi)
- **Lisapraktika:** Loo Terraform Cloud tööruum ja remote state

---

### **Moodul 8: Terraform Edasijõudnud (5h)**

**Kontaktaja Struktuur:**
- Pilve ressursid ja providerid (1.5h)
- AWS/Azure põhilised ressursid (1.5h)
- Terraform Workspaces ja keskkonnad (1h)
- Turvalisus ja IAM (1h)
- **Boonus:** Edasijõudnud Terraform mustrid ja optimeerimine

**Käsitletud Teemad:**
- Pilve ressursid ja providerid
- AWS/Azure põhilised ressursid
- Terraform Workspaces ja keskkonnad
- Turvalisus ja IAM
- Edasijõudnud Terraform mustrid
- Optimeerimine ja parimad praktikad

**Kodutööd:**
- **Ülesanne 1:** Loo pilve infrastruktuur AWS/Azure'is
- **Ülesanne 2:** Loe pilve ressursid ja turvalisus (3-4 tundi)
- **Lisapraktika:** Loo mitme keskkonna Terraform konfiguratsioon

---

### **Moodul 9: Kubernetes Sügavõte (5h)**

**Kontaktaja Struktuur:**
- K8s arhitektuur ja kontseptsioonid (1.5h)
- Kohalik klastri haldamine (1.5h)
- Ressursside haldamine (1h)
- Helm charts tutvustus (1h)
- **Boonus:** Edasijõudnud K8s funktsioonid ja optimeerimine

**Käsitletud Teemad:**
- Kubernetes arhitektuur ja kontseptsioonid
- Kohalik klastri haldamine
- Ressursside haldamine ja skaleerimine
- Helm charts ja paketid
- Edasijõudnud K8s funktsioonid
- Optimeerimine ja parimad praktikad

**Kodutööd:**
- **Ülesanne 1:** Kohalik K8s klastri haldamine
- **Ülesanne 2:** Loe K8s arhitektuur ja ressursid (3-4 tundi)
- **Lisapraktika:** Loo ja kasuta Helm chart'i

---

### **Moodul 10: CI/CD Pipeline'id (5h)**

**Kontaktaja Struktuur:**
- CI/CD kontseptsioonid ja töövood (1h)
- GitHub Actions ja workflow'id (1.5h)
- Jenkins vs GitHub Actions võrdlus (1.5h)
- Täielik automatiseerimise pipeline (1h)
- **Boonus:** GitOps ja DevOps praktikad

**Käsitletud Teemad:**
- CI/CD kontseptsioonid ja töövood
- GitHub Actions ja workflow'id
- Jenkins vs GitHub Actions võrdlus
- Täielik automatiseerimise pipeline
- GitOps ja DevOps praktikad
- Pipeline optimeerimine ja turvalisus

**Kodutööd:**
- **Ülesanne 1:** Täielik automatiseerimise pipeline
- **Ülesanne 2:** Loe GitOps ja DevOps praktikad (3-4 tundi)
- **Lisapraktika:** Loo Jenkins pipeline ja võrdle seda GitHub Actions'iga

---

### **Moodul 11: Turvalisus ja Jälgimine (5h)**

**Kontaktaja Struktuur:**
- DevSecOps kontseptsioonid (1h)
- Turvalisuse skaneerimine (1.5h)
- Logide analüüs ja jälgimine (1.5h)
- Prometheus ja Grafana (1h)
- **Boonus:** Observability ja APM tööriistad

**Käsitletud Teemad:**
- DevSecOps kontseptsioonid
- Turvalisuse skaneerimine ja analüüs
- Logide analüüs ja jälgimine
- Prometheus ja Grafana
- Observability ja APM tööriistad
- Turvalisuse parimad praktikad

**Kodutööd:**
- **Ülesanne 1:** Turvalisuse skaneerimine ja logide analüüs
- **Ülesanne 2:** Loe DevSecOps ja observability (3-4 tundi)
- **Lisapraktika:** Loo Prometheus ja Grafana dashboard

---

### **Moodul 12: Lõpuprojekt ja Integratsioon (5h)**

**Kontaktaja Struktuur:**
- Projekti planeerimine ja arhitektuur (1h)
- Kõigi tööriistade integratsioon (2h)
- Projekti dokumentatsioon (1h)
- Esitlemine ja koodireview (1h)
- **Boonus:** Meeskonnatöö ja koodireview praktikad

**Käsitletud Teemad:**
- Projekti planeerimine ja arhitektuur
- Kõigi tööriistade integratsioon
- Projekti dokumentatsioon
- Esitlemine ja koodireview
- Meeskonnatöö ja koodireview praktikad
- Projekti haldamine ja versioneerimine

**Kodutööd:**
- **Ülesanne 1:** Kõigi tööriistade integratsioon
- **Ülesanne 2:** Projekti dokumentatsioon ja esitlemine (3-4 tundi)
- **Lisapraktika:** Tee koodireview ja saada tagasisidet

---

## 📁 Failide Struktuur

### Iga Moodul Sisaldab:
```
modul_nimi/
├── lecture.md              # Peamine loengumaterjal
├── lab.md                  # Praktilised harjutused
├── homework.md             # Praktiline ülesanne (Ülesanne 1)
├── reading_materials.md    # Teooria ja taust (Ülesanne 2)
└── additional_practice.md  # Lisapraktika ja boonusülesanded
```

### Võrdlusmaterjal (kui rakendatav):
```
modul_nimi/
├── reference/              # Kiired viited ja juhendid
├── examples/               # Koodinäited ja mallid
└── solutions/              # Lahendused ja selgitused
```

---

## 🎯 Õpieesmärgid

- **Põhjalik praktiline kogemus** kõigi automatiseerimise tööriistadega
- **Projektipõhise õppimise** lähenemine
- **Meeskonnatöö** oskused ja koodireview praktikad
- **Tööstuse standardid** ja parimad praktikad
- **Iseseisev õppimine** lugemiülesannete kaudu
- **Edasijõudnud kontseptsioonid** ja optimeerimine
- **Turvalisus ja jälgimine** DevOps kontekstis

---

## 📝 Hindamisstrateegia

- **Ülesanne 1:** Praktiline töö (hinnatakse funktsionaalsuse järgi)
- **Ülesanne 2:** Lugemise refleksioon (hinnatakse mõistmise järgi)
- **Lisapraktika:** Boonusülesanded ja edasijõudnud kontseptsioonid
- **Portfoolio:** GitHub repositoorium kogu tööga
- **Lõpuprojekt:** Kõigi tööriistade integratsioon ja dokumentatsioon
- **Meeskonnatöö:** Koodireview ja koostöö oskused

---

## 🔧 Seadistamise Juhendid

### **Enne kursuse alustamist:**
- **Windows kasutajad:** [Windows Seadistamise Juhend](WINDOWS_SETUP_GUIDE.md)
- **Linux/macOS kasutajad:** [Kodu Masina Ehitus Juhend](docker_orchestration/kodu_masina_ehitus_juhend.md)

### **Vajalikud tööriistad:**
- Git (versioonihaldus)
- Docker Desktop (konteinerid)
- Ansible (konfiguratsiooni haldamine)
- Terraform (infrastruktuuri kood)
- kubectl + Minikube (Kubernetes)
- VSCode (arenduskeskkond)
- AWS CLI (pilve ressursid)
- Azure CLI (pilve ressursid)

---

## 📊 Ajaplaneerimine

### **Kontaktõpe:** 60 tundi (12 moodulit × 5h)
### **Iseseisev õppimine:** 90 tundi (12 moodulit × 7.5h)
### **Kokku:** 150 tundi

### **Nädalaplaneerimine:**
- **Nädal 1-3:** Moodulid 1-3 (Git, Ansible, Docker)
- **Nädal 4-6:** Moodulid 4-6 (Docker Orkestratsioon, Ansible Edasijõudnud, Rollid)
- **Nädal 7-9:** Moodulid 7-9 (Terraform, Terraform Edasijõudnud, Kubernetes)
- **Nädal 10-12:** Moodulid 10-12 (CI/CD, Turvalisus, Lõpuprojekt)

---

## 🚀 Edasijõudnud Funktsioonid

- **Pilve integratsioon:** AWS, Azure, GCP
- **Turvalisus:** DevSecOps, skaneerimine, IAM
- **Jälgimine:** Prometheus, Grafana, ELK stack
- **Orkestreerimine:** Docker Swarm, Kubernetes
- **Automatiseerimine:** CI/CD, GitOps, Infrastructure as Code
