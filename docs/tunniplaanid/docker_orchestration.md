# Tunnikava: Docker Compose ja Mitme Konteineri Haldamine

**Kestus:** 3 × 45 min  
**Tase:** Kutsekeskharidus, II kursus  
**Eeldused:** Docker fundamentals, container basics, terminal skills  
**Materjalid:** loeng.md, labor.md, kodutoo.md, lisapraktika.md, seadistus.md

## Õpiväljundid

Pärast seda õppetundi oskavad õppurid:
- Kirjutada ja käivitada Docker Compose faile
- Ehitada multi-container rakendusi
- Mõista teenuste vahelist suhtlust ja võrgustikku
- Hallata erinevaid keskkondi (development, production)
- Debugida ja tõrkeotsingut teha
- Mõista orkestreerimise põhimõtteid ja vajadust

---

## Pedagoogiline raamistik

See tunniplaan põhineb "How People Learn" (National Research Council, 2000) põhimõtetel:

### 1. Eelnev teadmine

Õppurid tulevad tundi teadmistega Docker konteinerite kohta. Aktiveerime neid teadmisi ja ehitame neile peale uusi kontseptsioone. Docker Compose on loogiline järgmine samm pärast ühe konteineri haldamise õppimist.

### 2. Mõistmine üle memoreerimise

Fookus on mõistmisel MIKS me vajame Compose'i, mitte lihtsalt käskude päheõppimisel. Kasutame päriselu probleeme (mitme konteineri käsitsi haldamise raskused) et motiveerida lahendust.

### 3. Metakognitsioon

Iga tunni osa sisaldab refleksiooni hetki kus õppurid mõtlevad OMA õppimisele: "Mis mul klikkis? Mis oli raske? Kuidas ma seda kasutaksin?"

### 4. Formatiivne hindamine

Pidev tagasiside läbi Kontrollküsimuste ja praktiliste ülesannete. Õpetaja näeb koheselt kes vajab täiendavat abi.

---

## Õpetamismeetodid

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|-----------------|
| **Live coding** | Õpetaja näitab terminalis, õppurid järgivad | Docker Compose demo, troubleshooting |
| **Think-Pair-Share** | Mõtle (30s) → Aruta paariga (2min) → Jaga klassiga | Kontrollküsimuste järel |
| **Guided practice** | Õpetaja juhendab, õppurid teevad kaasa | Lab ülesanded |
| **Scaffolding** | Alusta lihtsa YAML'iga, lisa järk-järgult | Compose faili ehitamine |
| **Just-in-time teaching** | Seleta kontsepti SIIS kui vaja | DNS, volumes - kui jõuame nende juurde |
| **Error-based learning** | Lase õppuritel vigu teha ja debugida | Troubleshooting harjutused |
| **Peer instruction** | Õppurid aitavad üksteist | Labori ajal |

---

## Näpunäited algajale õpetajale

### Tehnilised ettevalmistused

1. **VM'id peavad olema valmis** - testi enne tundi et Docker töötab kõigis VM'ides
2. **Port forwarding peab olema seadistatud** - õppurid peavad brauseris rakendust nägema
3. **Varuplaan kui internet aeglane** - lae Docker image'd ette alla lab VM'idesse
4. **Backup slides** - kui live coding ebaõnnestub, on sul visuaalsed slaidid

### Õpetamise nõuanded

1. **Ära kiirusta** - YAML süntaks on õppuritele uus ja vead on frustrreerivad
2. **Kasuta analoogiaid** - "Compose on nagu orkestri juht", "Services on nagu osakonnad firmas"
3. **Näita vigu** - tee tahtlikult viga ja näita kuidas debugida
4. **Küsi "Miks?"** - ära ütle lihtsalt "tee nii", seleta miks see on hea praktika
5. **Jälgi aeglasemaid** - liiga kiire tempo on peamine probleem IT õppes

### Levinud õppurite probleemid

1. **YAML taandvead** - seleta et YAML on tundlik tühikute suhtes
2. **Segadus volumes vs bind mounts** - kasuta visuaalseid skeeme
3. **DNS ei tööta** - seleta et teenuse nimi = hostname, see on automaatne
4. **"See ei tööta"** - õpeta süsteemset debugging protsessi (logid → status → health)

---

## 1. Sissejuhatus ja motivatsioon

**Aeg:** 45 min  
**Eesmärk:** Mõista MIKS me vajame Docker Compose'i  
**Meetodid:** Loeng + live demo + diskussioon

### Minutiplaan

**0-5 min: Aktiveeri eelnevad teadmised**
- "Kes käivitas labori tunnis rohkem kui 2 konteinerit? Kuidas te seda tegite?"
- Kirjuta tahvlile: docker run käsud mis nad ütlevad
- Näita kui palju käske ja parameetreid see nõuab

**5-15 min: Probleem**
- Näita live: käivita käsitsi 2 konteinerit (DB + API)
- Demonstreeri raskused:
  - IP aadress muutub
  - Pead meeles pidama järjekorda
  - Pead ootama et DB valmis saaks
