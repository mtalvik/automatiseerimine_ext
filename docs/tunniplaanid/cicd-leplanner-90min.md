# CI/CD Pipeline GitHubis

**LePlanner:** https://leplanner.ee/en/scenario/5444  
**Klass:** 12 | **Kestus:** 90 min | **Õpiväljund:** ÕV7

---

## Kodutöö

Loe 20-min loeng: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/loeng/

---

## Tunni kulg

| Tegevus | min | Vorm | Materjal |
|---------|-----|------|----------|
| Mentimeter quiz | 10 | Klass | 5 küsimust: workflow, job, step, CI vs CD, runner |
| Live demo | 10 | Klass | GitHub Actions workflow loomine, validate stage |
| Hands-on 1: Validate + Test | 20 | Paarid | Tahtlikud vead: syntax, negatiivne hind, version |
| Paus | 15 | - | - |
| Hands-on 2: Build + Docker | 20 | Paarid | Tahtlik viga: EXPOSE 8080→5000, health check |
| Hands-on 3: Deploy | 10 | Paarid | Manual approval, environments |
| Tulemused | 5 | Klass | Paarid näitavad pipeline'e |
| Exit ticket | 5 | Individuaalne | Mentimeter: keerulisem? õppisin? enesekindel? |

---

## Hindamine: CI/CD Pipeline Rubriik

| Kriteerium | 1p | 2p | 3p | 4p |
|------------|----|----|----|----|
| Pipeline | 1 stage | 2 stages | 3 stages | 4 stages + approval |
| YAML | Ei tööta | Töötab, vigu | Töötab | + dokumenteeritud |
| Vead | Ei parandanud | 1-2 | 3-4 | Kõik + selgitas |
| Docker | Puudub | Build | Build + push | + health check |
| Testid | Puuduvad | Lokaalselt | CI's | + täiendavad |
| README | Puudub | Minimaalne | + badge | + screenshots |
| Approval | Puudub | Seadistatud | Testitud | + juhised |
| Väljakutsed | 0 | 1 | 2 | 3 |

**Max:** 32p | **Skaal:** 29-32→5, 23-28→4, 17-22→3, 11-16→2

---

## Materjalid

- Loeng: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/loeng/
- Labor: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/labor/
- Kodutöö: https://mtalvik.github.io/automatiseerimine_ext/cicd_basics/kodutoo/
- Mentimeter quiz + exit ticket
- GitHub account (kõik)

---

## Õpetajale

**Enne:**
- Saada loeng 2 päeva ette
- Valmista Mentimeter quiz + exit
- Demo repo valmis
- Kontrolli GitHub account'id

**Tunnis:**
- Quiz max 10 min
- Demo = täpselt nagu labor
- Õpeta logide lugemist
- "Pipeline fail = õppimine!"

**Probleemid:**
- Actions ei käivitu → `.github/workflows/`?
- Permission denied → Workflow permissions
- Health check timeout → `sleep 10`
- YAML indent → VS Code extension
