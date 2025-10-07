# Tunnikava: Docker

**Kestus:** 4 x 45 min + 1.5h kodutöö  
**Tase:** Põhitase  
**Eeldused:** Põhiline käsurida, Git  
**Materjalid:** loeng.md, labor.md, kodutoo.md, lisapraktika.md

---

## Õpiväljundid

Pärast moodulit õpilane:
- ÕV1: Selgitab, mis probleemi Docker lahendab; eristab container'eid VM'idest
- ÕV2: Käivitab konteinereid, kasutab `docker run`, `ps`, `logs`, `exec` käske
- ÕV3: Kirjutab lihtsa Dockerfile'i ja ehitab image'i
- ÕV4: Kasutab volume'e andmete säilitamiseks ja porte võrgustikuks
- ÕV5: Rakendab põhilisi best practices'eid (.dockerignore, multi-stage, cache)

---

## Pedagoogiline Raamistik

### Põhiprintsiibid (allikas: "How People Learn", NRC 2000)

**1. Eelteadmised (Prior Knowledge):**
- Õpilased teavad "Works on My Machine" probleemi isiklikust kogemusest
- Alati küsi enne õpetamist: "Kas oled kunagi kogenud, et kood töötab sul, aga sõbral mitte?"
- Ehita uus teadmine olemasoleva peale (VM → container analoogia)

**2. Arusaamine > memoriseerimine:**
- Õpeta miks Docker on vajalik, mitte ainult kuidas käske kasutada
- Vähem käske, rohkem sügavust (5-6 core concepts vs 20+ commands)
- Kontseptsioonid > käsud (image vs container, immutability, layering)

**3. Metakognitsioon:**
- Õpilased peavad jälgima oma õppimist
- Refleksioonid iga bloki lõpus (1-2 min)
- Kontrollküsimused: "Miks kasutada volume? Millal build uuesti?"

---

## Õpetamismeetodid

| Meetod | Kirjeldus | Millal Kasutada |
|--------|-----------|-----------------|
| **Passiivne** | Loeng, demo (õpetaja näitab) | Blokk 1 algus (max 15 min) |
| **Aktiivne** | Õpilane teeb ise (guided practice) | Enamik lab'i aega (3 x 45 min) |
| **Interaktiivne** | Paaristöö, arutelu, selgitamine | Iga bloki lõpp (peer review) |
| **Think-aloud** | Õpetaja mõtleb valjusti (model thinking) | Demo ajal (Dockerfile build) |
| **Formatiivne** | Kontroll ilma hindeta (checklists) | Iga blokk (low-stakes) |

---

## Näpunäited Algajale Õpetajale

### Enne Tundi

- [ ] Kontrolli, kas Docker on kõigil installitud (`docker --version`)
- [ ] Valmista ette näidis-Dockerfile (et ei peaks tunnis tühjalt lehelt alustama)
- [ ] Pull'i ette populaarsed image'd (`nginx`, `alpine`, `python:3.11-alpine`)
- [ ] Testi, et Docker töötab (`docker run hello-world`)
- [ ] Mac'il: Docker Desktop peab töötama; Linux'il: docker daemon

### Tunni Ajal

**Image download võtab aega:** Esimesel `docker run` korral võib võtta 10-30s (normaalne)

**"Miks pull?" on hea küsimus:** Selgita, et Docker laeb image'd Docker Hub'ist

**Container nimed võivad konfliktsid:** Kasuta `--name` või `docker rm` vana

**Port conflicts:** Kui port 8080 on hõivatud, kasuta 8081, 8082 jne

**Cache demo on võimas:** Build Dockerfile kaks korda - näita, kui kiire cache on

### Kui Midagi Läheb Valesti

**"Permission denied":** Linux/Mac vajab `sudo` või lisada kasutaja docker gruppi

**"Cannot connect to Docker daemon":** Docker Desktop ei tööta (macOS/Windows)

**"Port already allocated":** Teine container kasutab sama porti → `docker ps` ja `docker stop`

**"No such image":** Image'i nimi on vale või pole pull'itud → kontrolli `docker images`

---

## 1. Loeng ja Lab: Docker Põhitõed ja Esimesed Container'id

**Aeg:** 45 min  
**Eesmärk:** Mõista, miks Docker on vajalik, käivitada esimesed container'id  
**Meetodid:** Mini-loeng (max 15 min), think-aloud demo, juhendatud praktika

