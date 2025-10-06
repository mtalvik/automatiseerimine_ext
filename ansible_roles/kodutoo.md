#  Ansible vs Puppet Kodutöö: Võrdlev Analüüs

**Tähtaeg:** Järgmise nädala alguseks  


---

##  Ülesande kirjeldus

Ehitage sama infrastruktuur nii Ansible kui ka Puppet'iga, et mõista erinevusi ja sarnasusi automatiseerimise tööriistades.

---

##  Ülevaade

**Ehitate:**
- Nginx + SSL + virtual hosts
- PostgreSQL + algne skeem  
- Monitoring + logid

**Õpite:**
- Push-based (Ansible) vs pull-based (Puppet) erinevused
- Agentless vs agent-based arhitektuurid
- Deployment strateegiate praktilised aspektid

---

## Setup (15min)

```bash
# Klooni starter repo
git clone [teacher-repo]/ansible-puppet-comparison.git
cd ansible-puppet-comparison
git checkout -b homework-[nimi]

# Repository struktuur
ls -la
# ansible/ - poolik Ansible kood (puudub SSL ja virtual hosts)
# puppet/ - poolik Puppet kood (puudub SSL ja monitoring)
# vagrant/ - test VM-id (isoleeritud keskkonnad)
```

**Starter kood:** Repository sisaldab põhifunktsionaalsust, kuid SSL, virtual hosts ja monitoring vajate ise lisada. See võimaldab keskenduda praktilisele võrdlusele.

---

## Ansible osa (60min)

### VM käivitamine
```bash
cd vagrant/
vagrant up ansible-vm
vagrant ssh ansible-vm
```

**Vagrant kasutamine:** Isoleeritud testikeskkond, mis ei mõjuta teie põhisüsteemi. Saate eksperimenteerida turvaliselt.

### Lisa puuduvad osad
```bash
cd ../ansible/
cat requirements.md  # täpne nimekiri, mis lisada
```

**SSL lisamine:**
```yaml
# roles/nginx/tasks/ssl.yml
- name: Create SSL directory
  file:
    path: /etc/nginx/ssl
    state: directory
    mode: '0755'

- name: Generate self-signed SSL certificate  
  command: openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/C=EE/CN=localhost"
  args:
    creates: /etc/nginx/ssl/nginx.crt
```

**Ise-allkirjastatud sertifikaadid:** Testimiseks piisav, produktsioonis kasutaksite CA-st saadud sertifikaate.

**Virtual hosts konfiguratsioon:**
```yaml
- name: Create virtual host directories
  file:
    path: /var/www/{{ item }}
    state: directory
    owner: www-data
    mode: '0755'
  loop: [site1, site2]

- name: Create site content
  copy:
    content: "<h1>{{ item }}</h1><p>Virtual host content</p>"
    dest: /var/www/{{ item }}/index.html
  loop: [site1, site2]
```

**Virtual hosts:** Võimaldab ühel serveril mitut erinevat veebisaiti. Ressursi säästlik ja praktikas levinud lahendus.

### Test ja commit
```bash
ansible-playbook site.yml --ask-become-pass
curl -k https://localhost  # SSL testimine
curl -k https://localhost/site1  # Virtual host testimine
git add . && git commit -m "Ansible SSL + vhosts töötab"
```

**Testimine:** Kontrollige nii SSL funktsionaalsust kui ka virtual hosts'e. `-k` flag ignoreerib ise-allkirjastatud sertifikaadi hoiatusi.

---

## Puppet osa (60min)

### VM vahetamine
```bash
vagrant destroy ansible-vm
vagrant up puppet-vm  
vagrant ssh puppet-vm
```

**Eraldi VM:** Puhas keskkond Puppet'i jaoks. Võimaldab objektiivselt võrrelda mõlemat lähenemist.

### Lisa samad funktsioonid Puppet'iga
```bash
cd ../puppet/
cat requirements.md  # sama funktsionaalsus, erinev süntaks
```

**SSL Puppet'is:**
```puppet
# modules/nginx/manifests/ssl.pp
class nginx::ssl {
  file { '/etc/nginx/ssl':
    ensure => 'directory',
    mode   => '0755',
  }
  
  exec { 'generate-ssl-cert':
    command => 'openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/C=EE/CN=localhost"',
    creates => '/etc/nginx/ssl/nginx.crt',
    path    => '/usr/bin',
    require => File['/etc/nginx/ssl'],
  }
}
```

