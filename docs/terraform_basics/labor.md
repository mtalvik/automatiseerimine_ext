# Terraform Alused Labor

**Eeldused:** WinKlient setup tehtud, VSCode, SSH võtmed seadistatud

**Platvorm:** Terraform (local → remote progression)

**Kestus:** ~90-120 min (2×45 min)

**Dokumentatsioon:** [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

## Õpiväljundid

- Paigaldad Terraform'i ja kontrollid versiooni
- Lood esimese Terraform konfiguratsiooni kohalikus failisüsteemis
- Käivitad Terraform workflow'i: init → plan → apply → destroy
- Mõistad state faili rolli ja struktuuri
- Kasutad muutujaid ja väljundeid (variables, outputs)
- Provisionerid remote serverile SSH kaudu

---

## OSA 1: Terraform Paigaldamine (WinKlient)

### 1.1 Paigaldamine

**PowerShell (Admin):**

```powershell
# Chocolatey kaudu (lihtsaim)
choco install terraform

# VÕI käsitsi:
# Lae: https://www.terraform.io/downloads
# Paki lahti C:\terraform\
# Lisa PATH'i: System → Environment Variables
```

### 1.2 Kontrolli

```powershell
terraform version
```

**Oodatav:**

```
Terraform v1.9.5
on windows_amd64
```

### 1.3 Töökaust

```powershell
mkdir C:\terraform-labs
cd C:\terraform-labs
code .  # Avab VSCode
```

**Validation:**
- [ ] `terraform version` töötab
- [ ] VSCode avatud `C:\terraform-labs`

---

## OSA 2: Esimene Projekt - Local Files

Alustame lihtsast: loome faile WinKlient'i. Pole võrku, pole SSH't - puhas Terraform õppimine.

### 2.1 main.tf - Esimene Konfiguratsioon

**VSCode:** Loo fail `main.tf`

```hcl
# main.tf
# Esimene Terraform projekt - loome lokaalseid faile

terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "greeting" {
  filename = "${path.module}/output/hello.txt"
  content  = "Tere, Terraform!\nSee fail on loodud IaC-ga.\n"
  
  file_permission = "0644"
}

resource "local_file" "config" {
  filename = "${path.module}/output/app.conf"
  content  = <<-EOT
    server {
      port = 8080
      host = "localhost"
    }
  EOT
  
  file_permission = "0644"
}
```

**Mis siin toimub?**

- `terraform {}` - provider'i nõuded
- `local` provider - loob faile kohalikku failisüsteemi
- `${path.module}` - praegune kaust
- `<<-EOT` - multi-line string (heredoc syntax)

### 2.2 Workflow: Init

Terminal VSCode's (`` Ctrl+` ``):

```powershell
terraform init
```

**Väljund:**

```
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 2.4"...
- Installing hashicorp/local v2.4.1...
- Installed hashicorp/local v2.4.1 (signed by HashiCorp)

Terraform has been successfully initialized!
```

**Mis juhtus?**

1. Lõi `.terraform/` kausta
2. Laadis `local` provider'i
3. Lõi `.terraform.lock.hcl` (dependency lock)

**Kontrolli:**

```powershell
ls -Force  # Näed .terraform/ kausta
```

### 2.3 Workflow: Plan

```powershell
terraform plan
```

**Väljund:**

```terraform
Terraform will perform the following actions:

  # local_file.config will be created
  + resource "local_file" "config" {
      + content              = <<-EOT
            server {
              port = 8080
              host = "localhost"
            }
        EOT
      + filename             = "./output/app.conf"
      + id                   = (known after apply)
    }

  # local_file.greeting will be created
  + resource "local_file" "greeting" {
      + content              = "Tere, Terraform!\nSee fail on loodud IaC-ga.\n"
      + filename             = "./output/hello.txt"
      + id                   = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

**Sümboolid:**

- `+` = luuakse
- `-` = kustutatakse
- `~` = muudetakse
- `-/+` = asendatakse

**TÄHTIS:** Plan ei muuda midagi! See on preview.

### 2.4 Workflow: Apply

```powershell
terraform apply
```

Küsib kinnitust:

```
Do you want to perform these actions?
  Enter a value: yes
```

**Väljund:**

```
local_file.config: Creating...
local_file.greeting: Creating...
local_file.config: Creation complete after 0s
local_file.greeting: Creation complete after 0s

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

**Kontrolli:**

```powershell
cat output/hello.txt
cat output/app.conf
```

**Validation:**
- [ ] `output/` kaust eksisteerib
- [ ] 2 faili loodud
- [ ] `terraform.tfstate` eksisteerib

### 2.5 State File

```powershell
cat terraform.tfstate
```

See on JSON, kus Terraform mäletab kõike.

**Tähtsad osad:**

```json
{
  "version": 4,
  "terraform_version": "1.9.5",
  "resources": [
    {
      "type": "local_file",
      "name": "greeting",
      "instances": [
        {
          "attributes": {
            "filename": "./output/hello.txt",
            "content": "Tere, Terraform!...",
            "id": "a4f2e..."
          }
        }
      ]
    }
  ]
}
```

**Miks oluline?**

Terraform võrdleb:
- **Soovitud:** `main.tf` fail
- **Praegune:** `terraform.tfstate`
- **Muudatus:** `terraform plan` näitab vahet

**KRIITILINE:** Ära kustuta state'i! Backup'i alati!

### 2.6 Muudatuste Test

Muuda `main.tf`:

```hcl
resource "local_file" "greeting" {
  filename = "${path.module}/output/hello.txt"
  content  = "Tere, MUUDETUD Terraform!\n"  # ← MUUTSIME
  
  file_permission = "0644"
}
```

```powershell
terraform plan
```

**Näed:**

```terraform
  # local_file.greeting must be replaced
-/+ resource "local_file" "greeting" {
      ~ content  = "Tere, Terraform!..." -> "Tere, MUUDETUD Terraform!\n"
      ~ id       = "a4f2e..." -> (known after apply)
        # (2 unchanged attributes hidden)
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

`-/+` = kustutab vana, loob uue (sest faili sisu ei saa "muuta", peab asendama).

```powershell
terraform apply -auto-approve
cat output/hello.txt  # Uus sisu
```

### 2.7 Workflow: Destroy

**HOIATUS:** Kustutab KÕIK ressursid!

```powershell
terraform destroy
```

Küsib kinnitust:

```
Do you really want to destroy all resources?
  Enter a value: yes
```

**Väljund:**

```
local_file.config: Destroying...
local_file.greeting: Destroying...
local_file.config: Destruction complete after 0s
local_file.greeting: Destruction complete after 0s

Destroy complete! Resources: 2 destroyed.
```

**Kontrolli:**

```powershell
ls output/  # TÜHI!
cat terraform.tfstate  # resources: [] (tühi)
```

---

## OSA 3: Variables ja Outputs

Loome paindlikuma konfiguratsiooni.

### 3.1 Taasta Ressursid

```powershell
terraform apply -auto-approve
```

### 3.2 variables.tf

**Loo fail:** `variables.tf`

```hcl
# variables.tf
# Input muutujad

variable "environment" {
  description = "Keskkonna nimi (dev/test/prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment peab olema: dev, test või prod"
  }
}

