# Git Labor

**Eeldused:** VirtualBox, Vagrant, VS Code  
**Platvorm:** Ubuntu VM, Git, GitHub  
**Kestus:** ~3 tundi

## Õpiväljundid

Pärast laborit oskate:

1. **Seadistada** Vagrant VM ja ühendada VS Code'iga
2. **Konfigureerida** Git keskkonda ja teha commit'e
3. **Hallata** branch'e, merge'ida ja lahendada konflikte
4. **Ühendada** GitHub'iga läbi SSH
5. **Rakendada** Pull Request workflow'i

---

## 1. Vagrant VM Seadistamine

> Teeme KÕIK Git töö Ubuntu VM-is. Host masinas Git'i ei paigalda.

### 1.1 Kontrolli Eeldused (Windows)

```powershell
vagrant --version
VBoxManage --version
code --version
```

Kui midagi puudub, paigalda enne jätkamist.

### 1.2 Loo Vagrantfile

Loo projektikaust:

```bash
mkdir git-labor-vm
cd git-labor-vm
```

Loo fail `Vagrantfile` (vali ÜKS variant):

**Variant A: Üks VM (piisav Git laboriks)**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  
  config.vm.define "controller" do |c|
    c.vm.hostname = "controller"
    c.vm.network "private_network", ip: "192.168.56.10"
  end
end
```

**Variant B: Kolm VM-i (Ansible/Automation laboriks)**

```ruby
Vagrant.configure("2") do |config|
  config.vm.define "gitlab" do |vm|
    vm.box = "generic/ubuntu2204"
    vm.hostname = "gitlab"
    
    vm.network "public_network"
    vm.network "private_network", ip: "10.11.12.21", virtualbox__intnet: "git_lab"
    
    vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "1024"]
      vb.customize ["modifyvm", :id, "--cpus", "1"]
      vb.name = "GIT-LAB"
    end
    
    vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y git
    SHELL
  end
end
```

**Git laboriks piisab Variant A.**

### 1.3 Käivita VM

```bash
vagrant up
vagrant status
```

Kontrolli SSH parameetreid:

```bash
vagrant ssh-config
```

Salvesta väljund - vajad VS Code ühenduseks.

### 1.4 Ühenda VS Code Remote-SSH

**Samm 1: Lisa SSH Config**

VS Code: `Ctrl+Shift+P` → `Remote-SSH: Open SSH Configuration File`

Vali esimene fail (`C:\Users\SINUNIMI\.ssh\config`)

Lisa (võta `Port` ja `IdentityFile` väärtused `vagrant ssh-config` väljundist):

```sshconfig
Host controller
    HostName 127.0.0.1
    Port 2222
    User vagrant
    IdentityFile C:/path/to/git-labor-vm/.vagrant/machines/controller/virtualbox/private_key
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```

Salvesta (`Ctrl+S`)

**Samm 2: Ühenda**

`Ctrl+Shift+P` → `Remote-SSH: Connect to Host` → vali `controller`

Vali platform: `Linux`

**Samm 3: Ava Kaust**

Open Folder → vali `/vagrant` (jagatud kaust) või `/home/vagrant`

**Kontrolli:** VS Code vasakul all nurgas: `SSH: controller`

---

## 2. Git Seadistamine VM-is

> Kõik järgnevad käsud: VS Code terminal (ühendatud VM-iga)

### 2.1 Kontrolli Git

```bash
git --version
```

Kui puudub:

```bash
sudo apt update
sudo apt install -y git
```

### 2.2 Konfigureeri Kasutajainfo

```bash
git config --global user.name "Sinu Nimi"
git config --global user.email "sinu.email@example.com"
git config --global core.editor "code --wait"
```

Kontrolli:

```bash
git config --list | grep user
```

Peaksid nägema:
```
user.name=Sinu Nimi
user.email=sinu.email@example.com
```

### 2.3 GitHub Konto (kui puudub)

1. Mine `https://github.com` → Sign up
2. Kinnita e-post
3. Settings → Password and authentication → Lülita sisse 2FA

### Kontrollnimekiri

- [ ] `git --version` töötab VM-is
- [ ] `git config user.name` näitab sinu nime
- [ ] GitHub konto olemas

---

## 3. Esimene Repositoorium

### 3.1 Loo Repo

```bash
mkdir git-labor
cd git-labor
git init
```

Väljund:
```
Initialized empty Git repository in /home/vagrant/git-labor/.git/
```

### 3.2 Loo README ja Commit

```bash
echo "# Git Labor Projekt" > README.md
echo "See on minu esimene Git repositoorium." >> README.md

git status
```

Lisa ja commit:

```bash
git add README.md
git commit -m "Esimene commit: lisa README"
```

Vaata ajalugu:

```bash
git log --oneline
```

### 3.3 Lisa Failid

Loo Python fail:

```bash
cat > hello.py << 'EOF'
def greet(name):
    return f"Tere, {name}!"

if __name__ == "__main__":
    print(greet("Git"))
EOF
```

Loo kalkulaator:

