# WinKlient Jumpbox Setup

---

## 1. Võrk

**Login:** `kasutaja` / `Passw0rd`

**Settings** → **Network & Internet** → **Ethernet** → **Properties** → **IPv4**

**Märgi:** `Use the following IP address`

| Väli | Väärtus |
|------|---------|
| IP address | 10.0.82.10 |
| Subnet mask | 255.255.255.0 |
| Default gateway | 10.0.82.1 |
| Preferred DNS | 8.8.8.8 |
| Alternate DNS | 1.1.1.1 |

**Test:**

```powershell
ping 8.8.8.8
```

---

## 2. VSCode

**Microsoft Store:** Otsi "Visual Studio Code" → Install

**Extensions (Ctrl+Shift+X):**
- Remote - SSH
- GitLens
- YAML

---

## 3. SSH Setup

### Generate Key

```powershell
ssh-keygen -t ed25519 -C "nimi@hkhk.edu.ee"
```

**Passphrase:** 
- Tühi (3x ENTER) - lihtsam ✅
- Või sisesta → seadista SSH Agent (vt allpool)

### SSH Agent (kui kasutad passphrase)

**PowerShell (Admin):**

```powershell
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
ssh-add C:\Users\kasutaja\.ssh\id_ed25519
```

### Copy Keys (Automaatne)

**Salvesta:** `setup-ssh.ps1`

```powershell
# SSH key setup script with auto-test
$pubKey = Get-Content C:\Users\kasutaja\.ssh\id_ed25519.pub
$servers = @(
    @{IP="10.0.82.20"; Name="ubuntu1"},
    @{IP="10.0.82.21"; Name="ubuntu2"},
    @{IP="10.0.82.30"; Name="alma1"},
    @{IP="10.0.82.31"; Name="alma2"}
)
$password = "Passw0rd"

Write-Host "`n=== SSH Key Setup ===" -ForegroundColor Cyan

foreach ($srv in $servers) {
    Write-Host "`nSetting up $($srv.Name) ($($srv.IP))..." -ForegroundColor Yellow
    
    # Setup commands
    $commands = "mkdir -p ~/.ssh; chmod 700 ~/.ssh; echo '$pubKey' >> ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys"
    
    # Execute with password (first time)
    $result = echo $password | ssh -o StrictHostKeyChecking=no kasutaja@$($srv.IP) $commands 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Setup: OK" -ForegroundColor Green
        
        # Test key-based login
        Write-Host "  Testing..." -ForegroundColor Yellow
        $testResult = ssh -o BatchMode=yes -o ConnectTimeout=5 kasutaja@$($srv.IP) "hostname" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Test: OK - No password needed!" -ForegroundColor Green
        } else {
            Write-Host "  Test: FAILED - Still asks password!" -ForegroundColor Red
        }
    } else {
        Write-Host "  Setup: FAILED" -ForegroundColor Red
    }
}

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Try: ssh ubuntu1" -ForegroundColor White
```

**Käivita:**

```powershell
powershell -ExecutionPolicy Bypass -File setup-ssh.ps1
```

### Hostname Setup (Optional)

**Salvesta:** `setup-hostnames.ps1`

```powershell
# Hostname setup script - Automatic
# Download plink if not exists
$plinkPath = "C:\Windows\System32\plink.exe"
if (-not (Test-Path $plinkPath)) {
    Write-Host "Downloading plink.exe..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plinkPath
}

$servers = @(
    @{IP="10.0.82.20"; Hostname="ubuntu1"},
    @{IP="10.0.82.21"; Hostname="ubuntu2"},
    @{IP="10.0.82.30"; Hostname="alma1"},
    @{IP="10.0.82.31"; Hostname="alma2"}
)

$password = "Passw0rd"

Write-Host "`n=== Hostname Setup ===" -ForegroundColor Cyan

foreach ($srv in $servers) {
    Write-Host "`nSetting $($srv.IP) -> $($srv.Hostname)..." -ForegroundColor Yellow
    
    # Use plink with password
    $cmd = "echo $password | sudo -S hostnamectl set-hostname $($srv.Hostname)"
    & $plinkPath -batch -pw $password kasutaja@$($srv.IP) $cmd 2>$null
    
    # Verify
    $check = & $plinkPath -batch -pw $password kasutaja@$($srv.IP) "hostname" 2>$null
    
    if ($check -eq $srv.Hostname) {
        Write-Host "  SUCCESS: $check" -ForegroundColor Green
    } else {
        Write-Host "  FAILED: Still $check" -ForegroundColor Red
    }
}

Write-Host "`n=== Done ===" -ForegroundColor Cyan
```

**Käivita:**

```powershell
powershell -ExecutionPolicy Bypass -File setup-hostnames.ps1
```

### SSH Config

**VSCode:** Ctrl+Shift+P → "Remote-SSH: Open SSH Configuration File"

**Vali:** `C:\Users\kasutaja\.ssh\config`

**Lisa:**

```
Host *
    User kasutaja
    PubkeyAuthentication yes
    PreferredAuthentications publickey

Host ubuntu1
    HostName 10.0.82.20

Host ubuntu2
    HostName 10.0.82.21

Host alma1
    HostName 10.0.82.30

Host alma2
    HostName 10.0.82.31
```

**Test:**

```powershell
ssh alma1
ssh ubuntu1
```

---

## 4. VSCode Remote-SSH

### Alma Linux Prerequisites

**Alma vajab `tar` VSCode server'i jaoks:**

```powershell
ssh alma1 "sudo dnf install -y tar"
ssh alma2 "sudo dnf install -y tar"
```

**Parool:** `Passw0rd`

### Connect to Servers

1. **Ctrl+Shift+P**
2. "Remote-SSH: Connect to Host"
3. Vali host: `ubuntu1`, `ubuntu2`, `alma1`, `alma2`
4. Uus aken → Terminal (`` Ctrl+` ``)

Valmis! ✅