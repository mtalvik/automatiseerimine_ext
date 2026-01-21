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

Miks me alustame just sellise failiga? Terraform vajab alati kahte asja: **provider'i konfiguratsioon** (kellega suhtleme) ja **ressursside definitsioonid** (mida loome). Alustame mõlemaga korraga, et näha täielikku pilti.

Loo VSCode's uus fail nimega `main.tf`:

```hcl
# =============================================================================
# TERRAFORM SEADED JA PROVIDER
# =============================================================================
# Iga Terraform projekt algab sellega, et ütleme milliseid provider'eid vajame.
# Provider on plugin, mis "räägib" mingi platvormiga - AWS, Azure, või nagu
# meie puhul, kohaliku failisüsteemiga.

terraform {
  required_providers {
    # "local" on provider'i nimi, mida kasutame koodis
    local = {
      source  = "hashicorp/local"  # Kust Terraform selle laeb (Registry)
      version = "~> 2.4"           # ~> tähendab: 2.4, 2.5, 2.9 OK, aga 3.0 mitte
    }
  }
}

# =============================================================================
# RESSURSID - MIDA ME LOOME
# =============================================================================
# resource on Terraform'i põhielement - iga ressurss on üks "asi" mida hallata.
# Süntaks: resource "TÜÜP" "NIMI" { seaded }
#   - TÜÜP: tuleb provider'ist, määrab mida loome (local_file = fail)
#   - NIMI: sina valid, kasutatakse viitamiseks teistes kohtades

# Esimene fail - lihtne tekstifail
resource "local_file" "greeting" {
  # ${path.module} = kaust kus see .tf fail asub
  # Terraform loob "output" kausta automaatselt kui seda pole
  filename = "${path.module}/output/hello.txt"
  
  # Faili sisu - \n tähendab uut rida
  content  = "Tere, Terraform!\nSee fail on loodud IaC-ga.\n"
}

# Teine fail - konfiguratsioonifail
resource "local_file" "config" {
  filename = "${path.module}/output/app.conf"
  
  # <<-EOT on "heredoc" - võimaldab kirjutada mitut rida
  # ilma \n märkideta. Loetavam kui "rida1\nrida2\nrida3"
  # EOT = End Of Text (võid kasutada mis tahes sõna, nt EOF)
  content  = <<-EOT
    server {
      port = 8080
      host = "localhost"
    }
  EOT
}
```

**Miks just nii?**

Provider'i plokk on nagu `import` või `require` teistes keeltes - ütled Terraformile, mida vajad. Versioonipiirang `~> 2.4` on oluline: see lubab automaatseid uuendusi (2.5, 2.6...), aga kaitseb sind breaking change'ide eest versioon 3.0-s.

Ressursside nimed (`greeting`, `config`) on sinu valitud. Need on olulised, sest hiljem viitad neile kujul `local_file.greeting.filename` - näiteks kui tahad ühe ressursi väljundit kasutada teise sisendina.

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

Miks eraldi fail? Terraform loeb kõik `.tf` failid kaustast, seega võiksime kõik panna `main.tf`-i. Aga eraldi `variables.tf` teeb koodi loetavamaks - keegi kes tahab muuta seadeid, leiab need kohe üles.

Loo fail `variables.tf`:

```hcl
# =============================================================================
# SISENDMUUTUJAD (Input Variables)
# =============================================================================
# Muutujad teevad konfiguratsiooni taaskasutatavaks.
# Sama kood töötab dev, test ja prod keskkonnas - muudad ainult muutujaid.

# Keskkonna muutuja - määrab kas dev, test või prod
variable "environment" {
  description = "Keskkonna nimi (dev/test/prod)"  # Dokumentatsioon teistele
  type        = string                             # Andmetüüp: string, number, bool, list, map
  default     = "dev"                              # Vaikeväärtus kui kasutaja ei anna

  # Validation tagab, et keegi ei pane "banana" keskkkonnaks
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment peab olema: dev, test või prod."
  }
}

# Rakenduse nimi - kasutatakse failinimedes
variable "app_name" {
  description = "Rakenduse nimi"
  type        = string
  default     = "myapp"
}

# Port number - näitab kuidas number tüüp töötab
variable "port" {
  description = "Rakenduse port"
  type        = number    # number, mitte string! Terraform kontrollib tüüpi
  default     = 8080

  # Kontrollime, et port oleks mõistlikus vahemikus
  # && on "ja" operaator - mõlemad tingimused peavad olema tõesed
  validation {
    condition     = var.port > 1024 && var.port < 65535
    error_message = "Port peab olema vahemikus 1025-65534."
  }
}
```

