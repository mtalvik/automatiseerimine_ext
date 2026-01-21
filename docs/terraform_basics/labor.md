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
- Kasutad provisioner'eid remote serverile SSH kaudu

---

## OSA 1: Terraform Paigaldamine (WinKlient)

Enne kui saame Terraformiga midagi teha, peame selle paigaldama. Windows'is on lihtsaim viis kasutada Chocolatey paketihaldust, mis töötab sarnaselt Linuxi apt või yum käskudega.

### 1.1 Paigaldamine

Ava PowerShell administraatori õigustega ja käivita:

```powershell
choco install terraform -y
```

Kui Chocolatey pole paigaldatud, kasuta alternatiivi:

```powershell
# Windows 10/11 - winget
winget install HashiCorp.Terraform

# VÕI käsitsi:
# 1. Lae https://terraform.io/downloads
# 2. Paki lahti C:\terraform\
# 3. Lisa C:\terraform PATH'i
```

Chocolatey laeb Terraformi alla, pakib lahti ja lisab PATH'i automaatselt. Kui Chocolatey pole paigaldatud, saad Terraformi ka käsitsi paigaldada: lae ZIP fail [terraform.io/downloads](https://www.terraform.io/downloads) lehelt, paki lahti näiteks `C:\terraform\` kausta ja lisa see kaust süsteemi PATH keskkonnamuutujasse.

### 1.2 Kontrolli paigaldust

Sulge ja ava PowerShell uuesti (et PATH uueneks), seejärel kontrolli:

```powershell
terraform version
```

Peaksid nägema midagi sellist:

```
Terraform v1.9.x
on windows_amd64
```

Konkreetne versiooninumber võib erineda, aga oluline on, et käsk töötab ja näitab versiooni.

### 1.3 Töökaust

Loome labori jaoks eraldi kausta, kus hoiame kõiki Terraform projekte:

```powershell
mkdir C:\terraform-labs
cd C:\terraform-labs
code .
```

Viimane käsk avab VSCode praeguses kaustas. VSCode on hea Terraform'i jaoks, sest HashiCorp pakub ametlikku laiendit, mis annab süntaksi esiletõstmise ja automaatse lõpetamise.

**Validation:**
- [ ] `terraform version` näitab versiooni
- [ ] VSCode avatud `C:\terraform-labs` kaustas

---

## OSA 2: Esimene Projekt - Local Files

Alustame kõige lihtsamast võimalikust Terraform projektist: loome faile oma arvuti failisüsteemi. See ei vaja võrguühendust, pilve kontot ega SSH seadistust - puhas Terraform õppimine ilma lisatüsistusteta.

Miks alustame kohalike failidega? Sest see võimaldab keskenduda Terraformi põhitöövoole (init, plan, apply, destroy) ilma, et peaksime muretsema võrguprobleemide või autentimise pärast. Kui mõistad, kuidas Terraform töötab lokaalselt, on pilve või serverite haldamine lihtsalt teise provider'i kasutamine - põhimõtted jäävad samaks.

### 2.1 Projekti struktuur

Loome esimese projekti jaoks eraldi kausta:

```powershell
mkdir local-files
cd local-files
```

Iga Terraform projekt elab oma kaustas. Terraform loeb kõik `.tf` failid kaustast ja käsitleb neid ühe konfiguratsioonina.

### 2.2 main.tf - Esimene konfiguratsioon

Loo VSCode's uus fail nimega `main.tf` ja kirjuta sinna:

```hcl
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
}

resource "local_file" "config" {
  filename = "${path.module}/output/app.conf"
  content  = <<-EOT
    server {
      port = 8080
      host = "localhost"
    }
  EOT
}
```

Vaatame seda koodi lähemalt, sest siin on mitu olulist kontseptsiooni.

Esimene plokk `terraform {}` ütleb Terraformile, milliseid provider'eid me vajame. Provider on plugin, mis teab, kuidas konkreetse platvormiga suhelda. Meie kasutame `local` provider'it, mis oskab luua faile kohalikku failisüsteemi. Versioon `~> 2.4` tähendab "versioon 2.4 või uuem, aga mitte 3.0" - see tagab, et meie kood töötab ka tulevikus, kui ilmuvad uuemad versioonid.

Järgmised kaks plokki on `resource` plokid. Ressurss on midagi, mida Terraform loob ja haldab. Süntaks on `resource "<TYPE>" "<NAME>"` - tüüp tuleb provider'ist (`local_file`) ja nimi valid ise (`greeting`, `config`). Seda nime kasutad hiljem ressursile viitamiseks.

