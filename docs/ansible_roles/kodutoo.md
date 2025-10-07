# Ansible vs Puppet Kodutöö: Võrdlev Infrastruktuuri Automatiseerimine

Ehitate sama veebiserveri infrastruktuuri kahel erineval viisil - Ansible'i (push-based) ja Puppet'iga (pull-based). Võtab umbes 4-6 tundi, sõltuvalt kogemusest ja kui põhjalikku võrdlust teostate. Projekt simuleerib reaalset olukorda, kus peate valima automatiseerimistehnoloogia ettevõtte jaoks ja põhjendama valikut.

**Eeldused:** Ansible rollide labor läbitud, Vagrant kogemus, Git kasutamine  
**Esitamine:** GitHub avalik repositoorium, sisaldab nii Ansible kui Puppet lahendust, README.md ja COMPARISON.md  
**Tähtaeg:** Järgmise nädala algus

---

Ettevõtted seisavad tihti automatiseerimistehnoloogia valiku ees. Ansible on populaarne oma lihtsuse tõttu. Puppet on tugev suurte infrastruktuuride haldamisel. Mõlemad suudavad sama tulemust, aga erinevate meetoditega. See projekt õpetab teil mõista nende erinevusi praktikas, mitte ainult teooriast.

## 1. Projekti Ülevaade

Loote täieliku veebiserveri seadistuse, mis sisaldab:
- Nginx veebiserver koos SSL sertifikaatidega
- Kaks virtual host'i (test.local ja demo.local)
- PostgreSQL andmebaas koos esialse schema'ga
- Põhiline monitoring (health check script)
- Logide rotatsioon

Kõik see tehakse kahel viisil - esmalt Ansible'iga, seejärel Puppet'iga. Lõpptulemus peab mõlemal juhul olema identne, aga implementatsioon erineb.

## 2. Keskkonna Seadistamine

Kasutate Vagrant'i kahte isoleeritud VM'i jaoks. Üks Ansible'i jaoks, teine Puppet'i jaoks. See võimaldab õiglast võrdlust - mõlemad algavad puhtalt lehelt.

### Git repositooriumi loomine
```bash
mkdir ansible-puppet-comparison
cd ansible-puppet-comparison
git init
```

Looge README.md esmase struktuuriga:
```markdown
# Ansible vs Puppet: Practical Comparison

Comparative infrastructure automation project implementing identical web server setup using both Ansible and Puppet.

## Project Goal

Understand practical differences between push-based (Ansible) and pull-based (Puppet) automation approaches.

## Infrastructure Components

- Nginx with SSL
- Virtual hosts (test.local, demo.local)
- PostgreSQL database
- Health monitoring
- Log rotation

## Repository Structure
```
ansible/          - Ansible implementation
puppet/           - Puppet implementation
vagrant/          - VM configurations
COMPARISON.md     - Detailed comparison
```

## Setup Instructions

[Täidetakse hiljem]
```

### Vagrantfile loomine
```ruby
# vagrant/Vagrantfile
Vagrant.configure("2") do |config|
  
  # Ansible VM
  config.vm.define "ansible" do |ansible|
    ansible.vm.box = "ubuntu/focal64"
    ansible.vm.hostname = "ansible-test"
    ansible.vm.network "private_network", ip: "192.168.56.10"
    ansible.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
  end
  
  # Puppet VM
  config.vm.define "puppet" do |puppet|
    puppet.vm.box = "ubuntu/focal64"
    puppet.vm.hostname = "puppet-test"
    puppet.vm.network "private_network", ip: "192.168.56.11"
    puppet.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
  end
end
```

Commit esmane struktuur:
```bash
git add .
git commit -m "Initial project structure"
```

## 3. Ansible Implementatsioon

Ansible osa kasutab rolle, mida laboris õppisite. Loote kolm rolli: nginx, postgresql, monitoring. Iga roll on modulaarne ja taaskasutatav.

### Ansible projekti struktuur
```bash
mkdir -p ansible/{roles,group_vars,inventory}
cd ansible
```

