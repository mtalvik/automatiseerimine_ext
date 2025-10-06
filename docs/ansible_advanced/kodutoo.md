# Ansible Kodutöö: Veebirakendus Vault'iga

**Tähtaeg:** Järgmise nädala alguseks  

---

## **OLULINE: Kui kasutad päris pilve servereid!**

**NB!** Seda kodutööd saab teha ka kohalike VM'idega (VirtualBox/Vagrant) - see on TASUTA!

**Aga kui kasutad pilve (AWS EC2, Azure VM, DigitalOcean):**

###  Enne alustamist:

1. **Seadista billing alerts** (vaata Terraform homework hoiatust)
2. **Kasuta väiksemaid instance'eid:**
   - AWS: `t2.micro` või `t3.micro` (Free Tier)
   - Azure: `B1s` (väike ja odav)
   - DigitalOcean: `$6/month droplet`

3. ** KUSTUTA serverid pärast testimist!**
   ```bash
# AWS
   aws ec2 terminate-instances --instance-ids i-xxxxx
   
# Azure
   az vm delete --name myvm --resource-group mygroup --yes
   
# Või Terraform destroy
   terraform destroy
   ```

### SOOVITATAV: Kasuta kohalikke VM'e

**Tasuta ja turvaline variant:**
```bash
# Vagrant setup (kohalikud VM'id)
vagrant up
ansible-playbook -i inventory site.yml
vagrant destroy  # pärast testimist
```

---

## Ülesanne

Juurutage veebirakendus (teie valik) kasutades:
- Ansible Vault paroolide jaoks
- Template'e konfiguratsioonifailidele  
- Handler'eid teenuste haldamiseks
- Kahte keskkonda (dev/prod)

---

##  Nõuded

### 1. Vault (25 punkti)
- [ ] Vähemalt 5 krüpteeritud muutujat
- [ ] Paroolid peavad olema vault'is
- [ ] Vault muutujate kasutamine template'ides

### 2. Template'id (25 punkti)
- [ ] Vähemalt 2 Jinja2 template'i
- [ ] Kasutage `{% if %}` tingimusi
- [ ] Erinevad konfiguratsioonid dev/prod jaoks

### 3. Handler'id (20 punkti)
- [ ] Vähemalt 2 handler'it
- [ ] Teenuste restart/reload
- [ ] Käivituvad ainult muudatuste korral

### 4. Struktuur (15 punkti)
```
teie-projekt/
├── inventory/hosts.yml
├── group_vars/
│   └── all/vault.yml
├── templates/
├── playbooks/
└── README.md
```

### 5. Dokumentatsioon (15 punkti)
- [ ] README.md
- [ ] Screenshot'id (vault krüpteeritud, rakendus töötab)
- [ ] Käivitamise juhised

---

## Vihjed

### Vault'i loomine
```bash
# Looge krüpteeritud fail
ansible-vault create group_vars/all/vault.yml

# Vaadake sisu
ansible-vault view group_vars/all/vault.yml

# Käivitage playbook
ansible-playbook site.yml --ask-vault-pass
```

### Template'i näpunäide
```jinja2
# Keskkonna järgi erinevad väärtused
{% if env_type == 'production' %}
# Tootmise seadistused
{% else %}
# Arenduse seadistused
{% endif %}

# Muutuja vault'ist
password = {{ vault_db_password }}
```

### Handler'i näpunäide
```yaml
tasks:
  - name: Deploy config
    template:
      src: config.j2
      dest: /etc/app/config
    notify: restart service

handlers:
  - name: restart service
    service:
      name: myapp
      state: restarted
```

---

## Kasulikud lingid

