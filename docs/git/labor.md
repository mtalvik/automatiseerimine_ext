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

### 1.2 Loo Vagrantfile

```bash
mkdir git-labor-vm
cd git-labor-vm
```

Loo fail `Vagrantfile`:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  
  config.vm.define "controller" do |c|
    c.vm.hostname = "controller"
    c.vm.network "private_network", ip: "192.168.56.10"
  end
end
```

### 1.3 Käivita VM

```bash
vagrant up
vagrant status
```

### 1.4 Loo SSH võti (Windows)

**PowerShell/CMD:**

```bash
ssh-keygen -t ed25519 -C "sinu@email.com"
```

- Fail: default Enter
- Passphrase: tühi Enter

**Saada võti VM-i:**

```bash
type C:\Users\SINUNIMI\.ssh\id_ed25519.pub | vagrant ssh -- "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"
```

Kui ei tööta:

```bash
vagrant upload C:\Users\SINUNIMI\.ssh\id_ed25519.pub /tmp/key.pub
vagrant ssh -c "mkdir -p ~/.ssh && cat /tmp/key.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"
```

### 1.5 VS Code Remote-SSH

`Ctrl+Shift+P` → `Remote-SSH: Open SSH Configuration File`

```sshconfig
Host controller
    HostName 127.0.0.1
    Port 2222
    User vagrant
    IdentityFile C:/Users/SINUNIMI/.ssh/id_ed25519
    StrictHostKeyChecking no
```

Ühenda: `Ctrl+Shift+P` → `Remote-SSH: Connect to Host` → `controller`

Platform: `Linux`

Open Folder → `/home/vagrant`

Kontrolli: VS Code vasakul all `SSH: controller`

---

## 2. Git Seadistamine VM-is

### 2.1 Kontrolli Git

```bash
git --version
```

Kui puudub:

```bash
sudo apt update
sudo apt install -y git
```

### 2.2 Konfigureeri

```bash
git config --global user.name "Sinu Nimi"
git config --global user.email "sinu.email@example.com"
git config --global core.editor "nano"
```

Kontrolli:

```bash
git config --list | grep user
```

### 2.3 GitHub Konto

1. `https://github.com` → Sign up
2. Kinnita e-post
3. Settings → 2FA

### Kontrollnimekiri

- [ ] `git --version` töötab
- [ ] `git config user.name` näitab nime
- [ ] GitHub konto olemas

---

## 3. Esimene Repositoorium

### 3.1 Loo Repo

```bash
mkdir git-labor
cd git-labor
git init
```

### 3.2 Loo README ja Commit

```bash
cat > README.md << 'EOF'
# Git Labor Projekt

See on minu esimene Git repositoorium.

## Eesmärk
Õppida Git põhitõdesid ja workflow'sid.
EOF

git status
git add README.md
git commit -m "Esimene commit: lisa README"
git log --oneline
```

### 3.3 Lisa Failid

Loo bash script:

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Tere, Git!"
EOF

chmod +x hello.sh
```

Loo tekstifail:

```bash
cat > notes.txt << 'EOF'
Git Labor Märkmed
=================

1. Git init - loo repo
2. Git add - lisa staged
3. Git commit - salvesta
EOF
```

Commit:

```bash
git add .
git commit -m "Lisa skriptid ja märkmed"
git log --oneline --graph
```

### Kontrollnimekiri

- [ ] Vähemalt 2 commit'i
- [ ] `git status` näitab "clean"
- [ ] `git log` näitab ajalugu

---

## 4. .gitignore

### 4.1 Loo Probleemsed Failid

```bash
echo "Error log" > debug.log
mkdir temp
touch temp/cache.tmp
cat > .env << 'EOF'
API_KEY=secret123
DATABASE_URL=postgresql://localhost/db
EOF
```

### 4.2 Loo .gitignore

```bash
cat > .gitignore << 'EOF'
# Logid
*.log

# Temp
temp/
*.tmp

# Secrets
.env
.env.local

# OS
.DS_Store
Thumbs.db
EOF
```

Kontrolli:

```bash
git status
```

Näed ainult `.gitignore`!

```bash
git add .gitignore
git commit -m "Lisa .gitignore"
```

### Kontrollnimekiri

- [ ] `.gitignore` loodud
- [ ] `.env` ignoreeritud

---

## 5. Branch'id

### 5.1 Loo Branch

```bash
git checkout -b feature/scripts
```

### 5.2 Tööta Branch'is

```bash
cat > backup.sh << 'EOF'
#!/bin/bash
echo "Backup started..."
tar -czf backup.tar.gz notes.txt
echo "Backup complete!"
EOF

chmod +x backup.sh

git add backup.sh
git commit -m "Lisa backup skript"
```

### 5.3 Vaheta Branch

```bash
git checkout main
ls -la
```

`backup.sh` puudub main'is!

### 5.4 Teine Branch

```bash
git checkout -b feature/docs
```

```bash
cat > INSTALL.md << 'EOF'
# Paigaldusjuhend

## Eeldused
- Git 2.0+
- Bash

## Sammud
1. Clone repo
2. Käivita skriptid
EOF

