# GitHub Täiendavad Tööriistad

**Kasutamine:** Kiire ülevaade kaasaegsetest GitHub funktsioonidest

---

## GitHub Actions

Automatiseeritud töövood - testid, build, deployment käivituvad automaatselt.

**Näide:** Test käivitub iga push'i peale
```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v3
      - run: npm test
```

**Rohkem:** Vaata `lisapraktika.md` GitHub Actions harjutust

---

## Dev Containers

Määratle arenduskeskkond koodis - iga arendaja saab täpselt sama keskkonna.

**Fail:** `.devcontainer/devcontainer.json`

**Põhimõte:** "See töötab minu masinas" probleem lahendatud.

---

## GitHub Codespaces

Arenduskeskkond brauseris - ei pea midagi installima.

**Kasutamine:** Repository → Code → Open with Codespaces

**Pluss:** Uus meeskonnaliige saab alustada minutitega.

---

## Millal kasutada?

| Tööriist | Millal |
|----------|--------|
| **Actions** | Automatiseeri testimine, deployment |
| **Dev Containers** | Meeskonnatöö, keeruline setup |
| **Codespaces** | Kiire alustamine, õppimine |

---

**Rohkem infot:**

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Codespaces](https://docs.github.com/en/codespaces)