variable "app_name" {
  description = "Rakenduse nimi"
  type        = string
  default     = "myapp"
}

variable "port" {
  description = "Rakenduse port"
  type        = number
  default     = 8080
  
  validation {
    condition     = var.port > 1024 && var.port < 65535
    error_message = "Port peab olema vahemikus 1024-65535"
  }
}
```

### 3.3 Kasuta Variables

Muuda `main.tf`:

```hcl
resource "local_file" "config" {
  filename = "${path.module}/output/${var.app_name}.conf"
  content  = <<-EOT
    # ${var.app_name} Configuration
    # Environment: ${var.environment}
    
    server {
      port = ${var.port}
      host = "localhost"
      env  = "${var.environment}"
    }
  EOT
  
  file_permission = "0644"
}
```

```powershell
terraform plan
```

Näed, et fail nimi muutub `app.conf` → `myapp.conf`.

### 3.4 Anna Variables Käsurealt

```powershell
terraform apply -var="environment=prod" -var="port=9090" -var="app_name=webserver"
```

**VÕI** loo `terraform.tfvars`:

```hcl
# terraform.tfvars
environment = "prod"
app_name    = "webserver"
port        = 9090
```

```powershell
terraform apply
```

Terraform laeb automaatselt `terraform.tfvars`.

### 3.5 outputs.tf

**Loo fail:** `outputs.tf`

```hcl
# outputs.tf
# Info pärast apply'd