git add INSTALL.md
git commit -m "Lisa paigaldusjuhend"
```

Vaata branch'e:

```bash
git log --oneline --graph --all
```

### Kontrollnimekiri

- [ ] 2+ branch'i loodud
- [ ] Commit'id branch'ides
- [ ] `git branch` näitab kõiki

---

## 6. Merge

### 6.1 Fast-Forward Merge

```bash
git checkout main
git merge feature/docs
ls -la
```

`INSTALL.md` on nüüd main'is!

### 6.2 Three-Way Merge

```bash
git merge feature/scripts
```

Nano avaneb - salvesta `Ctrl+O`, sulge `Ctrl+X`.

### 6.3 Kustuta Branch'id

```bash
git branch -d feature/docs
git branch -d feature/scripts
git branch
```

### Kontrollnimekiri

- [ ] Merge'isid branch'id
- [ ] Branch'id kustutatud
- [ ] Main'is mõlema kood

---

## 7. Konfliktid

### 7.1 Loo Konflikt

Branch 1:

```bash
git checkout -b fix/greeting-estonian
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Tere, Git! Kuidas läheb?"
EOF

git add hello.sh
git commit -m "Lisa pikem tervitus eesti keeles"
```

Branch 2 (main):

```bash
git checkout main
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Hello, Git! Welcome!"
EOF

git add hello.sh
git commit -m "Muuda tervitus inglise keeleks"
```

Merge - konflikt:

```bash
git merge fix/greeting-estonian
```

Väljund: "CONFLICT (content): Merge conflict"

### 7.2 Lahenda Konflikt

```bash
cat hello.sh
```

Näed:

```bash
#!/bin/bash
<<<<<<< HEAD
echo "Hello, Git! Welcome!"
=======
echo "Tere, Git! Kuidas läheb?"
>>>>>>> fix/greeting-estonian
```

Redigeeri:

```bash
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Tere / Hello, Git!"
EOF
```

Lõpeta:

```bash
git add hello.sh
git commit
```

Nano - salvesta ja sulge.

### Kontrollnimekiri

- [ ] Konflikt loodud
- [ ] Lahendatud käsitsi
- [ ] Merge lõpetatud

---

## 8. GitHub ja SSH

### 8.1 SSH Võti VM-is

```bash
ssh-keygen -t ed25519 -C "sinu.email@example.com"
```

Enter kõigile.

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Kopeeri väljund.

### 8.2 Lisa GitHub'i

1. GitHub → Settings
2. SSH and GPG keys
3. New SSH key
4. Title: "VM controller"
5. Key: kleebi
6. Add SSH key

Testi:

```bash
ssh -T git@github.com
```

Oodatav: "Hi KASUTAJANIMI!..."

### 8.3 Loo GitHub Repo

1. GitHub → "+" → New repository
2. Name: `git-labor`
3. Jäta tühjaks
4. Create repository

### 8.4 Ühenda Remote

```bash
git remote add origin git@github.com:KASUTAJANIMI/git-labor.git
git push -u origin main
git remote -v
```

### 8.5 Push ja Pull

Kohalik muudatus:

```bash
echo "" >> README.md
echo "## GitHub Integratsioon" >> README.md

git add README.md
git commit -m "Dokumenteeri GitHub"
git push
```

GitHub'is (veebis):

1. Ava README.md
2. Edit
3. Lisa: "Muudatus GitHub'ist"
4. Commit changes

Pull:

```bash
git pull
cat README.md
```

### Kontrollnimekiri

- [ ] SSH seadistatud
- [ ] Remote lisatud
- [ ] Push töötab
- [ ] Pull töötab

---

## 9. Pull Requests

### 9.1 Loo Feature Branch

```bash
git checkout -b feature/documentation
```

```bash
cat > USAGE.md << 'EOF'
# Kasutamisjuhend

## Skriptid

### hello.sh
Tervitusprogramm.
```bash
./hello.sh
```

### backup.sh
Varundamine.
```bash
./backup.sh
```

## Arendamine

1. Loo branch: `git checkout -b feature/uus`
2. Tee muudatused
3. Commit: `git commit -m "Lisa uus"`
4. Push: `git push origin feature/uus`
5. Tee Pull Request
EOF

git add USAGE.md
git commit -m "Lisa kasutamisjuhend"
git push -u origin feature/documentation
```

### 9.2 Tee Pull Request

GitHub:

1. "feature/documentation had recent pushes"
2. Compare & pull request
3. Title: "Lisa kasutamisjuhend"
4. Description:

```
## Muudatused
- Lisasin USAGE.md
- Dokumenteeritud skriptid

## Kontroll
- [x] Testitud
- [x] Vormindatud
```

5. Create pull request

### 9.3 Merge PR

1. Files changed
2. Approve
3. Merge pull request
4. Confirm
5. Delete branch

### 9.4 Uuenda Lokaalne

```bash
git checkout main
git pull origin main
git branch -d feature/documentation
```

### Kontrollnimekiri

- [ ] PR loodud
- [ ] Merge'itud GitHub'is
- [ ] Pull'itud
- [ ] Local branch kustutatud

---

## Lõplik Kontrollnimekiri

- [ ] Vagrant VM töötab, VS Code ühendatud
- [ ] Git konfigureeritud
- [ ] 5+ commit'i
- [ ] .gitignore olemas
- [ ] 2+ branch'i merge'itud
- [ ] Konflikt lahendatud
- [ ] SSH GitHub'iga
- [ ] Remote push/pull töötab
- [ ] PR workflow tehtud

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

1. Push kõik:

```bash
git status
git push --all origin
```

2. README algusesse:

```markdown
# Git Labor Projekt

**Autor:** Sinu Nimi  
**Kuupäev:** 2025-XX-XX
```

3. Kontrolli GitHub'is
4. Esita link: `https://github.com/KASUTAJANIMI/git-labor`