**Miks validation on oluline?**

Ilma validatsioonita saaksid vea alles `apply` ajal, võib-olla keset deploy'd. Validatsioon tabab vead kohe `plan` ajal ja annab selge eestikeelse teate. See säästab aega ja peavalu.

### 3.3 main.tf muutujatega

Nüüd kasutame defineeritud muutujaid ressurssides. Muutujatele viitamine käib `var.nimi` süntaksiga.

Loo fail `main.tf`:

```hcl
# Provider jääb samaks nagu enne
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

# =============================================================================
# RESSURSID MUUTUJATEGA
# =============================================================================
# Nüüd kasutame var.xxx muutujaid hardcoded väärtuste asemel.
# ${var.nimi} - kui muutuja on stringi sees
# var.nimi - kui muutuja on eraldi väärtus

resource "local_file" "greeting" {
  filename = "${path.module}/output/hello.txt"
  
  # Muutujad stringi sees - kasuta ${var.xxx} süntaksit
  content  = <<-EOT
    Tere tulemast ${var.app_name} rakendusse!
    Keskkond: ${var.environment}
    Port: ${var.port}
  EOT
}

resource "local_file" "config" {
  # Failinimi sisaldab nüüd rakenduse nime JA keskkonda
  # dev: myapp-dev.conf, prod: myapp-prod.conf
  # Nii saad hoida erinevaid keskkondi koos ilma konfliktita
  filename = "${path.module}/output/${var.app_name}-${var.environment}.conf"
  
  content  = <<-EOT
    # ${var.app_name} Configuration
    # Environment: ${var.environment}
    # Genereeritud Terraformiga

    server {
      port = ${var.port}
      host = "localhost"
      env  = "${var.environment}"
    }
  EOT
}
```

**Miks muutujad failinimes?**

`${var.app_name}-${var.environment}.conf` tähendab, et sama koodiga saad luua `myapp-dev.conf`, `myapp-test.conf` ja `myapp-prod.conf` - ainult muutuja väärtust muutes. See on taaskasutuse võlu.

### 3.4 outputs.tf - Väljundite defineerimine

Outputs on vastupidised muutujatele: muutujad on SISEND (annad väärtused Terraformile), outputs on VÄLJUND (Terraform annab sulle infot). Outputs on kasulik näiteks siis, kui Terraform loob serveri ja tahad teada selle IP-aadressi.

Loo fail `outputs.tf`:

```hcl
# =============================================================================
# VÄLJUNDID (Outputs)
# =============================================================================
# Outputs näitavad infot pärast apply'd.
# Kasulik: IP-aadressid, URL-id, failide teed, jne.
# Neid saab lugeda käsurealt: terraform output
# Või JSON formaadis skriptide jaoks: terraform output -json

# Lihtne output - ainult üks väärtus
output "config_file_path" {
  description = "Loodud config faili asukoht"
  # local_file.config viitab ressursile main.tf-st
  # .filename on selle ressursi atribuut
  value       = local_file.config.filename
}

output "greeting_file_path" {
  description = "Tervitusfaili asukoht"
  value       = local_file.greeting.filename
}

# Keerulisem output - mitu väärtust koos (object)
# See on mugav kui tahad kõik olulise info ühes kohas
output "summary" {
  description = "Deployment kokkuvõte"
  value = {
    app         = var.app_name                   # Sisendmuutuja väärtus
    environment = var.environment                # Sisendmuutuja väärtus
    port        = var.port                       # Sisendmuutuja väärtus
    config_path = local_file.config.filename     # Ressursi atribuut
  }
}
```

