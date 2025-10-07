# Ansible Rollid

**Eeldused:** Ansible playbook'ide põhitundmine, YAML süntaks, Linux süsteemiadministreerimine  
**Platvorm:** Ansible 2.9+, Ubuntu 20.04+, testikeskkonnaks Vagrant

## Õpiväljundid

Pärast seda teemat õppija:
- Mõistab rollide eesmärki ja nende kohta infrastruktuuri automatiseerimisel
- Selgitab Galaxy standardi rolli struktuuri komponente ja nende vastutusalasid
- Eristab muutujate prioriteete (defaults, vars, inventory) ja oskab neid strateegiliselt kasutada
- Võrdleb template'ide ja staatiliste failide lähenemisi konfiguratsioonihalduses
- Rakendab handlers'eid teenuste ohutukuks taaskäivitamiseks ainult muudatuste korral

---
![Ansible Role directory structure](https://automateinfra.com/wp-content/uploads/2021/03/image-3.png?w=593)


Ansible playbook'id algavad tavaliselt lihtsalt. Paigaldate Nginx'i, kopeerite konfiguratsiooni, käivitate teenuse. Fail on 50 rida, kõik toimib. Siis tuleb vajadus sama teha PostgreSQL'iga. Kopeerite koodi, muudate paari rida. Nüüd on kaks playbook'i, mõlemad 50 rida, 80% kood on identne. Kolmas projekt vajab Nginx'i ja PostgreSQL'i koos. Kas kopeerida mõlemad kokku ühte 100-realiseks faili? Kuidas hooldada seda, kui Nginx'i konfiguratsioon peab muutuma kõikides projektides?

Selline kordus on probleem, mida rollid lahendavad. Roll on isoleeritud, taaskasutatav komponent, mis täidab ühte selget eesmärki. Mõelge sellele nagu funktsioonidele programmeerimises - te ei kirjuta sama koodi kümme korda, vaid loote funktsiooni ja kutsute seda kümme korda. Ansible rollid järgivad sama printsiipi: kirjutage kord, kasutage mitmetes projektides.

## 1. Rollide Vajadus ja Arhitektuur

### Playbook'ide Evolutsioon

Vaatleme tüüpilist playbook'ide arenguteed ettevõttes. Alguses on üks lihtne deploy script, mis paigaldab rakenduse. See kasvab aja jooksul, lisanduvad backup'id, monitoring, turvaseaded. Aasta pärast on teil 500-realine playbook, mida on raske mõista ja muuta. Iga muudatus nõuab hoolikat testimist, sest kõik on omavahel põimunud.

Rollid lahendavad selle struktureeritud lagunemisega. Iga vastutusala eraldatakse omaette mooduliks. Nginx'i roll tegeleb ainult veebiserveri paigaldamise ja konfigureerimisega. PostgreSQL'i roll fokuseerib andmebaasile. Monitoring roll lisab Prometheus agendi. Kui vaja nginx'i uuendada, muudate ainult nginx rolli - teised jäävad puutumata.

See modulaarsus toob kaasa ka testimise lihtsuse. Iga rolli saab testida isoleeritult. Nginx roll peab töötama iseseisvalt, PostgreSQL roll samuti. Seejärel ühendame need playbook'is kokku, teades et iga komponent on juba valideeritud. Veamänguruum väheneb oluliselt.

### Galaxy Standard

Ansible Galaxy on rollide jagamise platvorm, kuid see määratleb ka standardi rolli struktuuri kohta. See standard pole suvaline - see on praktikas väljakujunenud parim lähenemine. Kui kõik rollid järgivad sama struktuuri, siis ükskõik kelle rolli te vaatate, oskate kohe öelda kus asuvad tasks, kus template'id, kus muutujad.

```
nginx-webserver/
├── defaults/
│   └── main.yml          # Madalama prioriteediga vaikeväärtused
├── vars/
│   └── main.yml          # Kõrgema prioriteediga muutujad
├── tasks/
│   ├── main.yml          # Peamine tasks'ide loend
│   ├── install.yml       # Paigaldamise tasks'id
│   └── configure.yml     # Konfiguratsiooni tasks'id
├── templates/
│   └── nginx.conf.j2     # Jinja2 template'id
├── files/
│   └── ssl-params.conf   # Staatilised failid
├── handlers/
│   └── main.yml          # Teenuste restart/reload handlerid
├── meta/
│   └── main.yml          # Rolli metadata ja dependencies
└── README.md             # Dokumentatsioon
```

See struktuur on kavandatud lähtudes eraldatuse põhimõttest. Tasks'id kirjeldavad mida teha. Template'id sisaldavad kuidas konfigureerida. Variables määravad parameetrid. Handlers haldavad teenuseid. Meta kirjeldab sõltuvusi. Iga kaust omab selget vastutust ja neid muudetakse erinevatel põhjustel.

Allikas: [Ansible Galaxy](https://galaxy.ansible.com/ui/)


### Rollide Anatoomia

Vaatleme iga komponenti lähemalt, alustades metadata'st. Meta kaust sisaldab `main.yml` faili, mis kirjeldab rolli ennast - autor, toetatud platvormid, sõltuvused teistest rollidest. See ei mõjuta käitumist, aga on kriitiline kui jagame rolli teistega või kasutame Galaxy'st allalaetud rolle.

```yaml
# meta/main.yml
galaxy_info:
  author: "DevOps Team"
  description: "Production-grade Nginx with SSL"
  min_ansible_version: "2.9"
  platforms:
    - name: Ubuntu
      versions: [focal, jammy]
dependencies:
  - role: firewall
    vars:
      firewall_allowed_ports: [80, 443]
```

Dependencies sektsioonis määratleme teised rollid, mida meie roll vajab. Kui nginx roll vajab firewall'i, siis Ansible käivitab automaatselt firewall rolli enne nginx rolli. See dependency chain tagab õige järjekorra ilma et playbook'is peaks seda käsitsi haldama.

Tasks kaust sisaldab tegevuste definitsioone. Peamine `main.yml` toimib tavaliselt orchestrator'ina, kutsudes välja spetsiifilisemaid tasks faile. See hoiab koodi organiseerituna - paigaldamine ühes failis, konfigureerimine teises, teenuse haldamine kolmandas. Iga fail on 20-50 rida selget, fookustatud koodi, mitte 200 rida kõike kokku segamini.

## 2. Variables ja Nende Prioriteedid

### Defaults vs Vars

Ansible'il on keeruline muutujate prioriteetide süsteem, kuid rollide kontekstis on kaks peamist kohta: `defaults/main.yml` ja `vars/main.yml`. Nende erinevus pole ainult nimes - nad teenivad erinevaid strateegilisi eesmärke ja omavad drastiliselt erinevaid prioriteete.

Defaults on madalama prioriteediga muutujad. Peaaegu kõik muu võib neid üle kirjutada - inventory muutujad, playbook vars, group_vars. Need on mõeldud mõistlikeks vaikeväärtusteks, mida kasutaja peaks saama kergesti muuta. Näiteks nginx rolli puhul võiks defaults sisaldada HTTP porti, worker processes arvu, timeout väärtusi. Need on parameetrid, mida erinevates keskkondades sageli koohandatakse.

```yaml
# defaults/main.yml
nginx_http_port: 80
nginx_https_port: 443
nginx_worker_processes: "{{ ansible_processor_vcpus }}"
nginx_worker_connections: 1024
nginx_keepalive_timeout: 65
nginx_client_max_body_size: "1m"
```

Vars on kõrgema prioriteediga ja neid on raskem üle kirjutada. Need on mõeldud väärtustele, mis on rolli sisemise loogika jaoks kriitilised. OS-spetsiifilised paketinimed, konfiguratsioonifailide asukohad, teenuse nimed - need ei tohiks kasutaja poolt juhuslikult muutuda. Kui keegi proovib Ubuntu süsteemis nginx paketi nimeks määrata "httpd", peaks see ebaõnnestuma.

```yaml
# vars/main.yml
_nginx_packages:
  Debian: [nginx, ssl-cert]
  RedHat: [nginx, mod_ssl]

nginx_packages: "{{ _nginx_packages[ansible_os_family] }}"
nginx_config_path: "/etc/nginx"
nginx_service_name: "nginx"
```

Allkriipsuga eesliited (`_nginx_packages`) on konventsioon märkimaks sisemisi muutujaid, mida kasutaja ei peaks otse kasutama. Tegelik muutuja `nginx_packages` valitakse dünaamiliselt OS perekonna põhjal. See abstraheerimine lubab rollil töötada erinevates operatsioonisüsteemides ilma et kasutaja peaks sellest muretsema.

Allikas: [Ansible Variable Precedence — Ivan Krizsan](https://www.ivankrizsan.se/2021/12/13/ansible-variable-precedence/)

### Template Variables

Jinja2 template'id võimaldavad konfiguratsioone dünaamiliseks muuta, kuid nende oskuslik kasutamine nõuab strateegilist mõtlemist. Iga template muutuja on sõltuvus - punkt, kus käitumine muutub. Liiga palju muutujaid teeb rolli raskesti hooldatavaks, liiga vähe muutujaid teeb selle jäigaks.

Hea praktika on pakkuda mõistlikke vaikeväärtusi ja lubada neid vajadusel kohandada. Näiteks nginx'i worker processes võiks vaikimisi vastata CPU tuumade arvule, aga produktsioonis võib soovida selle käsitsi seadistada kõrgema väärtuse peale koormuse testimise põhjal.

```nginx
# templates/nginx.conf.j2
user {{ nginx_user | default('www-data') }};
worker_processes {{ nginx_worker_processes | default(ansible_processor_vcpus) }};
pid {{ nginx_pid_file | default('/run/nginx.pid') }};

events {
    worker_connections {{ nginx_worker_connections | default(1024) }};
    use {{ nginx_event_method | default('epoll') }};
}
```

Jinja2 `default()` filter on turvavariant. Kui muutujat pole defineeritud, kasutatakse default väärtust. See muudab template vastupidavamaks vigadele, kuid loob ka implitsiitseid sõltuvusi. Dokumentatsioonis peab selgitama mitte ainult millised muutujad on saadaval, vaid ka mis on nende vaikeväärtused template tasandil.

Conditional logic template'ides võimaldab käitumise kohandamist. SSL konfiguratsiooni saab kaasata ainult kui SSL on lubatud. Gzip kompressioon aktiveerub optional seadistuse põhjal. See teeb ühest template'ist mitme variandi allikas, vältides konfiguratsioonifailide proliferatsiooni.

```nginx
http {
    {% if nginx_gzip_enabled | default(true) %}
    gzip on;
    gzip_comp_level {{ nginx_gzip_level | default(6) }};
    gzip_types {{ nginx_gzip_types | default('text/plain text/css application/json') }};
    {% endif %}
    
    {% if nginx_ssl_enabled | default(false) %}
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers {{ nginx_ssl_ciphers | default('HIGH:!aNULL:!MD5') }};
    ssl_prefer_server_ciphers on;
    {% endif %}
}
```
[![Jinja2 in Ansible](https://yugencorpblogs.wordpress.com/wp-content/uploads/2020/05/jinja2-ansible.jpg)](https://yugencorpblogs.wordpress.com/2020/05/06/jinja2-template-for-ansible/)


## 3. Tasks Organiseerimine

### Include vs Import

Ansible pakub kahte mehhanismi tasks'ide eraldamiseks: `include_tasks` ja `import_tasks`. Nende valik pole triviaalne - neil on erinev käitumine ja jõudlus. Import on staatiline, juhtub playbook'i parse'imise ajal. Include on dünaamiline, juhtub käitamise ajal.

Import on kiirem ja võimaldab Ansible'il kogu playbook'i struktuuri kohe valideerida. Kui teil on süntaksiviga imporditud tasks'is, Ansible leiab selle enne käitamise algust. Include on paindlikum - saab kasutada conditionals'ega ja loops'idega dünaamiliselt määramaks milliseid tasks'e käivitada. Tavaliselt rollides kasutatakse include_tasks, sest paindlikkus on olulisem kui minimaalne jõudluse võit.

```yaml
# tasks/main.yml
- name: "Validate configuration"
  include_tasks: validate.yml

- name: "Install Nginx"
  include_tasks: install.yml

- name: "Configure Nginx"
  include_tasks: configure.yml

- name: "Setup SSL"
  include_tasks: ssl.yml
  when: nginx_ssl_enabled | default(false)

- name: "Setup virtual hosts"
  include_tasks: vhosts.yml
  when: nginx_vhosts | length > 0
```

See struktuur loeb nagu sisukord. Main.yml kirjeldab kõrge taseme loogikat - mida tehakse ja millises järjekorras. Igal alamfailil on konkreetne vastutus. Validate.yml kontrollib sisendeid, install.yml paigaldab pakette, configure.yml seadistab põhikonfiguratsiooni. SSL ja virtual hosts on optional - need käivitatakse ainult kui kasutaja on need funktsionaalsused sisse lülitanud.

### Idempotence


Ansible'i fundamentaalne printsiip on idempotentsus - playbook'i saab käivitada mitu korda ilma ebasoovitatavate kõrvalefektideta. Esimesel korral tehakse muudatused, teisel korral tuvastab Ansible et soovitud olek on juba saavutatud ja jätab kõik muutmata. See on võimas omadus, mis nõuab hoolikat tasks'ide kavandamist.

Mõned moodulid on automaatselt idempotentsed. File moodul kontrollib faili olemasolu ja õigusi enne midagi muutmast. Package moodul kontrollib kas pakett on juba paigaldatud. Template moodul võrdleb olemasolevat faili uue sisuga ja kopeerib ainult kui need erinevad. Need moodulid teevad idempotentsuse lihtsamaks.

Command ja shell moodulid on probleemsed. Need käivitavad käsu alati, olenemata olekust. Kui käsk on `rm -rf /tmp/mydir`, siis esimesel korral see eemaldab kausta, teisel korral ebaõnnestub sest kaust puudub. Idempotentsuse tagamiseks tuleb kasutada `creates` või `removes` parameetreid, või vältida neid mooduleid üldse kui on olemas parem alternatiiv.

```yaml
- name: "Generate SSL certificate"
  command: >
    openssl req -x509 -nodes -days 365
    -newkey rsa:2048
    -keyout /etc/ssl/private/nginx.key
    -out /etc/ssl/certs/nginx.crt
    -subj "/C=EE/O=Example/CN={{ ansible_fqdn }}"
  args:
    creates: /etc/ssl/certs/nginx.crt
```

Creates parameeter ütleb "käivita see käsk ainult kui seda faili pole olemas". Kui sertifikaat eksisteerib, Ansible jätab käsu vahele. See tagab idempotentsuse - esimesel korral genereeritakse sertifikaat, järgnevatel kordadel mitte. Ilma creates'ita genereeritaks iga kord uus sertifikaat, mis põhjustaks teenuse restarti ja potentsiaalselt klientide ühenduste katkemist.

Allikas : [What is Idempotency in Ansible](https://medium.com/@haroldfinch01/what-is-idempotency-in-ansible-9d264c116193)

## 4. Handlers ja Teenuste Haldamine

### Handlers'i Roll

Handlers on spetsiaalne tasks'i tüüp, mis käivitatakse ainult kui neid "notifitakse" ja ainult playbook'i lõpus. See on kriitiline teenuste haldamiseks. Kui muudate nginx'i konfiguratsiooni kümnes kohas, te ei taha et nginx restart'itaks kümme korda - üks kord lõpus on piisav.

```yaml
# handlers/main.yml
- name: restart nginx
  service:
    name: nginx
    state: restarted

- name: reload nginx
  service:
    name: nginx
    state: reloaded

- name: validate nginx config
  command: nginx -t
```

Restart vs reload valik on oluline. Restart peatab teenuse täielikult ja käivitab uuesti - see katkestab aktiivsed ühendused. Reload loeb konfiguratsiooni uuesti ilma teenust peatamata - aktiivsed ühendused jätkuvad, uued ühendused kasutavad uut konfiguratsiooni. Produktsioonis eelistatakse reload'i, aga mõned muudatused (näiteks SSL sertifikaadi vahetus) võivad nõuda restart'i.

Tasks'id notifivad handlers'eid muudatuste korral. Ansible jälgib iga task'i "changed" staatust. Kui task muudab midagi, ta märgib end muudetuks ja käivitab notify direktiivi. Kui task ei muuda midagi (näiteks fail on juba olemas õigete õigustega), notify'i ei käivitata.

```yaml
# tasks/configure.yml
- name: "Copy main nginx config"
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    validate: nginx -t -c %s
  notify:
    - validate nginx config
    - reload nginx

- name: "Copy SSL certificate"
  copy:
    src: "{{ nginx_ssl_cert }}"
    dest: /etc/ssl/certs/nginx.crt
    mode: '0644'
  notify: restart nginx
  when: nginx_ssl_enabled
```

Validate parameeter template moodulil on turvavariant. Enne kui Ansible kopeerib uue konfiguratsioonifaili kohale, ta käivitab validatsiooni käsu ajutise failiga. Kui nginx -t ebaõnnestub, Ansible ei kopeeri faili ja playbook ebaõnnestub. See ennetab olukorda, kus vigane konfiguratsioon läheb live'i ja nginx ei käivitu enam.

Allikas: [How to Use Handlers in Ansible](https://medium.com/cloudnloud/how-to-use-handlers-in-ansible-9e62e17c3b61)

### Teenuse State Management

Service moodul haldab systemd teenuseid, kuid sellel on nüansse. State parameeter võib olla started, stopped, restarted, reloaded. Enabled parameeter määrab kas teenus käivitatakse boot'imisel. Need on sõltumatud - teenus võib olla started aga mitte enabled, või enabled aga mitte started.

```yaml
- name: "Ensure nginx is running and enabled"
  service:
    name: nginx
    state: started
    enabled: yes
```

See task tagab kaks asja. Esiteks, nginx on hetkel käimas. Teiseks, nginx käivitatakse automaatselt kui server reboot'ib. Ansible kontrollib mõlemat tingimust ja teeb muudatused ainult vajadusel. Kui nginx on juba käimas ja enabled, task ei muuda midagi.

Rollides on tavaline pattern kontrollida teenuse olekut mitmetes kohtades. Install tasks'is võib teenus stopped olla kuni konfiguratsioon on paigas. Configure tasks'is käivitatakse teenus pärast konfiguratsiooni. Handlers restart'ivad või reload'ivad teenust muudatuste korral. See etapiline lähenemine tagab et teenus pole käimas pooliku konfiguratsiooniga.

## 5. Dependencies ja Role Composition

### Meta Dependencies

Rollid ei eksisteeri isolatsioonis - nad sõltuvad teineteisest. Nginx roll võib vajada firewall'i, mis avab HTTP ja HTTPS pordid. Rakenduse roll vajab andmebaasi rolli. Monitoring roll sõltub kõikidest teistest rollidest, sest ta peab neid monitorima. Need sõltuvused deklareeritakse meta/main.yml failis.

```yaml
# meta/main.yml
dependencies:
  - role: common
    vars:
      common_packages: [curl, vim, git]
  
  - role: firewall
    vars:
      firewall_allowed_tcp_ports: [80, 443]
      firewall_allowed_udp_ports: []
  
  - role: ssl-certificates
    when: nginx_ssl_enabled | default(false)
```

Ansible täidab dependencies enne rolli ennast. Kui käivitate nginx rolli, Ansible esiteks täidab common, siis firewall, siis ssl-certificates, ja alles siis nginx rolli task'id. See automaatne dependency resolution vähendab playbook'ide keerukust - te ei pea käsitsi järjestama rolle õiges järjekorras.

Dependencies võivad omakorda omada dependencies. See loob dependency graafi, mida Ansible lahendab topological sort'iga. Kui kolm rolli kõik sõltuvad common rollist, Ansible käivitab common rolli ainult üks kord, mitte kolm korda. See vältib dubleerimist ja kiirendab täitmist.

### Shared State

Rollid jagavad muutujaid läbi erinevate Ansible scope'ide. Playbook vars on kõikidele rollidele nähtavad. Group_vars kohalduvad teatud host'ide gruppidele. Host_vars on spetsiifilised üksikutele host'idele. Rollide vaheline kommunikatsioon toimub peamiselt läbi nende jagatud muutujate.

```yaml
# group_vars/webservers/shared.yml
app_user: webapp
app_port: 3000
ssl_enabled: true
environment: production

# Nginx roll kasutab neid
nginx_proxy_pass: "http://localhost:{{ app_port }}"
nginx_ssl_enabled: "{{ ssl_enabled }}"

# Application roll kasutab neid
app_listen_port: "{{ app_port }}"
app_run_as_user: "{{ app_user }}"
```

See lähenemine võimaldab rollide koordineerimist ilma et nad otse teineteisest sõltuksid. Nginx roll ei pea teadma application rolli sisemisest struktuurist - mõlemad kasutavad jagatud muutujaid kui lepingut. Kui muudate app_port'i väärtust, mõlemad rollid kohanduvad automaatselt.

Registered variables võimaldavad rollide vahelist andmete edasiandmist käitusajal. Kui üks roll genereerib parooli või võtme, saab selle registreerida ja teised rollid saavad seda kasutada. See on võimas, aga nõuab hoolikat dokumenteerimist - ei ole ilmne milliseid muutujaid roll ekspordib.

```yaml
- name: "Generate database password"
  set_fact:
    db_password: "{{ lookup('password', '/dev/null length=32') }}"
  run_once: true

- name: "Store password for other roles"
  set_fact:
    postgres_password: "{{ db_password }}"
```

## 6. Testimine ja Kvaliteedikontroll

### Role Testing Strategies

Rollide testimine erineb playbook'ide testimisest. Roll peab töötama isoleeritult, erinevates operatsioonisüsteemides, erinevate parameetritega. Molecule on de facto standard rolli testimiseks - see loob ajutisi teste keskkondi (Docker containers, Vagrant VMs), käivitab rolli nendega ja kontrollib tulemust.

Testimise kihid algavad süntaksi valideerimisest. Ansible-lint kontrollib common anti-pattern'eid - deprecated moodulid, ebaefektiivsed konstruktsioonid, turvaprobleemid. Yamllint tagab YAML süntaksi korrektsuse. Need tööriistad leiavad põhivead enne kui playbook üldse käivitatakse.

```yaml
# .ansible-lint
skip_list:
  - '106'  # Role name with galaxy prefix
warn_list:
  - experimental
  - role-name
```

Integration tests kontrollivad kas roll tegelikult teeb seda, mida lubab. Pärast nginx rolli käivitamist peaks nginx olema käimas, kuulama õigeid porte, serveeriva kohandatud konfiguratsiooni. Molecule võimaldab kirjutada verify tasks'e, mis kontrollivad neid tingimusi.

```yaml
# molecule/default/verify.yml
- name: Verify nginx is running
  service:
    name: nginx
    state: started
  check_mode: yes
  register: nginx_service
  failed_when: nginx_service.changed

- name: Test HTTP response
  uri:
    url: http://localhost
    status_code: 200
```

### Continuous Integration

Rollid peaksid olema testitud igal commit'il. GitHub Actions, GitLab CI, Jenkins - kõik võimaldavad automatiseeritud testimist. Tüüpiline CI pipeline käivitab linting'i, siis Molecule teste erinevates OS'ides, siis publitseerib rolli Galaxy'sse kui kõik õnnestub.

```yaml
# .github/workflows/test.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        distro: [ubuntu2004, ubuntu2204, debian11]
    steps:
      - uses: actions/checkout@v2
      - name: Run Molecule tests
        run: molecule test
        env:
          MOLECULE_DISTRO: ${{ matrix.distro }}
```

See matrix strategy testib rolli kolmes erinevas distributsionis paralleelselt. Kui roll ebaõnnestub ühes OS'is, CI ebaõnnestub ja merge blokitakse. See tagab et roll töötab deklareeritud platvormides enne kui see produktsiooni jõuab.

## 7. Galaxy ja Rollide Jagamine

### Publishing Best Practices

Ansible Galaxy on rollide jagamise platvorm, kuid hea roll pole ainult töötav kood - see on dokumentatsioon, näited, versioonihaldus. README.md on esimene punkt kus potentsiaalne kasutaja otsustab kas teie rolli kasutada. See peab sisaldama selget kirjeldust, installatsiooni juhiseid, muutujate dokumentatsiooni, kasutusnäiteid.

```markdown
# Ansible Role: nginx-pro

Production-ready Nginx role with SSL, virtual hosts, and performance tuning.

## Requirements

- Ansible 2.9+
- Ubuntu 20.04+ or Debian 11+

## Role Variables

- `nginx_worker_processes`: Number of worker processes (default: auto-detect CPU cores)
- `nginx_ssl_enabled`: Enable SSL support (default: false)
- `nginx_vhosts`: List of virtual hosts (default: [])

## Example Playbook

```yaml
- hosts: webservers
  roles:
    - role: nginx-pro
      vars:
        nginx_ssl_enabled: true
        nginx_vhosts:
          - name: example.com
            root: /var/www/example
```
```

Semantic versioning on oluline. Versioon 1.2.3 tähendab: major.minor.patch. Patch muudatused on bugfixid, mis ei muuda API'd. Minor muudatused lisavad funktsionaalsusi tagasiühilduvalt. Major muudatused võivad murda olemasolevat kasutust. Kasutajad peavad saama usaldada et kui nad lukustavad rolli versioonile 1.x, ei murra uuendused nende playbook'e.

Galaxy import käsib lokaalset Git repositooryt. Tag'id muutuvad Galaxy versioonideks. Iga muudatus peab olema git tag'itud enne Galaxy'sse importimist. See annab selge ajaloo ja võimaldab kasutajatel valida täpset versiooni mida nad usaldavad.

```bash
git tag -a v1.2.0 -m "Add virtual hosts support"
git push origin v1.2.0
ansible-galaxy import username repository-name
```

---

Rollid transformeerivad Ansible'i ad-hoc skriptimise tööriistast tõeliseks Infrastructure as Code platvormiks. Iga roll on komponent, mida saab testida, versiooni all hoida, jagada. Koos moodustavad need taaskasutatavate komponentide teegi, mis kiirendab iga järgmise projekti arengut. Infrastruktuuri ehitamine muutub komponentide kompositsiooniks, mitte kõige algusest skriptide kirjutamiseks.