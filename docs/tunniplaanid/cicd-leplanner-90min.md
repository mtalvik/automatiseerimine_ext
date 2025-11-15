# Tunnikava: CI/CD Pipeline GitHubis

**Õppeaine:** Informaatika  
**Klass:** 12  
**Tunni teema:** Pidev integratsioon ja tarnimine (CI/CD)  
**Õpiväljund:** ÕV7 - Automatiseerib tarkvara arenduse ja juurutamise CI/CD'ga  
**Aeg:** 90 minutit  
**Õpetaja:** [Nimi]

---

## Tunni eesmärgid

**Õpilane:**
- Loob GitHub Actions pipeline'i põhistruktuuri (validate, test, build, deploy)
- Debugib pipeline vigu logide abil
- Seadistab automaatse testimise ja Docker build'i
- Rakendab manual approval'i production deployment'iks

---

## Õpilaste eelteadmised

- Git põhitõed (commit, push, branch)
- Docker põhitõed (build, run, image)
- YAML süntaksi alused
- **Kodutöö:** Loetud 20-min loengmaterjal CI/CD kohta

---

## Õppevahendid ja materjalid

- GitHub account (iga õpilane)
- Mentimeter (quiz + exit ticket)
- Projektor (demo)
- Labor juhendid: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/labor/
- Loeng: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/loeng/

---

## Tunnikäik

| Tunni osa | Aeg | Õpetaja tegevus | Õpilaste tegevus | Hindamine | Põhjendused |
|-----------|-----|-----------------|------------------|-----------|-------------|
| **Kodutöö kontroll** | 10 min | Avab Mentimeter quiz'i, jälgib vastuseid | Vastavad 5 küsimusele: workflow, job, step, CI vs CD, runner | Formatiivne: quiz tulemused | Kontroll kas loengmaterjal loetud |
| **Live demo** | 10 min | Näitab GitHub Actions workflow'i loomist, validate stage, tahtlik viga | Vaatavad demoüt, teevad märkmeid | - | Visualiseerimine, protsessi mõistmine |
| **Hands-on 1** | 20 min | Jälgib paaride tööd, aitab YAML süntaksiga, troubleshooting | Paarides loovad validate + test stages, parandavad tahtlikke vigu: syntax error, negatiivne hind, version mismatch | Formatiivne: kas pipeline töötab | Praktika, vigade leidmine õpetab debugimist |
| **Paus** | 15 min | - | Puhkavad | - | - |
| **Hands-on 2** | 20 min | Aitab Docker build'iga, selgitab health check'i | Paarides lisavad build stage, leiavad Dockerfile vea (EXPOSE 8080→5000), parandavad | Formatiivne: health check õnnestub | Docker integratsioon, praktiline debug |
| **Hands-on 3** | 10 min | Selgitab manual approval'i vajalikkust | Paarides lisavad deploy stage, seadistavad GitHub Environments, teevad approval | Formatiivne: deployment töötab | Production kaitse mõistmine |
| **Tulemused** | 5 min | Modereerib, küsib täpsustavaid küsimusi | 2-3 paari näitavad oma pipeline'e, selgitavad vigu ja lahendusi | - | Õppimine teistelt, suuline esitlus |
| **Exit ticket** | 5 min | Avab Mentimeter, tutvustab kodutööd | Vastavad refleksiooni küsimustele: keerulisem? õppisin? enesekindel? | Formatiivne: refleksioon | Tagasiside õpetajale, metakognitsioon |

---

## Diferentseerimine

**Tugõppijatele:**
- Valmis starter repository
- Pair programming tugevama õpilasega
- Lisaaeg harjutusteks

**Andekamale:**
- Paralleelsed job'id
- Cache'imine
- Matrix strategy

---

## Kodutöö

**Tähtaeg:** Järgmine tund

**Ülesanded:**
- Väljakutse 6.1: Lisa uus endpoint + test
- Väljakutse 6.2: README + CI/CD badge  
- Väljakutse 6.3: Mõtiskle rollback'i üle

**Hindamine:** 32 punkti (rubriik eraldi dokumendis)

---

## Märkused

**Õpetajale:**
- Saada loengmaterjal 2 päeva ette
- Kontrolli GitHub account'id
- "Pipeline fail = õppimine, mitte probleem!"