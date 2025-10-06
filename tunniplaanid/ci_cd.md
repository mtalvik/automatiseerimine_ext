# Tunnikava: CI/CD – Pidev Integratsioon ja Tarnimine (4×45 min) + 1.5h kodutöö

**Tase:** Keskmine (eelteadmised: Git, Docker, YAML)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`

---

## 🎯 Õpiväljundid
- ÕV1: Selgitab, mis on CI/CD ja miks see on vajalik; eristab CI vs CD
- ÕV2: Seadistab GitHub Actions/GitLab CI pipeline'i esimese job'iga
- ÕV3: Kirjutab YAML pipeline'e testide ja build'i jaoks
- ÕV4: Automatiseerib Docker image build'i ja push'i registrisse
- ÕV5: Rakendab põhilisi best practices'eid (secrets, caching, parallel jobs)

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased teavad käsitsi deploy'imist – ehita CI/CD sellele
2. **Arusaamine:** Õpeta MIKS automatiseerimine on vajalik
3. **Metakognitsioon:** Pipeline debug = õppimine vigadest

---

## 🛠️ Õpetamismeetodid

| Meetod | Kirjeldus | Millal |
|--------|-----------|--------|
| **Passiivne** | Loeng, demo | Blokk 1 (≤15 min) |
| **Aktiivne** | Pipeline kirjutamine | Lab (3×45 min) |
| **Interaktiivne** | Paaristöö debug | Iga blokk lõpus |

---

## 👨‍🏫 Näpunäited

### Enne tundi:
- [ ] GitHub/GitLab konto olemas
- [ ] Näidis repo valmis
- [ ] Actions/CI on enabled

### Tunni ajal:
- **Pipeline ebaõnnestub PALJU:** See on normaalne! Õppimine vigadest
- **YAML indentation JÄLLE:** Sama probleem kui Ansible/K8s
- **Secrets setup:** GitHub Secrets on kriitiline Docker Hub jaoks
- **Pipeline võtab aega:** Esimene run 2-5 min

### Troubleshooting:
- **"Syntax error":** YAML indentation
- **"Permission denied":** Secrets pole õigesti seadistatud
- **"Image not found":** Vale Docker Hub repo nimi
- **"Job failed":** Vaata logs – tavaliselt test fail või build error

---

## Blokk 1 (45 min) – CI/CD põhitõed ja esimene pipeline

- **Eesmärk:** Mõista CI/CD vajadust, luua esimene GitHub Actions workflow
- **Meetodid:** mini-loeng (≤15 min), demo, juhendatud praktika
- **Minutiplaan:**
  - 0–5: "Kui tüütu on deploy'ida käsitsi 10× päevas?"
  - 5–15: CI/CD kontseptsioonid (commit → test → build → deploy)
  - 15–25: Demo: esimene `.github/workflows/ci.yml`, push, vaata run'i
  - 25–45: Lab: õpilased loovad esimese workflow'i (hello world)
- **Kontrollnimekiri:**
  - [ ] GitHub Actions enabled
  - [ ] Esimene workflow fail loodud
  - [ ] Pipeline käivitus edukalt
- **Refleksioon:** "Kuidas CI/CD võiks su aega säästa?"

---

## Blokk 2 (45 min) – Testide ja build'i automatiseerimine

- **Eesmärk:** Lisada testid ja build pipeline'i
- **Minutiplaan:**
  - 0–10: Tests + build demo (Python/Node näide)
  - 10–35: Lab: lisa tests (pytest/jest), build (Docker)
  - 35–45: Paariskontroll + refleksioon
- **Kontrollküsimused:** "Miks testid enne build'i?"

---

## Blokk 3 (45 min) – Docker image build ja registry push

- **Eesmärk:** Automatiseerida Docker image build ja push Docker Hub'i
- **Minutiplaan:**
  - 0–15: Docker build in CI demo, secrets setup
  - 15–40: Lab: build image, push Docker Hub'i, testi pull
  - 40–45: Refleksioon
- **Kontrollküsimused:** "Miks secrets, mitte hardcoded passwords?"

---

## Blokk 4 (45 min) – Best practices ja troubleshooting

- **Eesmärk:** Optimeerida pipeline'e, debugida probleeme
- **Minutiplaan:**
  - 0–20: Caching, parallel jobs, matrix builds demo
  - 20–40: Lab: optimeeri oma pipeline (cache, parallel)
  - 40–45: Quiz + kodutöö
- **Kontrollküsimused:** "Kuidas pipeline'i kiiremaks teha?"

---

## Kodutöö (1.5h)

- **Ülesanne:** Loo täielik CI/CD pipeline Python/Node projektile
- **Kriteeriumid:**
  - [ ] Tests run automatically
  - [ ] Docker image build ja push
  - [ ] Badge README.md's
  - [ ] README refleksiooniga

---

## 📖 Viited

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitLab CI Docs**: https://docs.gitlab.com/ee/ci/
- **Pedagoogika**: NRC (2000) *How People Learn*

---

## 🎓 Kokkuvõte

**Teha:**
- ✅ Näita, kui tüütu käsitsi deploy on
- ✅ Lase pipeline'il faili'da – õppimine!
- ✅ Alusta lihtsast (hello world)
- ✅ GitHub Actions (kõige lihtsam!)

**Mitte teha:**
- ❌ Jenkins kohe (liiga keeruline!)
- ❌ 50 stage'i pipeline
- ❌ Production deploy (too risky!)

