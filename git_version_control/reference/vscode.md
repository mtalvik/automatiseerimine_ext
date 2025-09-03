# VS Code Seadistamise Juhend

## Mis on IDE (Integrated Development Environment)?

**IDE** on integreeritud arenduskeskkond - üks programm, mis sisaldab kõiki arendamiseks vajalikke tööriistu:

### Traditsiooniline vs IDE Töövoog

| Traditsioooniline | IDE (VS Code) |
|---|---|
| Notepad koodi kirjutamiseks | **Code Editor** - syntax highlighting |
| Command line kompileerimiseks | **Integrated Terminal** - käsud sama aknas |
| Eraldi FTP klient failide üleslaadimiseks | **Remote Extensions** - otseühendus |
| Git bash versioonihalduseks | **Source Control** - Git integreeritud |
| Veebilehtisja vigade otsimiseks | **Debugging** - breakpointid, watches |

### IDE vs Code Editor vs Text Editor

| Tüüp | Näited | Eelised | Puudused |
|---|---|---|---|
| **Text Editor** | Notepad, gedit | Kiire, lihtne | Pole programmeerimisfunktsioone |
| **Code Editor** | **VS Code**, Sublime | Kerge, laiendatav | Vajab seadistamist |
| **IDE** | IntelliJ, Eclipse | Kõik kaasas | Raske, aeglane |

**VS Code on hübriid** - Code Editor, mida saab laienduste abil IDE-ks muuta!

### Miks VS Code DevOps-ile?
- **Kerge ja kiire** - käivitub sekundiga
- **Laiendatav** - lisa ainult see, mida vajad
- **Multi-language** - Python, YAML, JSON, Bash, Dockerfile
- **Remote-first** - loodud serveritega töötamiseks
- **Git-centered** - versioonihaldus on süvuti integreeritud

## 1. VS Code Installimine

### Windows
```powershell
winget install Microsoft.VisualStudioCode
```
Või lae alla: https://code.visualstudio.com

### macOS
```bash
brew install --cask visual-studio-code
```

### Linux (Ubuntu/Debian)
```bash
sudo snap install code --classic
```

## 2. Vajalikud Laiendused

### Laienduste Allikad
- **VS Code sisene**: `Ctrl+Shift+X` - põhiline viis
- **VS Marketplace**: https://marketplace.visualstudio.com/ - brauseris sirvimine
- **Teemade galerii**: https://vscodethemes.com/ - visuaalsete teemade sirvimine
- **Command line**: `code --install-extension publisher.name`

### Installimisvõimalused

| Meetod | Kuidas kasutada | Millal kasutada | Näide |
|---|---|---|---|
| **VS Code GUI** | `Ctrl+Shift+X` → otsi → Install | Tavakasutus | Otsi "Prettier" |
| **Marketplace veeb** | Sirvi → Install → ava VS Code | Laienduste uurimine | marketplace.visualstudio.com |
| **Teemade galerii** | Vali teema → Install → ava VS Code | Visuaalse disaini valik | vscodethemes.com |
| **Command line** | `code --install-extension ms-vscode-remote.remote-ssh` | Automiseering, skriptid | Bulk install |
| **VSIX fail** | Download .vsix → Install from VSIX | Erilaiendused, beta versioonid | .vsix local install |

### Teemade Installimine
1. Mine https://vscodethemes.com/
2. Sirvi visuaalselt erinevaid teemasid (Dark, Light, High Contrast)
3. Kliki **Install** → avaneb VS Code
4. Teema aktiveeritakse automaatselt

### Minu lemmikud laiendused

Ava VS Code → Vajuta `Ctrl+Shift+X` → Paigalda järgmised:

| Laienduse nimi | Autor | Otsingusõna | Marketplace ID | Kasutus |
|---|---|---|---|---|
| Remote - SSH | Microsoft | "Remote - SSH" | `ms-vscode-remote.remote-ssh` | Serveritega töötamiseks |
| Remote Explorer | Microsoft | "Remote Explorer" | `ms-vscode.remote-explorer` | Remote ühenduste haldamiseks |
| Prettier - Code formatter | Prettier | "Prettier" | `esbenp.prettier-vscode` | Koodi automaatseks formateerimiseks |
| GitHub Actions | GitHub | "GitHub Actions" | `github.vscode-github-actions` | CI/CD töövoogluste jaoks |
| GitHub Codespaces | GitHub | "GitHub Codespaces" | `github.codespaces` | Pilve arenduskeskkonnaks |
| indent-rainbow | oderwat | "indent-rainbow" | `oderwat.indent-rainbow` | Taanduste visualiseerimiseks (YAML!) |