```bash
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
EOF
```

Lisa ja commit korraga:

```bash
git add .
git commit -m "Lisa Python skriptid"
```

### Kontrollnimekiri

- [ ] Vähemalt 2 commit'i tehtud
- [ ] `git status` näitab "working tree clean"
- [ ] `git log --oneline` näitab ajalugu

---

## 4. .gitignore

### 4.1 Loo Probleemsed Failid

```bash
echo "Error log" > debug.log
mkdir __pycache__
touch __pycache__/test.pyc
cat > .env << 'EOF'
API_KEY=secret123
DATABASE_URL=postgresql://localhost/db
EOF
```

### 4.2 Loo .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtuaalsed keskkonnad
venv/
env/

# IDE
.vscode/
.idea/

# Keskkonna muutujad
.env
.env.local

# Logid
*.log

# OS failid
.DS_Store
Thumbs.db
EOF
```

Kontrolli:

```bash
git status
```

Näed ainult `.gitignore` - teised failid on ignoreeritud!

Commit:

```bash
git add .gitignore
git commit -m "Lisa .gitignore"
```

### Kontrollnimekiri

- [ ] `.gitignore` loodud
- [ ] `.env` ei ilmu `git status` väljundis

---

## 5. Branch'id

### 5.1 Loo Branch

```bash
git branch feature/string-utils
git checkout feature/string-utils
```

Või lühemalt:

```bash
git checkout -b feature/math-operations
```

### 5.2 Tööta Branch'is

Oled `feature/math-operations` branch'is:

```bash
cat >> calculator.py << 'EOF'

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b
EOF
```

Commit:

```bash
git add calculator.py
git commit -m "Lisa korrutamine ja jagamine"
```

### 5.3 Vaheta Branch

```bash
git checkout main
```

Kontrolli - `calculator.py` muudatusi pole siin näha!

### 5.4 Teine Branch

```bash
git checkout -b feature/string-utils
```

Loo uus fail:

```bash
cat > string_utils.py << 'EOF'
def reverse(text):
    return text[::-1]

def count_words(text):
    return len(text.split())

if __name__ == "__main__":
    print(reverse("tere"))
EOF
```

Commit:

```bash
git add string_utils.py
git commit -m "Lisa string utils"
```

Vaata branch'e:

```bash
git log --oneline --graph --all
```

### Kontrollnimekiri

- [ ] Lõid vähemalt 2 branch'i
- [ ] Tegid commit'e branch'ides
- [ ] `git branch` näitab kõiki branch'e

---

## 6. Merge

### 6.1 Fast-Forward Merge

```bash
git checkout main
git merge feature/string-utils
```

Väljund: "Fast-forward"

Kontrolli:

```bash
ls -la
```

`string_utils.py` on nüüd main'is!

### 6.2 Three-Way Merge

```bash
git merge feature/math-operations
```

Git avab editori - salvesta ja sulge.

Väljund: "Merge made by the 'recursive' strategy"

### 6.3 Kustuta Branch'id

```bash
git branch -d feature/string-utils
git branch -d feature/math-operations
```

Kontrolli:

```bash
git branch
```

### Kontrollnimekiri

- [ ] Merge'isid mõlemad branch'id
- [ ] Branch'id kustutatud
- [ ] Main'is on mõlema branch'i kood

---

## 7. Konfliktid

### 7.1 Loo Konflikt

Branch 1:

```bash
git checkout -b fix/greeting-estonian
cat > hello.py << 'EOF'
def greet(name):
    return f"Tere, {name}! Kuidas läheb?"

if __name__ == "__main__":
    print(greet("Git"))
EOF
git add hello.py
git commit -m "Lisa pikem tervitus eesti keeles"
```

Branch 2 (main):

```bash
git checkout main
cat > hello.py << 'EOF'
def greet(name):
    return f"Hello, {name}! Welcome!"

if __name__ == "__main__":
    print(greet("Git"))
EOF
git add hello.py
git commit -m "Muuda tervitus inglise keeleks"
```

Merge - konflikt:

```bash
git merge fix/greeting-estonian
```

Väljund: "CONFLICT (content): Merge conflict in hello.py"

### 7.2 Lahenda Konflikt

Vaata faili:

```bash
cat hello.py
```

Näed konfliktimärke:

```python
def greet(name):
<<<<<<< HEAD
    return f"Hello, {name}! Welcome!"
=======
    return f"Tere, {name}! Kuidas läheb?"
>>>>>>> fix/greeting-estonian

if __name__ == "__main__":
    print(greet("Git"))
```

Redigeeri faili - vali või kombineeri:

```bash
cat > hello.py << 'EOF'
def greet(name):
    """Tervitab mõlemas keeles."""
    return f"Tere / Hello, {name}!"

if __name__ == "__main__":
    print(greet("Git"))
