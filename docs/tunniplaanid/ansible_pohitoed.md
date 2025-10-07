# Tunnikava: Ansible Põhitõed

**Kestus:** 4×45 min + 1.5h kodutöö  
**Tase:** Põhitase  
**Eeldused:** Linux käsurida, SSH põhitõed, YAML süntaksi alused  
**Materjalid:** loeng.md, labor.md, kodutoo.md, lisapraktika.md, lisamaterjalid.md, seadistus.md, Vagrantfile

---

## Õpiväljundid

Pärast seda moodulit õpilased:

- Selgitavad, mis probleemi Ansible lahendab ja eristavad seda teistest automatiseerimistööriistadest
- Seadistavad inventory faili ja SSH ühendused mitme serveri jaoks
- Kirjutavad esimese playbook'i YAML süntaksiga ja kasutavad põhilisi mooduleid
- Kasutavad ad-hoc käske serverite haldamiseks ja info kogumiseks
- Rakendavad idempotentsuse printsiipi ja best practices'eid

---

## Pedagoogiline Raamistik

See tunnikava järgib "How People Learn" (National Research Council, 2000) põhimõtteid, mis rõhutavad kolme kriitlist elementi õppimisprotsessis.

### Eelteadmised (Prior Knowledge)

Uus teadmine ehitub alati olemasoleva peale. Enne Ansible õpetamist aktiveerige õpilaste eelteadmised:

- Küsige: "Kas olete kunagi seadistanud mitu serverit käsitsi? Kuidas see oli?"
- Ühendage uus vana külge: SSH → Ansible SSH, shell scripts → playbooks
- Tunnistage, et õpilased on kogenud "klikka 10 korda sama asja" probleemi

### Arusaamine üle memoriseerimise

Õpilased peavad mõistma kontseptsioone, mitte ainult süntaksit:

- Õpetage MIKS Ansible on vajalik, mitte ainult KUIDAS YAML kirjutada
- Vähem mooduleid, rohkem sügavust (5-6 põhimoodulit vs kõik 3000+)
- Fookus kontseptsioonidel: idempotence, declarative, agentless

### Metakognitsioon

Õpilased peavad jälgima oma õppimist:

- Refleksioonid iga bloki lõpus (1-2 minutit)
- Kontrollküsimused: "Miks idempotence on oluline? Millal kasutada playbook vs ad-hoc?"
- Kodutöö refleksioon (5 küsimust) võimaldab õpilastel hinnata oma mõistmist

---

## Õpetamismeetodid

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|----------------|
| Passiivne | Loeng, demonstratsioon (õpetaja näitab) | Blokk 1 algus, maksimaalselt 15 min |
| Aktiivne | Õpilane teeb ise (juhendatud praktika) | Enamik labori aega (3×45 min) |
| Interaktiivne | Paaristöö, arutelu, selgitamine | Iga bloki lõpp (peer review) |
| Think-aloud | Õpetaja mõtleb valjusti (model thinking) | Demo ajal (YAML debugging) |
| Formatiivne | Kontroll ilma hindeta (checklists) | Iga blokk (low-stakes assessment) |

---

## Näpunäited Algajale Õpetajale

### Enne tundi

Kontrollige järgmist enne tunni algust:

- [ ] Ansible on kõigil õpilastel installeeritud: `ansible --version`
- [ ] 2-VM setup on valmis (Vagrant või cloud VMs)
- [ ] SSH ühendus on testitud (passwordless SSH on kriitiline)
- [ ] Näidis playbook ja inventory on ette valmistatud
- [ ] YAML linter on saadaval (`yamllint` või online validator)

### Tunni ajal - Tüüpilised probleemid

**YAML indentation vead**
- Kõige levinum algajate viga
- Kasutage ainult tühikuid, MITTE tab'e
- Soovitus: näidake ette õige ja vale näide kõrvuti

