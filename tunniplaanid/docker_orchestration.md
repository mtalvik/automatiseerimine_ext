# Tunnikava: Docker Compose – Mitme Konteineri Orkestreerim ine (4×45 min) + 1.5h kodutöö

**Tase:** Keskmine (eelteadmised: Docker Basics, YAML, võrgustik)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`

---

## 🎯 Õpiväljundid
- ÕV1: Selgitab, mis probleemi Docker Compose lahendab (mitme container'i haldamine)
- ÕV2: Kirjutab `docker-compose.yml` faili mitme teenuse jaoks
- ÕV3: Kasutab networks ja volumes Compose'is
- ÕV4: Haldab multi-container rakendusi (`up`, `down`, `logs`, `ps`)
- ÕV5: Rakendab best practices'eid (environment variables, health checks)

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased teavad `docker run` – Compose on parem
2. **Arusaamine:** Õpeta MIKS käsk käsu järel on tüütu
3. **Metakognitsioon:** Declarative vs imperative

---

## 🛠️ Õpetamismeetodid

| Meetod | Kirjeldus | Millal |
|--------|-----------|--------|
| **Passiivne** | Loeng, demo | Blokk 1 (≤15 min) |
| **Aktiivne** | Compose file kirjutamine | Lab (3×45 min) |
| **Interaktiivne** | Paaristöö debug | Iga blokk lõpus |

---

## 👨‍🏫 Näpunäited

### Enne tundi:
- [ ] Docker Compose installeeritud (`docker-compose --version`)
- [ ] Näidis `docker-compose.yml` valmis
- [ ] Multi-container probleem selge

### Tunni ajal:
- **YAML indentation JÄLLE!**
- **Networks auto-create:** Compose loob automaatselt
- **depends_on != wait_for_healthy:** Oluline erinevus!
- **Volumes persist:** Pärast `down` andmed jäävad

### Troubleshooting:
- **"Service X not found":** Vale service nimi
- **"Port already allocated":** Teine container kasutab
- **"Connection refused":** Service pole valmis – lisa healthcheck

---

## Blokk 1 (45 min) – Docker Compose põhitõed ja esimene stack

- **Eesmärk:** Mõista Compose vajadust, kirjutada esimene `docker-compose.yml`
- **Minutiplaan:**
  - 0–5: "Kui tüütu on 5× `docker run` käsku?"
  - 5–15: Compose vs käsud, YAML struktuur
  - 15–25: Demo: web + db compose file, `docker-compose up`
  - 25–45: Lab: loo esimene 2-service stack
- **Refleksioon:** "Kuidas Compose lihtsustab su elu?"

---

## Blokk 2 (45 min) – Networks ja service discovery

- **Eesmärk:** Mõista, kuidas container'id suhtlevad Compose'is
- **Minutiplaan:**
  - 0–10: Networks demo (auto-create, DNS)
  - 10–35: Lab: test service-to-service communication
  - 35–45: Paariskontroll
- **Kontrollküsimused:** "Kuidas web leiab db container'i?"

---

## Blokk 3 (45 min) – Volumes ja andmete püsivus

- **Eesmärk:** Kasutada volumes andmete säilitamiseks
- **Minutiplaan:**
  - 0–15: Volumes demo (named vs anonymous)
  - 15–40: Lab: lisa volumes DB jaoks, test persistence
  - 40–45: Refleksioon

---

## Blokk 4 (45 min) – Environment variables ja best practices

- **Eesmärk:** Parameetriseerida Compose environment'idega
- **Minutiplaan:**
  - 0–20: `.env` file, `env_file`, health checks demo
  - 20–40: Lab: lisa env vars, health checks
  - 40–45: Quiz + kodutöö

---

## Kodutöö (1.5h)

- **Ülesanne:** Loo 3-tier web app Compose'iga (nginx + API + PostgreSQL)
- **Kriteeriumid:**
  - [ ] 3 services `docker-compose.yml`'is
  - [ ] Networks ja volumes õigesti
  - [ ] `.env` file parameetritele
  - [ ] README refleksiooniga

---

## 📖 Viited

- **Docker Compose Docs**: https://docs.docker.com/compose/
- **Compose Best Practices**: https://docs.docker.com/compose/production/
- **Pedagoogika**: NRC (2000) *How People Learn*

---

## 🎓 Kokkuvõte

**Teha:**
- ✅ Näita 5× `docker run` vs 1× `docker-compose up`
- ✅ Networks auto-create on maagia!
- ✅ Health checks, mitte ainult `depends_on`
- ✅ `.env` file secrets jaoks

**Mitte teha:**
- ❌ Production deploy (see on Kubernetes!)
- ❌ 10 services korraga
- ❌ Swarm mode (too advanced)

