# Lõpuprojekt: DevOps Integratsioon

**Kestus:** 4 tundi  
**Teemad:** Projekti planeerimine, arhitektuur, integratsioon, dokumentatsioon, esitlus

---

## 🎯 Õpiväljundid

Pärast seda loengut oskate:
- Planeerida täielikku DevOps infrastruktuuri
- Integreerida kõiki õpitud tööriistu ühes projektis
- Dokumenteerida arhitektuuri ja tehnilisi otsuseid
- Esitleda projekti professionaalselt
- Teha koodireview'd teiste projektidele

---

## 📖 Projekti Ülevaade

### Mis on lõpuprojekt?

Lõpuprojekt on praktiline töö, kus integreerite kõiki õpitud DevOps tööriistu ühes päris projektis. See ei ole lihtsalt kodutöö, vaid professionaalne projekt, mis demonstreerib teie oskusi.

### Projekti eesmärgid

- **Integratsioon:** Kasutada kõiki õpitud tööriistu koos
- **Praktika:** Rakendada teadmisi päris projektis
- **Dokumentatsioon:** Luua professionaalne dokumentatsioon
- **Esitlus:** Õppida esitlema tehnilisi lahendusi
- **Koostöö:** Töötada meeskonnas ja teha koodireview'd

---

## 📋 Projekti Nõuded

### Kohustuslikud komponendid

**1. Git Version Control** (kõigile)
- Repository struktuur
- Branch'ide haldamine
- Commit'ide kvaliteet

**2. Vali 2-3 tööriista** (vali endale sobivad):

**Valik A: Docker + Kubernetes**
- Rakenduse konteineriseerimine
- Kubernetes deployment
- CI/CD pipeline

**Valik B: Terraform + Ansible**
- Infrastruktuuri automatiseerimine
- Serverite konfigureerimine
- Deployment automatiseerimine

**Valik C: Docker + CI/CD**
- Konteineriseerimine
- Automatiseeritud build ja deploy
- Testimine

**Valik D: Kubernetes + Monitoring**
- Rakenduse orkestreerimine
- Monitoring ja alerting
- Scaling

### Valikulised komponendid (boonus)

- **Monitoring:** Prometheus, Grafana
- **Security:** Vulnerability scanning
- **Backup:** Automated backups
- **Documentation:** API docs, runbooks

---

## 🎯 Projekti Valikud

### Valik 1: Lihtne Veebirakendus

**Kirjeldus:** Lihtne veebirakendus (blog, todo, portfolio)

**Komponendid:**
- Frontend (HTML/CSS/JS või React)
- Backend API (Node.js/Python)
- Andmebaas (SQLite/PostgreSQL)

**Vali 2-3 tööriista:**
- Docker (konteineriseerimine)
- Kubernetes (deployment)
- CI/CD (automatiseerimine)

### Valik 2: API Teenus

**Kirjeldus:** REST API teenus (kasutajad, tooted, andmed)

**Komponendid:**
- API server (Node.js/Python)
- Andmebaas
- Dokumentatsioon

**Vali 2-3 tööriista:**
- Docker (konteineriseerimine)
- Terraform (infrastruktuur)
- Ansible (konfiguratsioon)

### Valik 3: Monitoring Dashboard

**Kirjeldus:** Lihtne monitoring dashboard

**Komponendid:**
- Dashboard (React/Vue.js)
- Data API
- Andmebaas

**Vali 2-3 tööriista:**
- Kubernetes (deployment)
- Monitoring (Prometheus/Grafana)
- CI/CD (automatiseerimine)

---

## 📊 Projekti Struktuur

### 1. Planeerimine (1 nädal)

**Sisaldab:**
- Projekti valik ja põhjendus
- Arhitektuuri kavandamine
- Tehniliste otsuste dokumenteerimine
- Timeline ja milestone'id
- Ressursside planeerimine

**Tulemused:**
- Projekti kirjeldus
- Arhitektuuridiagramm
- Tehniliste otsuste dokument
- Projektplaan

### 2. Arendamine (2-3 nädalat)

