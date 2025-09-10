# Ansible Reading Material - Kompaktne Versioon

**Aeg:** 90min lugemist | **Tähtaeg:** Enne järgmist tundi

---

## Kohustuslik lugemine (60min)

### 1. Ansible Arhitektuur (20min)
**Põhiteemad:**
- Agentless vs agent-based süsteemid
- Control node ja managed nodes
- SSH kommunikatsioon
- Playbook'i käivitamise tsükkel

**Küsimused endile:**
- Miks agentless on parem/halvem?
- Kuidas toimub autentimine?
- Mis juhtub playbook käivitamisel?

### 2. YAML Süntaks (20min)
**Põhiteemad:**
- Taandrimine ja struktuur
- Andmetüübid (string, list, dict)
- Ansible YAML konventsioonid
- Levinud vead

**Praktilised oskused:**
- YAML valideerimise tööriistad
- Debug tehnikad

### 3. Ansible Moodulid (20min)
**Põhiteemad:**
- Core vs community moodulid
- Idempotency kontseptsioon
- Mooduli dokumentatsiooni lugemine
- Parameetrid ja tagastusväärtused

---

## Valikuline lugemine (30min)

### 4. Best Practices (15min)
- Playbook'i struktuur
- Muutujate nimetamine
- Error handling
- Turvalisus

### 5. Alternatiivid (15min)
- Ansible vs Puppet/Chef/Salt
- Millal millist tööriista kasutada

---

## Kiirviide

**Põhikäsud:**
```bash
ansible --version
ansible all -m ping
ansible-inventory --list
ansible-playbook playbook.yml --check
```

**YAML näide:**
```yaml
---
- name: Näide
  hosts: all
  vars:
    app: myapp
  tasks:
    - name: Install
      package:
        name: nginx
        state: present
```

---

## Reflektsioon (200-300 sõna)

Kirjuta `ansible_basics_reading_reflection.md` faili:

1. **Peamine insight** - mis oli kõige huvitavam?
2. **Küsimused** - mis jäi ebaselgeks?
3. **Praktika** - kuidas agentless arhitektuur aitab?
4. **Edasi** - mida tahaksid rohkem õppida?

---

## Järgmiseks tunniks

Valmista ette:
- Küsimused lugemisest
- Praktikas proovimise ideed
- YAML süntaksi mõistmine
- Automation projektide mõtted

**Kasulikud lingid:**
- [Ansible Docs](https://docs.ansible.com/)
- [Module Index](https://docs.ansible.com/ansible/latest/modules/)
- [Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible Galaxy](https://galaxy.ansible.com/)
