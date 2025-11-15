# Ansible Automatiseerimine

**LePlanner:** https://leplanner.ee/en/scenario/5443  
**Klass:** 12 | **Kestus:** 90 min | **Õpiväljundid:** ÕV3, ÕV4

---

## Tunni kulg

| Tegevus | min | Vorm | Materjal |
|---------|-----|------|----------|
| Probleemi tutvustus | 10 | Klass | Stsenaarium: 10 serverit, manuaalne vs automatiseeritud |
| Ansible alused | 10 | Individuaalne | YAML syntax refresher, Ansible quick reference |
| Rühmad + planeerimine | 10 | Rühmad (3-4) | Miro/Google Docs template, rollid |
| Playbook Osa 1 | 20 | Rühmad | Nõuded, Ansible docs, inventory näidis |
| Paus | 15 | - | - |
| Playbook Osa 2 + test | 15 | Rühmad | Testing checklist, troubleshooting guide |
| Peer review | 15 | Paarid | Review template, rubriik |
| Refleksioon | 5 | Klass | Padlet exit ticket |

---

## Hindamine: Ansible Playbook Rubriik

| Kriteerium | 1p | 2p | 3p | 4p |
|------------|----|----|----|----|
| Süntaks | Ei tööta | Töötab, vigu | Töötab | + best practices |
| Idempotentsus | Puudub | Osaline | Täielik | + testitud |
| Muutujad | Ei kasuta | Kasutab halvasti | Kasutab hästi | + dokumenteeritud |
| Error handling | Puudub | Minimaalne | Hea | Põhjalik |
| Dokumentatsioon | Puudub | Minimaalne | Hea README | + näited |
| Struktuur | Kaootiline | Põhiline | Hästi loetav | Modulaarne (roles) |
| Testimine | Ei testitud | 1 kord | Mitu korda | Automatiseeritud |
| Best practices | Ei järgi | Mõningaid | Enamikku | Kõiki + security |

**Max:** 32p | **Skaal:** 29-32→5, 23-28→4, 17-22→3, 11-16→2

**Kontrollnimekiri:**
- [ ] Playbook käivitub ilma vigadeta
- [ ] Kõik tarkvarad installitakse
- [ ] Teenused käivituvad automaatselt
- [ ] README.md olemas
- [ ] Git'is, informatiivsed commit'id
- [ ] Peer review tehtud

---

## Materjalid

- Labor: https://mtalvik.github.io/automatiseerimine_ext/ansible_basics/labor/
- Kodutöö: https://mtalvik.github.io/automatiseerimine_ext/ansible_basics/kodutoo/
- Ansible dokumentatsioon: https://docs.ansible.com
- Inventory template, playbook skeleton

---

## Õpetajale

**Enne:**
- Testserverid/konteinerid töötavad
- Inventory template valmis
- Ansible installitud kõikidel

**Tunnis:**
- Playbook võtab rohkem aega - jälgi
- YAML syntax abi vajadusel
- Julgusta dokumentatsiooni kasutama
- "Vead on normaalsed!"

**Probleemid:**
- YAML indent → yamllint.com
- Permissions → sudo setup
- SSH keys → ssh-copy-id
- Syntax check → ansible-playbook --syntax-check
