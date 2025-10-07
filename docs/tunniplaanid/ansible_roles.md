# Tunnikava: Ansible Roles – Korduvkasutatavad Playbook'id (4×45 min) + 4-6h kodutöö

**Tase:** Keskmine (eelteadmised: Ansible Basics, YAML, playbooks, Vagrant)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`, `lisapraktika.md`

---

## 🎯 Õpiväljundid

- ÕV1: Mõistab rollide eesmärki ja Galaxy standardi struktuuri komponente
- ÕV2: Loob production-ready rolle Galaxy konventsioonide järgi
- ÕV3: Eristab muutujate prioriteete (defaults, vars, group_vars) ja kasutab neid strateegiliselt
- ÕV4: Rakendab handlers'eid teenuste ohutukuks taaskäivitamiseks
- ÕV5: Implementeerib template'ides conditional logic'ut ja variable layering'ut
- ÕV6: Haldab role dependencies ja role composition'i
- ÕV7: Võrdleb push-based (Ansible) ja pull-based (Puppet) automatiseerimist

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased on kirjutanud playbook'e ja kogenud duplication pain point'e
2. **Constructivist Learning:** Õpilased ehitavad production-ready role kätest üles
3. **Problem-Based Learning:** Alusta "500-realise playbook" probleemiga, roles on lahendus
4. **Scaffolding:**
   - Blokk 1: Lihtne role struktuuri loomine
   - Blokk 2-3: Lisa komplekssust (variables, templates, conditions)
   - Blokk 4: Integreeri kõik kokku (SSL, vhosts, handlers)
5. **Metakognitsioon:**
   - DRY (Don't Repeat Yourself) principle
   - Separation of Concerns (iga kaust oma vastutus)
   - Infrastructure as Code best practices
6. **Formatiivne hindamine:**
   - Iga bloki lõpus validation check
   - Idempotence test (käivita kaks korda)
   - Peer review paariskontroll
7. **Summaarse hindamine:** Võrdlusprojekt (Ansible vs Puppet) näitab mõistmist

---

## 🛠️ Õpetamismeetodid

| Meetod | Kirjeldus | Millal | Aeg |
|--------|-----------|--------|-----|
| **Passiivne** | Mini-loeng (kontseptid) | Iga bloki algus | ~10 min/blokk |
| **Demonstratiivne** | Live coding demo | Pärast mini-loengut | ~10-15 min/blokk |
| **Aktiivne** | Hands-on lab (role ehitamine) | Peamine õppimine | ~20-25 min/blokk |
| **Interaktiivne** | Paaristöö code review | Bloki lõpus | ~5 min/blokk |
| **Reflektiivne** | Kontrollküsimused, validation | Iga bloki lõpp | ~5 min/blokk |
| **Võrdlev** | Kodutöö (Ansible vs Puppet) | Pärast tundi | 4-6h |

**Õpetaja roll:**

- **Guide on the side, not sage on the stage** - õpilased loovad, õpetaja juhib
- Live demo'des näita ka VIGU - see on oluline õppimiseks
- Vagrant VM'i troubleshooting on osa õppimisest
- Rõhuta et Galaxy'st leitavad rollid on õppimise allikas

---

## 👨‍🏫 Näpunäited

### Enne tundi

- [ ] Ansible Basics ja playbook'ide teema lõpetatud
- [ ] Vagrant testkeskkond kontrollitud (VirtualBox paigaldatud)
- [ ] Demo role valmis (`ansible-galaxy init nginx-webserver` kõigi komponentidega)
- [ ] 500-realise monoliter playbook näide ettevalmistatud
- [ ] Geerlingguy rolle uuritud (head production näited)

### Tunni ajal

- **Galaxy struktuur on range:** `tasks/main.yml`, `handlers/main.yml` jne – rõhuta konventsiooni ja selle eesmärki!
- **Defaults vs vars segadus:** See on #1 küsimus! Demo precedence hierarchy graafikuga
- **Handlers vs tasks:** Õpilased ei mõista miks handler käivitub alles play lõpus
- **Idempotence:** Käivita role KAKS KORDA iga demo ajal - näita "ok" vs "changed"
- **Template validation:** `validate: 'nginx -t -c %s'` on life-saver - rõhuta!
- **No_log flag:** Näita kuidas secrets ei lokaalu (security!)
- **Include_tasks conditionals:** `when` töötab include_tasks'iga, mitte import_tasks'iga

### Troubleshooting

- **"Role not found":** Kontrolli `ansible-config dump | grep ROLES_PATH`
- **"Handler not triggered":**
  - `notify` nimi ei ühti handlers/main.yml nimega (case-sensitive!)
  - Task ei muutnud midagi (pole "changed")
  - Handler syntax error - testida `--syntax-check`
- **"Template error":**
  - Jinja2 süntaks vale (unustatud `%}`)
  - Undefined muutuja - kasuta `| default('value')`
  - Wrong filter syntax
- **"Nginx config test failed":**
  - Missing includes (sites-enabled/* path vale)
  - SSL cert path ei eksisteeri
  - Validate käsk sai vigase conf
- **Vagrant VM ei käivitu:**
  - VirtualBox versioon konflikt
  - Port forwarding conflict (8080 juba kasutusel)
  - Insufficient memory
- **Variables precedence segadus:**
  - Näita hierarchy diagrammi
  - Demo: `ansible localhost -m debug -a "var=muutuja" -e "muutuja=override"`

---

## 1. Rollide Vajadus ja Galaxy Standard (45 min)

- **Eesmärk:** Mõista miks modulariseerimine on kriitiline, tutvuda Galaxy standardiga
- **Minutiplaan:**
  - 0–5: Hook: "500-realine playbook probleem - kas see on tuttav?"
  - 5–15: Loeng: Playbook'ide evolutsioon, rollide arhitektuur
  - 15–25: Demo: Galaxy standard struktuur (`ansible-galaxy init nginx-webserver`)
  - 25–40: Lab Osa 1: Vagrant keskkond üles, role struktuur loomine
  - 40–45: Refleksioon: "Miks iga kaust omab kindlat eesmärki?"
- **Materjalid:** loeng.md, labor.md

---

## 2. Variables Strateegia ja Prioriteedid (45 min)

- **Eesmärk:** Mõista defaults vs vars, OS-spetsiifiline konfiguratsioon
- **Minutiplaan:**
  - 0–10: Loeng: Variables precedence hierarchy, defaults vs vars roll
  - 10–20: Demo: OS-spetsiifiline variables mapping (_nginx_packages_map)
  - 20–40: Lab Osa 2: defaults/main.yml ja vars/main.yml loomine
  - 40–45: Kontrollküsimus: "Millal kasuta defaults, millal vars?"
- **Näpunäide:** Õpilased segivad tihti defaults ja vars - rõhuta prioriteete!
- **Materjalid:** loeng.md, labor.md

---

## 3. Tasks Organiseerimine ja Idempotence (45 min)

- **Eesmärk:** Struktureerida tasks'e loogiliselt, tagada idempotentsus
- **Minutiplaan:**
  - 0–10: Loeng: include_tasks vs import_tasks, idempotence põhimõtted
  - 10–25: Demo: Modular tasks structure (install.yml, configure.yml, ssl.yml)
  - 25–40: Lab Osa 3: Tasks'ide implementeerimine (validation, install, configure)
  - 40–45: Testimine: käivita role kaks korda, vaata "changed" vs "ok"
- **Troubleshooting:** "Role not found" - kontrolli ANSIBLE_ROLES_PATH
- **Materjalid:** loeng.md, labor.md

---

## 4. Templates, Handlers ja SSL (45 min)

- **Eesmärk:** Jinja2 templates dynamic config'uks, handlers service management'iks
- **Minutiplaan:**
  - 0–10: Loeng: Jinja2 conditional blocks, handlers vs tasks
  - 10–25: Demo: nginx.conf.j2 template, SSL setup, handler triggering
  - 25–40: Lab Osa 4: Templates, SSL certificates, virtual hosts, handlers
  - 40–45: Validation: curl -k (localhost), check handlers käivitusid
- **Kontrollküsimus:** "Miks reload on parem kui restart?"
- **Materjalid:** loeng.md, labor.md

---

## Kodutöö (4-6h)

- **Ülesanne:** Ansible vs Puppet võrdlusprojekt - ehita sama veebiserveri infrastruktuur mõlemal viisil
- **Komponendid:**
  - Nginx veebiserver SSL'iga
  - Kaks virtual host'i (test.local, demo.local)
  - PostgreSQL andmebaas
  - Health check monitoring
  - Log rotation
- **Kriteeriumid:**
  - [ ] Ansible implementatsioon 3 rolliga (nginx, postgresql, monitoring)
  - [ ] Puppet implementatsioon samade komponentidega
  - [ ] Mõlemad VM'id (Vagrant) töötavad identset konfiguratsiooni
  - [ ] COMPARISON.md põhjaliku analüüsiga (architecture, syntax, performance, use cases)
  - [ ] README setup juhenditega
  - [ ] 5 refleksioonküsimusele vastatud
  - [ ] Git repository avalik GitHubis
- **Hindamine:** 100% (Ansible 25%, Puppet 25%, Võrdlus 20%, Dokumentatsioon 15%, Koodiqualiteet 10%, Refleksioon 5%)
- **Boonus võimalused:** +15% (Docker deployment, CI/CD pipeline, performance benchmarks)

---

## 📖 Viited

**Dokumentatsioon:**

- **Ansible Roles Docs:** <https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html>
- **Ansible Galaxy:** <https://galaxy.ansible.com/>
- **Ansible Vault:** <https://docs.ansible.com/ansible/latest/user_guide/vault.html>
- **Jinja2 Templates:** <https://jinja.palletsprojects.com/>

**Raamatud:**

- Jeff Geerling: *Ansible for DevOps* (praktiline guide)
- Lorin Hochstein & René Moser: *Ansible: Up and Running*

**Community Ressursid:**

- Geerlingguy's Ansible Roles: <https://github.com/geerlingguy> (production-ready näited)
- Ansible Community: <https://docs.ansible.com/ansible/latest/community/>

**Pedagoogika:**

- NRC (2000) *How People Learn*
- Constructivist learning theory - "õpi tehes"

---

## 🎓 Kokkuvõte

**Teha:**

- ✅ Näita 500-realise playbook probleem ja kuidas roles lahendab
- ✅ Galaxy standard struktuur (`ansible-galaxy init`)
- ✅ Defaults vs vars prioriteedid (praktiline demo!)
- ✅ Idempotence testimine (run kaks korda)
- ✅ Handlers workflow (notify → play end → trigger)
- ✅ Jinja2 conditional logic template'ides
- ✅ OS-spetsiifiline variables mapping
- ✅ SSL setup ja validation
- ✅ DRY principle läbiv teema

**Mitte teha:**

- ❌ Galaxy publish esimesel tunnil (liiga advanced)
- ❌ Molecule testing framework (lisapraktika teema)
- ❌ Complex role dependencies (meta/dependencies) - maini ainult
- ❌ Multiple vault passwords - basic vault piisab

**Lisapraktika õpilastele kes kiiresti valmis:**

- Multi-OS rollide tugi (Ubuntu + CentOS)
- Environment layering (dev/staging/prod)
- Ansible Vault integratsioon