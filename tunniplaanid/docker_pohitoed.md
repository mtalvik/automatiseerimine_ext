# Tunnikava: Docker – Konteinerite Põhitõed (4×45 min) + 1.5h kodutöö

**Tase:** Põhitase (eelteadmised: põhiline käsurida, Git)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`

---

## 🎯 Õpiväljundid (Learning Outcomes)
- ÕV1: Selgitab, mis probleemi Docker lahendab; eristab container'eid VM'idest
- ÕV2: Käivitab konteinereid, kasutab `docker run`, `ps`, `logs`, `exec` käske
- ÕV3: Kirjutab lihtsa Dockerfile'i ja ehitab image'i
- ÕV4: Kasutab volume'e andmete säilitamiseks ja ports'e võrgustikuks
- ÕV5: Rakendab põhilisi best practices'eid (`.dockerignore`, multi-stage, cache)

---

## 📚 Pedagoogiline raamistik (allikas: "How People Learn", NRC 2000)

### Kolm põhiprintsiipi, mida see tunnikava järgib:

1. **Eelteadmised (Prior Knowledge):**
   - Õpilased teavad "Works on My Machine" probleemi (isiklik kogemus)
   - ALATI küsi enne õpetamist: "Kas oled kunagi kogenud, et kood töötab sul, aga sõbral mitte?"
   - Ehita uus teadmine olemasoleva peale (VM → container analoogia)

2. **Arusaamine > memoriseerimine (Understanding > Facts):**
   - Õpeta MIKS Docker on vajalik, mitte ainult KUIDAS käske kasutada
   - Vähem käske, rohkem sügavust (5-6 core concepts vs 20+ commands)
   - Kontseptsioonid > käsud (image vs container, immutability, layering)

3. **Metakognitsioon (Metacognition):**
   - Õpilased peavad jälgima oma õppimist
   - Refleksioonid iga bloki lõpus (1-2 min)
   - Kontrollküsimused: "Miks kasutada volume? Millal build uuesti?"

---

## 🛠️ Õpetamismeetodid (Teaching Methods)

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|----------------|
| **Passiivne** | Loeng, demo (õpetaja näitab) | Blokk 1 algus (≤15 min) |
| **Aktiivne** | Õpilane teeb ise (guided practice) | Enamik lab'i aega (3×45 min) |
| **Interaktiivne** | Paaristöö, arutelu, selgitamine | Iga bloki lõpp (peer review) |
| **Think-aloud** | Õpetaja mõtleb valjusti (model thinking) | Demo ajal (Dockerfile build) |
| **Formatiivne** | Kontroll ilma hindeta (checklists) | Iga blokk (low-stakes) |

---

## 👨‍🏫 Näpunäited algajale õpetajale

### Enne tundi:
- [ ] Kontrolli, kas Docker on kõigil installeeritud (`docker --version`)
- [ ] Valmista ette näidis-Dockerfile (et ei peaks tunnis tühjalt lehelt alustama)
- [ ] Pull'i ette populaarsed image'd (`nginx`, `alpine`, `python:3.9-slim`)
- [ ] Testi, et Docker töötab (`docker run hello-world`)
- [ ] Macil: Docker Desktop peab töötama; Linuxil: docker daemon

### Tunni ajal:
- **Image download võtab aega:** Esimesel `docker run` korral võib võtta 10-30s (normaalne!)
- **"Miks pull?" on hea küsimus:** Selgita, et Docker laeb image'd Docker Hub'ist
- **Container nimed võivad konfliktsid:** Kasuta `--name` või `docker rm` vana
- **Port conflicts:** Kui port 8080 on hõivatud, kasuta 8081, 8082 jne
- **Cache demo on võimas:** Build Dockerfile 2× – näita, kui kiire cache on!

### Kui midagi läheb valesti:
- **"Permission denied":** Linux/Mac vajab `sudo` või lisada kasutaja docker gruppi
- **"Cannot connect to Docker daemon":** Docker Desktop ei tööta (macOS/Windows)
- **"Port already allocated":** Teine container kasutab sama porti → `docker ps` ja `docker stop`
- **"No such image":** Image'i nimi on vale või pole pull'itud → kontrolli `docker images`

---

## Blokk 1 (45 min) – Loeng ja Lab I: Docker põhitõed ja esimesed container'id

- **Eesmärk:** Mõista, miks Docker on vajalik, käivitada esimesed container'id
- **Meetodid:** mini-loeng (≤15 min), think-aloud demo, juhendatud praktika
- **Minutiplaan:**
  - 0–5: Eelteadmised (kiirkirjutus "Kas oled kogenud 'töötab mul, aga sõbral mitte'?")
  - 5–15: Põhimõisted (container vs VM, image vs container, Docker Hub) ja MIKS Docker
  - 15–25: Demo (think-aloud): `docker run hello-world`, `docker run nginx`, port mapping selgitus
  - 25–45: Juhendatud praktika: õpilased käivitavad nginx, alpine, vaatavad logs'e (Lab Samm 1)
- **Kontrollnimekiri:**
  - [ ] Docker töötab (`docker --version`)
  - [ ] Käivitatud vähemalt 2 erinevat container'it (hello-world, nginx)
  - [ ] Mõistab image vs container erinevust (küsi: "Mis on image?")
- **Refleksioon (1–2 min):** "Mis oli kõige üllatavam Docker'i kohta? Kui kiire see oli?"
- **Fun Poll:** "Kui Docker oleks sõiduk, siis milline? A) auto B) rongi vagun C) helikopter 🚁"
- **Kohandus:** Kui kiired, lisa `docker exec -it` tutvustus; kui aeglane, keskendu ainult `docker run`

---

## Blokk 2 (45 min) – Lab II: Container'ide haldamine ja interaktiivsus

- **Eesmärk:** Hallata container'eid, siseneda töötavatesse container'itesse, mõista käske
- **Meetodid:** lühidemo + iseseisev praktika, paariskontroll
- **Minutiplaan:**
  - 0–10: Demo: `docker ps`, `docker logs`, `docker stop/start/rm`, `docker exec -it`
  - 10–35: Juhendatud praktika: õpilased käivitavad Alpine container'i, sisenevad, uurivad (Lab Samm 2)
  - 35–40: Interaktiivne shell (`docker exec -it alpine sh`), fail loomine, container kustutamine
  - 40–45: Paariskontroll: selgita partnerile, mis vahe on `docker stop` ja `docker rm` vahel
- **Kontrollnimekiri:**
  - [ ] Oskab vaadata töötavaid container'eid (`docker ps`)
  - [ ] Oskab siseneda container'isse (`docker exec -it`)
  - [ ] Mõistab, et container on ajutine (pärast `rm` kaob andmed)
- **Kontrollküsimused:** "Miks kaovad failid pärast `docker rm`?" "Kuidas säilitada andmeid?"
- **Refleksioon (1–2 min):** "Kujuta ette, et container on hotellituba. Mis juhtub pärast checkout'i?"
- **Kohandus:** Kui kiired, tutvusta volume'e juba siin; kui aeglane, jäta `exec` valikuliseks

---

## Blokk 3 (45 min) – Lab III: Dockerfile ja image'ide loomine

- **Eesmärk:** Kirjutada esimene Dockerfile, ehitada image, mõista layer'eid ja cache'i
- **Meetodid:** demo + juhendatud praktika, iseseisev töö
- **Minutiplaan:**
  - 0–10: Dockerfile demo: `FROM`, `COPY`, `RUN`, `CMD` selgitus + think-aloud (Lab Samm 3)
  - 10–30: Juhendatud praktika: õpilased kirjutavad Dockerfile'i Python/Node rakendusele, build'ivad
  - 30–40: Cache demo: build 2× sama Dockerfile – näita, kui kiire cache on! Muuda 1 rida – näita rebuild
  - 40–45: Refleksioon ja kokkuvõte
- **Kontrollnimekiri:**
  - [ ] Dockerfile on loodud (vähemalt FROM, COPY, CMD)
  - [ ] Image on edukalt build'itud (`docker build -t minu-app .`)
  - [ ] Container töötab image'ist (`docker run minu-app`)
- **Kontrollküsimused:** "Mis on layer? Miks cache on oluline?"
- **Refleksioon (1–2 min):** "Dockerfile on nagu retsept. Mis on kõige tähtsam osa retseptis?"
- **Kohandus:** Kui kiired, lisa multi-stage build demo; kui aeg otsa, jäta cache selgitus kodutööks

---

## Blokk 4 (45 min) – Lab IV: Volumes, Networks ja Best Practices

- **Eesmärk:** Kasutada volume'e andmete säilitamiseks, mõista võrgustikku, rakendada best practices
- **Meetodid:** demo + praktika, näited (hea vs halb), viktoriin
- **Minutiplaan:**
  - 0–15: Volume demo: `-v` flag, andmete säilimine pärast `docker rm` (Lab Samm 4)
  - 15–30: Juhendatud praktika: loo volume, mount andmebaasi, kontrolli andmete säilimist
  - 30–40: Best practices: `.dockerignore`, väiksemad image'd, multi-stage (näited)
  - 40–45: Docker Quiz (lõbus viktoriin) + kodutöö tutvustus
- **Kontrollnimekiri:**
  - [ ] Volume on loodud ja töötab
  - [ ] Andmed säilivad pärast container'i kustutamist
  - [ ] Mõistab `.dockerignore` otstarvet
- **Kontrollküsimused:** "Millal kasutada volume? Mida `.dockerignore` teeb?"
- **Refleksioon (1–2 min):** "Mida teeksid järgmisel korral teisiti? Mis oli kõige kasulikum?"
- **Kohandus:** Kui kiired, tutvusta Docker Compose; kui aeg napib, jäta networks valikuliseks

---

## Kodutöö (1.5h, isetempoline)

- **Ülesanne:** Ehita Flask/Node chat bot Docker container'is; kirjuta Dockerfile; kasuta volume'e
- **Kriteeriumid:**
  - [ ] Dockerfile on olemas ja töötab
  - [ ] Image build'ub ilma vigadeta
  - [ ] Container töötab ja on ligipääsetav (port mapping)
  - [ ] `.dockerignore` on olemas
  - [ ] README.md sisaldab käivitamisjuhendit
- **Oluline:** Refleksioon README.md lõpus (5 küsimust, 2-3 lauset igaüks) – see on metakognitsioon praktikas!
- **Esitamine:** GitHub repo link (Dockerfile, kood, README)

---

## 📖 Viited ja täiendav lugemine (õpetajale)

### Pedagoogilised alused:
1. **National Research Council (2000).** *How People Learn: Brain, Mind, Experience, and School.* Washington, DC: The National Academies Press.
   - Peatükk 1: "Learning: From Speculation to Science" – eelteadmised, arusaamine, metakognitsioon
   - Peatükk 2: "How Experts Differ from Novices" – miks arusaamine > meeldejätmine

2. **Bransford, J., & Schwartz, D. (1999).** "Rethinking Transfer: A Simple Proposal with Multiple Implications." *Review of Research in Education, 24*, 61-100.
   - Transfer = õpilased kannavad teadmisi üle uutesse olukordadesse (refleksioon aitab!)

3. **Black, P., & Wiliam, D. (1998).** "Assessment and Classroom Learning." *Assessment in Education, 5*(1), 7-74.
   - Formatiivne hindamine = feedback ilma hindeta (checklists, peer review)

### Docker-spetsiifilised ressursid:
- **Docker Documentation**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Play with Docker** (brauseris): https://labs.play-with-docker.com/

### Õpetamise strateegiad:
- **Think-Aloud Protocol**: Verbaliseeri oma mõtteprotsess build ajal ("Hmm, build ebaõnnestus... proovin `docker logs`")
- **Reciprocal Teaching**: Õpilased õpetavad üksteist (pair-check)
- **Metacognitive Prompts**: "Mis oli raske? Kuidas lahendada? Mida teeksid teisiti?"

---

## 🎓 Kokkuvõte (TL;DR algajale õpetajale)

**Mida teha:**
1. ✅ Alusta eelteadmistega ("Works on my machine" probleem)
2. ✅ Õpeta MIKS Docker on vajalik (mitte ainult KUIDAS)
3. ✅ Maksimaalselt 15 min loengut, ülejäänu praktika
4. ✅ Cache demo on WOW-moment (build 2×, näita kiirust)
5. ✅ Pair-check (õpilased selgitavad üksteisele image vs container)
6. ✅ Formatiivne hindamine (checklists, no grades)

**Mida MITTE teha:**
1. ❌ Ära õpeta 20 käsku – keskendu 5-6 kontseptsioonile (run, build, ps, logs, exec, volume)
2. ❌ Ära loengi 45 minutit – õpilased vajavad tegemist
3. ❌ Ära eelda, et kõik Docker image'd on kohe cache'is – esimene pull võtab aega!
4. ❌ Ära unusta port conflicts – õpilased võivad kasutada sama porti
5. ❌ Ära hüppa Docker Compose'i – see on järgmine moodul!

**Edu!** 🚀 Kui küsimusi, vaata `loeng.md`, `labor.md`, `kodutoo.md` – seal on kõik välja kirjutatud.

