# Tunnikava: Ansible Roles – Korduvkasutatavad Playbook'id (4×45 min) + 1.5h kodutöö

**Tase:** Keskmine (eelteadmised: Ansible Basics, YAML, playbooks)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`

---

## 🎯 Õpiväljundid
- ÕV1: Selgitab, miks roles on paremad kui monoliitsed playbook'id
- ÕV2: Loob esimese role'i standardse struktuuriga (`ansible-galaxy init`)
- ÕV3: Kasutab tasks, handlers, templates, defaults role'is
- ÕV4: Impordib ja kasutab rolle playbook'ides
- ÕV5: Jagab rolle Ansible Galaxy'ga

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased teavad playbook'e – roles on parem abstraktion
2. **Arusaamine:** Õpeta MIKS modulariseerimine on vajalik
3. **Metakognitsioon:** DRY principle (Don't Repeat Yourself)

---

## 🛠️ Õpetamismeetodid

| Meetod | Kirjeldus | Millal |
|--------|-----------|--------|
| **Passiivne** | Loeng, demo | Blokk 1 (≤15 min) |
| **Aktiivne** | Role loomine | Lab (3×45 min) |
| **Interaktiivne** | Paaristöö review | Iga blokk lõpus |

---

## 👨‍🏫 Näpunäited

### Enne tundi:
- [ ] Ansible Basics lõpetatud
- [ ] Näidis role valmis (`ansible-galaxy init webserver`)
- [ ] Mitme playbook'i probleem selge

### Tunni ajal:
- **Role struktuur on range:** `tasks/main.yml` jne – rõhuta konventsiooni!
- **Handlers vs tasks:** Õpilased segivad
- **Galaxy search:** Näita, kuidas leida rolle
- **Dependencies:** Role võib sõltuda teisest role'ist

### Troubleshooting:
- **"Role not found":** Vale path või nimi
- **"Handler not triggered":** `notify` vale või puudub
- **"Template error":** Jinja2 süntaks vale

---

## Blokk 1 (45 min) – Roles põhitõed ja struktuur

- **Eesmärk:** Mõista roles'ide vajadust, luua esimene role
- **Minutiplaan:**
  - 0–5: "Kuidas sa kopeerid sama playbook kood 10× projektis?"
  - 5–15: Roles vs playbooks, role struktuur
  - 15–25: Demo: `ansible-galaxy init webserver`, vaata struktuuri
  - 25–45: Lab: loo esimene role (nginx)
- **Refleksioon:** "Miks on role parem kui monoliter playbook?"

---

## Blokk 2 (45 min) – Tasks, handlers, templates

- **Eesmärk:** Kasutada role komponente (tasks, handlers, templates)
- **Minutiplaan:**
  - 0–10: Handlers demo (nginx restart on change)
  - 10–35: Lab: lisa tasks, handler, Jinja2 template
  - 35–45: Paariskontroll
- **Kontrollküsimused:** "Millal handler triggerdab?"

---

## Blokk 3 (45 min) – Variables ja defaults

- **Eesmärk:** Parameetriseerida rolle variables'idega
- **Minutiplaan:**
  - 0–15: `defaults/main.yml` vs `vars/main.yml` demo
  - 15–40: Lab: lisa defaults, kasuta role'i erinevate parameetritega
  - 40–45: Refleksioon

---

## Blokk 4 (45 min) – Ansible Galaxy ja korduvkasutus

- **Eesmärk:** Jagada ja kasutada rolle Galaxy'st
- **Minutiplaan:**
  - 0–20: Galaxy demo, requirements.yml, role install
  - 20–40: Lab: import role Galaxy'st, kasuta projects
  - 40–45: Quiz + kodutöö

---

## Kodutöö (1.5h)

- **Ülesanne:** Loo 3-tier stack role'idega (webserver, appserver, database)
- **Kriteeriumid:**
  - [ ] 3 eraldi role'i
  - [ ] Playbook kasutab kõiki role
  - [ ] README refleksiooniga

---

## 📖 Viited

- **Ansible Roles Docs**: https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html
- **Ansible Galaxy**: https://galaxy.ansible.com/
- **Pedagoogika**: NRC (2000) *How People Learn*

---

## 🎓 Kokkuvõte

**Teha:**
- ✅ Näita monoliter playbook probleem
- ✅ `ansible-galaxy init` struktuur
- ✅ DRY principle
- ✅ Galaxy search demo

**Mitte teha:**
- ❌ Keerulised dependencies kohe
- ❌ 20 role'i korraga
- ❌ Galaxy publish (liiga advanced)