### Inventory ja variables
```ini
# inventory/hosts
[webservers]
ansible-test ansible_host=192.168.56.10 ansible_user=vagrant
```
```yaml
# group_vars/webservers.yml
---
# Nginx configuration
nginx_ssl_enabled: true
nginx_vhosts:
  - name: test.local
    root: /var/www/test
    ssl: true
  - name: demo.local
    root: /var/www/demo
    ssl: true

# PostgreSQL configuration
postgresql_version: "12"
postgresql_databases:
  - name: webapp
postgresql_users:
  - name: webuser
    password: "changeme123"
    db: webapp

# Monitoring
monitoring_enabled: true
health_check_interval: "*/5"
```

### Nginx role loomine
```bash
cd roles
ansible-galaxy init nginx
```

Nginx tasks (lühendatud näide):
```yaml
# roles/nginx/tasks/main.yml
---
- name: "Install Nginx"
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: "Setup SSL certificates"
  include_tasks: ssl.yml
  when: nginx_ssl_enabled

- name: "Configure virtual hosts"
  include_tasks: vhosts.yml

- name: "Ensure nginx is running"
  service:
    name: nginx
    state: started
    enabled: yes
```
```yaml
# roles/nginx/tasks/ssl.yml
---
- name: "Create SSL directories"
  file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - /etc/ssl/certs
    - /etc/ssl/private

- name: "Generate self-signed certificate"
  command: >
    openssl req -x509 -nodes -days 365 -newkey rsa:2048
    -keyout /etc/ssl/private/nginx.key
    -out /etc/ssl/certs/nginx.crt
    -subj "/C=EE/O=ITS24/CN={{ ansible_fqdn }}"
  args:
    creates: /etc/ssl/certs/nginx.crt
```

### PostgreSQL role
```yaml
# roles/postgresql/tasks/main.yml
---
- name: "Install PostgreSQL"
  apt:
    name:
      - postgresql
      - postgresql-contrib
      - python3-psycopg2
    state: present

- name: "Ensure PostgreSQL is running"
  service:
    name: postgresql
    state: started
    enabled: yes

- name: "Create databases"
  postgresql_db:
    name: "{{ item.name }}"
    state: present
  loop: "{{ postgresql_databases }}"
  become_user: postgres

- name: "Create users"
  postgresql_user:
    name: "{{ item.name }}"
    password: "{{ item.password }}"
    db: "{{ item.db }}"
    priv: ALL
  loop: "{{ postgresql_users }}"
  become_user: postgres
```

### Monitoring role
```yaml
# roles/monitoring/tasks/main.yml
---
- name: "Deploy health check script"
  template:
    src: health-check.sh.j2
    dest: /usr/local/bin/health-check.sh
    mode: '0755'

- name: "Setup cron for health checks"
  cron:
    name: "nginx health check"
    minute: "{{ health_check_interval }}"
    job: "/usr/local/bin/health-check.sh >> /var/log/health-check.log 2>&1"
```
```bash
# roles/monitoring/templates/health-check.sh.j2
#!/bin/bash
# Health check script managed by Ansible

DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo "$DATE - Nginx: OK"
else
    echo "$DATE - Nginx: FAILED"
fi

# Check PostgreSQL
if systemctl is-active --quiet postgresql; then
    echo "$DATE - PostgreSQL: OK"
else
    echo "$DATE - PostgreSQL: FAILED"
fi
```

### Main playbook
```yaml
# site.yml
---
- name: "Deploy web infrastructure"
  hosts: webservers
  become: yes
  
  roles:
    - nginx
    - postgresql
    - monitoring
```

### Testimine ja deploy
```bash
cd vagrant && vagrant up ansible
cd ../ansible
ansible-playbook -i inventory/hosts site.yml
```

Validation:
```bash
ansible webservers -i inventory/hosts -m command -a "systemctl status nginx"
ansible webservers -i inventory/hosts -m command -a "systemctl status postgresql"
curl -k https://192.168.56.10
```

Commit:
```bash
git add ansible/
git commit -m "Complete Ansible implementation with nginx, postgresql, monitoring"
```

## 4. Puppet Implementatsioon

Puppet kasutab erinevat struktuuri ja süntaksi. Agent töötab serveris ja küsib perioodiliselt konfiguratsiooni. Selles projektis kasutate masterless setup'i - agent apply rakendab manifeste lokaalal.

### Puppet projekti struktuur
```bash
mkdir -p puppet/{manifests,modules}
cd puppet
```

### Puppet modules loomine
```bash
cd modules
puppet module generate its24-nginx
puppet module generate its24-postgresql
puppet module generate its24-monitoring
```

