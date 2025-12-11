# Ansible Edasijõudnud Funktsioonid

**Eeldused:** Ansible põhiteadmised, YAML süntaks, Linux CLI  
**Platvorm:** Ansible 2.9+, Ubuntu/Debian/RHEL/CentOS

## Õpiväljundid

- Mõistab muutujate hierarhia põhimõtteid ja praktilist väärtust
- Selgitab template'ide eeliseid staatiliste failide ees
- Eristab handler'ite ja tavaliste task'ide kasutusviise
- Võrdleb paroolide haldamise lähenemisi ja Vault'i rolli
- Rakendab neid kontseptsioone reaalse infrastruktuuri automatiseerimisel

---

## 1. Kui Lihtsast Saab Keeruline

Eelmistes tundides õppisite Ansible põhitõdesid. Kirjutasite playbook'i, mis seadistas serveri - installis pakette, kopeeris faile, käivitas teenuseid. Kolme serveriga töötas see suurepäraselt. Üks playbook, kolm identset serverit, kõik lihtne.

Aga päris maailmas pole kunagi kolm identset serverit. Mõelge, mis juhtub, kui ettevõte kasvab. Esimesel kuul on teil kolm serverit ja üks playbook. Kolmandal kuul on servereid viisteist - osa veebiserveri, osa andmebaasid. Teete kaks playbook'i, ühe web'ile ja teise db'le. Kui midagi ühist muuta, muudate mõlemas.

Poole aasta pärast on servereid nelikümmend kolmes keskkonnas - development, staging, production. Nüüd on teil kuus playbook'i. Iga muudatus tähendab kuue faili muutmist. Teete vea ühes, sama viga on kuues.

Aasta pärast on servereid üle saja. Playbook'e on paarkümmend. Muudatuste tegemine võtab tunde. Code review on võimatu, sest keegi ei mäleta, mis kus on. Uus tiimiliige vaatab projekti ja küsib: "Kust ma üldse alustan?"

See pole hüpoteetiline stsenaarium. See on täpselt see, mis juhtub, kui kasutate ainult Ansible põhifunktsioone suure infrastruktuuri haldamiseks. Põhifunktsioonid lahendavad ühe serveri automatiseerimise probleemi. Aga suure infrastruktuuri haldamine on hoopis teine probleem, mis vajab teistsuguseid tööriistu.

Täna õpime neli kontseptsiooni, mis lahendavad selle probleemi: muutujate hierarhia, template'id, handler'id ja vault. Need pole lihtsalt "mugavad lisad" - need on fundamentaalsed tööriistad, ilma milleta professionaalne Ansible projekt ei toimi.

---

## 2. Muutujate Hierarhia

Kujutage ette, et teie rakendus peab töötama kolmes keskkonnas. Development'is jookseb see pordil 3000, debug on sisse lülitatud ja andmebaas asub localhost'is. Production'is jookseb pordil 443, debug on kindlasti välja lülitatud ja andmebaas asub eraldi serveris kuskil pilves.

Kõige lihtsam viis seda lahendada oleks kirjutada kaks playbook'i - üks development'ile, teine production'ile. Aga siis iga muudatus tuleb teha kaks korda. Kui keskkondi on kolm, siis kolm korda. Kui keskkondi on viis ja serveritüüpe on kolm, siis viisteist korda.

Ansible pakub elegantsema lahenduse: muutujate hierarhia. Idee on lihtne - defineerite muutujad erinevatel tasemetel ja spetsiifilisem tase võidab alati üldisema.

Mõelge sellest nagu pärimisest programmeerimises. Vanem klass defineerib üldised omadused, laps pärib need, aga võib üle kirjutada. Ansible'is töötab see samamoodi: `group_vars/all.yml` defineerib üldised muutujad kõigile serveritele, `group_vars/production.yml` kirjutab mõned neist üle production serverite jaoks, ja `host_vars/special-server.yml` kirjutab veel mõned üle ühe konkreetse serveri jaoks.

Vaatame, kuidas see praktikas välja näeb. Loome kataloogi struktuuri:

```
group_vars/
├── all.yml
├── development.yml
└── production.yml
```

Failis `group_vars/all.yml` defineerime seaded, mis kehtivad kõigile serveritele olenemata keskkonnast:

```yaml
app_name: "myapp"
app_user: "deploy"
timezone: "Europe/Tallinn"
log_format: "json"
```

Need on asjad, mis ei muutu keskkonnast keskkonda. Rakenduse nimi on sama, kasutaja on sama, ajavöönd on sama.

Failis `group_vars/development.yml` defineerime seaded, mis kehtivad ainult development keskkonnale:

```yaml
app_port: 3000
app_debug: true
log_level: "debug"
database_host: "localhost"
ssl_enabled: false
```

Ja failis `group_vars/production.yml` defineerime production seaded:

```yaml
app_port: 443
app_debug: false
log_level: "error"
database_host: "db.example.com"
ssl_enabled: true
```

Nüüd saate kirjutada ühe playbook'i, mis kasutab lihtsalt muutujaid nagu `{{ app_port }}` ja `{{ database_host }}`. Kui käivitate selle development inventory vastu, saab ta development väärtused. Kui käivitate production vastu, saab production väärtused. Sama playbook, sama loogika, erinevad tulemused.

See lähenemine lahendab ka olukorra, kus üks konkreetne server vajab erilisi seadeid. Näiteks kui teil on production keskkonnas üks server, millel on rohkem RAM-i ja mis peaks saama rohkem worker'eid, loote faili `host_vars/big-server.yml`:

```yaml
worker_count: 32
```

See server saab 32 worker'it, kõik teised production serverid saavad vaikeväärtuse.

Ansible kogub automaatselt ka infot iga serveri kohta - neid nimetatakse faktideks. Fakte näete käsuga `ansible server1 -m setup`. Seal on info CPU tuumade arvu kohta (`ansible_processor_vcpus`), RAM-i kohta (`ansible_memtotal_mb`), operatsioonisüsteemi kohta (`ansible_os_family`) ja palju muud.

Fakte saab kasutada dünaamiliseks konfiguratsiooniks. Näiteks kui tahate, et Nginx worker'ite arv vastaks CPU tuumade arvule, kirjutate:

```yaml
nginx_workers: "{{ ansible_processor_vcpus }}"
```

Server kahe tuumaga saab 2 worker'it, server kaheksa tuumaga saab 8. Te ei pea iga serveri jaoks käsitsi väärtust määrama - Ansible arvutab selle ise välja serveri tegelike ressursside põhjal.

---

## 3. Template'id

Muutujate hierarhia lahendab probleemi, kuidas anda playbook'ile erinevaid väärtusi erinevates kontekstides. Aga mis saab konfiguratsioonifailidest, mis lähevad serveritesse?

Võtame näiteks Nginx konfiguratsiooni. Development keskkonnas näeb see välja umbes nii:

```nginx
server {
    listen 8080;
    server_name localhost;
    error_log /var/log/nginx/error.log debug;
    
    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```

Production keskkonnas näeb sama konfiguratsioon välja hoopis teisiti:

