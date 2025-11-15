# Docker Konteinerite Loomine

**LePlanner:** https://leplanner.ee/en/scenario/5442  
**Klass:** 12 | **Kestus:** 90 min | **Õpiväljund:** ÕV2

---

## Tunni kulg

| Tegevus | min | Vorm | Materjal |
|---------|-----|------|----------|
| Sissejuhatus | 5 | Paarid | "Works on my machine", container vs VM |
| Docker Hub uurimine | 10 | Individuaalne | Worksheet, populaarsed image'id |
| Demo: Dockerfile | 5 | Klass | FROM, WORKDIR, COPY, RUN, CMD |
| Harjutus 1: Dockerfile | 20 | Paarid | Flask app, labor.md juhendid |
| Paus | 15 | - | - |
| Harjutus 2: Build + Run | 20 | Individuaalne | Environment vars, multi-stage |
| Testimine | 10 | Individuaalne | docker logs, docker exec |
| Exit ticket | 5 | Klass | Mentimeter: keerulisem? õppisin? |

---

## Digiõppevara

**1. Quiz (Google Forms):**
- 10 küsimust: Docker kontseptsioonid, Dockerfile süntaks
- Automaatne hindamine, kohene tagasiside
- https://docs.google.com/forms/d/e/1FAIpQLSdzu28vxMQHzW_qcUxXDe5nNmrRfs0OWg2_n3LNZMR4puxkNA/viewform

**2. Video (10 min):**
- Dockerfile loomine, image build, konteineri käivitus
- Integreeritud labor.md: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/
- Õpilased saavad pausida, oma tempos

**3. GitHub harjutused:**
- 6 praktilist ülesannet + TODO listid
- Labor: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/
- Kodutöö: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/kodutoo/
- Fork → commit → pull request → peer review

---

## Materjalid

- Labor: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/labor/
- Kodutöö: https://mtalvik.github.io/automatiseerimine_ext/docker_basics/kodutoo/
- Quiz: https://docs.google.com/forms/d/e/1FAIpQLSdzu28vxMQHzW_qcUxXDe5nNmrRfs0OWg2_n3LNZMR4puxkNA/viewform
- Docker Desktop, VS Code, Terminal

---

## Õpetajale

**Enne:**
- Docker Desktop käivitatud kõikidel
- Demo Dockerfile valmis
- Mentimeter exit ticket

**Tunnis:**
- Varu aega troubleshooting'uks
- Jälgi permission issues
- Paarid: erineva tasemega kokku

**Probleemid:**
- Port in use → docker ps, docker stop
- Permission denied → Run as Administrator
- Build slow → selgita layer cache