**SSH ühenduse vead**
- "Permission denied"
- kontrollige `~/.ssh/authorized_keys` õigusi (600)
- "Host unreachable"
- kontrollige IP aadresse inventory failis
- Alati testige esmalt: `ansible all -m ping`

**Idempotentsuse mõistmine**
- Õpilased küsivad: "Miks "changed: false"?"
- Selgitage: sama playbook võib käivitada 100 korda, tulemus sama
- Demonstreerige live: käivitage playbook kaks korda

**Aeglus esimesel käivitamisel**
- SSH handshake ja fact gathering võtab aega
- See on normaalne, ärge muretsege

### Kui midagi läheb valesti

**"Unreachable host"**
- SSH probleem
- Lahendus: `ansible all -m ping` ja kontrollige SSH ühendust käsitsi

**"Permission denied (publickey)"**
- SSH võti pole õigesti seadistatud
- Lahendus: `ssh-copy-id` või kontrollige `~/.ssh/authorized_keys`

**"sudo: a password is required"**
- `become: yes` on playbook'is, aga NOPASSWD pole seadistatud
- Lahendus: kasutage `--ask-become-pass` või seadistage passwordless sudo

**"YAML syntax error"**
- Taandete (indentation) viga
- Lahendus: kasutage `yamllint` või online YAML validator

---

## 1. Loeng ja Lab I: Ansible põhitõed ja SSH setup

**Aeg:** 45 min  
**Eesmärk:** Mõista, miks Ansible on vajalik; seadistada SSH ja inventory  
**Meetodid:** Mini-loeng (maksimaalselt 15 min), think-aloud demo, juhendatud praktika

### Minutiplaan

**0-5 min: Eelteadmiste aktiveerimine**
- Kiirkirjutus: "Kas olete kunagi seadistanud mitu serverit käsitsi? Kirjelda kogemust"
- Mõned õpilased jagavad (2-3 min)
- Siduge nende kogemus Ansible'i vajadusega

**5-15 min: Põhimõisted**
- Mis on Ansible ja MIKS see on vajalik
- Põhikontseptsioonid: agentless, idempotent, declarative
- YAML süntaksi kiirülevaade (indentation, lists, dicts)
- Ansible vs teised tööriistad (Puppet, Chef, SaltStack)

**15-25 min: Think-aloud demo**
- SSH võtmete genereerimine
- Võtme kopeerimine target serverisse
- Inventory faili loomine
- Esimene test: `ansible all -m ping`
- Mõelge valjusti: "Hmm, kas IP on õige? Kontrollin inventory faili..."

**25-45 min: Juhendatud praktika**
- Õpilased seadistavad SSH (labor.md)
- Loovad inventory faili
- Testivad: `ansible all -m ping`
- Õpetaja liigub ringi, aitab probleemide korral

### Kontrollnimekiri

Õpilased peavad saavutama:

- [ ] Ansible on installeeritud ja versioon kontrollitud
- [ ] SSH võtmed on genereeritud
- [ ] SSH ühendus töötab ilma paroolita
- [ ] Inventory fail on loodud õigete IP-dega
- [ ] `ansible all -m ping` tagastab SUCCESS mõlemale serverile

### Kontrollküsimused

Küsige õpilastelt:

- "Miks on SSH setup nii oluline Ansible'i jaoks?"
- "Mis juhtub, kui SSH võti pole õigesti seadistatud?"
- "Mida Ansible teeks ilma inventory failita?"

### Refleksioon

Viimased 1-2 minutit:

- "Mida õppisite selles blokis?"
- "Mis oli kõige raskem?"
- "Kui peaksite sõbrale selgitama, mis on Ansible, mida ütleksite?"

### Kohandus

**Kui õpilased on kiired:**

- Lisa Vagrant setup
- Tutvusta `ansible.cfg` faili
- Näita `ansible-doc` käsku

**Kui õpilased on aeglased:**

- Keskendu ainult ühele target serverile (mitte kahele)
- Kasuta Docker container'eid VM-ide asemel (kiirem setup)
- Jäta inventory gruppide selgitus järgmisesse blokki