**Puppet süntaks:** Ruby-põhine, deklaratiivne. `require` määrab sõltuvuste järjekorra.

**Monitoring lisamine:**
```puppet
# modules/monitoring/manifests/health.pp  
class monitoring::health {
  file { '/usr/local/bin/health-check.sh':
    content => template('monitoring/health-check.sh.erb'),
    mode    => '0755',
  }
  
  cron { 'nginx-health-check':
    command => '/usr/local/bin/health-check.sh >> /var/log/health.log',
    minute  => '*/5',
  }
}
```

**Monitoring:** Automaatne teenuste tervise kontroll. Cron käivitab skripti iga 5 minuti tagant.

### Test ja commit
```bash
sudo puppet apply --modulepath=modules manifests/site.pp
curl -k https://localhost  # sama tulemus kui Ansible'iga
sudo /usr/local/bin/health-check.sh  # monitoring test
git add . && git commit -m "Puppet sama tulemus"
```

**Puppet agent:** Pull-based arhitektuur. Agent küsib konfiguratsiooni serverilt ja rakendab muudatused.

---

## Võrdlus (30min)

### Praktilised erinevused

**Ansible (Push-based):**
- YAML süntaks - inimesele loetav
- SSH ühendus vajalik - agentless
- Kiire seadistamine väikestele projektidele
- Suurepärane ad-hoc taskide jaoks

**Puppet (Pull-based):**  
- Ruby süntaks - rohkem programmeerimislik
- Agent töötab serveris - autonoomne
- Keerukamate infrastruktuuride jaoks
- Tugev state management

### Deployment mudelid

**Ansible execution flow:**
```
Control node → SSH → Target servers → Execute tasks → Report back
```

**Puppet execution flow:**
```
Puppet master ← Agent checks in ← Target servers ← Apply catalog ← Report status
```

### README.md näide
```markdown
# Ansible vs Puppet Praktika

## Ehitatud funktsionaalsus
- SSL sertifikaadid ja HTTPS konfiguratsioon
- Virtual hosts mitme saidi jaoks
- Automaatne monitoring ja health checks
- Mõlemaga identne lõpptulemus

## Praktilised tähelepanekud

### Ansible kogemus
- Süntaks oli intuitiivne ja kiiresti omandatav
- Debug oli lihtne verbose flag'idega
- SSH seadistamine võttis aega alguses

### Puppet kogemus  
- Ruby süntaks nõudis rohkem harjutamist
- Resource dependencies olid võimsad
- Agent-based lähenemine tundus robuutsem

## Eelistus
[Vali ja põhjenda 2-3 lausega konkreetse kasutusstsenaariumi põhjal]

## Omandatud oskused
- SSL konfiguratsioon mõlemas tööriistas
- Virtual hosting seadistamine
- Monitoring implementeerimine
- Debug ja troubleshooting tehnikad
```

---

## Esitamine (15min)

```bash
git add .
git commit -m "Mõlemad deployment'id lõpetatud ja testitud"
git push origin homework-[nimi]
```

**Repository kontrollimine:**
- Mõlemad deployment'id annavad identse tulemuse
- README.md sisaldab praktilist võrdlust
- Commit ajalugu näitab progressi

---

## Debug näpunäited

**Ansible troubleshooting:**
```bash
ansible-playbook site.yml --check  # kuiv käik
ansible-playbook site.yml -v       # verbose väljund
ansible-lint .                     # koodi kvaliteet
```

**Puppet troubleshooting:**
```bash
sudo puppet apply manifests/site.pp --noop  # kuiv käik
sudo puppet apply manifests/site.pp --debug # debug info
puppet-lint modules/                         # koodi kvaliteet
```

**SSL testimine:**
```bash
openssl x509 -in /etc/nginx/ssl/nginx.crt -text -noout  # sertifikaadi info
curl -vk https://localhost  # detailne SSL handshake
```

**Teenuste kontroll:**
```bash
systemctl status nginx postgresql  # teenuste olek
journalctl -u nginx -f            # nginx logid reaalajas
netstat -tlnp | grep :443         # SSL port kontroll
```

