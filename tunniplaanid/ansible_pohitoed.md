# Tunnikava: Ansible – Põhitõed (4×45 min) + 1.5h kodutöö

**Tase:** Põhitase (eelteadmised: Linux käsurida, SSH, YAML basics)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`, `seadistus.md`

---

## 🎯 Õpiväljundid (Learning Outcomes)
- ÕV1: Selgitab, mis probleemi Ansible lahendab; eristab Ansible teistest automatiseerimis tööriistadest
- ÕV2: Seadistab inventory faili ja SSH ühendused mitme serveri jaoks
- ÕV3: Kirjutab esimese playbook'i YAML süntaksiga ja kasutab põhilisi mooduleid
- ÕV4: Kasutab ad-hoc käske serverite haldamiseks ja info kogumiseks
- ÕV5: Rakendab idempotentsuse printsiipi ja best practices'eid

---

## 📚 Pedagoogiline raamistik (allikas: "How People Learn", NRC 2000)

### Kolm põhiprintsiipi, mida see tunnikava järgib:

1. **Eelteadmised (Prior Knowledge):**
   - Õpilased on kogenud "klikka 10× sama asja" probleemi
   - ALATI küsi enne õpetamist: "Kas oled kunagi seadistanud mitu serverit käsitsi? Kuidas see oli?"
   - Ehita uus teadmine olemasoleva peale (SSH → Ansible SSH; shell scripts → playbooks)

2. **Arusaamine > memoriseerimine (Understanding > Facts):**
   - Õpeta MIKS Ansible on vajalik, mitte ainult KUIDAS YAML kirjutada
   - Vähem mooduleid, rohkem sügavust (5-6 core modules vs 3000+)
   - Kontseptsioonid > süntaks (idempotence, declarative, agentless)

3. **Metakognitsioon (Metacognition):**
   - Õpilased peavad jälgima oma õppimist
   - Refleksioonid iga bloki lõpus (1-2 min)
   - Kontrollküsimused: "Miks idempotence on oluline? Millal kasuta playbook vs ad-hoc?"

---

## 🛠️ Õpetamismeetodid (Teaching Methods)

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|----------------|
| **Passiivne** | Loeng, demo (õpetaja näitab) | Blokk 1 algus (≤15 min) |
| **Aktiivne** | Õpilane teeb ise (guided practice) | Enamik lab'i aega (3×45 min) |
| **Interaktiivne** | Paaristöö, arutelu, selgitamine | Iga bloki lõpp (peer review) |
| **Think-aloud** | Õpetaja mõtleb valjusti (model thinking) | Demo ajal (YAML debug) |
| **Formatiivne** | Kontroll ilma hindeta (checklists) | Iga blokk (low-stakes) |

---

## 👨‍🏫 Näpunäited algajale õpetajale

### Enne tundi:
- [ ] Kontrolli, kas Ansible on kõigil installeeritud (`ansible --version`)
- [ ] Valmista ette Vagrant 2-VM setup (või kasuta cloud VM'e)
- [ ] Testi SSH ühendust ise ette (passwordless SSH on kriitiline!)
- [ ] Valmista ette näidis-playbook ja inventory (et ei peaks tunnis tühjalt lehelt alustama)
- [ ] YAML süntaks on tundlik taandetele (indentation) – rõhuta seda!

### Tunni ajal:
- **YAML indentation errors:** Kõige levinum algajate viga – kasuta ainult tühikuid (MITTE tabs!)
- **SSH permission denied:** Kontrolli `~/.ssh/authorized_keys` õigusi (600)
- **"changed: true" vs "changed: false":** Õpilased küsivad, mis vahe on – selgita idempotence!
- **Ansible on aeglane esimesel korral:** Normaalne – SSH handshake, fact gathering võtab aega
- **Playbook run kordamine on OK:** Idempotence tähendab, et saad sama playbook'i jooksutada 100× – tulemus sama!

### Kui midagi läheb valesti:
- **"Unreachable host":** SSH probleem → kontrolli `ansible all -m ping`
- **"Permission denied (publickey)":** SSH võti pole õigesti seadistatud
- **"sudo: a password is required":** `become: yes` on playbook'is, aga NOPASSWD pole seadistatud sudoers'is
- **"YAML syntax error":** Indentation! Kasuta `yamllint` või online YAML validator

---

## Blokk 1 (45 min) – Loeng ja Lab I: Ansible põhitõed ja SSH setup

- **Eesmärk:** Mõista, miks Ansible on vajalik, seadistada SSH ja inventory
- **Meetodid:** mini-loeng (≤15 min), think-aloud demo, juhendatud praktika
- **Minutiplaan:**
  - 0–5: Eelteadmised (kiirkirjutus "Kas oled kunagi seadistanud mitu serverit käsitsi?")
  - 5–15: Põhimõisted (agentless, idempotent, declarative, YAML) ja MIKS Ansible
  - 15–25: Demo (think-aloud): SSH võtmete setup, inventory loomine, `ansible all -m ping`
  - 25–45: Juhendatud praktika: õpilased seadistavad SSH, loovad inventory, testivad ping (Lab Setup)
- **Kontrollnimekiri:**
  - [ ] Ansible on installeeritud (`ansible --version`)
  - [ ] SSH ühendus töötab (passwordless)
  - [ ] Inventory fail on loodud
  - [ ] `ansible all -m ping` tagastab SUCCESS
- **Refleksioon (1–2 min):** "Miks on SSH setup nii oluline? Mida Ansible teeks ilma selleta?"
- **Fun Poll:** "Kui Ansible oleks robot, siis milline? A) koristusrobot B) 🤖 universaalne assistent C) droon"
- **Kohandus:** Kui SSH probleemsed, kasuta Docker container'eid VM'ide asemel; kui kiired, lisa Vagrant setup

---

## Blokk 2 (45 min) – Lab II: Ad-hoc käsud ja esimesed moodulid

- **Eesmärk:** Kasutada ad-hoc käske serverite haldamiseks, tutvuda põhiliste mooduliega
- **Meetodid:** lühidemo + iseseisev praktika, paariskontroll
- **Minutiplaan:**
  - 0–10: Demo: ad-hoc käsud (`-m ping`, `-m command`, `-m shell`, `-m copy`, `-m apt`)
  - 10–35: Juhendatud praktika: õpilased käivitavad ad-hoc käske (info, failid, paketid) (Lab Samm 1-2)
  - 35–40: Arutelu: Millal kasutada ad-hoc vs playbook? (ad-hoc = quick one-off tasks)
  - 40–45: Paariskontroll: selgita partnerile, mis vahe on `-m command` ja `-m shell` vahel
- **Kontrollnimekiri:**
  - [ ] Oskab kasutada vähemalt 3 erinevat moodulit ad-hoc käskudes
  - [ ] Mõistab `command` vs `shell` vs `raw` erinevust
  - [ ] Teab, millal kasutada ad-hoc vs playbook
- **Kontrollküsimused:** "Miks `command` moodul on turvalisem kui `shell`?"
- **Refleksioon (1–2 min):** "Ad-hoc käsud on nagu ühekordsed skriptid. Millal need kasulikud on?"
- **Kohandus:** Kui kiired, tutvusta `ansible-doc` käsku; kui aeglane, keskendu ainult `ping` ja `command`

---

## Blokk 3 (45 min) – Lab III: Esimene playbook ja YAML süntaks

- **Eesmärk:** Kirjutada esimene playbook, mõista YAML süntaksit ja idempotentsust
- **Meetodid:** demo + juhendatud praktika, iseseisev töö
- **Minutiplaan:**
  - 0–10: YAML süntaksi demo: indentation, list, dict, key-value (think-aloud) + näita viga
  - 10–30: Juhendatud praktika: õpilased kirjutavad esimese playbook'i (nginx installimine) (Lab Samm 3)
  - 30–40: Idempotence demo: jooksuta sama playbook 2× – näita, et teine kord "changed: 0"
  - 40–45: Refleksioon ja kokkuvõte
- **Kontrollnimekiri:**
  - [ ] Playbook on kirjutatud ja töötab (YAML süntaks korrektne)
  - [ ] Nginx on installeeritud target serverites
  - [ ] Mõistab idempotentsust (sama playbook 2× = sama tulemus)
- **Kontrollküsimused:** "Mis on idempotence? Miks see oluline on?"
- **Refleksioon (1–2 min):** "Playbook on nagu retsept. Mis on kõige tähtsam osa?"
- **Kohandus:** Kui kiired, lisa handlers ja notify; kui aeg otsa, jäta idempotence demo kodutööks

---

## Blokk 4 (45 min) – Lab IV: Variables, templates ja best practices

- **Eesmärk:** Kasutada variables ja Jinja2 templates, rakendada best practices
- **Meetodid:** demo + praktika, näited (hea vs halb), viktoriin
- **Minutiplaan:**
  - 0–15: Variables demo: `vars:`, `vars_files:`, `{{ variable }}` (Lab Samm 4)
  - 15–30: Juhendatud praktika: lisa variables playbook'i, kasuta Jinja2 template nginx conf'ile
  - 30–40: Best practices: playbook struktuur, `ansible-lint`, naming conventions
  - 40–45: Ansible Quiz (lõbus viktoriin) + kodutöö tutvustus
- **Kontrollnimekiri:**
  - [ ] Variables toimivad playbook'is
  - [ ] Jinja2 template on loodud ja deploy'itud
  - [ ] Mõistab best practices põhimõtteid
- **Kontrollküsimused:** "Miks kasutada variables? Mis on Jinja2 eelised?"
- **Refleksioon (1–2 min):** "Mida teeksid järgmisel korral teisiti? Mis oli kõige kasulikum?"
- **Kohandus:** Kui kiired, tutvusta vault encrypted variables; kui aeg napib, jäta templates valikuliseks

---

## Kodutöö (1.5h, isetempoline)

- **Ülesanne:** Loo 3-tier web stack (web + app + db) 3 VM'is Ansible'iga; kirjuta playbook; kasuta roles
- **Kriteeriumid:**
  - [ ] 3 VM seadistatud (või Docker containers)
  - [ ] Playbook installeerib nginx, Python app, MySQL
  - [ ] Inventory on struktureeritud (groups)
  - [ ] Variables on kasutatud (ports, users, jne)
  - [ ] README.md sisaldab käivitamisjuhendit
- **Oluline:** Refleksioon README.md lõpus (5 küsimust, 2-3 lauset igaüks) – see on metakognitsioon praktikas!
- **Esitamine:** GitHub repo link (playbook, inventory, README)

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

### Ansible-spetsiifilised ressursid:
- **Ansible Documentation**: https://docs.ansible.com/
- **Ansible Galaxy**: https://galaxy.ansible.com/
- **Best Practices**: https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html
- **Ansible Lint**: https://ansible-lint.readthedocs.io/

### Õpetamise strateegiad:
- **Think-Aloud Protocol**: Verbaliseeri oma mõtteprotsess YAML kirjutamisel ("Hmm, indentation error... kontrollin tühikuid")
- **Reciprocal Teaching**: Õpilased õpetavad üksteist (pair-check)
- **Metacognitive Prompts**: "Mis oli raske? Kuidas lahendada? Mida teeksid teisiti?"

---

## 🎓 Kokkuvõte (TL;DR algajale õpetajale)

**Mida teha:**
1. ✅ Alusta eelteadmistega ("Kas oled seadistanud mitu serverit käsitsi?")
2. ✅ Õpeta MIKS Ansible on vajalik (mitte ainult KUIDAS YAML kirjutada)
3. ✅ Maksimaalselt 15 min loengut, ülejäänu praktika
4. ✅ SSH setup on kriitil ine – veendu, et see töötab enne playbook'e!
5. ✅ Idempotence demo on WOW-moment (jooksuta 2×, näita "changed: 0")
6. ✅ YAML indentation – rõhuta ainult tühikuid (MITTE tabs!)

**Mida MITTE teha:**
1. ❌ Ära õpeta 100 moodulit – keskendu 5-6 põhimoodulile (ping, command, copy, apt/yum, service, template)
2. ❌ Ära loengi 45 minutit – õpilased vajavad tegemist
3. ❌ Ära eelda, et SSH töötab kohe – esimene 20 min võib minna troubleshootingule!
4. ❌ Ära unusta YAML linter'it – `yamllint` on sinu sõber!
5. ❌ Ära hüppa roles'i – see on järgmine moodul!

**Edu!** 🚀 Kui küsimusi, vaata `loeng.md`, `labor.md`, `kodutoo.md` – seal on kõik välja kirjutatud.

