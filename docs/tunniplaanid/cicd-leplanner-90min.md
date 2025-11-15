# CI/CD Pipeline GitHubis - LePlanner Tunnikava

**Link:** https://leplanner.ee/en/scenario/5444  
**Kestus:** 90 min  
**Õpiväljund:** ÕV7 - Automatiseerib tarkvara arenduse ja juurutamise CI/CD'ga  
**Didaktiline lähenemine:** Ümberpööratud klassiruum

---

## Kodutöö (enne tundi)

**Õpilased loevad:**
- 20-min loengmaterjal: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/loeng/
- Põhikontseptsioonid: workflow, job, step, action, runner, events
- ByteByteGo CI/CD diagram

---

## Tunni struktuur

### Activity 1: Kodutöö kontroll - Mentimeter quiz (10 min, Whole class)
**Linked to:** ÕV7

**Teacher resource:**
- Mentimeter quiz link
- Vastuste ülevaade (5 küsimust)

**Student resource:**
- Mentimeter quiz - 5 küsimust (Co-Authorship: 2 - Interacting)
  1. Mis on workflow, job ja step?
  2. Kuidas GitHub Actions käivitub?
  3. Mis vahe on CI ja CD vahel?
  4. Kus peab .yml fail olema?
  5. Mis on runner?

---

### Activity 2: Live demo - Esimene pipeline (10 min, Whole class)
**Linked to:** ÕV7

**Teacher resource:**
- Demo GitHub repository
- Demo script: validate stage loomine
- Tahtlik viga demonstratsiooniks

**Student resource:**
- GitHub Actions dokumentatsioon (Co-Authorship: 0)
- Demo märkmed template (Co-Authorship: 1 - Annotating)
- YAML syntax reference (Co-Authorship: 0)

---

### Activity 3: Hands-on Osa 1 - Validate ja Test stages (20 min, Pair)
**Linked to:** ÕV7

**Teacher resource:**
- Troubleshooting common YAML errors
- Monitoring dashboard (kes on kinni jäänud)

**Student resource:**
- Labor ülesanded 2.1 ja 3.1-3.2 (Co-Authorship: 0)
- Starter repository (valikuline) (Co-Authorship: 5 - Remixing)
- GitHub Actions workflow template (Co-Authorship: 0)

**Tahtlikud vead õpilased peavad leidma:**
- Ülesanne 2.1: Süntaksi viga (`def home()` ilma koolonita)
- Ülesanne 3.1: Negatiivne hind (`price: -599`)
- Ülesanne 3.2: Versiooni mittevastavus (kood vs test)

---

### Activity 4: PAUS (15 min, Meta)

---

### Activity 5: Hands-on Osa 2 - Build stage + Docker (20 min, Pair)
**Linked to:** ÕV7

**Teacher resource:**
- Docker troubleshooting guide
- GitHub Container Registry setup juhend

**Student resource:**
- Labor ülesanne 4.1 (Co-Authorship: 0)
- Dockerfile best practices (Co-Authorship: 0)
- Docker build checklist (Co-Authorship: 1 - Annotating)

**Tahtlik viga Dockerfile'is:**
- `EXPOSE 8080` peaks olema `EXPOSE 5000`
- Health check fail'ib → õpilased debugivad logidest

---

### Activity 6: Hands-on Osa 3 - Deploy + Manual Approval (10 min, Pair)
**Linked to:** ÕV7

**Teacher resource:**
- Environment setup guide
- Approval workflow demo

**Student resource:**
- Deploy stage template (Co-Authorship: 0)
- GitHub Environments dokumentatsioon (Co-Authorship: 0)
- Manual approval setup juhend (Co-Authorship: 0)

---

### Activity 7: Demo ja tulemuste jagamine (5 min, Whole class)
**Linked to:** ÕV7

**Teacher resource:**
- Demo protocol (millele tähelepanu pöörata)

**Student resource:**
- Demo esitluse template (Co-Authorship: 6 - Creating)
  - Millised stage'id on?
  - Millised vead leidsid?
  - Kuidas debugisid?

---

### Activity 8: Exit Ticket - Mentimeter refleksioon (5 min, Individual)
**Linked to:** ÕV7