**Miks outputs on kasulik?**

1. **Pärast apply'd:** Näed kohe loodud failide asukohti
2. **Skriptides:** `terraform output -json summary` annab JSON-i, mida saad parserida
3. **Moodulites:** Kui kasutad seda koodi moodulina, saavad teised moodulid outputs'idele ligi

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

> **Märkus:** HashiCorp soovitab provisioner'ite asemel kasutada Ansibled (mida juba tunnete). Provisioner'id on "last resort". Meie kasutame neid õppimiseks, sest need näitavad Terraformi võimalusi.

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

Siin tuleb mitu uut kontseptsiooni korraga, aga ära muretse - käime need läbi samm-sammult. Põhiidee on lihtne: Terraform ühendub SSH kaudu serveriga ja käivitab seal käsud.

Loo fail `main.tf`:

```hcl
# =============================================================================
# PROVIDER: NULL
# =============================================================================
# "null" provider on eriline - ta ei loo midagi päriselt.
# Tema ainus eesmärk on pakkuda "null_resource" ressurssi,
# mis on konteiner provisioner'itele.
# Päris elus kasutaksid aws_instance, azurerm_virtual_machine jne.

terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

# =============================================================================
# MUUTUJAD SSH ÜHENDUSEKS
# =============================================================================
# Paneme SSH andmed muutujatesse, et oleks lihtne muuta
# (näiteks kui tahad testida teise serveriga)

variable "target_host" {
  description = "Ubuntu serveri IP-aadress"
  type        = string
  default     = "10.0.208.20"    # Ubuntu-1 IP sinu labori võrgus
}

variable "ssh_user" {
  description = "SSH kasutajanimi"
  type        = string
  default     = "kasutaja"       # Muuda kui sinu kasutaja on teine
}

variable "ssh_private_key" {
  description = "SSH privaatvõtme asukoht"
  type        = string
  default     = "~/.ssh/id_ed25519"  # Windowsis: C:\Users\SINU_NIMI\.ssh\id_ed25519
}

# =============================================================================
# NULL RESOURCE + PROVISIONER
# =============================================================================
# null_resource ei loo midagi - ta on lihtsalt "konteiner" provisioner'itele.
# Provisioner on kood, mis käivitub ressursi loomisel.

resource "null_resource" "system_info" {
  
  # CONNECTION: Kuidas Terraform serveriga ühendub
  # -------------------------------------------------
  # See plokk ütleb Terraformile SSH ühenduse parameetrid.
  # Ilma selleta ei tea Terraform, kuhu ühenduda.
  connection {
    type        = "ssh"                                      # SSH (Linux) või WinRM (Windows)
    host        = var.target_host                            # IP-aadress
    user        = var.ssh_user                               # Kasutajanimi
    private_key = file(pathexpand(var.ssh_private_key))      # SSH võtme SISU (mitte tee!)
    timeout     = "2m"                                       # Kui kaua oodata ühendust
  }
  # MIKS pathexpand()? Windows'is ei tööta ~ alati.
  # pathexpand("~/.ssh/id") -> "C:/Users/kasutaja/.ssh/id"
  #
  # MIKS file()? Connection tahab võtme SISU, mitte failiteed.
  # file() loeb faili ja tagastab selle sisu stringina.

  # REMOTE-EXEC: Käsud, mis käivitatakse serveris
  # -------------------------------------------------
  # inline = nimekiri käskudest, käivitatakse järjest
  provisioner "remote-exec" {
    inline = [
      # Iga string on üks käsk, mis käivitub Ubuntu serveris
      "echo '=== System Info ==='",
      "hostname",                              # Serveri nimi
      "whoami",                                # Praegune kasutaja
      "uname -a",                              # Kerneli info
      "echo ''",
      "echo '=== Network ==='",
      "ip -4 addr show | grep 'inet ' | head -2",  # IP-aadressid
      "echo ''",
      "echo '=== Disk ==='",
      "df -h / | tail -1",                     # Kettakasutus
      "echo ''",
      "echo '=== Done ==='"
    ]
  }
}

# Output kinnitab, et kõik õnnestus
output "status" {
  value = "SSH ühendus serveriga ${var.target_host} õnnestus!"
}
```

