# Tunnikava: Ansible Edasijõudnud Funktsioonid

**Kestus:** 3×45 min  
**Tase:** Edasijõudnud  
**Eeldused:** Ansible põhiteadmised, playbook'id, YAML süntaks  
**Materjalid:** loeng.md, labor.md, kodutoo.md, lisapraktika.md

---

## Õpiväljundid

Pärast seda õppetükki õpilane:
- Mõistab muutujate hierarhia põhimõtteid ja rakendab neid projektides
- Kirjutab Jinja2 template'eid dünaamiliste konfiguratsioonide loomiseks
- Kasutab handler'eid teenuste efektiivseks haldamiseks
- Krüpteerib tundlikud andmed Ansible Vault'iga
- Struktureerib Ansible projekte professionaalselt

---

## Pedagoogiline Raamistik

See õppetükk järgib "How People Learn" (National Research Council, 2000) põhimõtteid:

**Eelteadmised aktiveeritakse:**
Õpilased teavad juba, kuidas kirjutada lihtsaid playbook'e. Tunneme ära, et neil on kogemus copy-paste probleemiga - sama kood mitmes kohas. See on motivatsioon õppida abstraktsiooni (muutujad, template'id).

**Mõistmine üle memoreerimise:**
Ei õpeta ainult käske ("ansible-vault create..."), vaid MIKS vault on vajalik. Õpilased mõistavad, miks plain-text paroolid on probleem, seejärel õpivad lahendust.

**Metakognitsioon:**
Iga tunni lõpus reflekteeritakse: "Mis oli kõige raskem?" "Kuidas kasutaksid seda tulevikus?" Õpilased mõtlevad oma õppimise üle.

---

## Õpetamismeetodid

| Meetod | Kirjeldus | Millal kasutada |
|--------|-----------|-----------------|
| Otsene õpetus | Õpetaja näitab kontseptsiooni ja demonstreerib | Uute kontseptsioonide tutvustamine (muutujate hierarhia) |
| Juhitud praktika | Õpilased teevad koos õpetajaga | Labor'i esimesed sammud |
| Iseseisev praktika | Õpilased töötavad iseseisvalt | Labor'i lõpuosad, kodutöö |
| Think-Pair-Share | Mõtle → Aruta paarilisega → Jaga klassiga | Refleksioonid, kontrollküsimused |
| Debugging koos | Õpilased debugivad üksteise koodi | Kui keegi kinni jääb |

---

## Näpunäited Algajale Õpetajale

**Enne tundi:**
- Testi kõik labor'i sammud läbi - vault paroolid peavad töötama
- Valmista ette backup vault fail juhuks, kui õpilane unustab parooli
- Kontrolli, et kõigil on Ansible 2.9+ installitud
- Valmista ette "cheat sheet" Jinja2 süntaksiga

**Tunni ajal:**
- Vault parooli unustamine on KATASTROOF - rõhuta seda mitmel korral
- Kui õpilane küsib "miks mitte lihtsalt...?" - see on hea küsimus, arutle
- Template'id on keerulised - lase aega, ära kiirusta
- Kui keegi on kiire valmis, suuna lisapraktika juurde

**Levinud vead:**
- Õpilased panevad vault_pass faili Git'i - kontrolli .gitignore't
- Unustavad `{{ }}` template'ides - näita error message't
- Handler'id ei käivitu - selgita, et ainult kui midagi MUUTUB
- Muutujate hierarhia segane - joonista skeem tahvlile

**Kui midagi läheb valesti:**
- Labor'i server ei tööta? Kasuta localhost'i
- Vault parool ununes? Kasuta dekrüpteeritud backup faili
- Template ei genereeru? Kasuta `--check` mode'i testimiseks
- Õpilased ekslevad? Paus, joonista skeem, alusta otsast

---

## 1. Tund: Muutujate Hierarhia ja Skaleeritavus (45 min)

**Aeg:** 45 min  
**Eesmärk:** Mõista, miks muutujad lahendavad skaleeritavuse probleemi  
**Meetodid:** Otsene õpetus, demonstratsioon, juhitud praktika

### Minutiplaan

**0-5 min: Aktiviseerimine**
- "Kui palju servereid te hakkate haldama peale kooli? 3? 30? 300?"
- "Mis juhtub, kui teil on 50 playbook'i ja peate muutma üht asja?"
- Näita probleemi: 5 faili sama koodiga, viga ühes korduv kõigis

**5-15 min: Kontseptsiooni tutvustamine**
- Joonista tahvlile muutujate hierarhia
- Näita, kuidas spetsiifilisem võidab üldisema
- Demo: sama playbook, erinevad tulemused dev vs prod

**15-30 min: Demonstratsioon**
- Näita reaalajas: loo group_vars struktuuri
- Näita, kuidas üks muutuja override'ib teist
- Näita faktide kasutamist (ansible_processor_vcpus)

