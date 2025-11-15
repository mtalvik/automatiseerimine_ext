# Tunnikava: CI/CD Pipeline GitHubis

**Klass:** 12  
**Õppeaine:** Informaatika  
**Teema:** Pidev integratsioon ja tarnimine (CI/CD)  
**Kestus:** 90 minutit  
**Õpetaja:** [Nimi]  
**Kuupäev:** [Kuupäev]

---

## Õpiväljund
ÕV7: Automatiseerib tarkvara arenduse ja juurutamise CI/CD'ga

---

## Eesmärgid
Õpilane:
- Loob GitHub Actions pipeline'i põhistruktuuri
- Debugib pipeline vigu logide abil
- Seadistab automaatse testimise ja Docker build'i
- Rakendab manual approval'i production deployment'iks

---

## Eelteadmised
- Git põhitõed (commit, push, pull)
- Docker põhitõed (build, run)
- YAML süntaksi alused
- **Kodutöö:** Loetud 20-min loengmaterjal CI/CD kohta

---

## Tunni kulg

| Aeg | Tegevus | Töövorm | Kirjeldus |
|-----|---------|---------|-----------|
| 5 min | Sissejuhatus | Frontal | Tere tulemast, kodutöö kontroll Mentimeter'is |
| 5 min | Mentimeter quiz | Individuaalne | 5 küsimust loengmaterjali kohta |
| 10 min | Live demo | Frontal | Õpetaja näitab GitHub Actions workflow'i loomist |
| 20 min | Hands-on 1 | Paaristöö | Validate ja Test stages loomine |
| 15 min | Paus | - | - |
| 20 min | Hands-on 2 | Paaristöö | Build stage + Docker health check |
| 10 min | Hands-on 3 | Paaristöö | Deploy stage + manual approval |
| 5 min | Tulemuste jagamine | Frontal | 2-3 paari näitavad oma pipeline'e |
| 5 min | Exit ticket | Individuaalne | Refleksioon Mentimeter'is |

---

## Õppematerjalid ja vahendid

**Digitaalsed tööriistad:**
- GitHub account (iga õpilane)
- Mentimeter (quiz + exit ticket)
- Projektor (demo jaoks)

**Õppematerjalid:**
- Loeng: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/loeng/
- Labor: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/labor/
- Starter repository (valikuline)

**Tarkvara:**
- Git (kohalik arvuti)
- VS Code (soovituslik)
- Docker (ainult kohalikuks testimiseks)

---

## Diferentseerimine

**Tugõppijatele:**
- Valmis starter repository template'idega
- Samm-sammuline juhend screenshotidega
- Pair programming tugevama õpilasega
- Lisaaeg harjutuste tegemiseks

**Andekamale:**
- Paralleelsed job'id (test mitmel Python versioonil)
- Cache'imine (dependency install kiirem)
- Matrix strategy (testimine mitmel OS'il)
- Lisaülesanded: väljakutsed 6.1-6.3

---

## Hindamine

**Formatiivne:**
- Mentimeter quiz alguses (5p) - kas loeng loetud?
- Vaatlus paaristöö ajal
- GitHub Actions tulemused - kas pipeline töötab?
- Exit ticket refleksioon

**Summatiivne (kodutöö):**
- Pipeline struktuur (4p)
- Vigade parandamine (4p)
- Docker integration (4p)
- Testimine (4p)
- Dokumentatsioon (4p)
- Manual approval (4p)
- Väljakutsed (8p)
- **Kokku: 32p**

---

## Kodutöö
**Tähtaeg:** Järgmine tund

**Ülesanded:**
1. Väljakutse 6.1: Lisa uus endpoint + test
2. Väljakutse 6.2: README + CI/CD badge
3. Väljakutse 6.3: Mõtiskle rollback'i üle

**Esitamine:** GitHub repo link

---

## Refleksioon (õpetaja täidab pärast tundi)

**Mis õnnestus:**
- 
- 

**Mis vajab parandamist:**
- 
- 

**Järgmiseks korraks:**
- 
- 

---

## Märkused

**Tehnilised:**
- Kontrolli enne tundi, et kõikidel on GitHub account
- Demo repo peab olema valmis
- Mentimeter link valmis

**Pedagoogilised:**
- Rõhuta: "Pipeline'i fail = õppimise võimalus"
- Ära anna kohe lahendusi, õpeta logide lugemist
- Exit ticket on oluline tagasiside saamiseks
