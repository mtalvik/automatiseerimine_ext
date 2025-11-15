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

| # | Tegevus | Aeg | Vorm | Õpiväljund | Materjalid |
|---|---------|-----|------|------------|------------|
| 1 | **Mentimeter quiz** - kodutöö kontroll | 10 min | Whole class | ÕV7 | Mentimeter: 5 küsimust (workflow, job, step, CI vs CD, runner) |
| 2 | **Live demo** - GitHub Actions workflow | 10 min | Whole class | ÕV7 | Demo repo, validate stage, YAML syntax ref |
| 3 | **Hands-on 1** - Validate + Test stages | 20 min | Pair | ÕV7 | Labor 2.1, 3.1-3.2 (tahtlikud vead: syntax, negatiivne hind, version) |
| 4 | **PAUS** | 15 min | Meta | - | - |
| 5 | **Hands-on 2** - Build + Docker | 20 min | Pair | ÕV7 | Labor 4.1 (tahtlik viga: EXPOSE 8080→5000) |
| 6 | **Hands-on 3** - Deploy + Manual approval | 10 min | Pair | ÕV7 | GitHub Environments setup, approval workflow |
| 7 | **Demo tulemused** - paaride esitlused | 5 min | Whole class | ÕV7 | Demo template (stages, vead, debugging) |
| 8 | **Exit ticket** - Mentimeter refleksioon | 5 min | Individual | ÕV7 | Mentimeter: 5 küsimust (keerulisem? õppisin? enesekindel? huvitav? küsimus?) |

**KOKKU: 90 min**

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