output "config_file_path" {
  description = "Config faili asukoht"
  value       = local_file.config.filename
}

output "config_file_id" {
  description = "Faili hash"
  value       = local_file.config.id
}

output "summary" {
  description = "Deployment kokkuvõte"
  value = {
    app         = var.app_name
    environment = var.environment
    port        = var.port
    config_path = local_file.config.filename
  }
}
```

```powershell
terraform apply
```

**Pärast apply'd:**

```
Outputs:

config_file_id = "sha256:a4f2e..."
config_file_path = "./output/webserver.conf"
summary = {
  "app" = "webserver"
  "config_path" = "./output/webserver.conf"
  "environment" = "prod"
  "port" = 9090
}
```

**Küsi output'e:**

```powershell
terraform output
terraform output config_file_path
terraform output -json summary
```

**Validation:**
- [ ] Variables töötavad
- [ ] Outputs näidatakse pärast apply'd
- [ ] `terraform output` töötab

---

## OSA 4: Remote Provisioning (SSH → Ubuntu)

Nüüd liigume päris asjale: deploy'me Ubuntu-1 serverile.

### 4.1 Uus Projekt

```powershell
cd C:\terraform-labs
mkdir remote-setup
cd remote-setup
code .
```

### 4.2 main.tf - Null Resource + Remote-Exec

**Loo fail:** `main.tf`

```hcl
# main.tf
# Remote provisioning Ubuntu-1 serverile

terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

variable "target_host" {
  description = "Target Ubuntu server IP"
  type        = string
  default     = "10.0.208.20"  # Ubuntu-1
}

variable "ssh_user" {
  description = "SSH kasutaja"
  type        = string
  default     = "kasutaja"
}

variable "ssh_private_key" {
  description = "SSH private key path"
  type        = string
  default     = "~/.ssh/id_ed25519"
}

# Null resource - ei loo infrat, ainult käivitab provisioner'eid
resource "null_resource" "ubuntu_setup" {
  # Connection block - kuidas Terraform ühendub
  connection {
    type        = "ssh"
    host        = var.target_host
    user        = var.ssh_user
    private_key = file(var.ssh_private_key)
    timeout     = "2m"
  }

  # Remote-exec - käivita käsud remote serveris
  provisioner "remote-exec" {
    inline = [
      "echo '=== System Info ==='",
      "hostname",
      "uname -a",
      "whoami",
      "pwd",
      "echo '=== Network ==='",
      "ip -4 addr show | grep inet",
      "echo '=== Disk ==='",
      "df -h /",
      "echo '=== Done ==='",
    ]
  }
}