EOF
```

Märgi lahendatuks ja lõpeta:

```bash
git add hello.py
git commit
```

Git avab editori - salvesta ja sulge.

### Kontrollnimekiri

- [ ] Lõid konflikti
- [ ] Lahendas käsitsi
- [ ] Merge lõpetatud

---

## 8. GitHub ja SSH

### 8.1 Loo SSH Võti VM-is

```bash
ssh-keygen -t ed25519 -C "sinu.email@example.com"
```

Vajuta Enter kõigile küsimustele.

Käivita SSH agent:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Kopeeri avalik võti:

```bash
cat ~/.ssh/id_ed25519.pub
```

Kopeeri väljund.

### 8.2 Lisa Võti GitHub'i

1. GitHub → Settings (paremal üleval)
2. SSH and GPG keys
3. New SSH key
4. Title: "VM controller"
5. Key: kleebi avalik võti
6. Add SSH key

Testi:

```bash
ssh -T git@github.com
```

Oodatav: "Hi KASUTAJANIMI! You've successfully authenticated..."

### 8.3 Loo GitHub Repo

1. GitHub → "+" → New repository
2. Name: `git-labor`
3. Jäta tühjaks (EI lisa README)
4. Create repository

### 8.4 Ühenda Remote

```bash
git remote add origin git@github.com:TEIE-KASUTAJANIMI/git-labor.git
git push -u origin main
```

Asenda `TEIE-KASUTAJANIMI` oma GitHub kasutajanimega.

Kontrolli:

```bash
git remote -v
```

### 8.5 Push ja Pull

Tee kohalik muudatus:

```bash
echo "" >> README.md
echo "## GitHub Integratsioon" >> README.md

git add README.md
git commit -m "Dokumenteeri GitHub"
git push
```

Tee muudatus GitHub'is (veebis):

1. Ava README.md
2. Edit (pliiats)
3. Lisa rida: "Muudatus GitHub'ist"
4. Commit changes

Pull muudatused:

```bash
git pull
cat README.md
```

### Kontrollnimekiri

- [ ] SSH võti seadistatud
- [ ] Remote lisatud
- [ ] Push töötab
- [ ] Pull töötab

---

## 9. Pull Requests

### 9.1 Loo Feature Branch

```bash
git checkout -b feature/documentation
```

Loo USAGE.md:

```bash
cat > USAGE.md << 'EOF'
# Kasutamisjuhend

## Skriptid

### hello.py
Tervitusprogramm kahes keeles.

```bash
python3 hello.py
```

### calculator.py
Matemaatilised operatsioonid.

```bash
python3 calculator.py
```

### string_utils.py
Stringide töötlemine.

```bash
python3 string_utils.py
```

## Arendamine

1. Loo branch: `git checkout -b feature/uus`
2. Tee muudatused
3. Commit: `git commit -m "Lisa uus funktsioon"`
4. Push: `git push origin feature/uus`
5. Tee Pull Request GitHub'is
EOF
```

Commit ja push:

```bash
git add USAGE.md
git commit -m "Lisa kasutamisjuhend"
git push -u origin feature/documentation
```

### 9.2 Tee Pull Request

GitHub (veeb):

1. Näed bänneri: "feature/documentation had recent pushes"
2. Compare & pull request
3. Title: "Lisa kasutamisjuhend"
4. Description:

```
## Muudatused
- Lisasin USAGE.md
- Dokumenteeritud kõik skriptid

## Kontroll
- [x] Testitud
- [x] Vormindatud
```

5. Create pull request

### 9.3 Merge PR

1. Vaata "Files changed"
2. Approve (enda PR puhul)
3. Merge pull request
4. Confirm merge
5. Delete branch

### 9.4 Uuenda Lokaalne Repo

```bash
git checkout main
git pull origin main
git branch -d feature/documentation
```

### Kontrollnimekiri

- [ ] Lõid PR
- [ ] Merge'isid GitHub'is
- [ ] Pull'isid muudatused
- [ ] Kustutad local branch

---

## Lõplik Kontrollnimekiri

- [ ] Vagrant VM töötab ja VS Code ühendatud
- [ ] Git konfigureeritud VM-is
- [ ] Vähemalt 5 commit'i
- [ ] .gitignore olemas
- [ ] 2+ branch'i loodud ja merge'itud
- [ ] Konflikt lahendatud
- [ ] SSH GitHub'iga seadistatud
- [ ] Remote push/pull töötab
- [ ] PR workflow läbi proovitud

---

## Troubleshooting

**SSH Permission Denied**

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
```

**Push Rejected**

```bash
git pull origin main
# Lahenda konfliktid
git push origin main
```

**Merge Abort**

```bash
git merge --abort
```

**Force Delete Branch**

```bash
git branch -D branch-name
```

---

## Esitamine

Enne esitamist:

1. Push kõik muudatused:

```bash
git status  # peab olema clean
git push --all origin
```

2. README algusesse lisa:

```markdown
# Git Labor Projekt

**Autor:** Sinu Nimi  
**Kuupäev:** 2025-XX-XX
```

3. Kontrolli GitHub'is - kõik failid peavad olemas olema
4. Esita Google Classroom'is link: `https://github.com/TEIE-KASUTAJANIMI/git-labor`
