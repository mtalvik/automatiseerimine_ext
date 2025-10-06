# CI/CD Edasijõudnud Kodutöö: Projekti Lõpetamine

**Tähtaeg:** Järgmise nädala alguseks  

---

## Ülesande kirjeldus

Lõpeta oma automatiseerimise projekt ja dokumenteeri see. See on lõppprojekt, mis integreerib kõik õpitud DevOps tööriistad.

---

##  **Ülesanded**

### 1. Projekti dokumenteerimine

**Loo README.md fail oma projekti jaoks:**

```markdown
# Minu Automatiseerimise Projekt

## Kirjeldus
[Kirjelda oma projekti - mida sa tegid?]

## Tehnoloogiad
- [ ] Git
- [ ] Docker
- [ ] Ansible
- [ ] Terraform
- [ ] CI/CD

## Kuidas kasutada
[Lisa lihtsad juhendid]

## Tulemused
[Kirjelda, mida sa õppisid]
```

### 2. GitHub repository

**Loo GitHub repository:**
```bash
# 1. Loo uus repository GitHubis
# 2. Push'i oma kood
git remote add origin https://github.com/teie-kasutajanimi/projekti-nimi.git
git push -u origin main

# 3. Lisa README.md fail
# 4. Lisa .gitignore fail
```

### 3. Projekti esitlus

**Valmista ette 2-3 minutiline esitlus:**
- Mida sa tegid?
- Millised tehnoloogiad kasutasid?
- Mida sa õppisid?

---

 

---

##  Refleksioon (kirjuta README.md lõppu)

Lisa oma README.md faili lõppu peatükk **"## Refleksioon"** ja vasta järgmistele küsimustele:

### Küsimused (vasta 2-3 lausega igaühele):

1. **Mis oli selle lõppprojekti juures kõige raskem ja kuidas sa selle lahendasid?**
   - Näide: "Kõige raskem oli integreerida kõik tööriistad kokku. Tegin sammhaaval ja debugisin iga osa eraldi."

2. **Milline DevOps tööriist oli sulle kõige huvitavam ja miks?**
   - Näide: "Mulle meeldis Kubernetes, sest see on nii võimas – saab hallata tuhandeid container'eid automaatselt!"

3. **Kuidas saaksid neid oskusi kasutada oma tulevases töös või projektides?**
   - Näide: "Võiksin luua CI/CD pipeline'i oma projektidele, et deployment oleks automaatne ja kiire."

4. **Kui peaksid selgitama sõbrale, mis on DevOps ja miks see on kasulik, siis mida ütleksid?**
   - Näide: "DevOps on arenduse ja operations'i ühendamine – kood läheb automaatselt kasutajateni ilma käsitsi tööta!"

5. **Mis oli selle kursusel kõige väärtuslikum õppetund?**
   - Näide: "Sain aru, et automatiseerimine on võti – mis tahes, mida teed 2x käsitsi, peaks olema automatiseeritud!"

---

## Kontrollnimekiri (enne esitamist)

**Kontrolli need asjad:**

- [ ] GitHubis on avalik repositoorium
- [ ] CI/CD pipeline töötab (build → test → deploy)
- [ ] Docker image'id on loodud
- [ ] Kubernetes deployment töötab
- [ ] Rakendus on ligipääsetav (browser/curl test)
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus (mis see on?)
  - [ ] Arhitektuur (millised tööriistad, miks?)
  - [ ] Kuidas seadistada (sammhaaval)
  - [ ] Kuidas käivitada (käsud)
  - [ ] Screenshots (pipeline, deployed app)
  - [ ] Refleksioon (5 küsimuse vastused)
- [ ] Presentation valmis (2-3 min)
- [ ] Kõik muudatused on GitHubi push'itud

---

##  Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **CI/CD Pipeline** | 25% | Pipeline töötab, build + test + deploy |
| **Docker** | 15% | Container images korrektsed ja optimeeritud |
| **Kubernetes** | 20% | Deployment töötab, scaling võimalik |
| **Integratsioon** | 15% | Kõik tööriistad töötavad koos |
| **README** | 10% | Projekti kirjeldus, käivitamisjuhend, selge |
| **Refleksioon** | 10% | 5 küsimust vastatud, sisukas, näitab mõistmist |
| **Presentation** | 5% | 2-3 min esitlus, selge, professionaalne |

**Kokku: 100%**

---

## Abimaterjalid ja lugemine

**Kiirviited:**
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Docs](https://kubernetes.io/docs/home/)

**Kui abi vaja:**
1. Vaata `lisapraktika.md` faili täiendavate näidete jaoks
2. Kasuta `kubectl logs` ja `kubectl describe` debugging'uks
3. Kasuta GitLab/GitHub pipeline logs
4. Küsi klassikaaslaselt või õpetajalt

---

## Boonus (valikuline, +10%)

**Kui tahad ekstra punkte, tee üks või mitu neist:**

1. **Monitoring:** Lisa Prometheus + Grafana
2. **Automated rollback:** Pipeline automaatselt rollback kui deploy fallib
3. **Multi-environment:** Dev, Staging, Production (erinevad konfiguratsioonid)
4. **Performance testing:** Lisa load testing pipeline'i (k6, JMeter)
5. **Security scanning:** Lisa Trivy või Snyk pipeline'i

---

## **Järgmised sammud**

1. **Jätka õppimist** - proovi uusi tehnoloogiaid
2. **Ehita projekte** - harjuta oskusi
3. **Liitu kogukondadega** - õpi teistelt

** Palju õnne! Oled nüüd valmis automatiseerimise projektideks!**
