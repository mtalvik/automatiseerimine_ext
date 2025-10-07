# Terraform Labor: Infrastruktuur Koodina

**Eeldused:** Linux CLI põhiteadmised, teksteditori kasutamine

**Platvorm:** Terraform 1.0+ (kohalik)

## Õpiväljundid

Pärast seda labori õpilane:

- Käivitab Terraform workflow'i: init, plan, apply, destroy
- Loob kohalikke ressursse kasutades local provider'it
- Rakendab variables ja outputs dünaamiliseks konfiguratsiooniks
- Mõistab state faili rolli infrastruktuuri jälgimisel
- Debugib levinud probleeme Terraform'i kasutamisel

---

## 1. Terraform'i Installimine ja Seadistamine

Alustame Terraform'i installimisega teie operatsioonisüsteemi. Terraform on kompileeritud binaarfail, mis ei vaja eraldi runtime'i ega dependency'sid. See teeb installimise lihtsaks ning töötab ühesuguselt erinevates platvormides.

### macOS installimine

macOS'is on lihtsaim viis kasutada Homebrew pakettide haldurit. Kui teil Homebrew veel paigaldatud ei ole, installige see esmalt järgides juhiseid aadressil brew.sh. Seejärel saate Terraform'i installida ühe käsuga.
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Kontrollige installatsiooni õnnestumist versiooni kontrollimisega:
```bash
terraform --version
```

Peaksite nägema väljundit sarnaselt: `Terraform v1.6.0`. Kui saate veateate "command not found", kontrollige PATH muutujat või proovige terminali uuesti käivitada.

### Linux installimine

Linux süsteemidele on Terraform saadaval läbi ametliku HashiCorp repository. Debian/Ubuntu perede puhul lisame esmalt HashiCorp GPG võtme ja repository, seejärel installime paketi.
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install terraform
```

RHEL/CentOS/Fedora süsteemides kasutatakse yum või dnf:
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum install terraform
```

Kontrollige installatsiooni:
```bash
terraform --version
```

### Windows installimine

Windows puhul on kaks peamist võimalust: Chocolatey paketihaldur või manuaalne installimine. Chocolatey kasutamine on lihtsam ja võimaldab automaatselt uuendusi.

Chocolatey kasutamiseks avage PowerShell administraatori õigustega ja käivitage:
```powershell
choco install terraform
```

Manuaalseks installimiseks laadige binaarfail alla HashiCorp veebilehelt, ekstraktige see ja lisage PATH muutujasse. Seejärel avage uus terminal ning kontrollige:
```powershell
terraform --version
```

### Projekti kataloogi ettevalmistamine

Pärast Terraform'i installimist loome töökataloogi meie esimese projekti jaoks. See kaust hoiab kõiki Terraform'i konfiguratsioonifaile ning state'd.
```bash
mkdir ~/terraform-basics-lab
cd ~/terraform-basics-lab
```

Loome ka mõned alamkaustad organisatsiooni jaoks, kuigi need ei ole kohustuslikud:
```bash
mkdir -p configs scripts
```

Kontrollime, et Terraform töötab ja näeme saadaolevaid käske:
```bash
terraform --help
```

Väljund näitab kõiki Terraform'i põhikäske koos lühikese kirjeldusega. Põhilised käsud, mida kasutame, on `init`, `plan`, `apply` ja `destroy`.

**Validation:**
- [ ] `terraform --version` näitab versiooni numbrit
- [ ] Töökaust on loodud ja te olete selles
- [ ] `terraform --help` kuvab käskude nimekirja

---

## 2. Esimene Terraform Konfiguratsioon

Nüüd loome oma esimese Terraform'i konfiguratsiooni. Alustame võimalikult lihtsalt, et mõista põhiprintsiipe ilma liigse keerukuseta.

### Provider konfiguratsiooni loomine

Loome faili `main.tf`, mis sisaldab meie Terraform'i koodi. Esimene asi, mida vajame, on provider konfiguratsioon. Provider ütleb Terraform'ile, milliseid teenuseid kavatseme kasutada.
```bash
nano main.tf
```