---

##  Refleksioon (kirjuta README.md lõppu)

Lisa oma README.md faili lõppu peatükk **"## Refleksioon ja Võrdlus"** ja vasta järgmistele küsimustele:

### Küsimused (vasta 2-3 lausega igaühele):

1. **Milline tööriist oli sulle mugavam (Ansible või Puppet) ja miks?**
   - Näide: "Mulle meeldis Ansible rohkem, sest YAML on lihtsam lugeda kui Puppet DSL. Aga Puppet'i agent-based arhitektuur oli huvitav!"

2. **Mis oli kõige suurem erinevus Ansible ja Puppet vahel?**
   - Näide: "Push-based vs pull-based! Ansible'is ma käsitsi trigger'in, Puppet'is agent küsib ise uuendusi."

3. **Millises olukorras kasutaksid Ansible'i ja millises Puppet'it?**
   - Näide: "Ansible väikestele projektidele ja kiireks deployment'iks. Puppet suurele infrastruktuurile, kus on vaja pidevat automatiseerimist."

4. **Mis oli selle projekti juures kõige raskem ja kuidas sa selle lahendasid?**
   - Näide: "SSL sertifikaatide seadistamine oli raske. Otsisin dokumentatsioonist ja kasutasin `openssl` käsku testimiseks."

5. **Mis oli selle projekti juures kõige huvitavam või lõbusam osa?**
   - Näide: "Mulle meeldis näha, kuidas sama infrastruktuur töötab kahel erineval viisil! Nagu võrrelda kahte erinevat keelt."

---

##  Kontrollnimekiri (enne esitamist)

**Kontrolli need asjad:**

- [ ] GitHubis on avalik repositoorium
- [ ] Ansible osa töötab (Nginx + SSL + virtual hosts + PostgreSQL + monitoring)
- [ ] Puppet osa töötab (Nginx + SSL + virtual hosts + PostgreSQL + monitoring)
- [ ] Comparison.md sisaldab põhjalikku võrdlust
- [ ] README.md sisaldab:
  - [ ] Projekti kirjeldus
  - [ ] Kuidas seadistada (Ansible ja Puppet eraldi)
  - [ ] Kuidas käivitada
  - [ ] Refleksioon (5 küsimuse vastused)
- [ ] Kõik muudatused on GitHubi push'itud

---

##  Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Ansible osa** | 30% | Nginx + SSL + virtual hosts + PostgreSQL + monitoring töötavad |
| **Puppet osa** | 30% | Nginx + SSL + virtual hosts + PostgreSQL + monitoring töötavad |
| **Comparison.md** | 15% | Põhjalik võrdlus, näited, selge argumentatsioon |
| **Kood kvaliteet** | 10% | Struktuur, nimed, kommentaarid, best practices |
| **README** | 5% | Projekti kirjeldus, käivitamisjuhend, selge |
| **Refleksioon** | 10% | 5 küsimust vastatud, sisukas, näitab mõistmist |

**Kokku: 100%**

---

##  Abimaterjalid ja lugemine

**Ansible:**
- [Ansible Roles Docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Jinja2 Templates](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)

**Puppet:**
- [Puppet Language Basics](https://puppet.com/docs/puppet/latest/lang_summary.html)
- [Puppet Modules](https://puppet.com/docs/puppet/latest/modules_fundamentals.html)
- [Puppet Forge](https://forge.puppet.com/)

**Kui abi vaja:**
1. Vaata `lisapraktika.md` faili täiendavate näidete jaoks
2. Kasuta `ansible-playbook --check` ja `puppet apply --noop` kuivaks käiguks
3. Küsi klassikaaslaselt või õpetajalt

---

##  Boonus (valikuline, +10%)

**Kui tahad ekstra punkte, tee üks või mitu neist:**

1. **Docker deployment:** Käivita mõlemad lahendused Docker container'ites
2. **CI/CD pipeline:** Lisa GitHub Actions, mis testib mõlemat lahendust
3. **Molecule testing:** Lisa Ansible Molecule test suite
4. **Performance testing:** Võrdle deployment kiirust (time command)
5. **Multi-environment:** Dev vs Prod konfiguratsioonid mõlemas tööriistas

---

**Edu ja head võrdlemist!** 