output "connection_test" {
  value = "SSH connection successful to ${var.target_host}"
  depends_on = [null_resource.ubuntu_setup]
}
```

**Mis siin toimub?**

- `null_resource` - ei loo päris ressurssi, ainult käivitab provisioner'eid
- `connection {}` - SSH ühenduse parameetrid
- `provisioner "remote-exec"` - käivitab käsud remote masinas
- `file(var.ssh_private_key)` - loeb SSH võtme WinKlient'ist

### 4.3 Test SSH Ühendust

**Enne Terraform'i, testi SSH:**

```powershell
ssh kasutaja@10.0.208.20 "hostname"
```

Peaks näitama `ubuntu1` (kui `winklient-setup.md` tehtud).

### 4.4 Init ja Apply

```powershell
terraform init
```

```powershell
terraform plan
```

**Näed:**

```terraform
  # null_resource.ubuntu_setup will be created
  + resource "null_resource" "ubuntu_setup" {
      + id = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

```powershell
terraform apply
```

**Väljund:**

```
null_resource.ubuntu_setup: Creating...
null_resource.ubuntu_setup: Provisioning with 'remote-exec'...
null_resource.ubuntu_setup (remote-exec): Connecting to remote host via SSH...
null_resource.ubuntu_setup (remote-exec): Connected!
null_resource.ubuntu_setup (remote-exec): === System Info ===
null_resource.ubuntu_setup (remote-exec): ubuntu1
null_resource.ubuntu_setup (remote-exec): Linux ubuntu1 5.15.0-91-generic
null_resource.ubuntu_setup (remote-exec): kasutaja
null_resource.ubuntu_setup (remote-exec): /home/kasutaja
null_resource.ubuntu_setup (remote-exec): === Network ===
null_resource.ubuntu_setup (remote-exec):     inet 10.0.208.20/24
null_resource.ubuntu_setup (remote-exec): === Disk ===
null_resource.ubuntu_setup (remote-exec): /dev/sda1        20G  5.2G   14G  28% /
null_resource.ubuntu_setup (remote-exec): === Done ===
null_resource.ubuntu_setup: Creation complete after 2s

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
connection_test = "SSH connection successful to 10.0.208.20"
```

**Validation:**
- [ ] SSH ühendus õnnestus
- [ ] Näed Ubuntu-1 hostname'i
- [ ] Näed IP 10.0.208.20

### 4.5 Nginx Paigaldamine

Muuda `main.tf` provisioner:

```hcl
  provisioner "remote-exec" {
    inline = [
      "echo '=== Updating packages ==='",
      "sudo apt update -qq",
      
      "echo '=== Installing Nginx ==='",
      "sudo apt install -y nginx",
      
      "echo '=== Starting Nginx ==='",
      "sudo systemctl start nginx",
      "sudo systemctl enable nginx",
      
      "echo '=== Creating custom page ==='",
      "echo '<h1>Deployed by Terraform!</h1>' | sudo tee /var/www/html/index.html",
      
      "echo '=== Nginx Status ==='",
      "sudo systemctl status nginx --no-pager",
      
      "echo '=== Testing ==='",
      "curl -s localhost | grep -o '<h1>.*</h1>'",
      
      "echo '=== Done ==='",
    ]
  }
```

**Destroy vana ja loo uus:**

```powershell
terraform destroy -auto-approve
terraform apply
```

**Kontrolli brauseris (WinKlient):**

```
http://10.0.208.20
```

Peaks näitama: "Deployed by Terraform!"

### 4.6 Triggers - Käivita Uuesti

Probleem: `null_resource` käivitub ainult loomisel. Kui tahad uuesti käivitada?

**Lisa trigger:**

```hcl
resource "null_resource" "ubuntu_setup" {
  # Käivita uuesti, kui timestamp muutub
  triggers = {
    always_run = timestamp()
  }

  connection {
    # ... sama
  }

  provisioner "remote-exec" {
    # ... sama
  }
}
```

Nüüd iga `terraform apply` käivitab provisioner'i uuesti!

**VÕI kasuta UUID trigger:**

```hcl
  triggers = {
    deployment_id = uuid()
  }
```

### 4.7 Local-Exec (Klient Pool)

Kui tahad käivitada käske **WinKlient'is** (mitte Ubuntu's):

```hcl
  provisioner "local-exec" {
    command = "echo Deployment started > deployment.log"
  }

  provisioner "remote-exec" {
    # Deploy Ubuntu'sse
  }

  provisioner "local-exec" {
    command = "echo Deployment finished >> deployment.log"
  }
```

---

## OSA 5: File Provisioner

Kopeerime faile WinKlient'ist → Ubuntu.

### 5.1 Loo Konfiguratsioonifailid

**WinKlient:** `files/nginx.conf`