**Teacher resource:**
- Mentimeter exit ticket link
- Tulemuste analüüs

**Student resource:**
- Mentimeter exit ticket (Co-Authorship: 3 - Submitting)
  1. Mis oli kõige keerulisem täna? (avatud)
  2. Üks asi, mida õppisin CI/CD kohta (avatud)
  3. Kui enesekindel tunned end GitHub Actions'iga? (1-5)
  4. Milline stage oli kõige huvitavam? (valik)
  5. Üks küsimus, mis jäi vastamata (avatud)

**Teacher resource:**
- Kodutöö tutvustus (väljakutsed 6.1-6.3)

---

**KOKKU: 90 min (10+10+20+15+20+10+5+5)**

---

## Hindamisvahend: CI/CD Pipeline Rubriik

### Kasutamine
- **Millal:** Labor + kodutöö hindamisel
- **Kuidas:** Õpetaja kontrollib GitHub Actions tab'i ja repo struktuuri

### Kriteeriumid

| Kriteerium | 0-1p | 2p | 3p | 4p |
|------------|------|----|----|-----|
| **Pipeline struktuur** | 1 stage või ei tööta | 2 stages | 3 stages | 4 stages + manual approval |
| **YAML süntaks** | Vigu, ei käivitu | Käivitub, vigu | Töötab | Töötab + dokumenteeritud |
| **Vigade parandamine** | Ei parandanud | 1-2 viga | 3-4 viga | Kõik + selgitas |
| **Docker integration** | Build puudub | Build töötab | Build + push | Build + health check + push |
| **Testimine** | Testid puuduvad | Töötavad lokaalselt | Töötavad CI's | + täiendavad testid |
| **Dokumentatsioon** | README puudub | Minimaalne | + badge | Detailne + screenshots |
| **Manual approval** | Puudub | Seadistatud | Testitud | + juhised README's |
| **Väljakutsed** | Ei teinud | 1 tehtud | 2 tehtud | Kõik 3 tehtud |

**Maksimaalne:** 32 punkti

**Hindeskaal:**
- 29-32p → 5
- 23-28p → 4
- 17-22p → 3
- 11-16p → 2

### Kontrollnimekiri

**Tehnilised nõuded:**
- [ ] `.github/workflows/ci.yml` olemas
- [ ] Pipeline käivitub automaatselt
- [ ] Validate stage (Python syntax)
- [ ] Test stage (pytest)
- [ ] Build stage (Docker image)
- [ ] Deploy stage (vähemalt simulatsioon)

**Labor'i ülesanded:**
- [ ] Ülesanne 2.1: Süntaksi viga parandatud
- [ ] Ülesanne 3.1: Negatiivne hind parandatud
- [ ] Ülesanne 3.2: Versiooni mittevastavus parandatud
- [ ] Ülesanne 4.1: Dockerfile port parandatud

**Kodutöö:**
- [ ] Väljakutse 6.1: Uus endpoint + test
- [ ] Väljakutse 6.2: README + badge
- [ ] Väljakutse 6.3: Rollback mõtisklus

---

## Materjalid

**Loeng (kodutöö):**
- https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/loeng/

**Labor (tunnis):**
- https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/labor/

**Kodutöö:**
- https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/kodutoo/

**Tööriistad:**
- Mentimeter (quiz + exit ticket)
- GitHub account (kõik õpilased)
- Git (kohalik)
- VS Code (soovituslik)

---

## Märkused õpetajale

**Enne tundi:**
- [ ] Saada loengmaterjal 2 päeva ette
- [ ] Valmista Mentimeter quiz + exit ticket
- [ ] Tee labor ise läbi
- [ ] Demo repo valmis
- [ ] Kontrolli GitHub account'id

**Tunni ajal:**
- Quiz max 10 min - fookus praktikale
- Demo = täpselt nagu labor'is
- Õpeta logide lugemist, mitte kohe lahendusi
- "Pipeline fail = õppimise võimalus!"
- Exit ticket oluline tagasisideks

**Tüüpilised probleemid:**
- Actions ei käivitu → kas `.github/workflows/`?
- Permission denied → Settings → Workflow permissions
- Health check timeout → `sleep 10`
- YAML indent → VS Code extension