**30-40 min: Juhitud praktika**
- Õpilased loovad koos: group_vars/all/, group_vars/webservers/
- Defineerivad muutujaid: app_port, max_workers
- Testime koos: käivitame playbook, vaatame erinevaid tulemusi

**40-45 min: Refleksioon**
- Think-Pair-Share: "Kuidas see lahendab copy-paste probleemi?"
- Õpilased kirjutavad ühe lause: "Muutujate hierarhia on kasulik, sest..."

### Kontrollnimekiri

- [ ] Õpilased mõistavad, miks copy-paste ei skaleeru
- [ ] Õpilased teavad hierarhia järjekorda (host > group > all)
- [ ] Õpilased näevad, kuidas faktid töötavad
- [ ] Õpilased on loonud oma esimese group_vars struktuuri

### Kontrollküsimused

1. Mis juhtub, kui sama muutuja on group_vars/all/ ja host_vars/server1/ ?
2. Kuidas leida välja serveri RAM kogus Ansible faktidest?
3. Miks on DRY (Don't Repeat Yourself) oluline?

### Refleksioon (1-2 min kirjalik)

"Kirjelda ühe lausega, kuidas muutujate hierarhia aitab hallata suurt infrastruktuuri."

### Kohandus

**Kui õpilased on kiired:**
- Näita ka ansible.cfg failist muutujate seadistamist
- Tutvusta registered variables't

**Kui õpilased on aeglased:**
- Jäta faktid järgmisesse tundi
- Keskendu ainult group_vars/all vs group_vars/groupname

---

## 2. Tund: Jinja2 Template'id (45 min)

**Aeg:** 45 min  
**Eesmärk:** Kirjutada dünaamilisi konfiguratsioonifaile  
**Meetodid:** Demonstratsioon, juhitud praktika, iseseisev töö

### Minutiplaan

**0-5 min: Seostamine eelmisega**
- "Eelmine kord õppisime muutujaid. Nüüd panna need konfiguratsioonifailidesse."
- Näita probleemi: 2 nginx.conf faili dev ja prod jaoks

**5-20 min: Template'ide tutvustamine**
- Joonista: Template + Muutujad = Konfiguratsioonifail
- Näita Jinja2 süntaksit: `{{ }}`, `{% if %}`, `{% for %}`
- Demo: lihtne template, mis genereerib 2 erinevat faili

**20-35 min: Labor'i alustamine (juhitult)**
- Loome koos esimese template: nginx.conf.j2
- Lisame muutujad: `{{ server_name }}`
- Lisame tingimuse: `{% if ssl_enabled %}`
- Testimine: genereerime faili ja vaatame

**35-43 min: Iseseisev praktika**
- Õpilased lisavad loop'i virtual_hosts jaoks
- Õpilased lisavad filtreid (default, int)
- Õpetaja liigub ringi, aitab

**43-45 min: Kiire refleksioon**
- "Mis oli kõige keerulisem?" (näpuotsaga)
- "Mis eristab template'i tavalisest failist?"

### Kontrollnimekiri

- [ ] Õpilased eristavad `{{ }}` ja `{% %}`
- [ ] Õpilased on kirjutanud vähemalt ühe if tingimuse
- [ ] Õpilased on kasutanud vähemalt ühte loop'i
- [ ] Template genereerib töötava konfiguratsioonifaili

### Kontrollküsimused

1. Mis vahe on `{{ muutuja }}` ja `{% if muutuja %}` vahel?
2. Kuidas teha loop üle virtual_hosts listist?
3. Mida teeb filter `| default(80)`?

### Refleksioon (1 min kirjalik)

"Template'id on kasulikud, sest... (üks näide oma sõnadega)"

### Kohandus

**Kui õpilased on kiired:**
- Tutvusta makrosid: `{% macro %}`
- Näita template inheritance't

**Kui õpilased on aeglased:**
- Jäta loop edasisesse tundi
- Keskendu ainult muutujatele ja ühele if tingimusele

---

## 3. Tund: Handler'id ja Vault (45 min)

**Aeg:** 45 min  
**Eesmärk:** Efektiivne teenuste haldamine ja paroolide krüpteerimine  
**Meetodid:** Demonstratsioon, praktika, arutelu

### Minutiplaan

**0-3 min: Probleem**
- "Kui palju korda Apache restartib, kui muudate 5 konfiguratsioonifaili?"
- Näita probleemi: 5 restart'i = 5x downtime

**3-15 min: Handler'id**
- Selgita: handler käivitub ainult kui midagi muutub
- Selgita: käivitub ainult üks kord lõpus
- Demo: notify → handler → restart

**15-20 min: Handler'id praktikas**
- Õpilased lisavad handler'i oma playbook'i
- Testimine: käivitame 2x, teist korda ei restart'i

**20-25 min: Vault tutvustamine**
- "Kus te hoiate paroole? Git'is? MITTE KUNAGI!"
- Näita: plain text parool Git'is on katastroof
- Näita: krüpteeritud vault fail

**25-40 min: Vault praktika**
- Demonstreerin: `ansible-vault create secrets.yml`
- Õpilased teevad koos: loovad vault faili
- Lisavad paroole
- Kasutavad playbook'is: `{{ vault_mysql_password }}`
- Käivitamine: `--ask-vault-pass`

**40-45 min: Kriitiline teema**
- HOIATUS: vault parool unustamine = katastroof
- .gitignore kontroll: .vault_pass ei tohi Git'i minna
- Refleksioon: "Miks vault on parem kui plain-text?"

### Kontrollnimekiri

- [ ] Õpilased mõistavad handler'ite eesmärki
- [ ] Õpilased on loonud vähemalt ühe handler'i
- [ ] Õpilased on krüpteerinud vähemalt ühe vault faili
- [ ] Õpilased teavad, et .vault_pass ei tohi Git'i minna
- [ ] Playbook käivitub vault parooliga

### Kontrollküsimused

1. Miks handler käivitub ainult playbook'i lõpus?
2. Mis vahe on restart ja reload vahel?
3. Miks plain-text paroolid Git'is on ohtlikud?
4. Mis juhtub, kui unustad vault parooli?

### Refleksioon (1-2 min kirjalik)

"Handler'id säästävad... ja Vault kaitseb..."

### Kohandus

**Kui õpilased on kiired:**
- Näita listen groups't
- Tutvusta multiple vault ID'd

**Kui õpilased on aeglased:**
- Jäta vault järgmisesse tundi
- Keskendu ainult handler'itele

---

## Kodutöö: Production-Ready Ansible Projekt (1.5h)

**Eesmärk:** Rakendada kõiki õpitud tehnikaid ühes projektis

**Ülesanne:**
Loo LAMP stack deployment, mis kasutab kõiki õpitud tehnikaid:
- Muutujate hierarhia (group_vars/all, group_vars/dev, group_vars/prod)
- Jinja2 template'id (Nginx, MySQL, PHP konfiguratsioonid)
- Handler'id (teenuste restart/reload)
- Vault (database paroolid, API võtmed)

**Täpsem kirjeldus:** Vaata kodutoo.md

**Esitamine:**
- Git repository link
- README.md reflektsiooniga
- Töötav playbook (testime järgmine kord)

**Hindamiskriteeriumid:**

| Kriteerium | Punkte | Kirjeldus |
|------------|--------|-----------|
| Muutujate hierarhia | 20 | group_vars struktuur, vähemalt 2 keskkonda |
| Template'id | 25 | Vähemalt 2 template'i, kasutab tingimusi ja loop'e |
| Handler'id | 20 | Teenused restart'ivad ainult kui vaja |
| Vault | 20 | Kõik paroolid krüpteeritud, .vault_pass pole Git'is |
| Refleksioon | 15 | 5 küsimust vastatud, mõtlik analüüs |
| **Kokku** | **100** | |

**Boonus (+10%):**
- Kasuta ansible.cfg faili optimeerimiseks
- Lisa error handling (failed_when, ignore_errors)
- Dokumenteeri keerulised osad kommentaaridega

---

## Viited ja Täiendav Lugemine

**Ansible dokumentatsioon:**
- [Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Jinja2 Templates](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)
- [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)

**Pedagoogiline kirjandus:**
- National Research Council (2000). "How People Learn: Brain, Mind, Experience, and School"
- Sweller, J. (1988). "Cognitive load during problem solving"
- Vygotsky, L. S. (1978). "Mind in Society"

**Praktilised ressursid:**
- [Ansible Examples](https://github.com/ansible/ansible-examples)
- [Jeff Geerling's Blog](https://www.jeffgeerling.com/blog)

---

## Kokkuvõte

**Õpetajale meelespea:**

**Teha:**
- Aktiveeri eelteadmisi (copy-paste probleem)
- Selgita MIKS enne KUIDAS
- Anna aega praktikaks
- Liigu ringi, aita
- Küsi refleksioonikuisimusi

**Mitte teha:**
- Ära näita käske ilma selgituseta
- Ära kiirusta läbi kontseptsioonide
- Ära unusta vault parooli hoiatust
- Ära eelda, et kõik saavad ühel ajal valmis

**Kui midagi läheb valesti:**
- Pausi, selgita uuesti
- Joonista tahvlile
- Küsi õpilastelt: "Mis osa oli segane?"
- Kasuta Think-Pair-Share

**Edu näitajad:**
- Õpilased küsivad "miks" küsimusi (hea märk!)
- Õpilased aitavad üksteist
- Kodutööd on mitmekesised (ei ole kõik identsed)
- Õpilased kasutavad neid tehnikaid projektides

Järgmisel nädalal räägime Ansible Role'idest ja Galaxy'st - kuidas teha nendest tehnikatest korduvkasutatavad komponendid!