Sisestage järgmine kood:
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}
```

See plokk määrab kaks olulist asja. Esiteks, millist Terraform'i versiooni me vajame (1.0 või uuem). Teiseks, millist provider'it kasutame. Local provider võimaldab meil luua faile ja katalooge kohalikus failisüsteemis, mis on ideaalne õppimiseks.

### Esimese ressursi loomine

Nüüd lisame lihtsa ressursi - tekstifaili loomise. Lisage `main.tf` faili juurde:
```hcl
resource "local_file" "hello" {
  content  = "Tere! See fail on loodud Terraform'i abil."
  filename = "${path.module}/hello.txt"
}
```

Resource plokk koosneb neljast osast. Võtmesõna `resource` ütleb Terraform'ile, et soovime midagi luua. `local_file` on ressursi tüüp, mis määrab, et loome kohaliku faili. `hello` on meie valitud nimi, mida saame kasutada selle ressurssi viitamiseks. Ploki sisu kirjeldab, milline see fail peaks olema.

`path.module` on sisseehitatud muutuja, mis viitab kaustal, kus praegune `.tf` fail asub. Selle kasutamine tagab, et fail luuakse õigesse kohta sõltumata sellest, kust Terraform'i käivitatakse.

Salvestage fail (Ctrl+O, Enter, Ctrl+X nano's).

### Terraform'i initsialiseerimine

Enne kui saame oma konfiguratsiooni kasutada, peame Terraform'i initsialiseerima. See laeb alla vajaliku local provider'i ja valmistab töökataloogi ette.
```bash
terraform init
```

Näete väljundit, mis kirjeldab, mida Terraform teeb. See loob `.terraform` kausta ja laeb sinna local provider'i plugina. Selle kausta sisu on masinloetav ja seda pole vaja versioonihaldusesse panna.

Initsialisatsioon lõpeb sõnumiga "Terraform has been successfully initialized!" kui kõik läks hästi. Kui saite veateate, kontrollige, kas `main.tf` fail on õigesti vormindatud ning sisaldab kõiki vajalikke plokke.

**Validation:**
- [ ] `.terraform` kaust on loodud
- [ ] `.terraform.lock.hcl` fail on loodud
- [ ] Init lõppes edukalt ilma vigadeta

### Planeerimine enne rakendamist

Järgmine samm on planeerimis faas. See näitab meile, mida Terraform kavatseb teha, ilma midagi tegelikult muutmata. Planeerimine on oluline turvaline mehhanism.
```bash
terraform plan
```

Väljund peaks näitama midagi sellist:
```
Terraform will perform the following actions:

  # local_file.hello will be created
  + resource "local_file" "hello" {
      + content              = "Tere! See fail on loodud Terraform'i abil."
      + filename             = "./hello.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Plussmärk ressursi ees tähendab, et see luuakse. Veel pole midagi juhtunud - see on ainult plaan. Terraform ütleb meile, et kavatseb luua ühe faili. Mõned atribuudid nagu `id` on märgitud "known after apply", sest neid ei saa ette teada enne kui ressurss tõesti luuakse.

### Muudatuste rakendamine

Nüüd oleme valmis oma plaani teostama. Käsk `apply` viib muudatused ellu.
```bash
terraform apply
```

Terraform näitab uuesti plaani ja küsib kinnitust. See on viimane kontrollpunkt enne muudatuste tegemist. Tippige `yes` ja vajutage Enter.

Peaksite nägema:
```
local_file.hello: Creating...
local_file.hello: Creation complete after 0s

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Kontrollige, kas fail loodi:
```bash
ls -la hello.txt
cat hello.txt
```

Peaksite nägema faili sisuga "Tere! See fail on loodud Terraform'i abil."

**Validation:**
- [ ] `hello.txt` fail on loodud
- [ ] Faili sisu on õige
- [ ] `terraform.tfstate` fail on loodud
- [ ] Apply lõppes edukalt

---

## 3. State Faili Mõistmine

Märkasite tõenäoliselt, et apply käsu järel loodi fail nimega `terraform.tfstate`. See on Terraform'i state fail ja see on kriitilise tähtsusega Terraform'i töös.

### State faili uurimine

Vaatame state faili sisu:
```bash
cat terraform.tfstate
```

See on JSON vormingus fail, mis sisaldab teavet kõigi Terraform'i poolt hallatud ressursside kohta. Näete seal meie `local_file.hello` ressursi koos kõigi tema atribuutidega.

State fail on Terraform'i "mälu". Ilma selleta ei teaks Terraform, mis on juba olemas. Iga kord kui käivitate `terraform plan` või `apply`, loeb Terraform state faili, et kindlaks teha, mis on muutunud ja mida on vaja teha.

Proovime näha state'd inimloetaval kujul:
```bash
terraform show
```

See kuvab sama info, aga vormindatult ja loetavamalt. Näete ressursi tüüpi, nime ja kõiki atribuute.

### Ressursside loend

State failist saame küsida, milliseid ressursse Terraform haldab:
```bash
terraform state list
```

Väljund on lihtne nimekiri: `local_file.hello`. Kui meil oleks rohkem ressursse, näeksime neid kõiki siin.

### State'i värskendamine

Kujutage ette, et keegi muudab fail käsitsi väljaspool Terraform'i. Terraform ei tea sellest midagi, sest ta loeb ainult state faili. Saame state'i värskendada:
```bash
terraform refresh
```

See käsk loeb reaalsed ressursid ja uuendab state faili, kui leiab erinevusi. Praktikas see käsk on harva vajalik, sest `plan` ja `apply` teevad seda automaatselt.

**Validation:**
- [ ] `terraform.tfstate` fail eksisteerib
- [ ] `terraform show` kuvab ressurssi
- [ ] `terraform state list` näitab `local_file.hello`

---

## 4. Variables ja Dünaamiline Konfiguratsioon

Siiani olid kõik väärtused kõvakodeeritud `main.tf` failis. See ei ole paindlik - kui tahame muuta faili nime või sisu, peame koodi muutma. Variables võimaldavad eraldada konfiguratsioonid koodist.

### Variables faili loomine

Loome uue faili variables muutujate jaoks:
```bash
nano variables.tf
```

Lisame mõned kasulikud muutujad:
```hcl
variable "project_name" {
  description = "Projekti nimi, kasutatakse failide nimetamisel"
  type        = string
  default     = "terraform-basics"
  
  validation {
    condition     = length(var.project_name) > 3
    error_message = "Projekti nimi peab olema vähemalt 4 tähemärki pikk."
  }
}

variable "environment" {
  description = "Keskkond (development, staging, production)"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Keskkond peab olema: development, staging või production."
  }
}