`${path.module}` on Terraform'i sisseehitatud muutuja, mis viitab praegusele kaustale. See on kasulik, sest siis töötab konfiguratsioon olenemata sellest, kust seda käivitad.

`<<-EOT ... EOT` on heredoc süntaks, mis võimaldab kirjutada mitmerealisi stringe ilma `\n` märkideta. See teeb konfiguratsiooni loetavamaks, eriti kui failisisu on pikem.

### 2.3 Workflow: Init

Nüüd käivitame esimese Terraformi käsu. Init on alati esimene samm uue projekti puhul:

```powershell
terraform init
```

Näed väljundit:

```
Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 2.4"...
- Installing hashicorp/local v2.4.1...

Terraform has been successfully initialized!
```

Mis siin juhtus? Terraform lõi `.terraform/` kausta ja laadis sinna `local` provider'i. Provider on tegelikult eraldi programm (Go keeles kompileeritud binaar), mille Terraform käivitab, kui vaja ressursse luua või muuta. Init laeb ka `.terraform.lock.hcl` faili, mis lukustab provider'i täpse versiooni - see tagab, et meeskonnakaaslased saavad täpselt sama versiooni.

Init käsku tuleb käivitada:
- Projekti alguses (nagu praegu)
- Kui lisad uue provider'i
- Kui kloonid projekti teise arvutisse
- Kui muudad backend'i seadistust

### 2.4 Workflow: Plan

Enne kui Terraform midagi loob, tahame näha, mida ta kavatseb teha. Selleks on `plan` käsk:

```powershell
terraform plan
```

Väljund näitab täpselt, mida Terraform kavatseb teha:

```
Terraform will perform the following actions:

  # local_file.config will be created
  + resource "local_file" "config" {
      + content  = <<-EOT
            server {
              port = 8080
              host = "localhost"
            }
        EOT
      + filename = "./output/app.conf"
    }

  # local_file.greeting will be created
  + resource "local_file" "greeting" {
      + content  = "Tere, Terraform!..."
      + filename = "./output/hello.txt"
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

Plan väljundis näed sümboleid, mis ütlevad, mis toimub:

| Sümbol | Tähendus |
|--------|----------|
| `+` | ressurss luuakse |
| `-` | ressurss kustutatakse |
| `~` | ressurssi muudetakse (in-place) |
| `-/+` | ressurss asendatakse (kustuta + loo uus) |

See on üks Terraformi võimsamaid omadusi - sa näed alati ette, mis juhtub, enne kui midagi päriselt tehakse. Production keskkonnas on see kriitilise tähtsusega, sest vead võivad olla kulukad.

**Tähtis:** Plan ei muuda midagi! See on ainult eelvaade.

### 2.5 Workflow: Apply

Kui plaan tundub õige, rakendame muudatused:

```powershell
terraform apply
```

Terraform näitab uuesti plaani ja küsib kinnitust:

```
Do you want to perform these actions?
  Enter a value: yes
```

Kirjuta `yes` ja vajuta Enter. Terraform hakkab tööle:

```
local_file.config: Creating...
local_file.greeting: Creating...
local_file.config: Creation complete after 0s
local_file.greeting: Creation complete after 0s

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

Nüüd on failid loodud! Kontrolli:

```powershell
cat output/hello.txt
cat output/app.conf
```

Pane tähele, et Terraform lõi ka `output/` kausta automaatselt - `local_file` ressurss loob vajalikud kataloogid ise.

**Validation:**
- [ ] `output/` kaust eksisteerib
- [ ] `hello.txt` ja `app.conf` failid on sees
- [ ] `terraform.tfstate` fail on loodud

### 2.6 State faili uurimine

Märkasid, et tekkis fail nimega `terraform.tfstate`. See on Terraformi "mälu" - JSON fail, mis sisaldab infot kõigi loodud ressursside kohta. Vaatame seda:

```powershell
cat terraform.tfstate
```

Fail on pikk, aga põhiline struktuur on selline:

```json
{
  "version": 4,
  "resources": [
    {
      "type": "local_file",
      "name": "greeting",
      "instances": [
        {
          "attributes": {
            "filename": "./output/hello.txt",
            "content": "Tere, Terraform!...",
            "id": "abc123..."
          }
        }
      ]
    }
  ]
}
```

Miks on state nii oluline? Terraform töötab nii: ta võrdleb kolme asja:

1. **Soovitud seisu** - mida `main.tf` kirjeldab
2. **Teadaolevat seisu** - mida `terraform.tfstate` sisaldab
3. **Tegelikku seisu** - mis päriselt eksisteerib

