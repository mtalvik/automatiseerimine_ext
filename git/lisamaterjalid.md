# 📚 Git Õppematerjalid

**Eesmärk:** Git'i sügavamaks õppimiseks ja praktiliste oskuste arendamiseks  
**Aeg:** 2-3 tundi lugemist

---

## 📖 GitHubi Uued Tööriistad

GitHub ei ole enam lihtsalt koodimajutus. Tänapäeval pakub ta ka tööriistu, mis teevad arenduse, testimise ja keskkondade haldamise palju lihtsamaks. Kolm kõige olulisemat uuendust on **GitHub Actions**, **Dev Containers** ja **Codespaces**.

---

## ⚡ GitHub Actions – automatiseeritud töövood

GitHub Actions võimaldab käivitada **CI/CD protsesse** otse GitHubis: testide jooksutamine, lintimine, buildimine ja isegi automaatne deployment. Kõik käivitub, kui teed *push* või *pull requesti*.

Näide töövoost (`.github/workflows/ci.yml`):

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
```

👉 Lisalugemist:

* [FreeCodeCamp – GitHub Actions Step-by-Step](https://www.freecodecamp.org/news/learn-to-use-github-actions-step-by-step-guide/)
* [GitHub Docs – About Actions](https://docs.github.com/en/actions)

![GitHub Actions Workflow](https://miro.medium.com/v2/resize\:fit:720/format\:webp/0*sQyU_6RKSft1_DR0)

---

## 📦 Dev Containers – “see töötab minu masinas” probleem lahendatud

Dev Containers lubavad määratleda, milline arenduskeskkond projektile vaja on.
Näiteks `.devcontainer/devcontainer.json` fail võib öelda: kasuta Node 18, ava port 3000 ja installi sõltuvused.

See tähendab, et iga arendaja saab täpselt sama keskkonna – sõltumata opsüsteemist.

👉 Lisalugemist:

* [GitHub Docs – Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

---

## 🌐 GitHub Codespaces – arendus pilves

Codespaces viib Dev Containerid **otse pilve**. Ei pea enam midagi oma masinasse seadistama – piisab, kui avad repo GitHubis ja klikid *“Open with Codespaces”*.

* Avaneb VS Code brauseris või lokaalselt.
* Keskkond on kohe valmis tööks.
* Uus arendaja saab projektiga liituda minutitega.

👉 Lisalugemist:

* [DataCamp – GitHub Codespaces Tutorial](https://www.datacamp.com/tutorial/github-codespaces)
* [GitHub Docs – Developing in a Codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/developing-in-a-codespace)

![GitHub Codespaces Overview](https://docs.github.com/assets/cb-355846/mw-1440/images/help/codespaces/codespace-overview-annotated.webp)

---

💡 **Kokkuvõte:**

* **Actions** = automatiseeritud töövood (CI/CD)
* **Dev Containers** = ühtne arenduskeskkond Dockeri põhjal
* **Codespaces** = arendus pilves, kohe valmis

Need kolm tööriista viivad Giti ja GitHubi uuele tasemele – arendus ei ole enam ainult koodi kirjutamine, vaid ka keskkonna, töövoogude ja koostöö täielik integreerimine.