variable "file_count" {
  description = "Mitu näidisfaili luua"
  type        = number
  default     = 3
  
  validation {
    condition     = var.file_count > 0 && var.file_count <= 10
    error_message = "Failide arv peab olema vahemikus 1-10."
  }
}
```

Iga muutuja plokk sisaldab kirjeldust, tüüpi ja vaikeväärtust. Validatsioon kontrollib, et antud väärtus vastab meie reeglitele. Kui keegi proovib kasutada keelatud väärtust, annab Terraform veateate juba planeerimise faasis.

### Main faili uuendamine

Nüüd muudame `main.tf` faili kasutama neid muutujaid:
```hcl
resource "local_file" "example" {
  count    = var.file_count
  content  = "See on fail number ${count.index + 1} projektile ${var.project_name} (${var.environment})"
  filename = "${path.module}/${var.project_name}_${count.index + 1}.txt"
}
```

Siin kasutame `count` meta-argumenti, et luua mitu sarnast ressurssi. `count.index` annab praeguse iteratsiooni numbri (alates nullist). `var.project_name` ja `var.environment` viitavad meie muutujatele.

### Outputs faili loomine

Outputs võimaldavad meil näha olulist teavet pärast `apply` käsku. Loome `outputs.tf` faili:
```bash
nano outputs.tf
```
```hcl
output "created_files" {
  description = "Loodud failide nimed"
  value       = local_file.example[*].filename
}