`terraform plan` arvutab vahe soovitud ja teadaoleva seisu vahel ning näitab, mida muuta. `terraform apply` teeb muudatused ja uuendab state'i.

Ilma state'ita ei tea Terraform, mis on juba loodud. Kui kustutaksid state faili ja käivitaksid `terraform apply`, arvaks Terraform, et mitte midagi pole olemas, ja prooviks kõike uuesti luua.

**Oluline:** Ära kunagi kustuta ega muuda state faili käsitsi! Ja ära pane seda Git'i, sest see võib sisaldada tundlikku infot (paroole, võtmeid).

### 2.7 Muudatuste tegemine

Vaatame, kuidas Terraform käsitleb muudatusi. Muuda `main.tf` failis greeting ressurssi:

```hcl
resource "local_file" "greeting" {
  filename = "${path.module}/output/hello.txt"
  content  = "Tere, MUUDETUD Terraform!\nVersioon 2.0\n"
}
```

Nüüd käivita plan:

```powershell
terraform plan
```

Näed midagi sellist:

```
  # local_file.greeting must be replaced
-/+ resource "local_file" "greeting" {
      ~ content  = <<-EOT # forces replacement
          - Tere, Terraform!
          - See fail on loodud IaC-ga.
          + Tere, MUUDETUD Terraform!
          + Versioon 2.0
        EOT
      ~ id       = "abc123" -> (known after apply)
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

Pane tähele `-/+` sümbolit - see tähendab, et fail asendatakse. Local provider ei oska faili sisu "muuta" - ta kustutab vana ja loob uue. See on normaalne käitumine paljude ressursside puhul, kus teatud atribuute ei saa muuta ilma ressurssi uuesti loomata.

Rakenda muudatus:

```powershell
terraform apply -auto-approve
```

`-auto-approve` jätab kinnituse küsimise vahele. Kasuta seda ettevaatlikult - labori ja arenduse jaoks on see mugav, aga production'is on parem alati plaan üle vaadata.

```powershell
cat output/hello.txt
```

Näed uut sisu!

### 2.8 Workflow: Destroy

Lõpuks vaatame, kuidas ressursse kustutada:

```powershell
terraform destroy
```

Terraform näitab, mida ta kavatseb kustutada, ja küsib kinnitust. Kirjuta `yes`.

```
local_file.config: Destroying...
local_file.greeting: Destroying...
Destroy complete! Resources: 2 destroyed.
```

Kontrolli:

```powershell
ls output/
cat terraform.tfstate
```

Kaust on tühi (või puudub) ja state faili `resources` massiiv on tühi `[]`.

See on täielik Terraform töövoog: **init → plan → apply → destroy**. Kõik muu, mida Terraformiga teed, põhineb sellel tsüklil.

---

## OSA 3: Variables ja Outputs

Eelmises osas hardcodesime kõik väärtused otse `main.tf` faili. See töötab, aga pole paindlik - kui tahad sama konfiguratsiooni kasutada erinevates keskkondades (dev, test, prod) või erinevate parameetritega, peaksid koodi muutma. Variables lahendavad selle probleemi.

### 3.1 Uus projekt

Loome uue projekti, et alustada puhtalt lehelt:

```powershell
cd C:\terraform-labs
mkdir variables-demo
cd variables-demo
```

### 3.2 variables.tf - Muutujate defineerimine

Loo fail `variables.tf`:

```hcl
variable "environment" {
  description = "Keskkonna nimi (dev/test/prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment peab olema: dev, test või prod."
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
    error_message = "Port peab olema vahemikus 1025-65534."
  }
}
```

Vaatame muutuja definitsiooni osi:

- `description` - dokumentatsioon, mis aitab teistel mõista, mida muutuja teeb
- `type` - andmetüüp (string, number, bool, list, map, object)
- `default` - vaikeväärtus, kui kasutaja ei anna väärtust
- `validation` - reeglid, mis kontrollivad, kas väärtus on lubatud

Validation on eriti kasulik, sest see annab selge veateate, kui keegi proovib kasutada vale väärtust. Ilma selleta võid saada kryptilise vea alles apply ajal.

### 3.3 main.tf muutujatega

Loo fail `main.tf`, mis kasutab neid muutujaid:

```hcl
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
  content  = <<-EOT
    Tere tulemast ${var.app_name} rakendusse!
    Keskkond: ${var.environment}
    Port: ${var.port}
  EOT
}