---

## 2. Lab II: Ad-hoc käsud ja esimesed moodulid

**Aeg:** 45 min  
**Eesmärk:** Kasutada ad-hoc käske serverite haldamiseks; tutvuda põhiliste mooduliega  
**Meetodid:** Lühidemo (10 min) + iseseisev praktika, paariskontroll

### Minutiplaan

**0-10 min: Ad-hoc käskude demo**
- Mis on ad-hoc käsud ja millal neid kasutada
- Demo järgmiste moodulitega:
  - `ping`
  - ühenduse test
  - `command`
  - käsu käivitamine
  - `shell`
  - shell käsud (pipes, redirects)
  - `copy`
  - failide kopeerimine
  - `apt/yum`
  - pakettide installimine
- Rõhutage: ad-hoc = quick one-off tasks

**10-35 min: Juhendatud praktika**
- Õpilased käivitavad ad-hoc käske (labor.md)
- Info kogumine: hostname, uptime, memory
- Failide kopeerimine: test.txt → /tmp/
- Paketi installimine: htop
- Kasutaja loomine
- Õpetaja liigub ringi, vastab küsimustele

**35-40 min: Arutelu**
- Millal kasutada ad-hoc vs playbook?
- Ad-hoc: testimine, info kogumine, ühekordsed taskid
- Playbook: korduvad taskid, keeruline loogika, dokumentatsioon

**40-45 min: Paariskontroll**
- Õpilased selgitavad partnerile:
  - Mis vahe on `command` ja `shell` mooduli vahel?
  - Millal kasutada kumba?
- Õpetaja kuulab paare, annab tagasisidet

### Kontrollnimekiri

Õpilased peavad saavutama:

- [ ] Oskavad kasutada vähemalt 3 erinevat moodulit ad-hoc käskudes
- [ ] Mõistavad `command` vs `shell` vs `raw` erinevust
- [ ] Teavad, millal kasutada ad-hoc vs playbook
- [ ] Oskavad kasutada `--become` lippu

### Kontrollküsimused

- "Miks `command` moodul on turvalisem kui `shell`?"
- "Millal te eelistaksite ad-hoc käsku playbook'ile?"
- "Kuidas kontrollida, kas käsk õnnestus?"

### Refleksioon

- "Ad-hoc käsud on nagu ühekordsed skriptid. Millal need kasulikud on?"
- "Mis oli kõige huvitavam moodul ja miks?"

### Kohandus

**Kui kiired:**

- Tutvustage `ansible-doc` käsku
- Uurige `setup` moodulit (facts)
- Proovige filtreerimist: `--limit`, `--tags`

**Kui aeglased:**

- Keskenduge ainult `ping` ja `command` moodulitele
- Jätke `shell` ja keerulisemad moodulid valikuliseks
- Rohkem aega troubleshooting'ule

---

## 3. Lab III: Esimene playbook ja YAML süntaks

**Aeg:** 45 min  
**Eesmärk:** Kirjutada esimene playbook; mõista YAML süntaksit ja idempotentsust  
**Meetodod:** Demo + juhendatud praktika, iseseisev töö

### Minutiplaan