- Küsi: "Kujutage ette 5 konteinerit. Kui kaua läheks?"

**15-25 min: Lahendus - Docker Compose**
- Näita lihtsat docker-compose.yml faili
- Võrdle: 5 docker run käsku vs 1 docker-compose up
- Seleta deklaratiivne vs imperatiivne lähenemisviis
- Analoogia: "Compose on nagu retsept
- kirjeldad MIDA tahad, mitte KUIDAS teha"

**25-35 min: YAML põhitõed**
- Näita YAML struktuuri (taanded, lists, dictionaries)
- Hoiatus: YAML on VÄGA tundlik tühikute suhtes!
- Live demo: tee tahtlikult taande viga ja näita error message'it
- Õpeta: kasuta VSCode YAML extensioni

**35-40 min: Think-Pair-Share**
- Küsimus: "Millistes projektides te võiksite Compose'i kasutada?"
- 30s mõtle
- 2min arutle paarikaasega
- Jaga klassiga (3-4 õppurit)

**40-45 min: Ülevaade ja preview**
- Näita lühidalt (30s) töötavat multi-container Todo app'i
- "Selle me ehitame järgmistes tundides"
- Ülevaade järgmiste tundide teemadest

### Kontrollnimekiri

- [ ] Õppurid mõistavad MIKS Compose on vajalik
- [ ] Nägin et õppurid kirjutasid üles YAML põhitõdesid
- [ ] Vähemalt 5 õppurit jagas oma mõtteid diskussioonil
- [ ] Tehniline demo töötas (või oli backup plaan)

### Kontrollküsimused

Küsi 2-3 õppurilt:
1. "Mis on Docker Compose peamine eesmärk?"
   - Õige vastus: Mitme konteineri haldamine koos, deklaratiivselt
2. "Mis vahe on imperatiivsul ja deklaratiivsel lähenemine?"
   - Õige vastus: Imperatiivne = samm-sammult käsud, deklaratiivne = kirjelda tulemust

### Refleksioon

Küsi õppuritelt (1 min, suuline tagasiside):
- "Kellel on nüüd selge MIKS me vajame Compose'i?"
- "Kes tunneb end kindlalt YAML süntaksiga?" (kui alla 50%
- võta järgmises tunnis rohkem aega)

### Kohandus

**Kui õppurid on kiiremad:**
- Näita ka docker-compose.override.yml kontseptsiooni
- Alusta teenuste kirjeldamist (services sektsioon)

**Kui õppurid on aeglasemad:**
- Jäta YAML detailid järgmisesse tundi
- Fokuseeri rohkem motivatsioonile (probleemi mõistmine)

---

## 2. Teenused ja võrgustik

**Aeg:** 45 min  
**Eesmärk:** Kirjutada esimene Compose fail ja mõista teenuste suhtlust  
**Meetodid:** Scaffolded live coding + guided practice

### Minutiplaan

**0-5 min: Kordamine**
- "Mis oli eelmine kord kõige olulisem õppetund?"
- Kiire ülevaade: Compose peamine mõte, YAML struktuur

**5-20 min: Esimene Compose fail (scaffolded)**
- Ava VSCode ja loo tühi docker-compose.yml
- **Samm 1:** Ainult versioon ja üks teenus (nginx)
  
```yaml
  version: '3.8'
  services:
    web:
      image: nginx:alpine
      ports:
        - "8080:80"
  
```
- Käivita: `docker-compose up`
- Kontrolli brauseris: localhost:8080
- **Samm 2:** Lisa teine teenus (redis)
- **Samm 3:** Näita kuidas teenused näevad üksteist (DNS)
- Õppurid kirjutavad kaasa!

**20-30 min: DNS ja võrgustik**
- Seleta: teenuse nimi = hostname
- Demo: mine nginx konteinerisse ja pingi redis'e
  
```bash
  docker-compose exec web ping redis
  
```
- Näita et IP võib muutuda aga nimi jääb samaks
- Joonista tahvlile: Network diagram

**30-40 min: Guided practice**
- Õppurid lisavad oma Compose faili kolmanda teenuse (postgres)
- Õpetaja juhendab samm-sammult
- Käi ringi ja aita

**40-45 min: Troubleshooting harjutus**
- "Mida teha kui teenus ei käivitu?"
- Õpeta: `docker-compose logs`, `docker-compose ps`
- Näita reaalne error ja kuidas seda lahendada

### Kontrollnimekiri

- [ ] Kõik õppurid said esimese Compose faili tööle
- [ ] Vähemalt 80% mõistab DNS kontseptsiooni (kontrolli küsimustega)
- [ ] Nägin et õppurid kasutavad logs käsku

### Kontrollküsimused

1. "Kuidas üks teenus leiab teist teenust?"
   - Õige: teenuse nime järgi, DNS lahendab IP'ks
2. "Mida teha kui ei tea mis valesti läks?"
   - Õige: vaata logisid (docker-compose logs)