output "project_info" {
  description = "Projekti üldinfo"
  value = {
    name        = var.project_name
    environment = var.environment
    file_count  = var.file_count
  }
}
```

Esimene output kasutab splat operaatorit `[*]`, et koguda kõigi failide nimed. Teine output tagastab objekti projekti info kohta.

### Rakendamine

Kustutame vana ressursi ja loome uued:
```bash
terraform apply
```

Terraform märkab, et `local_file.hello` on kadunud koodist ja selle asemel on uued failid. See kustutab vana ja loob uued. Kinnitage `yes`.

Pärast apply lõppu näete outputs'e automaatselt. Võite ka hiljem küsida:
```bash
terraform output
terraform output created_files
```

**Validation:**
- [ ] Kolm faili on loodud
- [ ] Failide nimed kasutavad projekti nime
- [ ] `terraform output` näitab mõlemat väljundit
- [ ] Variables on õigesti rakendatud

---

## 5. Terraform.tfvars ja Väärtuste Seadmine

Vaikeväärtused on head, aga sageli tahame neid muuta ilma variables.tf faili muutmata. Selleks kasutatakse `terraform.tfvars` faili.

### Tfvars faili loomine
```bash
nano terraform.tfvars
```
```hcl
project_name = "minu-projekt"
environment  = "production"
file_count   = 5
```

Terraform loeb seda faili automaatselt ja kasutab seal olevaid väärtusi. Need override'ivad vaikeväärtused `variables.tf` failist.

### Muudatuste rakendamine
```bash
terraform plan
```

Terraform näitab, et failide nimed muutuvad (sest `project_name` muutus) ja lisandub kaks uut faili (sest `file_count` kasvas 3-lt 5-le). Rakendame:
```bash
terraform apply
```

Vanad failid kustutatakse ja luuakse viis uut faili uute nimedega.

### Käsurea kaudu väärtuste seadmine

Saate ka määrata väärtusi otse käsurealt:
```bash
terraform plan -var="file_count=2"
```

See on kasulik testimiseks või CI/CD pipeline'ides. Käsureal antud väärtused võtavad prioriteedi üle `.tfvars` faili ja vaikeväärtuste.

**Validation:**
- [ ] `terraform.tfvars` fail on loodud
- [ ] Failide nimed kajastavad uut projekti nime
- [ ] File count on 5
- [ ] `-var` lipuga saab väärtusi override'ida

---

## 6. Keerukamad Ressursid

Lihtsamad failid on head alguseks, aga Terraform võimaldab ka keerukamaid struktuure ja konfiguratsioone.

### Kataloogide loomine

Lisame `main.tf` faili kataloogi loomise:
```hcl
resource "local_directory" "config" {
  path = "${path.module}/${var.project_name}_config"
}

