# Tunnikava: Terraform – Põhitõed (4×45 min) + 1.5h kodutöö

**Tase:** Põhitase (eelteadmised: põhiline käsurida, failisüsteem)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`

---

## 🎯 Õpiväljundid (Learning Outcomes)
- ÕV1: Selgitab, mis on Infrastructure as Code ja miks see on vajalik
- ÕV2: Kirjutab lihtsat Terraform HCL koodi ja kasutab local provider'it
- ÕV3: Käivitab Terraform workflow'i: `init`, `plan`, `apply`, `destroy`
- ÕV4: Mõistab state faili rolli ja kuidas Terraform jälgib ressursse
- ÕV5: Rakendab põhilisi best practices'eid (variables, outputs, `.gitignore`)

---

## 📚 Pedagoogiline raamistik (allikas: "How People Learn", NRC 2000)

### Kolm põhiprintsiipi, mida see tunnikava järgib:

1. **Eelteadmised (Prior Knowledge):**
   - Õpilased on teinud käsitsi faile/kaustu (manual setup)
   - ALATI küsi enne õpetamist: "Kas oled kunagi seadistanud serverit käsitsi? Kui tüütu see oli?"
   - Ehita uus teadmine olemasoleva peale (käsitsi setup → declarative code)

2. **Arusaamine > memoriseerimine (Understanding > Facts):**
   - Õpeta MIKS IaC on vajalik, mitte ainult KUIDAS HCL süntaksit kirjutada
   - Vähem ressursside tüüpe, rohkem sügavust (3-4 core resources vs 1000+)
   - Kontseptsioonid > süntaks (declarative, state, idempotence)

3. **Metakognitsioon (Metacognition):**
   - Õpilased peavad jälgima oma õppimist
   - Refleksioonid iga bloki lõpus (1-2 min)
   - Kontrollküsimused: "Miks state on oluline? Millal `plan` vs `apply`?"

---

## 🛠️ Õpetamismeetodid (Teaching Methods)

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|----------------|
| **Passiivne** | Loeng, demo (õpetaja näitab) | Blokk 1 algus (≤15 min) |
| **Aktiivne** | Õpilane teeb ise (guided practice) | Enamik lab'i aega (3×45 min) |
| **Interaktiivne** | Paaristöö, arutelu, selgitamine | Iga bloki lõpp (peer review) |
| **Think-aloud** | Õpetaja mõtleb valjusti (model thinking) | Demo ajal (plan → apply) |
| **Formatiivne** | Kontroll ilma hindeta (checklists) | Iga blokk (low-stakes) |

---

## 👨‍🏫 Näpunäited algajale õpetajale

### Enne tundi:
- [ ] Kontrolli, kas Terraform on kõigil installeeritud (`terraform version`)
- [ ] Alusta LOCAL provider'iga (mitte AWS/Azure) – lihtsam ja tasuta!
- [ ] Valmista ette näidis `.tf` fail (et ei peaks tunnis tühjalt lehelt alustama)
- [ ] Selgita state faili enne `apply` käsku – see on kõige keerulisem kontseptsioon!
- [ ] HCL süntaks on sarnane JSON'ile – rõhuta seda

### Tunni ajal:
- **`terraform plan` on WOW-moment:** Näita, mida Terraform teeks ENNE tegelikku muudatust!
- **State fail on kriitiline:** Kõige levinum küsimus "Mis see `terraform.tfstate` on?"
- **Esimene `apply` võtab aega:** Provider download + setup võib võtta 10-30s
- **`.terraform/` kaust tekib:** Selgita, et see on cache ja tuleb `.gitignore`'ida
- **HCL errors:** Tavaliselt süntaksivead (puuduv `}`, vale indentation)

### Kui midagi läheb valesti:
- **"Error: Initialization required":** Unustatud `terraform init`
- **"Error locking state file":** Teine protsess kasutab – sulge see
- **"Resource already exists":** State ja reaalsus ei ühti – import või `terraform refresh`
- **"Provider not found":** `terraform init` pole käivitatud või vale versioon

---

## Blokk 1 (45 min) – Loeng ja Lab I: IaC põhitõed ja esimene resource

- **Eesmärk:** Mõista, mis on Infrastructure as Code, kirjutada esimene Terraform fail
- **Meetodid:** mini-loeng (≤15 min), think-aloud demo, juhendatud praktika
- **Minutiplaan:**
  - 0–5: Eelteadmised (kiirkirjutus "Kui tüütu on seadistada serverid käsitsi?")
  - 5–15: Põhimõisted (IaC, declarative, HCL, state) ja MIKS Terraform
  - 15–25: Demo (think-aloud): esimene `.tf` fail, `init`, `plan`, `apply`
  - 25–45: Juhendatud praktika: õpilased kirjutavad esimese resource'i (local_file) (Lab Samm 1)
- **Kontrollnimekiri:**
  - [ ] Terraform on installeeritud (`terraform version`)
  - [ ] Esimene `.tf` fail on loodud
  - [ ] `terraform init` käivitatud edukalt
  - [ ] `terraform apply` lõi faili
- **Refleksioon (1–2 min):** "Mis oli kõige üllatavam Terraform'i kohta? Kuidas see erineb käsitsi failide loomisest?"
- **Fun Poll:** "Kui Terraform oleks tööriist, siis milline? A) automaatpüstol B) 🤖 ehitusrobot C) joonistusmasin"
- **Kohandus:** Kui kiired, lisa `terraform destroy`; kui aeglane, keskendu ainult `init` ja `apply`

---

## Blokk 2 (45 min) – Lab II: State fail ja workflow

- **Eesmärk:** Mõista state faili rolli, kasutada Terraform workflow'i (`plan` → `apply` → `destroy`)
- **Meetodid:** lühidemo + iseseisev praktika, paariskontroll
- **Minutiplaan:**
  - 0–10: State fail demo: `terraform.tfstate` sisu, miks see on oluline
  - 10–35: Juhendatud praktika: muuda resource'i, jooksuta `plan`, vaata diff'i, `apply` (Lab Samm 2)
  - 35–40: `terraform destroy` demo – kõik ressursid kustutatakse
  - 40–45: Paariskontroll: selgita partnerile, miks state fail on vajalik
- **Kontrollnimekiri:**
  - [ ] Oskab kasutada `terraform plan` (vaadata muudatusi ENNE apply)
  - [ ] Mõistab state faili rolli (Terraform "mälu")
  - [ ] Oskab resource'i muuta ja uuesti `apply`
  - [ ] Teab, kuidas `destroy` töötab
- **Kontrollküsimused:** "Mis juhtub, kui state fail kaob? Miks ei tohi seda käsitsi muuta?"
- **Refleksioon (1–2 min):** "State fail on nagu Terraform mälu. Mida see meeles peab?"
- **Kohandus:** Kui kiired, tutvusta remote state; kui aeglane, jäta `destroy` valikuliseks

---

## Blokk 3 (45 min) – Lab III: Variables ja outputs

- **Eesmärk:** Kasutada variables parameetriseerimiseks ja outputs info väljastamiseks
- **Meetodid:** demo + juhendatud praktika, iseseisev töö
- **Minutiplaan:**
  - 0–10: Variables demo: `variable {}`, `var.name`, `terraform.tfvars` (Lab Samm 3)
  - 10–30: Juhendatud praktika: lisa variables (filename, content) ja outputs (file path)
  - 30–40: Iseseisev töö: loo 3+ faili variables'idega, jooksuta `plan` ja `apply`
  - 40–45: Refleksioon ja kokkuvõte
- **Kontrollnimekiri:**
  - [ ] Variables on deklareeritud ja kasutatud
  - [ ] `terraform.tfvars` fail on loodud
  - [ ] Outputs näitavad loodud ressursside infot
  - [ ] Mõistab, miks variables on kasulikud (reusability)
- **Kontrollküsimused:** "Miks kasutada variables? Mis vahe on `variable` ja `local` vahel?"
- **Refleksioon (1–2 min):** "Variables on nagu funktsiooni parameetrid. Miks need kasulikud on?"
- **Kohandus:** Kui kiired, lisa `locals {}` ja `count`; kui aeg otsa, jäta `outputs` valikuliseks

---

## Blokk 4 (45 min) – Lab IV: Best practices ja realworld use case

- **Eesmärk:** Rakendada best practices, kasutada Terraform real-world stsenaariumis
- **Meetodid:** demo + praktika, näited (hea vs halb), viktoriin
- **Minutiplaan:**
  - 0–15: Best practices demo: `.gitignore`, directory structure, naming (Lab Samm 4)
  - 15–30: Juhendatud praktika: loo struktureeritud projekt (modules, variables, outputs)
  - 30–40: Real-world demo: loo nginx config fail + directory Terraform'iga
  - 40–45: Terraform Quiz (lõbus viktoriin) + kodutöö tutvustus
- **Kontrollnimekiri:**
  - [ ] `.gitignore` on olemas (state, `.terraform/`)
  - [ ] Projekt on struktureeritud (failide nimed, kaustade struktuur)
  - [ ] Mõistab, mida MITTE commit'ida (state, credentials)
- **Kontrollküsimused:** "Miks ei tohi state faili Git'i panna? Mida peaks `.gitignore` sisaldama?"
- **Refleksioon (1–2 min):** "Mida teeksid järgmisel korral teisiti? Mis oli kõige kasulikum?"
- **Kohandus:** Kui kiired, tutvusta cloud provider'eid (AWS, Azure); kui aeg napib, jäta real-world demo kodutööks

---

## Kodutöö (1.5h, isetempoline)

- **Ülesanne:** Loo web serveri konfiguratsioon Terraform'iga (nginx config + html failid + directories); kasuta variables ja outputs
- **Kriteeriumid:**
  - [ ] Terraform failid on struktureeritud (`main.tf`, `variables.tf`, `outputs.tf`)
  - [ ] Loodud vähemalt 3 erinevat tüüpi resource'i (failid, kaustid, configs)
  - [ ] Variables on kasutatud (ports, paths, server_name)
  - [ ] Outputs näitavad loodud ressursside infot
  - [ ] `.gitignore` on olemas (state, `.terraform/`)
  - [ ] README.md sisaldab käivitamisjuhendit
- **Oluline:** Refleksioon README.md lõpus (5 küsimust, 2-3 lauset igaüks) – see on metakognitsioon praktikas!
- **Esitamine:** GitHub repo link (Terraform files, README)

---

## 📖 Viited ja täiendav lugemine

### Pedagoogilised alused:
1. **National Research Council (2000).** *How People Learn: Brain, Mind, Experience, and School.* Washington, DC: The National Academies Press.
   - Peatükk 1: "Learning: From Speculation to Science" – eelteadmised, arusaamine, metakognitsioon
   - Peatükk 2: "How Experts Differ from Novices" – miks arusaamine > meeldejätmine

2. **Bransford, J., & Schwartz, D. (1999).** "Rethinking Transfer: A Simple Proposal with Multiple Implications." *Review of Research in Education, 24*, 61-100.
   - Transfer = õpilased kannavad teadmisi üle uutesse olukordadesse (refleksioon aitab!)

3. **Black, P., & Wiliam, D. (1998).** "Assessment and Classroom Learning." *Assessment in Education, 5*(1), 7-74.
   - Formatiivne hindamine = feedback ilma hindeta (checklists, peer review)

### Terraform-spetsiifilised ressursid:
- **Terraform Documentation**: https://www.terraform.io/docs
- **Learn Terraform**: https://learn.hashicorp.com/terraform
- **Terraform Registry**: https://registry.terraform.io/
- **Best Practices**: https://www.terraform-best-practices.com/

### Õpetamise strateegiad:
- **Think-Aloud Protocol**: Verbaliseeri oma mõtteprotsess plan/apply ajal ("Hmm, see muudatus on ootamatu... vaatan state faili")
- **Reciprocal Teaching**: Õpilased õpetavad üksteist (pair-check)
- **Metacognitive Prompts**: "Mis oli raske? Kuidas lahendada? Mida teeksid teisiti?"

---

## 🎓 Kokkuvõte (TL;DR algajale õpetajale)

**Mida teha:**
1. ✅ Alusta eelteadmistega ("Kui tüütu on käsitsi setup?")
2. ✅ Õpeta MIKS IaC on vajalik (mitte ainult KUIDAS HCL kirjutada)
3. ✅ Maksimaalselt 15 min loengut, ülejäänu praktika
4. ✅ `terraform plan` on WOW-moment (näita diff'i ENNE apply!)
5. ✅ State fail demo on kriitiline – selgita põhjalikult!
6. ✅ Alusta LOCAL provider'iga (mitte AWS) – lihtsam ja tasuta!

**Mida MITTE teha:**
1. ❌ Ära hüppa cloud provider'itesse (AWS, Azure) kohe – liiga keeruline!
2. ❌ Ära õpeta 50 resource tüüpi – keskendu 3-4 põhilisele (file, dir, config)
3. ❌ Ära loengi 45 minutit – õpilased vajavad tegemist
4. ❌ Ära unusta `.gitignore`'i – state fail PEAB olema ignoreeritud!
5. ❌ Ära jäta state faili selgitamata – see on kõige keerulisem kontseptsioon!

**Edu!** 🚀 Kui küsimusi, vaata `loeng.md`, `labor.md`, `kodutoo.md` – seal on kõik välja kirjutatud.