### Refleksioon

Think-Pair-Share (2 min):
- "Mis oli selle tunni kõige huvitavam osa?"
- "Mis jäi ebaselgeks?"

### Kohandus

**Kui kiire:**
- Lisa volumes kontseptsioon
- Näita depends_on

**Kui aeglane:**
- Jäta postgres hilisemaks
- Rohkem aega DNS kontseptsioonile

---

## 3. Täielik Todo rakendus

**Aeg:** 45 min  
**Eesmärk:** Ehitada töötav multi-container rakendus  
**Meetodid:** Projekt-põhine õpe + peer instruction

### Minutiplaan

**0-5 min: Ülevaade**
- "Täna ehitame päris rakenduse: Todo app"
- Näita arhitektuuri: Nginx → Frontend → API → Database
- Kirjuta tahvlile: 4 teenust, nende rollid

**5-35 min: Labori aeg**
- Õppurid järgivad labor.md juhiseid
- Õpetaja käib ringi ja aitab
- **Peer instruction:** Kui keegi saab valmis, palun aidake naabrit
- Jälgi kes on takerdunud
- need vajavad rohkem abi

**Levinud probleemid (valmistud ette):**
- npm install võtab kaua
- seleta et see on normaalne
- Port conflict
- õpeta kuidas muuta porti
- Frontend ei näe API'd
- kontrolli nginx konfiguratsiooni

**35-40 min: Demo ja arutelu**
- Palun 1-2 õppurit näidata oma töötavat rakendust
- Küsi: "Mis oli kõige raskem?"
- Diskussioon: "Kus te seda võiksite kasutada?"

**40-45 min: Refleksioon ja kodutöö**
- Kiire ülevaade: mida õppisime?
- Tutvusta kodutööd (Redis cache lisamine)
- "Küsimusi? Nüüd või Discordis!"

### Kontrollnimekiri

- [ ] Vähemalt 70% õppureid sai rakenduse tööle
- [ ] Käisin iga õppuri juures vähemalt 2 korda
- [ ] Nägin et õppurid kasutavad debug oskusi (logs, ps)

### Kontrollküsimused

Labori lõpus küsi:
1. "Kuidas andmebaas ja API omavahel suhtlevad?"
2. "Mida teha kui frontend näitab tühja lehte?"

### Refleksioon

Kirjalik (2 min, paned Moodle'sse):
- "Mis oli selle projekti juures kõige raskem?"
- "Mida sa õppisid Docker Compose kohta?"

### Kohandus

**Kui kiire:**
- Lisa Redis cache (kodutöö ette)
- Näita scaling (`docker-compose up --scale`)

**Kui aeglane:**
- Loo grupid
- üks arvuti grupi kohta
- Võta rohkem aega troubleshooting'uks

---

## Kodutöö

**Ülesanne:** Lisa Redis cache Todo rakendusele (vt kodutoo.md)  
**Aeg:** 1.5 tundi  
**Esitamine:** Järgmise nädala algus  

**Eesmärk:** Kinnistada Compose oskused ja õppida uut teenust (Redis) lisama.

---

## Viited ja täiendav lugemine

### Õpetajale

- "How People Learn" (NRC, 2000)
- pedagoogiline raamistik
- "Make It Stick" (Brown, Roediger, McDaniel)
- õppimise teadus
- Docker Compose dokumentatsioon: https://docs.docker.com/compose/
- "Teaching Tech Together" (Greg Wilson)
- IT õpetamise parimad praktikad

### Õppuritele

- Docker Compose dokumentatsioon: https://docs.docker.com/compose/
- YAML syntax: https://yaml.org/
- Docker Compose best practices: https://docs.docker.com/compose/production/
- Awesome Compose (näited): https://github.com/docker/awesome-compose

---

## Kokkuvõte

### Õpetajana pead:

**Tegema:**
- Aktiveerima eelnevaid teadmisi enne uute kontseptsioonide õpetamist
- Näitama MIKS enne KUIDAS
- Kasutama päris näiteid ja analoogiaid
- Käima ringi ja aitama aeglasemaid õppureid
- Õpetama debug oskusi, mitte ainult "õigeid vastuseid"
- Andma aega refleksiooniks ja metakognitsiooniks

**MITTE tegema:**
- Liiga kiiresti edasi minna (YAML süntaks vajab aega!)
- Ainult loengut pidama
- praktika on kriitilise tähtsusega
- Eeldama et kõik õppurid on samas tempos
- Ignoreerima tehnilisi probleeme
- need on õppimise võimalused
- Andma valmis koodi ilma selgituseta
- Unustama tunnist lõbus teha
- motivatsioon on oluline!

### Õppurite õnnestumise märgid:

- Kirjutavad Compose faile ilma abi küsimata
- Kasutavad debug käske automaatselt
- Mõistavad DNS kontseptsiooni
- Näevad Compose'i väärtust oma projektides
- Oskavad seletada MIKS, mitte ainult KUIDAS
- Aitavad üksteist troubleshooting'uga