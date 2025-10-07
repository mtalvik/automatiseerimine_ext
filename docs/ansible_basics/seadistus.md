# Vagrant Seadistusjuhend Ansible Laboriks

See juhend aitab seadistada Vagrant-põhise labikeskkonna Ansible harjutusteks. Loote kaks virtuaalmasinat - ühe control node'iks ja teise target serveriks. Kogu protsess võtab umbes 15-20 minutit.

**Nõuded:** VirtualBox 6.1+, Vagrant 2.3+, 4GB vaba RAM-i

---

## Mis on Vagrant?

Vagrant on tööriist virtuaalmasinate haldamiseks läbi käsurea. See loeb Vagrantfile nimelist konfiguratsioonifaili ja loob automaatselt VM-id VirtualBoxi. Erinevalt käsitsi VM-ide loomisest on Vagrant:
- Kiirem (1 käsk vs 10 minutit hiireklõpsamist)
- Kordav (sama setup iga kord)
- Jagamist toetav (Vagrantfile on tekstifail, pane GitHubi)

---

## 1. Tarkvara paigaldamine

### Windows```powershell
# Paigalda VirtualBox
winget install Oracle.VirtualBox

# Paigalda Vagrant
winget install Hashicorp.Vagrant

# OLULINE: Taaskäivita Windows pärast installimist```

Alternatiiv - käsitsi allalaadimine:
- VirtualBox: https://virtualbox.org/wiki/Downloads
- Vagrant: https://developer.hashicorp.com/vagrant/downloads

### macOS```bash
# Paigalda Homebrew kui pole veel
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Paigalda VirtualBox ja Vagrant
brew install --cask virtualbox
brew install --cask vagrant```

### Linux (Ubuntu/Debian)```bash
# VirtualBox
sudo apt update
sudo apt install virtualbox -y

# Vagrant
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install vagrant -y```

### Kontrollimine```bash
# Kontrolli versioone
VBoxManage --version
# Peaks näitama: 7.0.x või 6.1.x

vagrant --version
# Peaks näitama: Vagrant 2.3.x või uuem```

---

## 2. Projekti seadistamine

### 2.1. Projekti kausta loomine```bash
# Loo projekti kaust
mkdir ansible-lab
cd ansible-lab```

### 2.2. Vagrantfile allalaadimine

Laadige alla `Vagrantfile` projektikursuse repositooriumist või looge see käsitsi. Vagrantfile peab olema täpselt projekti juurkaustas koos nimega `Vagrantfile` (ilma laiendita).

Vagrantfile seadistab:
- 2 Ubuntu 22.04 VM-i
- Controller: 192.168.56.10 (Ansible installitud)
- Web Server: 192.168.56.11 (target server)
- Ansible kasutaja mõlemas VM-is (parool: ansible123)
- Passwordless sudo
- SSH parooliga autentimine (initial setup jaoks)

### 2.3. Projekti struktuuri kontrollimine```bash
# Kontrolli et Vagrantfile on olemas
ls -la

# Peaks nägema:
# Vagrantfile```

---

## 3. VM-ide käivitamine

### 3.1. Esimene käivitamine

Esimene käivitamine võtab 5-10 minutit, sest Vagrant peab alla laadima Ubuntu base image (umbes 700MB) ja provisioning'i teostama.```bash
# Käivita mõlemad VM-id
vagrant up

# Näed väljundit:
# Bringing machine 'controller' up with 'virtualbox' provider...
# Bringing machine 'webserver' up with 'virtualbox' provider...
# ==> controller: Importing base box 'ubuntu/jammy64'...
# ...
# Controller ready! IP: 192.168.56.10
# Web server ready! IP: 192.168.56.11```

### 3.2. Staatuse kontrollimine```bash
# Kontrolli VM-ide staatust
vagrant status

# Väljund:
# Current machine states:
# controller                running (virtualbox)
# webserver                 running (virtualbox)```

---

## 4. VM-idega ühenduse loomine

### 4.1. Vagrant SSH abil

Kõige lihtsam viis on kasutada Vagrant sisseehitatud SSH-d:```bash
# Ühenda controller'iga
vagrant ssh controller

# Näed:
# Welcome to Ubuntu 22.04.x LTS
# ansible@ansible-controller:~$```

Teises terminaliaknas:```bash
# Ühenda webserver'iga
vagrant ssh webserver

# Näed:
# ansible@web-server:~$```

### 4.2. SSH kliendi abil

