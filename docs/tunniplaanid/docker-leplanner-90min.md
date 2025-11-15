# Docker Konteinerite Loomine - LePlanner Tunnikava

**Link:** https://leplanner.ee/en/scenario/5442  
**Kestus:** 90 min  
**Õpiväljund:** ÕV2 - Oskab luua ja seadistada konteinereid ja virtuaalmasinaid  
**Didaktiline lähenemine:** Avastusõpe + hands-on

---

## Tunni struktuur

| # | Tegevus | Aeg | Vorm | Õpiväljund | Materjalid |
|---|---------|-----|------|------------|------------|
| 1 | **Sissejuhatus** - "Miks Docker?" | 5 min | Pair | ÕV2 | Container vs VM, "Works on my machine" probleem |
| 2 | **Avastamine** - Docker Hub uurimine | 10 min | Individual | ÕV2 | Docker Hub worksheet, populaarsed image'id |
| 3 | **Demo** - Dockerfile anatoomia | 5 min | Whole class | ÕV2 | Live coding, FROM/WORKDIR/COPY/RUN/CMD, cheat sheet |
| 4 | **Harjutus 1** - Kirjuta Dockerfile | 20 min | Pair | ÕV2 | Flask app Dockerfile, labor.md juhendid |
| 5 | **PAUS** | 15 min | Meta | - | - |
| 6 | **Harjutus 2** - Build + Run | 20 min | Individual | ÕV2 | Environment variables, multi-stage build, optimization |
| 7 | **Testimine** - Troubleshooting | 10 min | Individual | ÕV2 | docker logs, docker exec, debugging checklist |
| 8 | **Exit ticket** - Mentimeter | 5 min | Whole class | ÕV2 | Mentimeter: keerulisem? õppisin? küsimus? |

**KOKKU: 90 min**

---

**KOKKU: 90 min (5+10+5+20+15+20+10+5)**

---

## Digitaalne interaktiivne õppematerjal

### 1. Enesekontrolli quiz (Google Forms)
**Kasutuskoht:** Aktivatsiooni faas (tunni alguses) või kodutööna enne tundi

**Kirjeldus:**
- 10 küsimusega interaktiivne quiz
- Automaatne hindamine
- Kohene tagasiside
- Küsimused: Docker kontseptsioonid, Dockerfile süntaks, best practices

**Link:** https://docs.google.com/forms/d/e/1FAIpQLSdzu28vxMQHzW_qcUxXDe5nNmrRfs0OWg2_n3LNZMR4puxkNA/viewform

**Integratsioon:** Quiz tulemused näitavad kas õpilased on valmis praktiliseks tööks

---

### 2. Juhendav ekraanivideo (10 min)
**Kasutuskoht:** Demonstratsiooni faas või kodutööna (flipped classroom)

**Kirjeldus:**
- Screen recording Dockerfile loomisest
- Image'i ehitamine samm-sammult
- Konteineri käivitamine
- Põhiliste käskude kasutamine

**Integratsioon:** Video manustatud labor.md faili: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/

**Eelised:**
- Õpilased saavad pausida ja tagasi kerida
- Sobib oma tempos töötamiseks
- Vähendab korduvate küsimuste arvu

---

### 3. Interaktiivsed GitHubi harjutused
**Kasutuskoht:** Rakendamise ja integreerimise faas

**Struktuur:**

**Labor.md** - 6 praktilist harjutust:
- Link: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/
- Iga harjutus sisaldab TODO liste
- Selged success criteria
- Kontrollnimekiri

**Kodutoo.md** - Flask chatbot projekt:
- Link: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/kodutoo/
- Refleksiooniküsimused
- Peer review juhised

**Interaktiivsus:**
- Õpilased forgivad repo
- Commitivad oma lahendused
- Avanevad pull request'id
- Saavad peer review'd

---

## Materjalid

**Labor (tunnis):**
- https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/

**Kodutöö:**
- https://mtalvik.github.io/automatiseerimine_ext/docker_basics/kodutoo/

**Quiz:**
- https://docs.google.com/forms/d/e/1FAIpQLSdzu28vxMQHzW_qcUxXDe5nNmrRfs0OWg2_n3LNZMR4puxkNA/viewform

**Viited:**
- Docker dokumentatsioon: https://docs.docker.com
- Docker Hub: https://hub.docker.com

**Tarkvara:**
- Docker Desktop (installeeritud eelnevalt)
- VS Code + Docker extension
- Terminal/PowerShell

---

## Erinevus docker_pohitoed.md'st

- LePlanner tund on **90 min** (üks tund)
- docker_pohitoed.md on **180 min** (4 x 45 min, kogu moodul)
- LePlanner keskendub **Dockerfile loomisele**
- docker_pohitoed.md katab **kogu Docker mooduli** (põhitõed → volumes)

---

## Märkused õpetajale

**Enne tundi:**
- [ ] Docker Desktop käivitatud kõikidel õpilastel
- [ ] Valmis demo Dockerfile
- [ ] Mentimeter exit ticket valmis
- [ ] Kontrolli permission issues võimalust

**Tunni ajal:**
- Varu aega troubleshooting'uks - esimene kord võtab kauem
- Jälgi et õpilased ei jää kinni permission issues'tesse
- Paaride moodustamine: kombineeri erineva tasemega õpilasi
- Rõhuta: "Docker Hub uurimine = võti mõistmiseks"

**Diferentseerimine:**
- Tugõppijatele: valmis template Dockerfile
- Andekamale: multi-stage build väljakutse, Docker Compose

**Tüüpilised probleemid:**
- Port already in use → `docker ps` ja `docker stop`
- Permission denied → Windows: Run as Administrator
- Image build slow → selgita layer cache'i
