# Tunnikava: Ansible Advanced – Vault, Jinja2, ja Optimiseerim ine (4×45 min) + 1.5h kodutöö

**Tase:** Edasijõudnud (eelteadmised: Ansible Basics, Roles, YAML)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`

---

## 🎯 Õpiväljundid
- ÕV1: Kasutab Ansible Vault'i salajaste andmete krüpteerimiseks
- ÕV2: Kirjutab keerulisi Jinja2 template'eid filters ja loops'iga
- ÕV3: Optimeerib playbook'ide jõudlust (parallelism, facts caching)
- ÕV4: Kasutab callback plugins ja custom modules
- ÕV5: Debugib keerulisi playbook probleeme

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased teavad basic Ansible – vault on turvalisus
2. **Arusaamine:** Õpeta MIKS passwords ei tohi plain-text olla
3. **Metakognitsioon:** Performance troubleshooting

---

## 👨‍🏫 Näpunäited

### Enne tundi:
- [ ] Ansible Basics + Roles lõpetatud
- [ ] Näidis vault file valmis
- [ ] Performance probleem prep'itud

### Tunni ajal:
- **Vault password unustamine = katastroof:** Rõhuta!
- **Jinja2 on võimas:** Aga ka keeruline
- **Facts gathering võtab aega:** `gather_facts: no` kui pole vaja
- **Parallelism:** `forks` setting

---

## Blokk 1 (45 min) – Ansible Vault

- **Eesmärk:** Krüpteerida salajased andmed
- **Minutiplaan:**
  - 0–5: "Kus sa hoiad password'e? Git'is?!"
  - 5–15: Vault demo, encrypt/decrypt
  - 15–45: Lab: encrypt passwords, use in playbook
- **Refleksioon:** "Miks vault on parem kui plain-text?"

---

## Blokk 2 (45 min) – Advanced Jinja2

- **Eesmärk:** Kirjutada keerulisi template'eid
- **Minutiplaan:**
  - 0–15: Filters, loops, conditionals demo
  - 15–45: Lab: loo nginx config template filters'iga

---

## Blokk 3 (45 min) – Performance optimiseerim ine

- **Eesmärk:** Kiirendada playbook'e
- **Minutiplaan:**
  - 0–15: Forks, pipelining, facts caching demo
  - 15–45: Lab: benchmark + optimize playbook

---

## Blokk 4 (45 min) – Debugging ja troubleshooting

- **Minutiplaan:**
  - 0–20: Debug module, verbosity, strategy demo
  - 20–45: Lab: debug failing playbook + Quiz

---

## Kodutöö (1.5h)

- **Ülesanne:** Loo production-ready playbook vault + templates'iga
- **Kriteeriumid:**
  - [ ] Vault encrypted secrets
  - [ ] Complex Jinja2 templates
  - [ ] Optimized performance
  - [ ] README refleksiooniga

---

## 🎓 Kokkuvõte

**Teha:**
- ✅ Vault on MUST production'is
- ✅ Jinja2 filters on võimsad
- ✅ Performance matters

**Mitte teha:**
- ❌ Plain-text passwords!
- ❌ 1000 node'i ilma forks tuning'uta