**Mida see kood teeb samm-sammult:**

1. **Provider** - laeme `null` provider'i, mis annab meile `null_resource`
2. **Muutujad** - defineerime SSH ühenduse andmed (IP, kasutaja, võti)
3. **Connection** - ütleme Terraformile, kuidas SSH-ga ühenduda
4. **Remote-exec** - nimekiri käskudest, mis käivitatakse serveris

**Miks `file(pathexpand(...))` kombinatsioon?**

- `pathexpand("~/.ssh/id_ed25519")` → `C:/Users/kasutaja/.ssh/id_ed25519`
- `file("C:/Users/...")` → loeb faili sisu stringina

Connection vajab võtme **sisu**, mitte failiteed. Seega loeme faili ja anname sisu.

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

Nüüd teeme midagi kasulikku - paigaldame Nginx veebiserveri ja loome lihtsa veebilehe. See näitab, kuidas Terraform saab serverisse tarkvara paigaldada.

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

# Samad muutujad nagu enne
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
  
  # ==========================================================================
  # TRIGGERS - Millal käivitub uuesti?
  # ==========================================================================
  # Probleem: provisioner käivitub ainult ressursi LOOMISEL.
  # Kui ressurss on juba olemas, ei käivitu ta uuesti.
  #
  # Lahendus: triggers. Kui trigger'i väärtus muutub,
  # loeb Terraform seda kui "ressurss on muutunud" ja loob uuesti.
  #
  # Muuda "1" -> "2" kui tahad uuesti deploy'da ilma destroy'ta.
  triggers = {
    version = "1"
  }

  connection {
    type        = "ssh"
    host        = var.target_host
    user        = var.ssh_user
    private_key = file(pathexpand(var.ssh_private_key))
    timeout     = "5m"    # Pikem timeout, sest apt install võtab aega
  }

  # ==========================================================================
  # NGINX PAIGALDAMINE JA SEADISTAMINE
  # ==========================================================================
  # Iga käsk käivitub Ubuntu serveris järjest.
  # Kui üks käsk ebaõnnestub (exit code != 0), peatub kogu protsess.
  provisioner "remote-exec" {
    inline = [
      # Samm 1: Uuenda pakettide nimekiri
      # -qq = quiet mode, vähem väljundit
      "echo '>>> Uuendan pakettide nimekirja...'",
      "sudo apt-get update -qq",

      # Samm 2: Paigalda Nginx
      # -y = vastab automaatselt "yes" küsimustele
      "echo '>>> Paigaldan Nginx...'",
      "sudo apt-get install -y -qq nginx",

      # Samm 3: Loo custom veebileht
      # $(hostname) ja $(date) täidetakse serveris
      # tee kirjutab stdin'i faili (sudo õigustega)
      # > /dev/null peidab tee väljundi
      "echo '>>> Loon custom veebilehe...'",
      "echo '<html><body style=\"font-family: Arial; text-align: center; padding: 50px;\"><h1>Deployed by Terraform!</h1><p>Server: '$(hostname)'</p><p>Time: '$(date)'</p></body></html>' | sudo tee /var/www/html/index.html > /dev/null",

      # Samm 4: Käivita ja luba Nginx
      # enable = käivitub automaatselt serveri reboot'il
      # restart = käivita kohe
      "echo '>>> Käivitan Nginx...'",
      "sudo systemctl enable nginx",
      "sudo systemctl restart nginx",

      # Samm 5: Kontrolli, et töötab
      # curl localhost loeb veebilehe sisu
      # grep -o otsib ainult h1 tag'i
      "echo '>>> Kontrollin...'",
      "curl -s http://localhost | grep -o '<h1>.*</h1>'",

      "echo '>>> Valmis!'"
    ]
  }
}