**Ansible dokumentatsioon:**
- [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [Jinja2 Templates](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)
- [Handlers](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)

**Template'ide näited:**
- [Jinja2 if statements](https://jinja.palletsprojects.com/en/3.0.x/templates/#if)
- [Variables in templates](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)

**Vault praktikad:**
- [Best practices](https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data)

---

## Kontrollnimekiri

Enne esitamist kontrollige:

```bash
# 1. Vault on krüpteeritud?
file group_vars/all/vault.yml

# 2. Syntax OK?
ansible-playbook site.yml --syntax-check

# 3. Dry run töötab?
ansible-playbook site.yml --check

# 4. Screenshot'id tehtud?
ls screenshots/
```

---

##  Sagedased vead

1. **Vault parool Git'is** - ÄRGE committige `.vault_pass` faili
2. **Hardcoded paroolid** - Kõik paroolid vault'i
3. **Handler'id puuduvad** - Teenused peavad restartima ainult vajadusel
4. **Üks keskkond** - Peab olema dev JA prod

---

##  Nõutavad tõendid

1. Krüpteeritud vault: `cat group_vars/all/vault.yml | head`
2. Playbook töötab: terminal output
3. Rakendus töötab: browser screenshot
4. Handler käivitub: `RUNNING HANDLER` output'is

---

## Ideed projektiks

**Lihtne:** Static website (Apache + HTML templates)  
**Keskmine:** Blog platform (Apache + MySQL + PHP)  
**Keeruline:** API server (Nginx + PostgreSQL + Node.js)

Valige vastavalt oma oskustele!

---

**Esitamine:** GitHub link + screenshot'id

---

##  Refleksioon (kirjuta README.md lõppu)

Lisa oma README.md faili lõppu peatükk **"## Refleksioon"** ja vasta järgmistele küsimustele:

### Küsimused (vasta 2-3 lausega igaühele):

1. **Mis oli selle kodutöö juures kõige raskem ja kuidas sa selle lahendasid?**
   - Näide: "Kõige raskem oli Jinja2 templates - eriti loops ja conditions. Lugesin dokumentatsiooni ja tegin palju teste."

2. **Milline Ansible advanced kontseptsioon oli sulle kõige suurem "ahaa!"-elamus ja miks?**
   - Näide: "Ansible Vault! Nüüd saan aru, kuidas hoida paroole turvaliselt Git'is."

3. **Kuidas saaksid Ansible'i advanced funktsioone kasutada oma teistes projektides?**
   - Näide: "Võiksin luua template'eid oma standardsetele server config'idele ja kasutada vault'i secrets jaoks."

4. **Kui peaksid selgitama sõbrale, mis on Infrastructure as Code ja miks see on kasulik, siis mida ütleksid?**
   - Näide: "IaC on nagu retsept - kirjutad üles, mida tahad, ja Ansible teeb selle automaatselt kõikides serverites!"

5. **Mis oli selle kursusel kõige väärtuslikum õppetund?**
   - Näide: "Sain aru, et automatiseerimine on võti - kunagi enam ei sea ma servereid käsitsi!"

---

## Kontrollnimekiri (enne esitamist)

**Kontrolli need asjad:**

- [ ] GitHubis on avalik repositoorium
- [ ] Ansible project structure on korrektne
- [ ] Templates töötavad (dünaamilised configs)
- [ ] Vault on kasutatud (paroolid krüpteeritud)
- [ ] Playbook töötab ilma vigadeta
- [ ] Rakendus on funktsionaalne (testitud)
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus (mis see on?)
  - [ ] Arhitektuur (millised komponendid)
  - [ ] Kuidas seadistada (inventory, vault)
  - [ ] Kuidas käivitada (`ansible-playbook` käsud)
  - [ ] Screenshots (deployed app, configs)
  - [ ] Refleksioon (5 küsimuse vastused)
- [ ] Kõik muudatused on GitHubi push'itud

---

##  Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Funktsionaalsus** | 30% | Rakendus töötab, kõik komponendid korrektsed |
| **Templates** | 20% | Jinja2 templates dünaamilised ja korrektsed |
| **Vault** | 15% | Paroolid krüpteeritud, vault õigesti kasutatud |
| **Project structure** | 15% | Organiseeritud struktuur, group_vars/host_vars |
| **README** | 10% | Projekti kirjeldus, käivitamisjuhend, selge |
| **Refleksioon** | 10% | 5 küsimust vastatud, sisukas, näitab mõistmist |

**Kokku: 100%**

---

## Abimaterjalid ja lugemine

**Kiirviited:**
- [Ansible Jinja2 Templates](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)
- [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

**Kui abi vaja:**
1. Vaata `lisapraktika.md` faili täiendavate näidete jaoks
2. Kasuta `ansible-playbook --syntax-check` syntax kontrollikls
3. Kasuta `ansible-playbook --check` kuivaks käiguks
4. Küsi klassikaaslaselt või õpetajalt

---

## Boonus (valikuline, +10%)

**Kui tahad ekstra punkte, tee üks või mitu neist:**

1. **Dynamic inventory:** Kasuta dynamic inventory (AWS EC2, Azure)
2. **Ansible Tower/AWX:** Deploy projecti Tower/AWX kaudu
3. **Molecule testing:** Lisa Molecule test suite
4. **Multiple environments:** Dev, Staging, Production (erinevad vault failid)
5. **CI/CD integration:** Lisa GitLab CI/GitHub Actions Ansible jaoks

---

**Edu! **
