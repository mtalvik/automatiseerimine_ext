# 📝 Ansible Kodutöö: Veebirakendus Vault'iga

**Tähtaeg:** Järgmise nädala alguseks  
**Aeg:** 1.5-2 tundi

---

## 🎯 Ülesanne

Juurutage veebirakendus (teie valik) kasutades:
- Ansible Vault paroolide jaoks
- Template'e konfiguratsioonifailidele  
- Handler'eid teenuste haldamiseks
- Kahte keskkonda (dev/prod)

---

## 📋 Nõuded

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

## 💡 Vihjed

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

## 📚 Kasulikud lingid

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

## ✅ Kontrollnimekiri

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

## 🚫 Sagedased vead

1. **Vault parool Git'is** - ÄRGE committige `.vault_pass` faili
2. **Hardcoded paroolid** - Kõik paroolid vault'i
3. **Handler'id puuduvad** - Teenused peavad restartima ainult vajadusel
4. **Üks keskkond** - Peab olema dev JA prod

---

## 📸 Nõutavad tõendid

1. Krüpteeritud vault: `cat group_vars/all/vault.yml | head`
2. Playbook töötab: terminal output
3. Rakendus töötab: browser screenshot
4. Handler käivitub: `RUNNING HANDLER` output'is

---

## 🎯 Ideed projektiks

**Lihtne:** Static website (Apache + HTML templates)  
**Keskmine:** Blog platform (Apache + MySQL + PHP)  
**Keeruline:** API server (Nginx + PostgreSQL + Node.js)

Valige vastavalt oma oskustele!

---

**Esitamine:** GitHub link + screenshot'id

**Hindamine:**
- Töötab = 60%
- Õige struktuur = 20%  
- Dokumentatsioon = 20%

Edu! 🚀