```nginx
server {
    listen 8080;
    server_name _;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

**WinKlient:** `files/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Terraform Deploy</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; }
        .container { max-width: 800px; margin: 50px auto; padding: 20px; background: white; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Deployed by Terraform!</h1>
        <p>This page was deployed using Infrastructure as Code.</p>
        <p>Server: <strong>Ubuntu-1</strong></p>
        <p>Date: <strong><script>document.write(new Date().toISOString())</script></strong></p>
    </div>
</body>
</html>
```

### 5.2 File Provisioner

```hcl
resource "null_resource" "ubuntu_setup" {
  triggers = {
    config_hash = filemd5("${path.module}/files/nginx.conf")
    html_hash   = filemd5("${path.module}/files/index.html")
  }

  connection {
    type        = "ssh"
    host        = var.target_host
    user        = var.ssh_user
    private_key = file(var.ssh_private_key)
  }

  # 1. Kopeeri failid
  provisioner "file" {
    source      = "files/index.html"
    destination = "/tmp/index.html"
  }

  provisioner "file" {
    source      = "files/nginx.conf"
    destination = "/tmp/nginx-custom.conf"
  }

  # 2. Paigalda ja seadista
  provisioner "remote-exec" {
    inline = [
      "sudo apt update -qq && sudo apt install -y nginx",
      "sudo mv /tmp/index.html /var/www/html/",
      "sudo mv /tmp/nginx-custom.conf /etc/nginx/sites-available/custom",
      "sudo ln -sf /etc/nginx/sites-available/custom /etc/nginx/sites-enabled/",
      "sudo nginx -t",
      "sudo systemctl reload nginx",
      "echo 'Deployment complete!'",
    ]
  }
}
```

**Trigger hash:** Kui fail muutub, Terraform detects ja deploy'b uuesti!

```powershell
terraform apply
```

**Test:**

```
http://10.0.208.20:8080
```

---

## OSA 6: Troubleshooting

### 6.1 SSH Connection Failed

**Viga:**

```
Error: error connecting to SSH: dial tcp 10.0.208.20:22: i/o timeout
```

**Lahendused:**

```powershell
# Test ping
ping 10.0.208.20

# Test SSH käsitsi
ssh kasutaja@10.0.208.20

# Kontrolli SSH service Ubuntu's
ssh kasutaja@10.0.208.20 "sudo systemctl status ssh"

# Kontrolli firewall
ssh kasutaja@10.0.208.20 "sudo ufw status"
```

### 6.2 Permission Denied (publickey)

**Viga:**

```
Error: Permission denied (publickey)
```

**Lahendused:**

```powershell
# Kontrolli SSH võtit
ssh-add -l
cat ~/.ssh/id_ed25519.pub

# Kontrolli authorized_keys Ubuntu's
ssh kasutaja@10.0.208.20 "cat ~/.ssh/authorized_keys"

# Lisa võti käsitsi (kui puudub)
type ~/.ssh/id_ed25519.pub | ssh kasutaja@10.0.208.20 "cat >> ~/.ssh/authorized_keys"
```

### 6.3 Provisioner Failed

**Viga:**

```
Error: remote-exec provisioner error: Command exited with non-zero status: 1
```

**Debug:**

```hcl
  provisioner "remote-exec" {
    inline = [
      "set -x",  # Enable verbose logging
      "whoami",
      "pwd",
      "ls -la",
      # ... teised käsud
    ]
  }
```

**VÕI käivita käsitsi:**

```powershell
ssh kasutaja@10.0.208.20 "sudo apt update -qq && sudo apt install -y nginx"
```

### 6.4 State Lock

**Viga:**

```
Error: state locked
```

**Lahendus:**

```powershell
terraform force-unlock LOCK_ID
```

(Kasuta ainult kui kindel, et teine apply ei jookse!)

---

## Kontrollnimekiri

### OSA 1-2: Local Setup
- [ ] Terraform paigaldatud WinKlient'i
- [ ] `terraform version` töötab
- [ ] Local provider töötab
- [ ] Init/plan/apply/destroy workflow toimib
- [ ] State fail arusaadav

### OSA 3: Variables
- [ ] `variables.tf` töötab
- [ ] `-var` flag töötab
- [ ] `terraform.tfvars` laetakse
- [ ] Outputs näidatakse
- [ ] Validation constraint'd töötavad

### OSA 4-5: Remote Setup
- [ ] SSH ühendus Ubuntu-1'le
- [ ] `null_resource` + `remote-exec` töötab
- [ ] Nginx paigaldatud
- [ ] File provisioner kopeerib faile
- [ ] Trigger hash töötab
- [ ] Webpage accessible brauseris

### Troubleshooting
- [ ] SSH debug oskus
- [ ] Provisioner debug oskus
- [ ] State management

---

## Järgmine Samm

**Kodutöö:** Deploy sama setup Ubuntu-2'le, aga erineva konfiguratsiooniga (nginx port 9090, erinev HTML).

**Lisapraktika:** Multi-server deploy (mõlemad Ubuntu'd korraga).

**Allikas:** [Terraform Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)