**Sisaldab:**
- Infrastruktuuri loomine
- Rakenduse arendamine
- CI/CD pipeline seadistamine
- Testimine ja optimeerimine
- Dokumentatsiooni kirjutamine

**Tulemused:**
- Töötav rakendus
- Automatiseeritud deployment
- Testide kogum
- Tehniline dokumentatsioon

### 3. Esitlus (1 nädal)

**Sisaldab:**
- Projekti demo
- Arhitektuuri esitlus
- Tehniliste otsuste selgitus
- Koodireview teiste projektidele
- Tagasiside ja refleksioon

**Tulemused:**
- Esitlus (15-20 min)
- Demo (10-15 min)
- Koodireview (2-3 projekti)
- Refleksiooni dokument

---

## 🛠️ Tehnilised Nõuded

### Repository struktuur

```
lopuprojekt/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── decisions.md
│   └── deployment.md
├── infrastructure/
│   ├── terraform/
│   └── ansible/
├── application/
│   ├── frontend/
│   ├── backend/
│   └── docker/
├── kubernetes/
├── ci-cd/
└── monitoring/
```

### Dokumentatsiooni nõuded

**README.md:**
- Projekti kirjeldus
- Kiire alustamine
- Deploy'imise juhend
- API dokumentatsioon

**Architecture.md:**
- Süsteemi ülevaade
- Komponentide kirjeldus
- Andmevoog
- Turvalisuse aspektid

**Decisions.md:**
- Tehniliste otsuste põhjendused
- Alternatiivide võrdlus
- Kompromissid ja piirangud

---

## 📈 Hindamiskriteeriumid

### Funktsionaalsus (30%)

- [ ] Kõik komponendid töötavad
- [ ] CI/CD pipeline töötab
- [ ] Rakendus on deploy'itud
- [ ] Monitoring on seadistatud

### Tehniline kvaliteet (25%)

- [ ] Kood on puhas ja kommenteeritud
- [ ] Best practices on rakendatud
- [ ] Turvalisus on arvestatud
- [ ] Performance on optimeeritud

### Dokumentatsioon (20%)

- [ ] README on täielik
- [ ] Arhitektuur on dokumenteeritud
- [ ] Deploy'imise juhend on selge
- [ ] API on dokumenteeritud

### Integratsioon (15%)

- [ ] Kõik tööriistad on integreeritud
- [ ] Automatiseerimine on täielik
- [ ] Monitoring ja alerting töötab
- [ ] Backup ja recovery on seadistatud

### Esitlus (10%)

- [ ] Demo on sujuv
- [ ] Arhitektuur on selgitatud
- [ ] Küsimustele vastatakse
- [ ] Koodireview on kvaliteetne

---

## 📊 Hindamine

### Hindamiskriteeriumid

**1. Funktsionaalsus (40%)**
- Rakendus töötab
- Valitud tööriistad on kasutatud
- Basic error handling

**2. Tehniline kvaliteet (30%)**
- Koodi kvaliteet
- Tööriistade õige kasutamine
- Best practices

**3. Dokumentatsioon (20%)**
- README kvaliteet
- Deployment guide
- Tööriistade selgitus

**4. Esitlus (10%)**
- Selge esitlus
- Demo kvaliteet
- Vastused küsimustele

### Hinded

- **5 (väga hea):** Kõik valitud tööriistad hästi kasutatud, lisafunktsioonid
- **4 (hea):** Valitud tööriistad kasutatud, vähesed vead
- **3 (rahuldav):** Enamik valitud tööriistu kasutatud
- **2 (halb):** Vähem kui 2 tööriista kasutatud
- **1 (väga halb):** Projekt ei tööta

---

## 🎯 Järgmised sammud

1. **Valige projekt** - Mõelge, mis teid huvitab
2. **Planeerige arhitektuur** - Joonistage diagramm
3. **Alustage arendamist** - Loo repository
4. **Dokumenteerige** - Kirjutage kõik üles
5. **Testige** - Veenduge, et kõik töötab
6. **Esitage** - Valmistage demo ette

**Edu projekti tegemisel!** 🚀