```nginx
server {
    listen 443 ssl;
    server_name app.example.com;
    ssl_certificate /etc/ssl/app.crt;
    ssl_certificate_key /etc/ssl/app.key;
    error_log /var/log/nginx/error.log error;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

Port on erinev, SSL on ainult production'is, log level on erinev, proxy_pass port on erinev. Kuidas seda hallata?

Üks võimalus oleks hoida kahte eraldi faili - `nginx-dev.conf` ja `nginx-prod.conf`. Aga siis iga muudatus, mis puudutab mõlemat, tuleb teha kahes kohas. Ja kui keskkondi on rohkem kui kaks, läheb asi kiiresti käest ära.

Ansible lahendus on template'id. Template on fail, kus osad väärtused on asendatud muutujatega ja kus saab kasutada tingimusloogikat. Ansible kasutab Jinja2 template engine'it, mis on sama, mida kasutab näiteks Flask ja Django.

Selle asemel, et hoida kahte eraldi konfiguratsiooni, loote ühe template faili `nginx.conf.j2`:

```jinja2
server {
    listen {{ nginx_port }}{% if ssl_enabled %} ssl{% endif %};
    server_name {{ server_name }};
    
{% if ssl_enabled %}
    ssl_certificate /etc/ssl/{{ app_name }}.crt;
    ssl_certificate_key /etc/ssl/{{ app_name }}.key;
{% endif %}

    error_log /var/log/nginx/error.log {{ log_level }};
    
    location / {
        proxy_pass http://127.0.0.1:{{ app_port }};
    }
}
```

Topelt looksulud `{{ }}` tähistavad muutujaid - Ansible asendab need tegelike väärtustega. Protsendimärgid `{% %}` tähistavad loogikat - tingimusi ja tsükleid.

Kui `ssl_enabled` on `false`, siis kogu SSL sektsioon jäetakse välja. Kui see on `true`, lisatakse SSL konfiguratsioon. Üks fail, mitu võimalikku väljundit.

Playbook'is kasutate template moodulit:

```yaml
- name: Deploy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/app.conf
```

Ansible võtab template faili, asendab muutujad väärtustega ja kirjutab tulemuse serverisse.

Jinja2 võimaldab ka keerulisemat loogikat. Näiteks kui teil on mitu backend serverit ja tahate genereerida upstream konfiguratsiooni:

```jinja2
upstream backend {
{% for server in backend_servers %}
    server {{ server.host }}:{{ server.port }} weight={{ server.weight }};
{% endfor %}
}
```

Kui `backend_servers` on:

```yaml
backend_servers:
  - host: 10.0.0.1
    port: 8080
    weight: 5
  - host: 10.0.0.2
    port: 8080
    weight: 3
```

Siis genereeritakse:

```nginx
upstream backend {
    server 10.0.0.1:8080 weight=5;
    server 10.0.0.2:8080 weight=3;
}
```

Lisate uue serveri listi - template genereerib automaatselt uue rea. Te ei pea konfiguratsiooni käsitsi muutma.

Template'ides saab kasutada ka filtreid, mis töötlevad väärtusi. Näiteks `{{ ansible_memtotal_mb * 0.7 | int }}` võtab serveri RAM-i, korrutab 0.7-ga ja teisendab täisarvuks. Nii saate dünaamiliselt arvutada puhvri suurusi serveri tegelike ressursside põhjal.

---

## 4. Handler'id

Oleme nüüd jõudnud punkti, kus saame dünaamiliselt genereerida konfiguratsioone ja rakendada neid serveritesse. Aga mis juhtub, kui konfiguratsioon muutub? Enamik teenuseid ei loe konfiguratsiooni automaatselt uuesti - neid tuleb restartida või reload'ida.

Kõige lihtsam viis oleks lisada restart task kohe pärast konfiguratsiooni muutmist:

```yaml
- name: Deploy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/app.conf

- name: Restart nginx
  service:
    name: nginx
    state: restarted
```

See töötab, aga on kaks probleemi.

Esiteks, Nginx restarditakse iga kord, kui playbook käivitub, isegi kui konfiguratsioon tegelikult ei muutunud. Ansible template moodul on idempotentne - kui fail on juba õige sisuga, ei kirjutata seda üle. Aga restart task käivitub ikka.

Teiseks, mis siis, kui teil on mitu task'i, mis muudavad Nginx konfiguratsiooni? Võib-olla üks muudab põhikonfiguratsiooni, teine virtuaalhosti, kolmas SSL seadeid. Kui iga task'i järel on restart, siis Nginx restarditakse kolm korda. Iga restart katkestab kasutajate ühendused.

Handler'id lahendavad mõlemad probleemid. Handler on task, mis käivitub ainult siis, kui teda teavitatakse, ja käivitub ainult üks kord playbook'i lõpus.

```yaml
tasks:
  - name: Deploy main config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx

  - name: Deploy vhost config
    template:
      src: vhost.conf.j2
      dest: /etc/nginx/sites-available/app.conf
    notify: restart nginx

  - name: Deploy SSL config
    template:
      src: ssl.conf.j2
      dest: /etc/nginx/conf.d/ssl.conf
    notify: restart nginx

handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

Võtmesõna on `notify` - see ütleb Ansible'ile, et kui see task midagi muudab, tuleb teavitada handler'it nimega "restart nginx".

Mis juhtub, kui käivitate selle playbook'i?

Kui ükski konfiguratsioon ei muutu, ei teavitata handler'it ja Nginx ei restardi. Playbook käivitub, kontrollib faile, näeb et kõik on korras, ja lõpetab.

Kui üks konfiguratsioon muutub, teavitatakse handler'it üks kord ja Nginx restarditakse üks kord playbook'i lõpus.

Kui kõik kolm konfiguratsiooni muutuvad, teavitatakse handler'it kolm korda, aga ta käivitub ikka ainult üks kord. Ansible koondab teavitused ja käivitab handler'i ühekordselt pärast kõiki task'e.

See on oluline erinevus tavaliste task'idega. Tavalised task'id käivituvad järjekorras, igaüks omal ajal. Handler'id käivituvad alles playbook'i lõpus, pärast kõiki task'e, ja ainult üks kord olenemata sellest, mitu korda neid teavitati.

Teine oluline nüanss on restart versus reload. Paljud teenused toetavad mõlemat - restart peatab teenuse täielikult ja käivitab uuesti, reload laeb ainult konfiguratsiooni uuesti ilma teenust peatamata.

Reload on peaaegu alati parem valik, sest see ei katkesta olemasolevaid ühendusi. Kasutajad ei märka midagi. Restart tuleks kasutada ainult siis, kui reload ei piisa - näiteks kui muudate midagi, mis nõuab teenuse täielikku taaskäivitamist.

```yaml
handlers:
  - name: reload nginx
    service:
      name: nginx
      state: reloaded

  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

Konfiguratsioonifaili muutmisel kasutate tavaliselt reload. Versiooniuuenduse puhul restart.

---

## 5. Vault

Oleme nüüd jõudnud punkti, kus saame hallata keerukat infrastruktuuri ühe playbook'iga. Muutujate hierarhia annab erinevad väärtused erinevatele keskkondadele, template'id genereerivad konfiguratsioone, handler'id haldavad teenuste taaskäivitamist intelligentselt.

Aga üks probleem on veel lahendamata: paroolid.

Teie playbook vajab andmebaasi parooli, API võtmeid, SSL sertifikaatide privaatvõtmeid. Kuskil peavad need olema. Kõige lihtsam viis oleks panna need otse muutujate faili:

```yaml
database_password: "SuperSecret123"
api_key: "sk-1234567890abcdef"
```

See töötab, aga on katastroofiline turvarisk. See fail läheb Git'i. Nüüd on teie paroolid nähtavad kõigile, kellel on repositooriumi ligipääs. Ja Git ei unusta - isegi kui kustutate faili, jääb see ajalukku. Kolm aastat hiljem saab keegi vana commit'i kätte ja seal on teie production andmebaasi parool.

Ansible Vault lahendab selle probleemi. Vault krüpteerib failid AES-256 algoritmiga. Krüpteeritud faili sisu näeb välja nii:

```
$ANSIBLE_VAULT;1.1;AES256
38613338343231653830653636333438626231336163613863373334316563613638643664653563
6233376436623262613539363930663965313138653862650a373638363362633537343233653538
```

See on täielik jama ilma võtmeta. Võite selle rahulikult Git'i panna - keegi ei saa sellest midagi kätte ilma vault paroolita.

Vault'i kasutamine on lihtne. Uue krüpteeritud faili loomiseks:

```bash
ansible-vault create group_vars/production/vault.yml
```

See avab redaktori. Kirjutate oma saladused:

```yaml
vault_database_password: "SuperSecret123"
vault_api_key: "sk-1234567890abcdef"
```

Salvestades krüpteeritakse fail automaatselt.

Olemasoleva faili krüpteerimiseks:

```bash
ansible-vault encrypt secrets.yml
```

Krüpteeritud faili muutmiseks:

```bash
ansible-vault edit group_vars/production/vault.yml
```

Parim praktika on hoida krüpteeritud muutujad eraldi failist tavalistest. Loote kaks faili:

`group_vars/production/vars.yml` (avalik):
```yaml
database_host: "db.example.com"
database_user: "app"
database_password: "{{ vault_database_password }}"
```

`group_vars/production/vault.yml` (krüpteeritud):
```yaml
vault_database_password: "ActualSecretPassword"
```

Avalik fail viitab krüpteeritud muutujale. Prefiks `vault_` teeb kohe selgeks, mis on krüpteeritud ja mis mitte.

Playbook'i käivitamisel peate andma vault parooli:

```bash
ansible-playbook site.yml --ask-vault-pass
```

Või kasutate paroolifaili:

```bash
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