### Minutiplaan

**0-5 min:** Eelteadmised  
Kiirkirjutus: "Kas oled kogenud 'töötab mul, aga sõbral mitte'?"

**5-15 min:** Põhimõisted  
Container vs VM, image vs container, Docker Hub. Fookus: miks Docker.

**15-25 min:** Demo (think-aloud)  
`docker run hello-world`, `docker run nginx`, port mapping selgitus

**25-45 min:** Juhendatud praktika  
Õpilased käivitavad nginx, alpine, vaatavad logisid (labor.md)

### Kontrollnimekiri

- [ ] Docker töötab (`docker --version`)
- [ ] Käivitatud vähemalt 2 erinevat container'it (hello-world, nginx)
- [ ] Mõistab image vs container erinevust (küsi: "Mis on image?")

### Refleksioon

1-2 minutit: "Mis oli kõige üllatavam Docker'i kohta? Kui kiire see oli?"

### Kohandus

**Kui kiired:** Lisa `docker exec -it` tutvustus  
**Kui aeglane:** Keskendu ainult `docker run`

---

## 2. Lab: Container'ide Haldamine ja Interaktiivsus

**Aeg:** 45 min  
**Eesmärk:** Hallata container'eid, siseneda töötavatesse container'itesse  
**Meetodod:** Lühidemo + iseseisev praktika, paariskontroll

### Minutiplaan

**0-10 min:** Demo  
`docker ps`, `docker logs`, `docker stop/start/rm`, `docker exec -it`

**10-35 min:** Juhendatud praktika  
Õpilased käivitavad Alpine container'i, sisenevad, uurivad (labor.md)

**35-40 min:** Interaktiivne shell  
`docker exec -it alpine sh`, faili loomine, container kustutamine

**40-45 min:** Paariskontroll  
Selgita partnerile, mis vahe on `docker stop` ja `docker rm` vahel

### Kontrollnimekiri

- [ ] Oskab vaadata töötavaid container'eid (`docker ps`)
- [ ] Oskab siseneda container'isse (`docker exec -it`)
- [ ] Mõistab, et container on ajutine (pärast `rm` kaovad andmed)

### Kontrollküsimused

"Miks kaovad failid pärast `docker rm`?"  
"Kuidas säilitada andmeid?"

### Refleksioon

1-2 minutit: "Kujuta ette, et container on hotellituba. Mis juhtub pärast checkout'i?"

### Kohandus

**Kui kiired:** Tutvusta volume'e juba siin  
**Kui aeglane:** Jäta `exec` valikuliseks

---

## 3. Lab: Dockerfile ja Image'ide Loomine

**Aeg:** 45 min  
**Eesmärk:** Kirjutada esimene Dockerfile, ehitada image, mõista layer'eid ja cache'i  
**Meetodid:** Demo + juhendatud praktika, iseseisev töö

### Minutiplaan

**0-10 min:** Dockerfile demo  
`FROM`, `COPY`, `RUN`, `CMD` selgitus + think-aloud (labor.md)

**10-30 min:** Juhendatud praktika  
Õpilased kirjutavad Dockerfile'i Python/Node rakendusele, build'ivad

**30-40 min:** Cache demo  
Build kaks korda sama Dockerfile - näita, kui kiire cache on. Muuda 1 rida - näita rebuild.

**40-45 min:** Refleksioon ja kokkuvõte

### Kontrollnimekiri

- [ ] Dockerfile on loodud (vähemalt FROM, COPY, CMD)
- [ ] Image on edukalt build'itud (`docker build -t minu-app .`)
- [ ] Container töötab image'ist (`docker run minu-app`)

### Kontrollküsimused

"Mis on layer?"  
"Miks cache on oluline?"

### Refleksioon

1-2 minutit: "Dockerfile on nagu retsept. Mis on kõige tähtsam osa retseptis?"

### Kohandus

**Kui kiired:** Lisa multi-stage build demo  
**Kui aeg otsa:** Jäta cache selgitus kodutööks

---

## 4. Lab: Volumes, Networks ja Best Practices

**Aeg:** 45 min  
**Eesmärk:** Kasutada volume'e andmete säilitamiseks, mõista võrgustikku, rakendada best practices  
**Meetodid:** Demo + praktika, näited (hea vs halb), viktoriin

### Minutiplaan