### Nginx module
```puppet
# modules/nginx/manifests/init.pp
class nginx (
  Boolean $ssl_enabled = true,
  Array[Hash] $vhosts = [],
) {
  
  package { 'nginx':
    ensure => installed,
  }
  
  if $ssl_enabled {
    include nginx::ssl
  }
  
  file { '/etc/nginx/sites-enabled/default':
    ensure => absent,
    notify => Service['nginx'],
  }
  
  $vhosts.each |Hash $vhost| {
    nginx::vhost { $vhost['name']:
      root => $vhost['root'],
      ssl  => $vhost['ssl'],
    }
  }
  
  service { 'nginx':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    require    => Package['nginx'],
  }
}
```
```puppet
# modules/nginx/manifests/ssl.pp
class nginx::ssl {
  
  file { '/etc/ssl/certs':
    ensure => directory,
  }
  
  file { '/etc/ssl/private':
    ensure => directory,
    mode   => '0755',
  }
  
  exec { 'generate-ssl-cert':
    command => 'openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx.key -out /etc/ssl/certs/nginx.crt -subj "/C=EE/O=ITS24/CN=$(hostname -f)"',
    creates => '/etc/ssl/certs/nginx.crt',
    path    => ['/usr/bin', '/bin'],
    require => File['/etc/ssl/private'],
  }
  
  file { '/etc/ssl/private/nginx.key':
    ensure  => file,
    mode    => '0600',
    require => Exec['generate-ssl-cert'],
  }
}
```
```puppet
# modules/nginx/manifests/vhost.pp
define nginx::vhost (
  String $root,
  Boolean $ssl = true,
) {
  
  file { $root:
    ensure => directory,
    owner  => 'www-data',
    mode   => '0755',
  }
  
  file { "${root}/index.html":
    ensure  => file,
    content => "<h1>${name}</h1><p>Managed by Puppet</p>",
    owner   => 'www-data',
  }
  
  file { "/etc/nginx/sites-available/${name}.conf":
    ensure  => file,
    content => epp('nginx/vhost.conf.epp', {
      'name' => $name,
      'root' => $root,
      'ssl'  => $ssl,
    }),
    notify  => Service['nginx'],
  }
  
  file { "/etc/nginx/sites-enabled/${name}.conf":
    ensure => link,
    target => "/etc/nginx/sites-available/${name}.conf",
    notify => Service['nginx'],
  }
}
```

### PostgreSQL module
```puppet
# modules/postgresql/manifests/init.pp
class postgresql (
  String $version = '12',
  Array[Hash] $databases = [],
  Array[Hash] $users = [],
) {
  
  package { ['postgresql', 'postgresql-contrib']:
    ensure => installed,
  }
  
  service { 'postgresql':
    ensure  => running,
    enable  => true,
    require => Package['postgresql'],
  }
  
  $databases.each |Hash $db| {
    postgresql::database { $db['name']:
      require => Service['postgresql'],
    }
  }
  
  $users.each |Hash $user| {
    postgresql::user { $user['name']:
      password => $user['password'],
      database => $user['db'],
      require  => Postgresql::Database[$user['db']],
    }
  }
}
```

### Monitoring module
```puppet
# modules/monitoring/manifests/init.pp
class monitoring (
  String $interval = '*/5',
) {
  
  file { '/usr/local/bin/health-check.sh':
    ensure  => file,
    mode    => '0755',
    content => epp('monitoring/health-check.sh.epp'),
  }
  
  cron { 'health-check':
    command => '/usr/local/bin/health-check.sh >> /var/log/health-check.log 2>&1',
    minute  => $interval,
    require => File['/usr/local/bin/health-check.sh'],
  }
}
```

### Site manifest
```puppet
# manifests/site.pp
node 'puppet-test' {
  
  class { 'nginx':
    ssl_enabled => true,
    vhosts      => [
      {
        'name' => 'test.local',
        'root' => '/var/www/test',
        'ssl'  => true,
      },
      {
        'name' => 'demo.local',
        'root' => '/var/www/demo',
        'ssl'  => true,
      },
    ],
  }
  
  class { 'postgresql':
    version   => '12',
    databases => [
      { 'name' => 'webapp' },
    ],
    users     => [
      {
        'name'     => 'webuser',
        'password' => 'changeme123',
        'db'       => 'webapp',
      },
    ],
  }
  
  class { 'monitoring':
    interval => '*/5',
  }
}
```

