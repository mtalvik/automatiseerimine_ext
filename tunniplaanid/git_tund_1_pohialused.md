# Tunnikava: Git – Põhitõed (4×45 min) + 1.5h kodutöö

**Tase:** Põhitase (eelteadmised: ei pea teadma Git'i)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`, `lisapraktika.md`

---

## 🎯 Õpiväljundid (Learning Outcomes)
- ÕV1: Selgitab, mis probleemi Git lahendab; määratleb põhimõisted (repo, commit, branch, remote)
- ÕV2: Loob repo ja teeb ≥5 tähenduslikku commit'i erinevates branch'ides
- ÕV3: Kasutab töövoogu add → commit → push ja põhjendab valikuid
- ÕV4: Loob ja merge'ib lihtsaid branch'e; lahendab lihtsa merge konflikti
- ÕV5: Ühendab lokaalse repo GitHubiga ja teeb esimese pull request'i

---

## 📚 Pedagoogiline raamistik (allikas: "How People Learn", NRC 2000)

### Kolm põhiprintsiipi, mida see tunnikava järgib:

1. **Eelteadmised (Prior Knowledge):**
   - Õpilased tulevad tunni juba arusaamadega ("final_v2_REAL.py" probleem)
   - ALATI küsi enne õpetamist: "Kuidas sa praegu faile versioonid?"
   - Ehita uus teadmine olemasoleva peale

2. **Arusaamine > memoriseerimine (Understanding > Facts):**
   - Õpeta MIKS, mitte ainult KUIDAS
   - Vähem teemasid, rohkem sügavust (5 core concepts vs 20 commands)
   - Kontseptsioonid > käsud (workflow > individual commands)

3. **Metakognitsioon (Metacognition):**
   - Õpilased peavad jälgima oma õppimist
   - Refleksioonid iga bloki lõpus (1-2 min)
   - Kontrollküsimused: "Kas sa mõistad? Kuidas sa tead?"

---

## 🛠️ Õpetamismeetodid (Teaching Methods)

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|----------------|
| **Passiivne** | Loeng, demo (õpetaja näitab) | Blokk 1 algus (≤15 min) |
| **Aktiivne** | Õpilane teeb ise (guided practice) | Enamik lab'i aega (3×45 min) |
| **Interaktiivne** | Paaristöö, arutelu, selgitamine | Iga bloki lõpp (peer review) |
| **Think-aloud** | Õpetaja mõtleb valjusti (model thinking) | Demo ajal (Blokk 1) |
| **Formatiivne** | Kontroll ilma hindeta (checklists) | Iga blokk (low-stakes) |

---

## 👨‍🏫 Näpunäited algajale õpetajale

### Enne tundi:
- [ ] Kontrolli, kas Git on kõigil installeeritud (`git --version`)
- [ ] Valmista ette demo repo (et ei peaks tunnis tühjalt lehelt alustama)
- [ ] Ava `loeng.md` ja `labor.md` kahe ekraanina (lihtsam jagada)
- [ ] Testi SSH/HTTPS GitHub ühendust ise ette (et teaksid, kus probleemid võivad tekkida)

### Tunni ajal:
- **Ära karda vaikust:** 1-2 min refleksioon = normaalne (õpilased mõtlevad!)
- **Pair-check on võimas:** Kui õpilane seletab partnerile, ta õpib 2× rohkem
- **"Aga miks?" on parim küsimus:** Kui õpilane küsib, küsi tagasi "Mis sa arvad?"
- **Copy-paste on OK:** Lab'is võivad õpilased käske kopeerida (eesmärk = mõista workflow, mitte meelde jätta käske)

### Kui midagi läheb valesti:
- **"Olen ka algaja õpetaja, õpime koos!"** – ausus loob usalust
- **Git on raske kõigile alguses** – normaalne, et tekivad küsimused
- **Kasuta "parking lot"** – kirjuta keerulised küsimused tahvlile, vasta hiljem

---

## Blokk 1 (45 min) – Loeng ja Lab I: Git põhitõed
- Eesmärk: mõtestada versioonihaldus, seadistada Git, teha esimesed commit'id
- Meetodied: mini‑loeng (≤15 min), think‑aloud demo, juhendatud praktika
- Minutiplaan:
  - 0–5: Eelteadmised (kiirkirjutus „Kuidas versioonid praegu?") ja jagamine
  - 5–15: Põhimõisted (repo, commit, staging, log) ja MIKS Git on vajalik
  - 15–25: Demo (think‑aloud): `git config`, `git init`, README, `add`/`commit`, `log`
  - 25–45: Juhendatud praktika: õpilased teostavad sama ise (Harjutus 1.1, 1.2)
- Kontrollnimekiri: [ ] Git seadistatud; [ ] repo olemas, ≥2 commit'i; [ ] sõnumid tähenduslikud
- Refleksioon (1–2 min): „Mis oli kõige lahedam asi, mida õppisid?" + Fun Poll (Ctrl+Z vs commit)
- Kohandus: kui kiired, lisa `git diff` ja `.gitignore` tutvustus; kui aeglane, keskendu ainult 1 commit'ile

## Blokk 2 (45 min) – Lab II: Branching ja Merging
- Eesmärk: luua branch'e, arendada paralleelselt, merge'ida muudatusi
- Meetodid: lühidemo + iseseisev praktika, paariskontroll
- Minutiplaan:
  - 0–10: Demo: branch'ide idee, `git branch`, `git checkout -b`, töövoog
  - 10–35: Juhendatud praktika: loo 2 feature branch'i, arenda eraldi, merge main'i (Harjutus 2.1, 2.2)
  - 35–40: Merge konflikti demo ja lahendamine (Harjutus 2.3)
  - 40–45: Paariskontroll: selgita partnerile, miks branch'e kasutada
- Kontrollnimekiri: [ ] ≥2 branch'i loodud; [ ] merge'itud main'i; [ ] (bonus) konflikt lahendatud
- Refleksioon (1–2 min): „Millal on branch'id kasulikud?"
- Kohandus: kui konflikt liiga raske, jäta see valikuliseks; kui kiired, lisa rohkem branch'e

## Blokk 3 (45 min) – Lab III: GitHub ja Remote Repositories
- Eesmärk: ühendada lokaalne repo GitHubiga, push/pull, pull request
- Meetodid: demo + juhendatud praktika, iseseisev töö
- Minutiplaan:
  - 0–10: GitHub tutvustus, SSH võtmete seadistamine (Harjutus 3.1)
  - 10–30: Juhendatud praktika: loo GitHub repo, `git remote add`, `git push`, `git pull` (Harjutus 3.2)
  - 30–40: Pull Request workflow: loo branch, push, tee PR, merge (Harjutus 3.3)
  - 40–45: Refleksioon ja kokkuvõte
- Kontrollnimekiri: [ ] GitHub repo loodud; [ ] lokaalne ühendatud remote'iga; [ ] edukalt push'itud; [ ] (bonus) PR tehtud
- Refleksioon (1–2 min): „Miks on hea koodi GitHubi panna?"
- Kohandus: kui SSH keeruline, kasuta HTTPS; kui aeg otsa, jäta PR kodutööks

## Blokk 4 (45 min) – Kvaliteet, Parimad Tavad ja Kokkuvõte
- Eesmärk: `.gitignore`, head commit-sõnumid, best practices, kordamine
- Meetodid: näited (hea vs halb), probleemipõhine ülesanne, mäng/viktoriin
- Minutiplaan:
  - 0–10: Hea vs halb commit-sõnum (näited); `.gitignore` otstarve ja näited
  - 10–25: Praktika: lisa `.gitignore` oma projekti, paranda commit-sõnumeid
  - 25–35: Git best practices (kui tihti commit, millal push, mida mitte repos hoida)
  - 35–45: Commit Meme Check (lõbus viktoriin) + kodutöö tutvustus
- Kontrollnimekiri: [ ] `.gitignore` olemas ja põhjendatud; [ ] viimane sõnum selgitav; [ ] mõistab best practices
- Refleksioon (1–2 min): „Mida teeksid järgmisel korral teisiti? 6 sõnaga."
- Kohandus: kui aeg napib, jäta best practices kodutöö juurde; kui kiired, suuna boonus ülesannete juurde (tags, aliases, stash, README ilu)

## Kodutöö (1.5h, isetempoline)
- Ülesanne: Loo väike projekt; tee ≥5 sisulist commit'i tähenduslike sõnumitega; (valik) push GitHubi
- Kriteeriumid: repo olemas; ≥5 commit'i; sõnumid arusaadavad ja põhjendavad; õige töövoog
- **Oluline:** Refleksioon README.md lõpus (5 küsimust, 2-3 lauset igaüks) – see on metakognitsioon praktikas!
- Esitamine: repo link või .zip + `git log --oneline`

---

## 📖 Viited ja täiendav lugemine (õpetajale)

### Pedagoogilised alused:
1. **National Research Council (2000).** *How People Learn: Brain, Mind, Experience, and School.* Washington, DC: The National Academies Press.
   - Peatükk 1: "Learning: From Speculation to Science" – eelteadmised, arusaamine, metakognitsioon
   - Peatükk 2: "How Experts Differ from Novices" – miks arusaamine > meeldejätmine

2. **Bransford, J., & Schwartz, D. (1999).** "Rethinking Transfer: A Simple Proposal with Multiple Implications." *Review of Research in Education, 24*, 61-100.
   - Transfer = õpilased kannavad teadmisi üle uutesse olukordadesse (refleksioon aitab!)

3. **Black, P., & Wiliam, D. (1998).** "Assessment and Classroom Learning." *Assessment in Education, 5*(1), 7-74.
   - Formatiivne hindamine = feedback ilma hindeta (checklists, peer review)

### Git-spetsiifilised ressursid:
- **Pro Git raamat** (tasuta): https://git-scm.com/book/en/v2
- **GitHub Education**: https://education.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

### Õpetamise strateegiad:
- **Think-Aloud Protocol**: Verbaliseeri oma mõtteprotsess demo ajal ("Hmm, ma ei tea, mis siin juhtus... proovin `git status`")
- **Reciprocal Teaching**: Õpilased õpetavad üksteist (pair-check)
- **Metacognitive Prompts**: "Mis oli raske? Kuidas lahendada? Mida teeksid teisiti?"

---

## 🎓 Kokkuvõte (TL;DR algajale õpetajale)

**Mida teha:**
1. ✅ Alusta eelteadmistega ("Kuidas sa praegu versioonid?")
2. ✅ Õpeta MIKS (mitte ainult KUIDAS)
3. ✅ Maksimaalselt 15 min loengut, ülejäänu praktika
4. ✅ Refleksioon iga bloki lõpus (1-2 min)
5. ✅ Pair-check (õpilased selgitavad üksteisele)
6. ✅ Formatiivne hindamine (checklists, no grades)

**Mida MITTE teha:**
1. ❌ Ära õpeta 20 käsku – keskendu 5 kontseptsioonile
2. ❌ Ära loengi 45 minutit – õpilased vajavad tegemist
3. ❌ Ära eelda, et õpilased "lihtsalt saavad aru" – küsi, kontrolli, reflekteeri
4. ❌ Ära karda vigu – "õpime koos" on OK!

**Edu!** 🚀 Kui küsimusi, vaata `loeng.md`, `labor.md`, `kodutoo.md` – seal on kõik välja kirjutatud.