Alternatiivina saate kasutada tavalist SSH klienti (PuTTY, OpenSSH):```bash
# Controller
ssh ansible@192.168.56.10
# Parool: ansible123

# Web server
ssh ansible@192.168.56.11
# Parool: ansible123```

### 4.3. Kasutajad

Mõlemas VM-is on kaks kasutajat:

| Kasutaja | Parool | Kirjeldus |
|----------|--------|-----------|
| vagrant | vagrant | Vagrant default kasutaja, `vagrant ssh` kasutab seda |
| ansible | ansible123 | Meie loodud kasutaja Ansible harjutusteks |

---

## 5. Ansible labori alustamine

### 5.1. SSH võtmete seadistamine

Controller VM-is, ansible kasutajana:```bash
# Ühenda controller'iga
vagrant ssh controller

# Vaheta ansible kasutajale (kui vagrant kasutajana sisse logitud)
sudo su - ansible

# Kontrolli kes sa oled
whoami
# Peaks näitama: ansible

# Genereeri SSH võtmepaar
ssh-keygen -t ed25519
# Vajuta Enter kolm korda (vaikeväärtused)

# Kopeeri võti webserver'isse
ssh-copy-id ansible@192.168.56.11
# Sisesta parool: ansible123

# Testi ühendust (ei tohiks parooli küsida)
ssh ansible@192.168.56.11
# Kui õnnestus, oled webserver'is
hostname
# Peaks näitama: web-server
exit```

### 5.2. Inventory faili loomine```bash
# Controller VM-is, ansible kasutajana
cd ~
mkdir ansible_tutorial
cd ansible_tutorial

# Loo inventory fail
cat > inventory.ini << 'EOF'
[control]
localhost ansible_connection=local

[webservers]
web1 ansible_host=192.168.56.11 ansible_user=ansible

[all:children]
control
webservers
EOF

# Kontrolli faili
cat inventory.ini```

### 5.3. Esimene Ansible test```bash
# Testi ühendust kõigi serveritega
ansible -i inventory.ini all -m ping

# Peaks nägema:
# localhost | SUCCESS => {
#     "changed": false,
#     "ping": "pong"
# }
# web1 | SUCCESS => {
#     "changed": false,
#     "ping": "pong"
# }```

Kui näete SUCCESS mõlemal serveril, on Ansible korrektselt seadistatud!

---

## 6. Failide jagamine

Teie projekti kaust (kus Vagrantfile asub) on automaatselt jagatud mõlemasse VM-i kausta `/vagrant`.

### Windows/macOS/Linux```bash
# Teie hostis (Windows/macOS/Linux)
cd ansible-lab
echo "test content" > shared-file.txt

# VM-is (vagrant ssh controller)
ls /vagrant/
# Näed: shared-file.txt Vagrantfile

# Kopeeri fail ansible kasutaja kausta
cp /vagrant/shared-file.txt ~/```

See on kasulik:
- Playbook'ide kirjutamiseks host masinas (IDE/teksteditor)
- Failide jagamiseks VM-ide vahel
- Backup'ide tegemiseks

---

## 7. Vagrant põhikäsud

### Käivitamine ja peatamine```bash
# Käivita mõlemad VM-id
vagrant up

# Käivita ainult üks VM
vagrant up controller
vagrant up webserver

# Peata VM-id (RAM vabastatakse)
vagrant halt

# Taaskäivita VM-id
vagrant reload

# Taaskäivita koos provisioning'iga (kui muutsid Vagrantfile)
vagrant reload --provision```

### Staatuse ja info```bash
# Vaata VM-ide staatust
vagrant status

# Vaata SSH konfiguratsiooni
vagrant ssh-config

# Vaata VirtualBox GUI-s (optional)
VBoxManage list vms```

### Pause ja resume```bash
# Pause VM-id (suspend)
vagrant suspend

# Jätka VM-ide tööd
vagrant resume```

### Puhastamine```bash
# Kustuta VM-id täielikult (HOIATUS: kaob kõik andmed VM-ides!)
vagrant destroy

# Kustuta ainult üks VM
vagrant destroy controller