### Puppet apply
```bash
cd vagrant && vagrant up puppet
vagrant ssh puppet

# Puppet VM'is
sudo puppet module install puppetlabs-postgresql --version 6.0.0
sudo puppet apply --modulepath=/vagrant/puppet/modules /vagrant/puppet/manifests/site.pp
```

Validation:
```bash
systemctl status nginx postgresql
curl -k https://localhost
cat /var/log/health-check.log
```

Commit:
```bash
git add puppet/
git commit -m "Complete Puppet implementation with nginx, postgresql, monitoring"
```

## 5. Võrdlev Analüüs

Looge COMPARISON.md fail, mis dokumenteerib põhjaliku võrdluse. See on projekti kõige olulisem osa - näitab et mõistate mitte ainult kuidas, vaid miks.
```markdown
# Ansible vs Puppet: Detailed Comparison

## Architecture Comparison

### Ansible (Push-based)
- Control node SSH'ib target'itele
- Agentless - ainult Python vajalik target'il
- Sequential execution (default)
- Immediate changes

### Puppet (Pull-based)
- Agent küsib config'i serverilt (meie projektis masterless)
- Agent daemon töötab target'is
- Catalog compilation on server side
- Periodic convergence

## Syntax Comparison

### Ansible (YAML + Jinja2)
```yaml
- name: "Install nginx"
  apt:
    name: nginx
    state: present
```

Plussid:
- YAML on intuitiivne
- Jinja2 on võimas templating
- Procedural ja declarative mix

Miinused:
- YAML indentation errors
- Loops ja conditionals võivad olla verbose

### Puppet (DSL - Domain Specific Language)
```puppet
package { 'nginx':
  ensure => installed,
}
```

Plussid:
- Puhtalt declarative
- Type system on range
- Resource dependencies on explicit

Miinused:
- DSL süntaks on unikaalne
- Steep learning curve
- Ruby knowledge helps but not required

## Development Experience

### Ansible
- Kiirem arendus väikestele projektidele
- Debugging on lihtne --verbose flagidega
- Lokaalne testimine on straightforward
- Ad-hoc tasks on lihtsad

### Puppet
- Aeglasem algne setup
- Catalog compilation errors võivad olla cryptic
- Rspec-puppet testimine on võimas
- Resource relationships nõuavad planeerimist

## Performance

### Ansible
- SSH overhead iga connection kohta
- Parallelization võimalik (forks)
- Idempotence checks võivad olla slow
- Good: <100 nodes

### Puppet
- Agent cache minimeerib network traffic
- Catalog compilation on intensive
- Resources puhtalt declarative
- Scales: 1000+ nodes

## Use Case Recommendations

### Kasuta Ansible kui:
- Väike infrastruktuur (<50 nodes)
- Kiired deployment'id vajalikud
- Team on suured Python/YAML kogemusega
- Ad-hoc management on priority
- Cloud provisioning + config management

### Kasuta Puppet kui:
- Suur infrastruktuur (100+ nodes)
- Strong compliance requirements
- Complex resource dependencies
- Team on Ruby background
- Long-term configuration drift prevention

## Personal Reflection

[Sinu kogemus selle projektiga - mida õppisid, mis oli raske, mis oli huvitav]

## Conclusion

Mõlemad tööriistad on võimekad. Valik sõltub:
- Infrastruktuuri suurusest
- Team skill set'ist
- Workflow preferences (push vs pull)
- Existing tooling ecosystem

Ansible võidab lihtsuses ja kiiruses.
Puppet võidab scale'is ja robustsuses.
```

## Esitamine

### Repositooriumi viimistlemine

Veenduge et repositoorium sisaldab:
```
ansible-puppet-comparison/
├── README.md                    # Projekti ülevaade, setup juhend
├── COMPARISON.md                # Detailne võrdlus
├── ansible/
│   ├── inventory/
│   ├── group_vars/
│   ├── roles/
│   │   ├── nginx/
│   │   ├── postgresql/
│   │   └── monitoring/
│   └── site.yml
├── puppet/
│   ├── manifests/
│   │   └── site.pp
│   └── modules/
│       ├── nginx/
│       ├── postgresql/
│       └── monitoring/
└── vagrant/
    └── Vagrantfile
```