# Outputs näitavad kuidas ligi pääseda
output "web_url" {
  value = "Veebileht: http://${var.target_host}"
}

output "ssh_command" {
  value = "SSH: ssh ${var.ssh_user}@${var.target_host}"
}
```

**Mis muutus võrreldes eelmisega?**

1. **triggers** - uus plokk, mis kontrollib millal provisioner uuesti käivitub
2. **Pikem timeout** - apt install võtab aega, 2 minutit ei pruugi piisata
3. **Päris käsud** - apt update, apt install, systemctl

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

File provisioner kopeerib faile sinu arvutist serverisse. See on palju mugavam kui pikad `echo` käsud, eriti suuremate failide puhul. Vaatame, kuidas see töötab.

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
  
  # ==========================================================================
  # TRIGGER: filemd5() - automaatne redeploy kui fail muutub
  # ==========================================================================
  # filemd5() arvutab faili MD5 räsi (checksum).
  # Kui fail muutub, muutub räsi, trigger muutub, ressurss luuakse uuesti.
  #
  # See on PAREM kui manuaalne version = "1", "2", "3"...
  # sest sa ei pea meeles pidama versiooni muutmist.
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

  # ==========================================================================
  # FILE PROVISIONER - kopeeri fail serverisse
  # ==========================================================================
  # source = kohalik fail (WinKlient)
  # destination = asukoht serveris (Ubuntu)
  #
  # MIKS /tmp/? Sest meil pole õigust otse /var/www/html/ kirjutada.
  # Kopeerime /tmp/ ja liigutame siis sudo'ga.
  provisioner "file" {
    source      = "${path.module}/files/index.html"   # Sinu arvutist
    destination = "/tmp/index.html"                    # Serverisse /tmp/
  }

  # ==========================================================================
  # REMOTE-EXEC - liiguta fail õigesse kohta ja käivita Nginx
  # ==========================================================================
  # Provisioner'id käivituvad JÄRJEKORRAS.
  # Kõigepealt file (kopeeri), siis remote-exec (seadista).
  provisioner "remote-exec" {
    inline = [
      # Kontrolli kas Nginx on olemas, paigalda kui pole
      # command -v kontrollib kas käsk eksisteerib
      # &> /dev/null peidab väljundi
      "echo '>>> Kontrollin Nginx olemasolu...'",
      "if ! command -v nginx &> /dev/null; then",
      "  echo '>>> Paigaldan Nginx...'",
      "  sudo apt-get update -qq",
      "  sudo apt-get install -y -qq nginx",
      "fi",

      # Liiguta fail /tmp/ -> /var/www/html/
      # mv on kiirem kui cp + rm
      "echo '>>> Kopeerin veebilehe...'",
      "sudo mv /tmp/index.html /var/www/html/index.html",
      
      # Muuda omanik www-data'ks (Nginx kasutaja)
      "sudo chown www-data:www-data /var/www/html/index.html",

      # Taaskäivita Nginx, et muudatused rakenduks
      "echo '>>> Taaskäivitan Nginx...'",
      "sudo systemctl restart nginx",

      "echo '>>> Valmis!'"
    ]
  }
}

# Outputs
output "web_url" {
  value = "Veebileht: http://${var.target_host}"
}

output "deployed_file_hash" {
  description = "Deploy'tud faili MD5 hash"
  value       = filemd5("${path.module}/files/index.html")
}
```

**Miks just selline struktuur?**

1. **filemd5() trigger** - automaatne redeploy kui fail muutub, ei pea ise meeles pidama
2. **File provisioner** - kopeerib faili, palju lihtsam kui pikad echo käsud
3. **Kahe-sammuline protsess** - kopeeri /tmp/, liiguta sudo'ga - sest otse kirjutamiseks pole õigusi
4. **Provisioner'ite järjekord** - file ENNE remote-exec, vastasel juhul poleks faili mida liigutada

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
