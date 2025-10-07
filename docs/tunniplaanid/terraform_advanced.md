# Tunnikava: Terraform Advanced – Modules ja Remote State (4×45 min) + 1.5h kodutöö

**Tase:** Edasijõudnud (eelteadmised: Terraform Basics, HCL, state)  
**Materjalid:** `loeng.md`, `labor.md`, `kodutoo.md`, `lisapraktika.md`

---

## 🎯 Õpiväljundid
- ÕV1: Loob ja kasutab Terraform mooduleid korduvkasutuseks
- ÕV2: Seadistab remote state (S3/Terraform Cloud)
- ÕV3: Kasutab workspaces mitme environment'i jaoks
- ÕV4: Rakendab module versioning'ut ja dependencies
- ÕV5: Optimeerib state management'i ja locking'ut

---

## 📚 Pedagoogiline raamistik

1. **Eelteadmised:** Õpilased teavad basic Terraform – modules on DRY
2. **Arusaamine:** Õpeta MIKS modulariseerimine ja remote state
3. **Metakognitsioon:** State management best practices

---

## 👨‍🏫 Näpunäited

### Enne tundi:
- [ ] Terraform Basics lõpetatud
- [ ] Terraform Cloud konto (tasuta tier)
- [ ] Näidis module valmis

### Tunni ajal:
- **Modules != resources:** Oluline erinevus!
- **Remote state setup võtab aega:** 10-15 min
- **Workspaces on alternate environments:** dev, staging, prod
- **State locking:** S3 + DynamoDB või Terraform Cloud

---

## 1. Modules põhitõed

- **Eesmärk:** Luua esimene module
- **Minutiplaan:**
  - 0–5: "Kas kopeerid sama Terraform koodi mitu korda?"
  - 5–15: Modules struktuur, input/output variables
  - 15–45: Lab: loo web server module
- **Refleksioon:** "Miks modules paremad kui copy-paste?"

---

## 2. Remote state ja locking

- **Eesmärk:** Seadistada remote state S3 või Terraform Cloud'is
- **Minutiplaan:**
  - 0–15: Remote state demo, locking selgitus
  - 15–45: Lab: migrera local → remote state

---

## 3. Workspaces ja environments

- **Eesmärk:** Kasutada workspaces dev/staging/prod jaoks
- **Minutiplaan:**
  - 0–15: Workspaces demo
  - 15–45: Lab: loo 3 workspaces, deploy iga environment'i

---

## 4. Best practices ja troubleshooting

- **Minutiplaan:**
  - 0–20: Module registry, versioning, dependencies
  - 20–45: Lab + Quiz

---

## Kodutöö (1.5h)

- **Ülesanne:** Loo module library (web, db, network modules)
- **Kriteeriumid:**
  - [ ] 3 reusable modules
  - [ ] Remote state
  - [ ] README refleksiooniga

---

## 🎓 Kokkuvõte

**Teha:**
- ✅ DRY principle
- ✅ Remote state on production must!
- ✅ Workspaces demo

**Mitte teha:**
- ❌ 20 modules korraga
- ❌ Production state'i kustutamine (!)