resource "local_file" "config" {
  filename = "${path.module}/output/${var.app_name}-${var.environment}.conf"
  content  = <<-EOT
    # ${var.app_name} Configuration
    # Environment: ${var.environment}

    server {
      port = ${var.port}
      host = "localhost"
      env  = "${var.environment}"
    }
  EOT
}
```

Muutujatele viitamine käib `${var.muutuja_nimi}` süntaksiga (või ilma `${}` kui see on eraldiseisev väärtus, näiteks `port = var.port`).

Pane tähele, et konfiguratsioonifaili nimi sisaldab nüüd nii rakenduse nime kui keskkonda: `myapp-dev.conf`. See võimaldab hoida erinevate keskkondade faile koos ilma konfliktita.

### 3.4 outputs.tf - Väljundite defineerimine

Loo fail `outputs.tf`:

```hcl
output "config_file_path" {
  description = "Loodud config faili asukoht"
  value       = local_file.config.filename
}

output "greeting_file_path" {
  description = "Tervitusfaili asukoht"
  value       = local_file.greeting.filename
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

Outputs on kasulikud mitmel põhjusel:
- Näitavad olulist infot pärast apply'd (IP-aadressid, URL-id, failide teed)
- Võimaldavad teistel Terraform moodulitel kasutada sinu ressursside infot
- Saab neid pärida skriptidest (`terraform output -json`)

### 3.5 Käivitamine vaikeväärtustega

```powershell
terraform init
terraform apply -auto-approve
```

Näed väljundeid:

```
Outputs:

config_file_path = "./output/myapp-dev.conf"
greeting_file_path = "./output/hello.txt"
summary = {
  "app" = "myapp"
  "config_path" = "./output/myapp-dev.conf"
  "environment" = "dev"
  "port" = 8080
}
```

Kontrolli loodud faile:

```powershell
cat output/hello.txt
cat output/myapp-dev.conf
```

### 3.6 Muutujate andmine käsurealt

Vaikeväärtused on head arenduseks, aga production'i jaoks tahad teisi väärtusi. Üks viis on anda need käsurealt:

```powershell
terraform apply -var="environment=prod" -var="port=9090" -var="app_name=webserver" -auto-approve
```

Nüüd on loodud uued failid production seadetega. Vaata:

```powershell
ls output/
cat output/webserver-prod.conf
```

### 3.7 terraform.tfvars fail

Käsurea parameetrid on tüütud, kui neid on palju. Parem viis on kasutada `terraform.tfvars` faili. Loo see:

```hcl
environment = "prod"
app_name    = "webserver"
port        = 9090
```

Nüüd piisab lihtsalt:

```powershell
terraform apply -auto-approve
```

Terraform laeb `terraform.tfvars` automaatselt, kui see eksisteerib. Võid ka kasutada muid nimesid (näiteks `prod.tfvars`), aga siis pead viitama käsurealt: `terraform apply -var-file="prod.tfvars"`.

### 3.8 Väljundite pärimine

Väljundeid saab pärida ka pärast apply'd:

```powershell
terraform output                     # Kõik väljundid
terraform output config_file_path    # Üks väljund
terraform output -json summary       # JSON formaadis
```

See on kasulik skriptides, kus tahad Terraformi loodud infot edasi kasutada.

### 3.9 Validatsiooni testimine

Proovi anda vale keskkond:

```powershell
terraform apply -var="environment=invalid"
```

Saad selge veateate:

```
Error: Invalid value for variable

  on variables.tf line 1:
   1: variable "environment" {

Environment peab olema: dev, test või prod.
```

See on palju parem kui kryptilised vead hiljem!

**Validation:**
- [ ] Muutujad töötavad vaikeväärtustega
- [ ] `-var` flag töötab käsurealt
- [ ] `terraform.tfvars` laetakse automaatselt
- [ ] Outputs kuvatakse pärast apply'd
- [ ] Validation annab selge vea vale väärtuse korral

---

## OSA 4: Remote Provisioning (SSH → Ubuntu)

Siiani oleme töötanud ainult kohalike failidega. Nüüd liigume tõelise infrastruktuuri haldamise juurde - käivitame käske Ubuntu serveris üle SSH. See on esimene samm päris DevOps töövoo poole, kus Terraform haldab servereid, võrke ja teenuseid.

> **Märkus provisioner'ite kohta:** HashiCorp (Terraformi looja) soovitab keerulisema konfiguratsiooni jaoks kasutada spetsiaalseid tööriistu nagu Ansible. Provisioner'id on mõeldud "viimase võimalusena" olukordadeks, kus muud ei sobi. Meie kasutame neid õppimiseks, sest need näitavad hästi, kuidas Terraform saab serveritega suhelda. Päris töös kombineeritakse sageli Terraform (loob infrastruktuuri) + Ansible (konfigureerib selle).

### 4.1 Uus projekt

```powershell
cd C:\terraform-labs
mkdir remote-setup
cd remote-setup
```

### 4.2 SSH ühenduse kontrollimine

Enne Terraformi kasutamist veendu, et SSH ühendus töötab. See on kõige sagedasem probleemide allikas!

```powershell
ssh kasutaja@10.0.208.20 "hostname && whoami"
```

Peaksid nägema:

```
ubuntu1
kasutaja
```

Kui see ei tööta, siis Terraform ka ei tööta. Lahenda SSH probleem enne jätkamist:
- Kas IP on õige?
- Kas kasutajanimi on õige?
- Kas SSH võti on seadistatud?
- Kas Ubuntu server on käivitatud?

### 4.3 main.tf - Esimene remote-exec

Loo fail `main.tf`:

```hcl
terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

variable "target_host" {
  description = "Ubuntu serveri IP-aadress"
  type        = string
  default     = "10.0.208.20"
}

variable "ssh_user" {
  description = "SSH kasutajanimi"
  type        = string
  default     = "kasutaja"
}

variable "ssh_private_key" {
  description = "SSH privaatvõtme asukoht"
  type        = string
  default     = "~/.ssh/id_ed25519"
}

resource "null_resource" "system_info" {
  connection {
    type        = "ssh"
    host        = var.target_host
    user        = var.ssh_user
    private_key = file(pathexpand(var.ssh_private_key))
    timeout     = "2m"
  }

  provisioner "remote-exec" {
    inline = [
      "echo '=== System Info ==='",
      "hostname",
      "whoami",
      "uname -a",
      "echo ''",
      "echo '=== Network ==='",
      "ip -4 addr show | grep 'inet ' | head -2",
      "echo ''",
      "echo '=== Disk ==='",
      "df -h / | tail -1",
      "echo ''",
      "echo '=== Done ==='"
    ]
  }
}

output "status" {
  value = "SSH ühendus serveriga ${var.target_host} õnnestus!"
}
```

Vaatame seda koodi lähemalt, sest siin on mitu uut kontseptsiooni.

**null_resource** on eriline ressurss, mis ei loo tegelikult midagi. Ta on "konteiner" provisioner'itele - võimaldab käivitada käske ilma, et peaks looma mingit infrastruktuuri. Päris elus kasutad `aws_instance` või `azurerm_virtual_machine` ressursse, millel on samuti provisioner'id.

**connection** plokk ütleb Terraformile, kuidas serveriga ühenduda. Toetatud on SSH (Linux) ja WinRM (Windows). Meie kasutame SSH-d.

**pathexpand()** on Terraformi funktsioon, mis teisendab `~` täielikuks teeks. See on oluline Windows'is, kus `~` ei pruugi alati töötada. `pathexpand("~/.ssh/id_ed25519")` muutub näiteks `C:/Users/kasutaja/.ssh/id_ed25519`.

**file()** loeb faili sisu. Meie puhul loeb SSH privaatvõtme sisu ja edastab selle ühendusele.

**provisioner "remote-exec"** käivitab käsud remote serveris. `inline` parameeter on nimekiri käskudest, mis käivitatakse järjest.

### 4.4 Käivitamine

```powershell
terraform init
terraform plan
```

Plan näitab, et luuakse üks `null_resource`:

```
  # null_resource.system_info will be created
  + resource "null_resource" "system_info" {
      + id = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Rakenda:

```powershell
terraform apply -auto-approve
```

Näed, kuidas Terraform ühendub serveriga ja käivitab käsud:

```
null_resource.system_info: Creating...
null_resource.system_info: Provisioning with 'remote-exec'...
null_resource.system_info (remote-exec): Connecting to remote host via SSH...
null_resource.system_info (remote-exec): Connected!
null_resource.system_info (remote-exec): === System Info ===
null_resource.system_info (remote-exec): ubuntu1
null_resource.system_info (remote-exec): kasutaja
null_resource.system_info (remote-exec): Linux ubuntu1 5.15.0-91-generic ...
null_resource.system_info (remote-exec): 
null_resource.system_info (remote-exec): === Network ===
null_resource.system_info (remote-exec):     inet 10.0.208.20/24 brd 10.0.208.255
null_resource.system_info (remote-exec): 
null_resource.system_info (remote-exec): === Disk ===
null_resource.system_info (remote-exec): /dev/sda1        20G   5G   14G  28% /
null_resource.system_info (remote-exec): 
null_resource.system_info (remote-exec): === Done ===
null_resource.system_info: Creation complete after 3s

Outputs:
status = "SSH ühendus serveriga 10.0.208.20 õnnestus!"
```

See on esimene kord, kui Terraform suhtles päris serveriga! Käsud käivitusid Ubuntu masinas, mitte sinu arvutis.

**Validation:**
- [ ] SSH ühendus õnnestus
- [ ] Näed Ubuntu serveri infot (hostname, IP, disk)

### 4.5 Nginx veebiserveri paigaldamine

Nüüd teeme midagi kasulikku - paigaldame Nginx veebiserveri ja loome lihtsa veebilehe.

Kustuta esmalt vana ressurss ja loo uus konfiguratsioon. Asenda kogu `main.tf` sisu:

```hcl
terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

variable "target_host" {
  description = "Ubuntu serveri IP-aadress"
  type        = string
  default     = "10.0.208.20"
}

variable "ssh_user" {
  description = "SSH kasutajanimi"
  type        = string
  default     = "kasutaja"
}

variable "ssh_private_key" {
  description = "SSH privaatvõtme asukoht"
  type        = string
  default     = "~/.ssh/id_ed25519"
}

resource "null_resource" "nginx_setup" {
  # Trigger määrab, millal provisioner uuesti käivitub
  triggers = {
    version = "1"
  }

  connection {
    type        = "ssh"
    host        = var.target_host
    user        = var.ssh_user
    private_key = file(pathexpand(var.ssh_private_key))
    timeout     = "5m"
  }

  provisioner "remote-exec" {
    inline = [
      "echo '>>> Uuendan pakettide nimekirja...'",
      "sudo apt-get update -qq",

      "echo '>>> Paigaldan Nginx...'",
      "sudo apt-get install -y -qq nginx",

      "echo '>>> Loon custom veebilehe...'",
      "echo '<html><body style=\"font-family: Arial; text-align: center; padding: 50px;\"><h1>Deployed by Terraform!</h1><p>Server: '$(hostname)'</p><p>Time: '$(date)'</p></body></html>' | sudo tee /var/www/html/index.html > /dev/null",

      "echo '>>> Käivitan Nginx...'",
      "sudo systemctl enable nginx",
      "sudo systemctl restart nginx",

      "echo '>>> Kontrollin...'",
      "curl -s http://localhost | grep -o '<h1>.*</h1>'",

      "echo '>>> Valmis!'"
    ]
  }
}

output "web_url" {
  value = "Veebileht: http://${var.target_host}"
}

output "ssh_command" {
  value = "SSH: ssh ${var.ssh_user}@${var.target_host}"
}
```

Oluline uus element on **triggers**. See on map, mis määrab, millal provisioner uuesti käivitub. `null_resource` provisioner käivitub vaikimisi ainult ressursi loomisel. Kui tahad uuesti käivitada, pead kas ressursi kustutama (`terraform destroy`) või muutma trigger'it.

Kustuta vana ja loo uus:

```powershell
terraform destroy -auto-approve
terraform apply -auto-approve
```

Terraform ühendub serveriga, paigaldab Nginx ja loob veebilehe. Protsess võtab umbes minut.

Nüüd ava brauseris (WinKlient'is):

```
http://10.0.208.20
```

Peaksid nägema: **"Deployed by Terraform!"** koos serveri nime ja ajatempliga.

**Validation:**
- [ ] Nginx on paigaldatud
- [ ] Veebileht on nähtav brauseris

### 4.6 Triggeri kasutamine uuesti käivitamiseks

Oletame, et tahad veebilehe sisu muuta. Provisioner ei käivitu automaatselt, sest ressurss on juba loodud. Lahendus on muuta trigger'it.

Muuda `main.tf` failis:

```hcl
  triggers = {
    version = "2"  # Muutsime 1 -> 2
  }
```

Nüüd käivita:

```powershell
terraform apply -auto-approve
```

Terraform näeb, et trigger muutus, ja käivitab provisioner'i uuesti. See on kasulik, kui tahad uuesti deploy'da ilma ressurssi kustutamata.

Kui tahad, et provisioner käivituks **iga kord** (iga `apply` korral), kasuta:

```hcl
  triggers = {
    always = timestamp()
  }
```

`timestamp()` tagastab praeguse aja, mis on iga kord erinev, seega trigger muutub alati.

---

## OSA 5: File Provisioner

Eelmises osas lõime veebilehe sisu otse remote-exec käsus `echo` abil. See töötab, aga pole mugav pikemate failide puhul. File provisioner võimaldab kopeerida faile sinu arvutist serverisse.

### 5.1 Ettevalmistus - loo failid ENNE Terraformi

**Oluline:** Failid peavad eksisteerima enne `terraform plan` käivitamist! Terraform kontrollib failide olemasolu juba planeerimisel.

```powershell
mkdir files
```

Loo fail `files/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Terraform Deploy</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 40px 60px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 {
            color: #00ff88;
            margin: 0 0 20px 0;
            font-size: 2.5em;
        }
        .info {
            background: rgba(0,255,136,0.1);
            padding: 10px 20px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 3px solid #00ff88;
        }
        p { margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Deployed by Terraform!</h1>
        <div class="info">
            <p><strong>Server:</strong> Ubuntu-1</p>
            <p><strong>Method:</strong> File Provisioner</p>
        </div>
        <p style="margin-top: 20px; opacity: 0.7;">Infrastructure as Code in action</p>
    </div>
</body>
</html>
```

See on ilusam veebileht kui eelmine! CSS stiilid teevad selle visuaalselt atraktiivsemaks.

### 5.2 main.tf file provisioner'iga

Asenda kogu `main.tf` sisu:

```hcl
terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

variable "target_host" {
  description = "Ubuntu serveri IP-aadress"
  type        = string
  default     = "10.0.208.20"
}

variable "ssh_user" {
  description = "SSH kasutajanimi"
  type        = string
  default     = "kasutaja"
}

variable "ssh_private_key" {
  description = "SSH privaatvõtme asukoht"
  type        = string
  default     = "~/.ssh/id_ed25519"
}

resource "null_resource" "web_deploy" {
  # Trigger: kui HTML fail muutub, deploy uuesti
  triggers = {
    html_hash = filemd5("${path.module}/files/index.html")
  }

  connection {
    type        = "ssh"
    host        = var.target_host
    user        = var.ssh_user
    private_key = file(pathexpand(var.ssh_private_key))
    timeout     = "2m"
  }

  # Esimene samm: kopeeri fail serverisse
  provisioner "file" {
    source      = "${path.module}/files/index.html"
    destination = "/tmp/index.html"
  }

  # Teine samm: paigalda Nginx ja liiguta fail õigesse kohta
  provisioner "remote-exec" {
    inline = [
      "echo '>>> Kontrollin Nginx olemasolu...'",
      "if ! command -v nginx &> /dev/null; then",
      "  echo '>>> Paigaldan Nginx...'",
      "  sudo apt-get update -qq",
      "  sudo apt-get install -y -qq nginx",
      "fi",

      "echo '>>> Kopeerin veebilehe...'",
      "sudo mv /tmp/index.html /var/www/html/index.html",
      "sudo chown www-data:www-data /var/www/html/index.html",

      "echo '>>> Taaskäivitan Nginx...'",
      "sudo systemctl restart nginx",

      "echo '>>> Valmis!'"
    ]
  }
}

output "web_url" {
  value = "Veebileht: http://${var.target_host}"
}

output "deployed_file_hash" {
  description = "Deploy'tud faili MD5 hash"
  value       = filemd5("${path.module}/files/index.html")
}
```

Uued elemendid:

**filemd5()** arvutab faili MD5 räsi. Kui fail muutub, muutub ka räsi, mis omakorda muudab trigger'it. See on elegantsem kui manuaalne versiooni number - sa ei pea meeles pidama versiooni suurendamist.

**provisioner "file"** kopeerib faili kohalikust arvutist serverisse. `source` on kohalik tee, `destination` on tee serveris. Pane tähele, et kopeerime `/tmp/` kausta, mitte otse `/var/www/html/` - see on seetõttu, et meil pole õigusi otse sinna kirjutada. Pärast kopeerimist liigutame faili `sudo mv` abil.

**Provisioner'ite järjekord** on oluline! File provisioner käivitub enne remote-exec'i, sest see on esimesena defineeritud.

### 5.3 Käivitamine

Kustuta vana ressurss (kui on) ja käivita:

```powershell
terraform destroy -auto-approve
terraform apply -auto-approve
```

Näed, kuidas Terraform kopeerib faili ja seadistab serveri. Ava brauseris:

```
http://10.0.208.20
```

Näed oma kena uut veebilehte!

### 5.4 Automaatne re-deploy faili muutumisel

Nüüd tuleb magic - muuda `files/index.html` faili. Näiteks muuda pealkiri:

```html
<h1>🚀 Updated by Terraform!</h1>
```

Käivita plan:

```powershell
terraform plan
```

Terraform näitab, et trigger muutus:

```
  # null_resource.web_deploy must be replaced
-/+ resource "null_resource" "web_deploy" {
      ~ triggers = {
          ~ "html_hash" = "abc123..." -> "def456..."
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

Hash on erinev, seega Terraform tahab ressursi uuesti luua. Rakenda:

```powershell
terraform apply -auto-approve
```

Värskenda brauserit - näed uut pealkirja! See on Infrastructure as Code võlu: muudad faili, käivitad `terraform apply`, ja muudatus on serveris.

**Validation:**
- [ ] `files/index.html` eksisteerib ENNE terraform plan
- [ ] File provisioner kopeerib faili serverisse
- [ ] Veebileht on nähtav brauseris
- [ ] HTML faili muutmine triggerib automaatse re-deploy

---

## OSA 6: Puhastamine

Labori lõpus kustutame loodud ressursid:

```powershell
terraform destroy -auto-approve
```

See kustutab `null_resource`'i Terraformi state'ist. Aga pane tähele: **Nginx jääb Ubuntu serverisse alles!** Terraform ei tea, kuidas Nginxi eemaldada, sest ta ei loonud Nginxi kui ressurssi - ta ainult käivitas paigalduskäsu provisioner'i kaudu.

See on oluline mõista: provisioner'id on "fire-and-forget" - Terraform käivitab käsud, aga ei halda nende tulemusi. Kui tahad Nginx eemaldada:

```powershell
ssh kasutaja@10.0.208.20 "sudo apt-get remove -y nginx && sudo rm -rf /var/www/html/*"
```

Või jäta Nginx alles järgmisteks laboriteks!

---

## Troubleshooting

### SSH Connection Timeout

```
Error: timeout - last error: dial tcp 10.0.208.20:22: i/o timeout
```

See tähendab, et Terraform ei saa serveriga ühendust. Kontrolli:

```powershell
ping 10.0.208.20
ssh kasutaja@10.0.208.20 "echo OK"
```

Võimalikud põhjused:
- Ubuntu server pole käivitatud
- Vale IP-aadress
- Tulemüür blokeerib ühendust
- SSH teenus ei tööta serveris

### Permission Denied (publickey)

```
Error: ssh: handshake failed: ssh: unable to authenticate
```

SSH võti ei tööta. Kontrolli:

```powershell
cat ~/.ssh/id_ed25519.pub
ssh kasutaja@10.0.208.20 "cat ~/.ssh/authorized_keys"
```

Kas sinu avalik võti on serveri `authorized_keys` failis?

### File Not Found (filemd5)

```
Error: Invalid function argument: no file exists at "files/index.html"
```

Fail peab eksisteerima ENNE `terraform plan` käivitamist. Loo fail ja proovi uuesti.

### Provisioner Error (exit code 1)

```
Error: remote-exec provisioner error: Process exited with status 1
```

Mingi käsk ebaõnnestus. Debug:

1. Testi käsku otse SSH kaudu:
```powershell
ssh kasutaja@10.0.208.20 "sudo apt-get update"
```

2. Lisa provisioner'isse debug:
```hcl
provisioner "remote-exec" {
  inline = [
    "set -x",  # Näita iga käsku enne käivitamist
    "set -e",  # Peatu esimesel veal
    # ... ülejäänud käsud
  ]
}
```

---

## Kontrollnimekiri

### OSA 1-2: Local Setup
- [ ] Terraform paigaldatud ja töötab
- [ ] Local provider töötab
- [ ] Init → plan → apply → destroy tsükkel on selge
- [ ] State faili roll on arusaadav

### OSA 3: Variables ja Outputs
- [ ] Muutujad töötavad vaikeväärtustega
- [ ] Muutujaid saab anda käsurealt ja tfvars failist
- [ ] Outputs kuvatakse pärast apply'd
- [ ] Validation annab selge vea vale väärtuse korral

### OSA 4-5: Remote Provisioning
- [ ] SSH ühendus Ubuntu serveriga töötab
- [ ] `null_resource` + `remote-exec` töötab
- [ ] Nginx on paigaldatud ja veebileht töötab
- [ ] File provisioner kopeerib faile
- [ ] Trigger hash võimaldab automaatset re-deploy

---

## Järgmised sammud

**Kodutöö:** Loo projekt, mis deploy'b teise Ubuntu serverile (Ubuntu-2, teine IP) erineva veebilehega.

**Lisalugemine:**
- [Terraform Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)
- [Terraform Variables](https://developer.hashicorp.com/terraform/language/values/variables)
- [Local Provider Docs](https://registry.terraform.io/providers/hashicorp/local/latest/docs)

**Edasi:** Järgmistes tundides õpid remote state'i (kuidas meeskond jagab state'i), mooduleid (kuidas koodi taaskasutada) ja päris pilve ressursse (AWS, Azure).