**0-10 min: YAML süntaksi demo**
- YAML põhitõed: indentation, list, dict, key-value
- Think-aloud: kirjutage lihtne playbook valjusti mõeldes
- Näidake VALE näide (tab'id, vale indentation) ja ÕIGE näide
- Rõhutage: ainult tühikud, 2 tühiku taande

**10-30 min: Juhendatud praktika**
- Õpilased kirjutavad esimese playbook'i (labor.md)
- Eesmärk: nginx installimine
- Playbook struktuur:
  - `name`, `hosts`, `become`, `tasks`
  - Iga task vajab `name` ja moodulit
- Käivitage playbook: `ansible-playbook -i inventory playbook.yml`
- Troubleshootinge YAML vigu koos

**30-40 min: Idempotentsuse demo**
- Selgitage: idempotence = sama tulemus mitu korda
- Demo live: käivitage sama playbook teist korda
- Näidake: "changed: 0" vs "changed: 1"
- Arutelu: miks see oluline on?

**40-45 min: Refleksioon ja kokkuvõte**
- "Mis on idempotence ja miks see oluline on?"
- "Playbook on nagu retsept. Mis on kõige tähtsam osa?"

### Kontrollnimekiri

Õpilased peavad saavutama:

- [ ] Playbook on kirjutatud ja YAML süntaks on korrektne
- [ ] Nginx on edukalt installeeritud target serveritesse
- [ ] Playbook käivitus õnnestus ilma vigadeta
- [ ] Mõistavad idempotentsust (teine käivitus ei muuda midagi)
- [ ] Teavad, kuidas debugida YAML vigu

### Kontrollküsimused

- "Mis on idempotence? Anna näide."
- "Miks on YAML indentation nii oluline?"
- "Kuidas kontrollida, kas playbook on idempotentne?"

### Refleksioon

- "Mis oli playbook'i kirjutamisel kõige raskem?"
- "Kuidas te debugisite YAML vigu?"

### Kohandus

**Kui kiired:**

- Lisage handlers ja notify
- Tutvustage `--check` režiimi (dry run)
- Lisage mitu taski ühte playbook'i

**Kui aeg otsa:**

- Jätke idempotentsuse demo kodutööks
- Keskenduge ainult lihtsa playbook'i kirjutamisele
- Handlers järgmises blokis

---

## 4. Lab IV: Variables, templates ja best practices

**Aeg:** 45 min  
**Eesmärk:** Kasutada variables ja Jinja2 templates; rakendada best practices  
**Meetodod:** Demo + praktika, näited (hea vs halb)

### Minutiplaan

**0-15 min: Variables demo**
- Mis on variables ja miks neid kasutada
- Variables deklareerimine: `vars:`, `vars_files:`
- Variables kasutamine: `{{ variable }}`
- Demo: lisa variables playbook'i (labor.md)
- Näidised: port number, username, app name

**15-30 min: Jinja2 templates**
- Mis on Jinja2 ja millal seda kasutada
- Template struktuur: `{{ variable }}`, `{% for %}`, `{% if %}`
- Demo: loo nginx config template
- Juhendatud praktika: õpilased loovad template'i
- Deploy template: `template` moodul

**30-40 min: Best practices**
- Playbook struktuur: loetav, kommenteeritud
- Naming conventions: kirjeldavad nimed, snake_case
- `ansible-lint` tutvustus
- Group_vars ja host_vars
- Idempotentsuse kontroll

**40-45 min: Kodutöö tutvustus**
- Kodutöö ülevaade: LAMP stack deployment
- Nõuded ja hindamiskriteeriumid
- Tähtaeg ja esitamise viis
- Küsimused

### Kontrollnimekiri

Õpilased peavad saavutama:

- [ ] Variables toimivad playbook'is
- [ ] Jinja2 template on loodud
- [ ] Template on edukalt deploy'itud serverisse
- [ ] Mõistavad best practices põhimõtteid
- [ ] Teavad, kuidas kasutada `ansible-lint`

### Kontrollküsimused

- "Miks kasutada variables?"
- "Mis on Jinja2 eelised plain failide ees?"
- "Millal kasutada template'i vs copy?"

### Refleksioon

- "Mida teeksite järgmisel korral teisiti?"
- "Mis oli selles blokis kõige kasulikum?"
- "Kui peaksite sõbrale selgitama, mida Ansible teeb, mida ütleksite?"

### Kohandus

**Kui kiired:**

- Tutvustage Ansible Vault (encrypted variables)
- Group_vars ja host_vars kaustad
- Complex Jinja2: filters, loops

**Kui aeg napib:**

- Jätke templates valikuliseks
- Keskenduge ainult variables'ile
- Best practices lühemalt

---

## Kodutöö

**Aeg:** 1.5 tundi (isetempolise)  
**Ülesanne:** Loo LAMP stack deployment Ansible'iga

### Nõuded

Õpilased peavad looma:

- [ ] Ansible projekti koos inventory failiga
- [ ] Playbook'id Apache, MySQL ja PHP paigaldamiseks
- [ ] Variables group_vars kaustas
- [ ] Template nginx/apache konfiguratsiooni jaoks
- [ ] README.md käivitamisjuhendiga
- [ ] Refleksioon README.md lõpus (5 küsimust)

### Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| Funktsionaalsus | 40% | LAMP stack töötab, kõik teenused käivituvad |
| Koodikvaliteet | 30% | Playbook'id organiseeritud, variables kasutatud, idempotentne |
| Dokumentatsioon | 15% | README selge, käivitamisjuhend täpne |
| Refleksioon | 15% | 5 küsimust vastatud, sisukas, näitab mõistmist |

### Refleksioonikü simused

README.md lõpus peavad olema vastused (2-3 lauset igaüks):

1. Mis oli selle kodutöö juures kõige raskem ja kuidas lahendasite?
2. Milline Ansible kontseptsioon oli teile kõige suurem "ahaa!" hetk ja miks?
3. Kuidas saaksite Ansible'i kasutada oma teistes projektides või töös?
4. Kui peaksite sõbrale selgitama, mis on Ansible ja miks see kasulik, mida ütleksite?
5. Mis oli selle projekti juures kõige lõbusam või huvitavam osa?

### Esitamine

- GitHub avalik repositoorium
- Link esitatakse õppeplatvormi
- Tähtaeg: järgmise nädala algus

---

## Viited ja Täiendav Lugemine

### Pedagoogilised alused

**National Research Council (2000).** How People Learn: Brain, Mind, Experience, and School. Washington, DC: The National Academies Press.
- Peatükk 1: Learning: From Speculation to Science
- Peatükk 2: How Experts Differ from Novices

**Bransford, J., & Schwartz, D. (1999).** Rethinking Transfer: A Simple Proposal with Multiple Implications. Review of Research in Education, 24, 61-100.

**Black, P., & Wiliam, D. (1998).** Assessment and Classroom Learning. Assessment in Education, 5(1), 7-74.

### Ansible ressursid

- Ansible Documentation: https://docs.ansible.com/
- Ansible Galaxy: https://galaxy.ansible.com/
- Ansible Best Practices: https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html
- Ansible Lint: https://ansible-lint.readthedocs.io/

### Õpetamise strateegiad

**Think-Aloud Protocol**
- Verbaliseeri oma mõtteprotsess YAML kirjutamisel
- Näide: "Hmm, indentation error... kontrollin tühikuid"

**Reciprocal Teaching**
- Õpilased õpetavad üksteist
- Paaristöö ja peer review

**Metacognitive Prompts**
- "Mis oli raske? Kuidas lahendasite? Mida teeksite teisiti?"

---

## Kokkuvõte

### Mida teha

1. Alustage eelteadmistega: "Kas olete seadistanud mitu serverit käsitsi?"
2. Õpetage MIKS Ansible on vajalik, mitte ainult KUIDAS
3. Maksimaalselt 15 minutit loengut, ülejäänu praktika
4. SSH setup on kriitiline - veenduge, et see töötab
5. Idempotence demo on WOW-moment - jooksutage playbook kaks korda
6. YAML indentation - rõhutage ainult tühikuid

### Mida mitte teha

1. Ärge õpetage 100 moodulit - keskendu 5-6 põhimoodulile
2. Ärge loengige 45 minutit - õpilased vajavad tegemist
3. Ärge eeldage, et SSH töötab kohe - esimene 20 min võib minna troubleshooting'ule
4. Ärge unustage YAML linter'it - `yamllint` on teie sõber
5. Ärge hüpake rolle'i - see on järgmine moodul

Edu õpetamisel! Kui küsimusi, vaadake loeng.md, labor.md ja kodutoo.md - seal on kõik detailselt kirjas.