Paroolifail peab loomulikult olema `.gitignore`'is.

See lahendab turvaprobleemi eleganselt. Saladused on versioonihaldsuses, aga krüpteeritult. Saate teha code review'd, näha muudatuste ajalugu, kasutada branch'e - kõike, mida Git pakub. Aga keegi ei näe tegelikke paroole ilma vault võtmeta.

---

## 6. Tervikpilt

Need neli kontseptsiooni - muutujate hierarhia, template'id, handler'id ja vault - ei ole isoleeritud trikid. Need töötavad koos, moodustades tervikliku süsteemi suure infrastruktuuri haldamiseks.

Muutujate hierarhia annab teile võimaluse defineerida erinevad väärtused erinevatele kontekstidele - keskkondadele, serveritüüpidele, üksikutele serveritele. Kirjutate ühe playbook'i, mis töötab kõigis kontekstides.

Template'id kasutavad neid muutujaid konfiguratsioonifailide genereerimiseks. Üks template genereerib erinevaid väljundeid vastavalt kontekstile. Development saab oma konfiguratsiooni, production oma.

Handler'id haldavad teenuste taaskäivitamist intelligentselt. Konfiguratsioon muutub - teenus laetakse uuesti. Konfiguratsioon ei muutu - midagi ei tehta. Mitu konfiguratsiooni muutub - teenus laetakse ikka ainult üks kord.

Vault hoiab saladused turvaliselt. Paroolid on versioonihaldsuses, aga krüpteeritult. Saate teha code review'd ja jälgida ajalugu ilma turvariske võtmata.

Kokku pannes saate süsteemi, kus üks käsk deployb teie rakenduse ükskõik millisesse keskkonda:

```bash
ansible-playbook -i inventory/production site.yml --ask-vault-pass
```

Sama playbook, sama template'id, sama loogika. Erinevad muutujad annavad erinevad tulemused.

---

## Kokkuvõte

Ansible põhifunktsioonid lahendavad ühe serveri automatiseerimise. Edasijõudnud funktsioonid lahendavad suure infrastruktuuri haldamise.

Muutujate hierarhia võimaldab kirjutada ühe playbook'i, mis töötab erinevates kontekstides. Spetsiifilisem väärtus võidab üldisema. Faktid annavad automaatse info serveri ressursside kohta.

Template'id genereerivad konfiguratsioone dünaamiliselt. Üks mall, mitu väljundit. Jinja2 annab muutujad, tingimused ja tsüklid.

Handler'id käivituvad ainult kui midagi muutus ja ainult üks kord. See vähendab ülearust taaskäivitamist ja hoiab teenused stabiilsena.

Vault krüpteerib saladused. Paroolid on versioonihaldsuses turvaliselt. Ilma võtmeta on fail loetamatu.

Järgmine samm on labor, kus rakendate kõik need kontseptsioonid praktiliselt.

---

## Ressursid

- [Ansible Variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)
- [Jinja2 Templates](https://jinja.palletsprojects.com/en/3.1.x/templates/)
- [Ansible Handlers](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)
- [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