### Marketplace Kasutamine
1. Mine https://marketplace.visualstudio.com/
2. Otsi laiendust (nt "Docker")
3. **Install** → avaneb VS Code automaatselt
4. Või kopeeri **Marketplace ID** → käsurea install

## 7. SSH Seadistamine

### SSH võtme loomine:
```bash
ssh-keygen -t rsa -b 4096 -C "sinu.email@example.com"
```

### VS Code SSH config:
Vajuta `F1` → `Remote-SSH: Open Configuration File`

Lisa:
```
Host serverinimi
    HostName IP.aadress.või.domeen
    User kasutajanimi
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

## 8. Põhiseadistused

Ava Settings (`Ctrl+,`) ja lisa:

```json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "files.autoSave": "afterDelay",
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "yaml.format.enable": true
}
```

## 4. Virtuaalmasinad ja Ühendused

### Võimalikud Keskkonnad

| Keskkond | Installimisviis | IP aadressi leidmine |
|---|---|---|
| **WSL2** (Windows) | `wsl --install Ubuntu` | Automaatne (localhost) |
| **Multipass** | `multipass launch --name dev` | `multipass list` |
| **VirtualBox** | GUI kaudu Ubuntu ISO | VM seadetest Network |
| **Docker** | `docker run -it ubuntu bash` | `docker inspect container_id` |

### WSL2 Ühendus (kõige lihtsam)
```bash
# Windows PowerShell-is
wsl --install Ubuntu
# Taaskäivita arvuti
# WSL2 käivitub automaatselt VS Code-s Remote Explorer-is
```

### Multipass Ühendus
```bash
# Masina loomine
multipass launch --name devserver --cpus 2 --mem 2G --disk 10G

# SSH info saamine
multipass info devserver

# VS Code config
Host multipass-dev
    HostName [IP multipass info käsust]
    User ubuntu
    IdentityFile ~/.ssh/id_rsa
```

### VirtualBox Ühendus
1. Loo Ubuntu VM VirtualBox-is
2. Network: Bridged Adapter või NAT + Port Forwarding
3. Ubuntu-s: `sudo apt install openssh-server`
4. Lisa VS Code SSH config-i

## 5. Remote Explorer Kasutamine

### Ühenduste Vaatamine
1. **Külgriba** → Remote Explorer ikoon
2. **SSH Targets** all näed kõiki seadistatud ühendusi  
3. **Kliki** masina nime → Connect in New Window

### Remote Extensions
Remote masinas on **eraldi extension store**:
- Ühenda remote masinaga
- Extensions paneel näitab "Install in SSH: serverinimi"
- Paigalda vajalikud extensions remote masinas

**Soovitatud remote extensions**:
- Python, Docker, YAML - kui vaja remote masinas

## 6. Mitme Terminali Kasutamine

### Terminal Loomine
```
Ctrl+Shift+` - Uus terminal
Ctrl+` - Terminali näitamine/peitmine
```

### Terminal Tüübid
| Kiirklahv | Terminal tüüp |
|---|---|
| `Ctrl+Shift+` | Kohalik terminal |
| Remote aknas: `Ctrl+Shift+` | Remote terminal |
| `+` nupp terminal paneelil | Lisa uus |

### Terminali Haldamine
- **Split Terminal**: Terminal paremklõps → "Split Terminal"  
- **Rename**: Terminal paremklõps → "Rename"
- **Kill Terminal**: Terminal paremklõps → "Kill Terminal"
- **Switch**: `Ctrl+PageUp/PageDown` või dropdown menüü

## 9. Kiire Test

1. Loo uus kaust ja ava VS Code-s
2. Loo fail `test.yaml`:
```yaml
server:
  host: localhost
  port: 8080
  settings:
    debug: true
    timeout: 30
```
3. Salvesta (`Ctrl+S`) - Prettier peaks formateerima
4. Vaata indent-rainbow värve