# Tunnikava: Docker Konteinerite Loomine

**Õppeaine:** Informaatika  
**Klass:** 12  
**Tunni teema:** Docker konteinerite loomine  
**Õpiväljund:** ÕV2 - Oskab luua ja seadistada konteinereid ja virtuaalmasinaid  
**Aeg:** 90 minutit  
**Õpetaja:** [Nimi]

---

## Tunni eesmärgid

**Õpilane:**
- Selgitab Docker'i kasulikkust ("Works on my machine" probleem)
- Loob Dockerfile'i Flask rakendusele
- Ehitab Docker image'i ja käivitab konteineri
- Debugib konteineriga seotud probleeme (logs, exec)

---

## Õpilaste eelteadmised

- Käsurida põhikäsud (cd, ls, mkdir)
- Python või muu programmeerimiskeele alused
- Git põhitõed

---

## Õppevahendid ja materjalid

- Docker Desktop (installeeritud eelnevalt)
- VS Code + Docker extension
- Labor juhendid: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/
- Quiz: https://docs.google.com/forms/d/e/1FAIpQLSdzu28vxMQHzW_qcUxXDe5nNmrRfs0OWg2_n3LNZMR4puxkNA/viewform
- Projektor (demo)

---

## Tunnikäik

| Tunni osa | Aeg | Õpetaja tegevus | Õpilaste tegevus | Hindamine | Põhjendused |
|-----------|-----|-----------------|------------------|-----------|-------------|
| **Sissejuhatus** | 5 min | Küsib: "Kes on deploy'inud koodi?", selgitab "Works on my machine" probleemi, container vs VM | Paarides arutavad kogemusi, kuulavad selgitust | - | Motiiveerimine, probleem mida Docker lahendab |
| **Avastamine** | 10 min | Juhendab Docker Hub'i uurimist, näitab populaarseid image'id | Individuaalselt uurivad Docker Hub'i, populaarseid image'id (nginx, postgres, python), täidavad worksheet'i | - | Avastusõpe, eelteadmiste aktiveerimine |
| **Demo** | 5 min | Live coding: näitab Dockerfile'i loomist, selgitab FROM, WORKDIR, COPY, RUN, CMD käske | Vaatavad demoüt, teevad märkmeid cheat sheet'ile | - | Visualiseerimine, süntaksi mõistmine |
| **Harjutus 1** | 20 min | Jälgib paaride tööd, aitab troubleshooting'uga | Paarides loovad Flask app Dockerfile'i, buildivad image'i, käivitavad konteineri, testavad | Formatiivne: kas rakendus töötab konteineris | Praktiline õppimine, hands-on kogemus |
| **Paus** | 15 min | - | Puhkavad | - | - |
| **Harjutus 2** | 20 min | Selgitab environment variables, multi-stage build'i, aitab vajadusel | Individuaalselt täiustavad Dockerfile'i, lisavad env vars, optimeerivad image size'i | Formatiivne: täiustatud Dockerfile | Süvendamine, keerulisemad kontseptsioonid |
| **Testimine** | 10 min | Näitab docker logs, docker exec käske | Individuaalselt kontrollivad logisid, debugivad probleeme, sisestuvad konteinerisse | Formatiivne: debugging õnnestub | Troubleshooting oskused, debug kultuur |
| **Exit ticket** | 5 min | Avab Mentimeter, tutvustab kodutööd | Vastavad küsimustele: keerulisem? õppisin? küsimus? | Formatiivne: refleksioon | Tagasiside, metakognitsioon |

---

## Digiõppevara

**1. Enesekontrolli quiz (Google Forms):**
- 10 küsimust Docker põhimõtete kohta
- Automaatne hindamine, kohene tagasiside
- Kasutatakse tunni alguses või kodutööna

**2. Ekraanivideo (10 min):**
- Dockerfile loomine, image build, konteineri käivitus
- Integreeritud labor.md faili
- Õpilased saavad pausida, oma tempos

**3. GitHub harjutused:**
- 6 praktilist ülesannet + TODO listid
- Fork → commit → pull request → peer review

---

## Diferentseerimine

**Tugõppijatele:**
- Valmis Dockerfile template
- Lisaaeg harjutusteks
- Pair programming tugevamaga

**Andekamale:**
- Multi-stage build väljakutse
- Docker Compose sissejuhatus
- Image optimization

---

## Kodutöö

**Tähtaeg:** Järgmine tund

**Ülesanded:**
- Flask chatbot projekt
- Dockerfile täiustamine
- Peer review

**Materjal:** https://mtalvik.github.io/automatiseerimine_ext/docker_basics/kodutoo/

---

## Märkused

**Õpetajale:**
- Kontrolli Docker Desktop töötab kõikidel
- Varu aega troubleshooting'uks
- Permission issues - Run as Administrator
- Rõhuta: "Vead on normaalsed, sellest õpime!"