resource "local_directory" "scripts" {
  path = "${path.module}/${var.project_name}_scripts"
}
```

### Konfiguratsioonifailide loomine

Loome JSON konfiguratsioonifaili:
```hcl
resource "local_file" "config_json" {
  content = jsonencode({
    project_name = var.project_name
    environment  = var.environment
    version      = "1.0.0"
    created_at   = timestamp()
    features = [
      "file_management",
      "configuration_generation"
    ]
  })
  filename = "${local_directory.config.path}/config.json"
  
  depends_on = [local_directory.config]
}
```

`jsonencode` funktsioon konverteerib Terraform'i objekti JSON stringiks. `timestamp()` annab praeguse aja. `depends_on` ütleb Terraform'ile, et see ressurss vajab kataloogi olemasolu.

### Skriptifaili loomine

Lisame veel Bash skripti:
```hcl
resource "local_file" "startup_script" {
  content = <<-EOF
    #!/bin/bash
    echo "==================================="
    echo "Projekt: ${var.project_name}"
    echo "Keskkond: ${var.environment}"
    echo "==================================="
    echo "Praegune kaust: $(pwd)"
    echo "Kuupäev: $(date)"
  EOF
  filename        = "${local_directory.scripts.path}/startup.sh"
  file_permission = "0755"
  
  depends_on = [local_directory.scripts]
}
```

`file_permission = "0755"` muudab faili käivitatavaks. Heredoc süntaks `<<-EOF ... EOF` võimaldab kirjutada mitmerealine tekst.

### Rakendamine
```bash
terraform apply
```

Terraform loob kaustad ja seejärel failid nendes kaustades, austades sõltuvusi.

Testige skripti:
```bash
bash minu-projekt_scripts/startup.sh
```

**Validation:**
- [ ] Kaks kataloogi on loodud
- [ ] JSON fail on kataloogis
- [ ] Skriptifail on käivitatav
- [ ] Skript töötab korrektselt

---

## 7. For_Each ja Dünaamilised Ressursid

Count on hea, kui vajate kindlat arvu sarnaseid ressursse. For_each on võimsam, kui iga ressurss peab olema unikaalne ja identifitseeritav.

### Map-põhise for_each

Lisame `variables.tf` faili uue muutuja:
```hcl
variable "config_files" {
  description = "Konfiguratsioonifailid luua"
  type = map(string)
  default = {
    "database" = "PostgreSQL configuration"
    "cache"    = "Redis configuration"
    "queue"    = "RabbitMQ configuration"
  }
}
```

Ja `main.tf` faili:
```hcl
resource "local_file" "service_configs" {
  for_each = var.config_files
  
  content  = each.value
  filename = "${local_directory.config.path}/${each.key}.conf"
  
  depends_on = [local_directory.config]
}
```

`each.key` annab map'i võtme (nt "database"), `each.value` annab väärtuse (nt "PostgreSQL configuration"). Iga element map'is loob ühe faili.

### Rakendamine
```bash
terraform apply
```

Kolm konfiguratsioonifaili luuakse: `database.conf`, `cache.conf` ja `queue.conf`.

For_each eelis count'i ees tuleb esile, kui eemaldame ühe elemendi. Lisage `terraform.tfvars` faili:
```hcl
config_files = {
  "database" = "PostgreSQL configuration"
  "queue"    = "RabbitMQ configuration"
}
```

Nüüd kui rakendame:
```bash
terraform apply
```

Terraform kustutab ainult `cache.conf` faili. Count'i puhul oleks ta uuesti loonud kõik failid uutes positsioonides.

**Validation:**
- [ ] Kolm konfiguratsioonifaili on loodud
- [ ] Cache.conf eemaldamine jätab teised alles
- [ ] `each.key` ja `each.value` töötavad õigesti

---

## 8. Ressursside Kustutamine

Infrastruktuur, mida ei kasutata, tuleks eemaldada. Terraform teeb selle lihtsaks.

### Terve infrastruktuuri kustutamine
```bash
terraform destroy
```

Terraform näitab, milliseid ressursse kavatseb kustutada. Vaadake nimekiri üle ja kinnitage `yes`. Terraform kustutab ressursid vastupidises järjekorras võrreldes nende loomisega, austades sõltuvusi.

Kontrollige:
```bash
ls
```

Kõik Terraform'i loodud failid ja kaustad on läinud. State fail on veel olemas, aga tühi.

### Osalise kustutamise

Kui soovite kustutada ainult kindlaid ressursse, saate kasutada `-target` lippu:
```bash
terraform destroy -target=local_file.example[0]
```

See kustutab ainult esimese `example` faili, jättes teised alles. `-target` on kasulik arenduses, aga tootmises tuleks vältida, kuna võib tekitada sõltuvusprobleeme.

**Validation:**
- [ ] Kõik failid ja kaustad on kustutatud
- [ ] State fail on tühi
- [ ] `terraform state list` ei näita midagi

---

## 9. Idempotentsuse Kontrollimine

Üks IaC peamisi põhimõtteid on idempotentsus - sama käsu korduvad käivitamised annavad sama tulemuse.

Loome infrastruktuuri uuesti:
```bash
terraform apply
```

Nüüd käivitame uuesti:
```bash
terraform apply
```

Terraform teeb plani ja ütleb: "No changes. Your infrastructure matches the configuration." Midagi ei muudeta, sest kõik on juba õiges olekus.

Muudame käsitsi ühe faili sisu:
```bash
echo "Modified manually" > minu-projekt_1.txt
```

Käivitage plan:
```bash
terraform plan
```

Terraform märkab erinevust ja soovib faili sisu taastada. Rakendades `apply` tagastatakse algne sisu. See on idempotentsus töös - Terraform tagab, et infrastruktuur vastab alati koodile.

**Validation:**
- [ ] Teine apply ei tee muudatusi
- [ ] Käsitsi muudetud fail taastatakse
- [ ] Terraform märkab erinevusi

---

## 10. Levinud Probleemid ja Lahendused

Terraform'i kasutamisel võivad tekkida erinevad probleemid. Vaatame levinumaid ja kuidas neid lahendada.

### Provider not found

Kui näete veateadet "provider not found", pole provider installitud. Lahendus:
```bash
terraform init
```

Init käsk laeb alla kõik vajalikud provider'id. Kui olete lisanud uue provider'i, käivitage init uuesti.

### State file locked

Kui keegi teine kasutab samaagselt sama state faili, näete lock veateadet. Oodake, kuni teine protsess lõpeb. Kui lock jääb kinni (näiteks kui protsess katkestati), saate selle käsitsi eemaldada:
```bash
terraform force-unlock <lock-id>
```

Lock ID on veateates näidatud. Olge ettevaatlik - eemaldage lock ainult siis, kui olete kindel, et ükski teine protsess ei kasuta state'd.

### Resource already exists

Kui ressurss eksisteerib juba väljaspool Terraform'i, ei saa Terraform seda uuesti luua. Lahendused:

1. Importige olemasolev ressurss:```bash
terraform import local_file.example ./existing-file.txt
```

2. Või kustutage käsitsi ja laske Terraform'il uuesti luua.

### Validation errors

Kui muutuja validatsioon ebaõnnestub, kontrollige `terraform.tfvars` faili väärtusi. Veateade ütleb täpselt, mis on valesti:
```
Error: Invalid value for variable