### Kontrollnimekiri

- [ ] Mõlemad lahendused (Ansible ja Puppet) on valmis
- [ ] Nginx töötab mõlemas VM'is koos SSL'iga
- [ ] PostgreSQL on paigaldatud ja konfigureeritud
- [ ] Virtual hosts test.local ja demo.local töötavad
- [ ] Monitoring health checks käivituvad
- [ ] README.md sisaldab setup juhendeid
- [ ] COMPARISON.md sisaldab põhjalikku analüüsi
- [ ] Git commit history on clean ja descriptive
- [ ] Repository on avalik GitHubis

### GitHub esitamine
```bash
# Create GitHub repo (via web interface)

git remote add origin https://github.com/yourusername/ansible-puppet-comparison.git
git branch -M main
git push -u origin main
```

## Refleksioon

Lisa README.md lõppu "## Reflection" peatükk ja vasta jäsugmistele küsimustele (2-3 lauset iga küsimuse kohta):

### Milline tööriist oli sulle mugavam (Ansible või Puppet) ja miks?

Näide: "Ansible oli mulle mugavam, sest YAML süntaks oli tuttav Dockerist ja Jinja2 template'd meenutasid Flask'i. Puppet DSL oli esialgu segaduses, eriti resource dependencies define'imine."

### Mis oli kõige suurem erinevus Ansible ja Puppet vahel?

Näide:
- "Push vs pull arhitektuur. Ansible'is sa kontrolid millal muudatused juhtuvad, Puppet'is agent otsustab. See muutis debugging'i
- Ansible'is näed kohe tulemust, Puppet'is pead ootama agent run'i."

### Millises olukorras kasutaksid Ansible'i ja millises Puppet'it?

Näide:
- "Ansible väikestele projektidele ja one-off deployment'idele. Puppet kui mul oleks 100+ serverit ja vaja compliance monitoring'u. Näiteks startup
- Ansible. Enterprise banking
- Puppet."

### Mis oli selle projekti juures kõige raskem ja kuidas sa selle lahendasid?

Näide: "Puppet resource dependencies olid keerulised. Näiteks nginx virtual host vajas SSL cert'i, mis vajas directory't. Otsisin Puppet docs'ist resource ordering ja kasutasin require attribute'e. Trial-and-error koos puppet apply --debug flag'iga aitas."

### Mis oli selle projekti juures kõige huvitavam või lõbusam osa?

Näide:
- "Kõige ägedam oli näha sama tulemust kahel erineval viisil. Nagu lahendada matemaatikaülesanne algebraliselt vs geomeetriliselt
- vastus sama, lähenemine erinev. Sain aru miks DevOps tööriistad pole 'one size fits all'."

## Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| Ansible implementatsioon | 25% | Nginx, PostgreSQL, monitoring töötavad; rollid struktureeritud |
| Puppet implementatsioon | 25% | Nginx, PostgreSQL, monitoring töötavad; moodulid struktureeritud |
| Võrdlev analüüs | 20% | COMPARISON.md on põhjalik, sisaldab code näiteid, use case soovitusi |
| Dokumentatsioon | 15% | README.md selge setup juhendiga, commit messages kirjeldavad muudatusi |
| Koodiqualiteet | 10% | Idempotence, DRY principle, proper variable usage |
| Refleksioon | 5% | 5 küsimust vastatud, näitab mõistmist, isiklik perspective |

**Kokku: 100%**

## Boonus

Valikulised täiendused (kuni +15%):

### Docker Deployment (+5%)
Käivita mõlemad lahendused Docker container'ites, mitte Vagrant VM'ides. Näitab container automation'i oskust.

### CI/CD Pipeline (+5%)
Lisa GitHub Actions, mis testib mõlemat lahendust pull request'i kohta. Automaatne validation.

### Performance Benchmark (+5%)
Mõõda deployment aega, resource usage, network traffic. Loo comparison chart.

### Multi-Environment Support (+3%)
Lisa dev/staging/prod environment tugi. Näita kuidas environment-specific variables töötavad.

### Advanced Monitoring (+2%)
Lisa Prometheus või Grafana. Real-time metrics collection.

---

Edu ja head automatiseerimist! See projekt õpetab tegelikke skills'e, mida kasutate DevOps töös.