# Kustuta ilma kinnitust küsimata
vagrant destroy -f```

---

## 8. Kasulikud näpunäited

### Git Bash Windows'is

Windows kasutajad, installige Git Bash parem terminali kogemus saamiseks:
- Allalaadimine: https://git-scm.com/download/win
- Git Bash annab Unix-stiilis käsud Windows'is

### Windows Terminal

Windows 11 kasutajad, kasutage Windows Terminal mitme tab'i jaoks:```powershell
# Installi Windows Terminal
winget install Microsoft.WindowsTerminal```

### VS Code Remote SSH

VS Code saab otse VM-iga ühenduda:

1. Installi VS Code extension: "Remote - SSH"
2. Vajuta F1 ja vali "Remote-SSH: Connect to Host"
3. Sisesta: `ansible@192.168.56.10`
4. Parool: `ansible123`

Nüüd saad editeerida faile VM-is otse VS Code'is!

### Snapshot'id

Salvesta VM-i olek enne eksperimenteerimist:```bash
# Loo snapshot
vagrant snapshot save controller before-experiment

# Taasta snapshot kui midagi katki läks
vagrant snapshot restore controller before-experiment

# Vaata snapshot'ide nimekirja
vagrant snapshot list

# Kustuta snapshot
vagrant snapshot delete controller before-experiment```

---

## 9. Troubleshooting

### VirtualBox konflikt Hyper-V'ga (Windows)

Kui saad vea "VirtualBox can't operate in Hyper-V mode":```powershell
# Käivita PowerShell administraatorina
bcdedit /set hypervisorlaunchtype off

# Taaskäivita Windows
# Pärast taaskäivitamist proovi uuesti
vagrant up```

### VM ei käivitu```bash
# Kontrolli VirtualBox staatust
VBoxManage list vms
VBoxManage list runningvms

# Kustuta ja loo uuesti
vagrant destroy -f
vagrant up```

### SSH ühenduse probleemid```bash
# Vaata SSH konfiguratsiooni
vagrant ssh-config

# Kopeeri SSH config faili ja proovi
vagrant ssh-config > ssh-config
ssh -F ssh-config controller

# Kui ikka ei tööta, regenereri SSH võtmed
ssh-keygen -R 192.168.56.10
ssh-keygen -R 192.168.56.11```

### Võrgu probleemid

Kui IP aadressid ei tööta:```bash
# Kontrolli VirtualBox network adapter'it
VBoxManage list hostonlyifs

# Kui puudub, loo
VBoxManage hostonlyif create

# Vagrantfile'is proovi teist IP range'i
# Muuda: 192.168.56.x -> 192.168.33.x```

### Provisioning ebaõnnestub```bash
# Käivita provisioning uuesti
vagrant provision

# VÕI reload koos provisioning'iga
vagrant reload --provision

# Kontrolli VM-is käsitsi
vagrant ssh controller
sudo apt update
sudo apt install ansible -y```

### Windows Firewall

Windows võib blokeerida ühendusi. Lisa erand:
1. Control Panel → Windows Defender Firewall
2. Advanced Settings → Inbound Rules → New Rule
3. Port → TCP → 22, 192.168.56.0/24

---

## 10. Puhastamine pärast labori

### Ajutine peatamine

Kui soovid jätkata hiljem:```bash
# Peata VM-id
vagrant halt

# Järgmisel korral käivita uuesti
vagrant up```

### Andmete salvestamine

Salvesta oma töö enne VM-ide kustutamist:```bash
# Controller VM-is
cd ~/ansible_tutorial
tar -czf ansible_work.tar.gz .

# Kopeeri /vagrant kausta (jagatud kaust)
cp ansible_work.tar.gz /vagrant/

# Nüüd fail on ka teie host masinas ansible-lab kaustas```

### Täielik puhastamine```bash
# Kustuta VM-id
vagrant destroy -f

# Kustuta allalaaditud box
vagrant box remove ubuntu/jammy64

# Kustuta projekti kaust (optional)
cd ..
rm -rf ansible-lab```

---

## 11. VM-ide detailid

| VM | Hostname | IP | RAM | CPU | Eesmärk |
|----|----------|-----|-----|-----|---------|
| Controller | ansible-controller | 192.168.56.10 | 1GB | 1 | Ansible control node |
| Web Server | web-server | 192.168.56.11 | 1GB | 1 | Target server |

Mõlemad:
- OS: Ubuntu 22.04 LTS (Jammy)
- Kasutajad: vagrant/vagrant, ansible/ansible123
- Sudo: passwordless
- SSH: parooliga autentimine lubatud

---

## 12. Järgmised sammud

1. Jätkake Ansible labori harjutustega
2. Looge oma playbook'e `/vagrant` kaustas (jagatud kaust)
3. Eksperimenteerige vabalt - saate alati `vagrant destroy` ja `vagrant up` teha
4. Kasutage snapshot'e vigade korral kiireks taastamiseks

Edu Ansible õppimisega!