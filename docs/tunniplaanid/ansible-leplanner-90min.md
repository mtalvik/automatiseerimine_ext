# Tunnikava: Ansible Automatiseerimine

**Õppeaine:** Informaatika  
**Klass:** 12  
**Tunni teema:** Ansible automatiseerimine - 10 serveri stsenaarium  
**Õpiväljundid:** ÕV3, ÕV4 - Ansible PlayBook ja automatiseerimine  
**Aeg:** 90 minutit  
**Õpetaja:** [Nimi]

---

## Tunni eesmärgid

**Õpilane:**
- Selgitab miks automatiseerimine on vajalik (manuaalne vs automaatne)
- Loob Ansible playbook'i serveri seadistamiseks
- Kasutab muutujaid, loops'e ja error handling'ut
- Teeb peer review teise rühma playbook'ile

---

## Õpilaste eelteadmised

- YAML süntaksi alused
- Linux käsurea põhitõed
- Serveri seadistamise mõiste (install, config, service)

---

## Õppevahendid ja materjalid

- Ansible (installeeritud)
- Testserverid või Docker konteinerid
- Labor juhendid: https://mtalvik.github.io/automatiseerimine_ext/ansible_basics/labor/
- Ansible dokumentatsioon: https://docs.ansible.com
- Miro või Google Docs (planeerimine)

---

## Tunnikäik

| Tunni osa | Aeg | Õpetaja tegevus | Õpilaste tegevus | Hindamine | Põhjendused |
|-----------|-----|-----------------|------------------|-----------|-------------|
| **Probleemi tutvustus** | 10 min | Esitab stsenaariumi: 10 serverit, manuaalne vs automatiseeritud workflow, näitab ajakulu võrdlust | Kuulavad, arutavad kuidas nad lahendaksid käsitsi | - | Probleemipõhine õpe, motivatsioon |
| **Ansible alused** | 10 min | Kordab YAML syntax'it, inventory, playbook, module kontseptsioone, näitab quick reference'i | Individuaalselt loevad Ansible refresher'it, kordavad mõisteid | - | Eelteadmiste aktiveerimine |
| **Rühmad + planeerimine** | 10 min | Moodustab rühmad 3-4 õpilast, selgitab rolle (koodija, testija, dokumenteerija) | Rühmades planeerivad lahendust Miro/Google Docs'is, jagavad rollid | - | Koostöö, planeerimine enne koodimist |
| **Playbook Osa 1** | 20 min | Jälgib rühmi, aitab YAML süntaksi ja module'itega, näitab common mistakes | Rühmades kirjutavad playbook'i (install nginx, postgresql, docker), kasutavad dokumentatsiooni | Formatiivne: kas playbook käivitub | Praktika, dokumentatsiooni kasutamine |
| **Paus** | 15 min | - | Puhkavad | - | - |
| **Playbook Osa 2 + test** | 15 min | Aitab troubleshooting'uga, selgitab idempotentsust | Rühmades täiustavad playbook'i, lisavad error handling, testavad, debugivad | Formatiivne: testid õnnestuvad | Kvaliteedi tõstmine, testimine |
| **Peer review** | 15 min | Jaotab paarid (rühm A vaatab rühma B tööd), selgitab rubriiki | Paarides teevad peer review, kasutavad rubriiki, annavad tagasisidet | Formatiivne: review kvaliteet | Õppimine teistelt, kriitilise mõtlemise areng |
| **Refleksioon** | 5 min | Avab Padlet'i, küsib: Mis oli raske? Mis õnnestus? Kodutöö tutvustus | Kirjutavad Padlet'isse exit ticket vastused | Formatiivne: refleksioon | Tagasiside, metakognitsioon |

---

## Hindamisvahend: Ansible Playbook Rubriik

| Kriteerium | 1p | 2p | 3p | 4p |
|------------|----|----|----|----|
| Süntaks | Ei tööta | Töötab, vigu | Töötab | + best practices |
| Idempotentsus | Puudub | Osaline | Täielik | + testitud |
| Muutujad | Ei kasuta | Kasutab halvasti | Kasutab hästi | + dokumenteeritud |
| Error handling | Puudub | Minimaalne | Hea | Põhjalik |
| Dokumentatsioon | Puudub | Minimaalne | Hea README | + näited |

**Max:** 32p | **Skaal:** 29-32→5, 23-28→4, 17-22→3, 11-16→2

---

## Diferentseerimine

**Tugõppijatele:**
- Playbook template struktuuriga
- Valmis näidisfailid
- Tugevama õpilasega paariks

**Andekamale:**
- Roles'ide kasutamine
- Ansible Vault
- Dynamic inventory

---

## Kodutöö

**Tähtaeg:** Järgmine tund

**Ülesanded:**
- Playbook'i täiustamine
- Dokumentatsiooni kirjutamine
- Refleksioon

**Materjal:** https://mtalvik.github.io/automatiseerimine_ext/ansible_basics/kodutoo/

---

## Märkused

**Õpetajale:**
- Testserverid valmis
- Inventory template valmis
- YAML syntax vigade abi valmis (yamllint.com)
- Julgusta õpilasi: "Vead on normaalsed!"