Environment must be one of: development, staging, production.
```

Parandage väärtus ja proovige uuesti.

**Validation:**
- [ ] Init lahendab provider probleemid
- [ ] Lock'i saab force-unlock'ida
- [ ] Import toob olemasoleva ressursi state'i

---

## Kokkuvõte

Selles laboris õppisime Terraform'i praktiliselt kasutama. Alustasime installimisest ja lihtsamatest ressurssidest, liikusime edasi variables ja outputs'i juurde, ning lõpuks uurisime keerukamaid konstruktsioone nagu for_each ja depends_on.

Peamised õpitud oskused:
- Terraform workflow'i samm-sammult teostamine
- Local provider'i kasutamine failide ja kataloogide loomiseks
- Variables kasutamine dünaamiliseks konfiguratsiooniks
- State faili rolli ja olulisuse mõistmine
- Levinud probleemide lahendamine

Järgmises praktikas ehitame keerukama infrastruktuuri, kasutades mooduleid ja korduvkasutatavaid komponente. Samuti õpime remote state haldamist ja meeskonnatöö põhimõtteid.

Jätkake eksperimenteerimist iseseisvalt. Proovige luua erinevaid ressursse, muuta konfiguratsioone ning vaadake, kuidas Terraform reageerib. Iga apply ja destroy tsükkel tugevdab arusaamist sellest, kuidas IaC töötab.