**0-15 min:** Volume demo  
`-v` flag, andmete säilimine pärast `docker rm` (labor.md)

**15-30 min:** Juhendatud praktika  
Loo volume, mount andmebaasi, kontrolli andmete säilimist

**30-40 min:** Best practices  
`.dockerignore`, väiksemad image'd, multi-stage (näited)

**40-45 min:** Docker viktoriin ja kodutöö tutvustus

### Kontrollnimekiri

- [ ] Volume on loodud ja töötab
- [ ] Andmed säilivad pärast container'i kustutamist
- [ ] Mõistab `.dockerignore` otstarvet

### Kontrollküsimused

"Millal kasutada volume?"  
"Mida `.dockerignore` teeb?"

### Refleksioon

1-2 minutit: "Mida teeksid järgmisel korral teisiti? Mis oli kõige kasulikum?"

### Kohandus

**Kui kiired:** Tutvusta Docker Compose  
**Kui aeg napib:** Jäta networks valikuliseks

---

## Kodutöö

**Aeg:** 1.5 tundi (isetempoline)  
**Ülesanne:** Ehita Flask chat bot Docker container'is; kirjuta Dockerfile; kasuta volume'e

### Kriteeriumid

- [ ] Dockerfile on olemas ja töötab
- [ ] Image build'ub ilma vigadeta
- [ ] Container töötab ja on ligipääsetav (port mapping)
- [ ] `.dockerignore` on olemas
- [ ] README.md sisaldab käivitamisjuhendit
- [ ] Refleksioon README.md lõpus (5 küsimust, 2-3 lauset igaüks)

**Oluline:** Refleksioon on metakognitsioon praktikas.

**Esitamine:** GitHub repository link (Dockerfile, kood, README)

---

## Viited ja Täiendav Lugemine

### Pedagoogilised Alused

**National Research Council (2000).** *How People Learn: Brain, Mind, Experience, and School.* Washington, DC: The National Academies Press.
- Peatükk 1: "Learning: From Speculation to Science"
- eelteadmised, arusaamine, metakognitsioon
- Peatükk 2: "How Experts Differ from Novices"
- miks arusaamine > meeldejätmine

**Bransford, J., & Schwartz, D. (1999).** "Rethinking Transfer: A Simple Proposal with Multiple Implications." *Review of Research in Education, 24*, 61-100.
- Transfer = õpilased kannavad teadmisi üle uutesse olukordadesse (refleksioon aitab)

**Black, P., & Wiliam, D. (1998).** "Assessment and Classroom Learning." *Assessment in Education, 5*(1), 7-74.
- Formatiivne hindamine = feedback ilma hindeta (checklists, peer review)

### Docker-Spetsiifilised Ressursid

- Docker Documentation: https://docs.docker.com/
- Docker Hub: https://hub.docker.com/
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/
- Play with Docker (brauseris): https://labs.play-with-docker.com/

### Õpetamise Strateegiad

**Think-Aloud Protocol:** Verbaliseeri oma mõtteprotsess build ajal ("Hmm, build ebaõnnestus... proovin `docker logs`")

**Reciprocal Teaching:** Õpilased õpetavad üksteist (pair-check)

**Metacognitive Prompts:** "Mis oli raske? Kuidas lahendada? Mida teeksid teisiti?"

---

## Kokkuvõte

### Mida Teha

1. Alusta eelteadmistega ("Works on my machine" probleem)
2. Õpeta miks Docker on vajalik (mitte ainult kuidas)
3. Maksimaalselt 15 min loengut, ülejäänu praktika
4. Cache demo on WOW-moment (build kaks korda, näita kiirust)
5. Pair-check (õpilased selgitavad üksteisele image vs container)
6. Formatiivne hindamine (checklists, no grades)

### Mida Mitte Teha

1. Ära õpeta 20 käsku - keskendu 5-6 kontseptsioonile (run, build, ps, logs, exec, volume)
2. Ära loengi 45 minutit - õpilased vajavad tegemist
3. Ära eelda, et kõik Docker image'd on kohe cache'is - esimene pull võtab aega
4. Ära unusta port conflicts - õpilased võivad kasutada sama porti
5. Ära hüppa Docker Compose'i - see on järgmine moodul

Kui küsimusi, vaata loeng.md, labor.md, kodutoo.md - seal on kõik välja kirjutatud.