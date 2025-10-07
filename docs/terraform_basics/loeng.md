# Terraform: Infrastruktuur Koodina

**Eeldused:** Linux CLI põhiteadmised, teksteditori kasutamine, versioonihalduse alused

**Platvorm:** Terraform (kohalik)

## Õpiväljundid

Pärast seda moodulit õpilane:
- Selgitab Infrastructure as Code kontseptsiooni ja selle eeliseid traditsioonilistele meetoditele
- Mõistab Terraform'i arhitektuuri, state haldamist ja provider süsteemi
- Kirjutab HCL süntaksit kasutades ressursse, muutujaid ja väljundeid
- Võrdleb erinevaid IaC tööriistu ja nende kasutusjuhte
- Rakendab Terraform workflow'i: init, plan, apply, destroy

---

## 1. Infrastructure as Code Mõiste ja Vajadus

Tänapäeva IT-süsteemid arenevad kiiresti ja nõuavad paindlikku, korduvkasutatavat infrastruktuuri haldamist. Infrastructure as Code (IaC) on lähenemisviis, kus infrastruktuuri komponendid kirjeldatakse deklaratiivse koodi abil, mitte konfigureeritakse käsitsi.

### Probleemid traditsionaalse lähenemisega

Traditsiooniline käsitsi konfiguratsioon toob kaasa mitmed väljakutsed. Inimeste tehtud vead on vältimatud, kui servereid konfigureeritakse käsitsi läbi graafilise liidese või käsurea. Iga muudatus võib tuua kaasa erinevuse võrreldes dokumentatsiooniga, sest dokumentatsioon ja reaalne olek lähevad ajapikku lahku. Skaleerumine muutub võimatuks, kui iga uus server vajab tunde aega käsitsi seadistamiseks.

Näiteks kui arendusmeeskond vajab uut testikeskkonda, võib käsitsi seadistamine võtta päevi. Iga server tuleb seadistada eraldi, kontrollida võrguseadeid, installida vajalik tarkvara ning veenduda, et kõik vastab tootmiskeskkonnale. Selle protsessi käigus on lihtne jätta mõni samm vahele või teha viga konfiguratsioonis, mis võib põhjustada probleeme hiljem.

### Infrastructure as Code lähenemisviis

IaC muudab infrastruktuuri haldamise fundamentaalselt. Kogu infrastruktuur kirjeldatakse koodis, mis on versioonihalduses ja mida saab testida nagu igat muud tarkvara. Kui teil on vaja uut serverit, ei hakka te käsitsi nupule vajutama, vaid muudate koodi ja lasete tööriistal see luua.

Selle lähenemise peamine eelis on konsistentsus. Kui infrastruktuur on kirjeldatud koodis, siis iga kord kui seda koodi käivitatakse, tekib täpselt sama tulemus. See välistab "töötab minu masinas" probleemi, sest kõik keskkonnad luuakse samast koodist. Lisaks võimaldab kood automatiseerida korduvaid ülesandeid, mis vähendab ajakulu ja vigu.

IaC toob kaasa ka parema koostöö võimaluse. Kuna infrastruktuurikood on Git'is, saavad meeskonnaliikmed teha code review'd, kommenteerida muudatusi ja hoida ajalugu. Iga muudatus on dokumenteeritud ning vajadusel saab tagasi pöörata varasema versiooni juurde.

### IaC põhimõtted ja eelised

Infrastructure as Code rajaneb mitmele olulisele põhimõttele. Esiteks on deklaratiivsus - kirjeldate, mida soovite, mitte kuidas seda saavutada. Näiteks ütlete "tahan kolme serveriga klastrit", mitte "loo esimene server, seejärel teine, siis kolmas". Tööriist väljastab kuidas see tehakse.

Idempotentsus on teine oluline põhimõte. Sama koodi korduvad käivitamised annavad alati sama tulemuse. Kui infrastruktuur on juba õiges olekus, ei tee tööriist midagi. Kui midagi on muutunud, taastatakse õige olek. See tähendab, et võite julgelt käivitada koodi mitu korda ilma muretsemata, et midagi läheb katki.

Versioonihaldus on lahutamatu osa IaC-st. Kogu infrastruktuurikood elab Git repositooriumis koos rakenduskoodiga. See võimaldab jälgida, kes tegi millal milliseid muudatusi ja miks. Kui mõni muudatus tekitab probleeme, saate kiiresti rollback'i teha varasema versiooni juurde.

Testimine muutub võimalikuks, kui infrastruktuur on kood. Saate kirjutada teste, mis kontrollivad, kas infrastruktuur vastab nõuetele. Näiteks saate automaatselt kontrollida, kas tulemüüri reeglid on õiged või kas andmebaasi backup on aktiveeritud. Need testid käivituvad enne tootmisse juurutamist ja hoiatavad probleemidest ette.

---

## 2. Terraform Arhitektuur ja Põhikomponendid

Terraform on HashiCorp'i loodud avatud lähtekoodiga tööriist, mis võimaldab infrastruktuuri kirjeldada deklaratiivse konfiguratsiooni kaudu. Erinevalt paljudest teistest tööriistadest on Terraform multi-cloud ja suudab hallata erinevaid platvorme ühtse süntaksiga.

### Terraform'i arhitektuur

Terraform'i tuumik koosneb mitmest komponendist, mis töötavad koos. Core engine loeb konfiguratsiooni faile, ehitab ressursside graafi ja määrab, millises järjekorras ressursse luua või muuta. See engine on kirjutatud Go keeles ja on sõltumatu konkreetsetest pilveteenustest.

Provider'id on pluginad, mis võimaldavad Terraform'il suhelda erinevate teenustega. Iga teenus (AWS, Azure, Docker, kohalik failisüsteem) vajab oma provider'it. Provider teab, kuidas konkreetse teenuse API'ga suhelda ja kuidas Terraform'i deklaratiivset koodi tõlkida API päringuteks. Näiteks AWS provider oskab luua EC2 instansse, S3 bucket'eid ja VPC'd.

State management on Terraform'i võtmekomponent. State fail sisaldab teavet selle kohta, millised ressursid on loodud, millised on nende ID'd ja atribuudid. Ilma state failita ei teaks Terraform, mis on juba olemas ja mida on vaja muuta. State fail on nagu infrastruktuuri "mälu", mis hoiab koodi ja reaalsuse vahelist seost.

Provisioner'id võimaldavad käivitada skripte või konfiguratsioonihaldustarkvara pärast ressursi loomist. Näiteks pärast serveri loomist võite installida seal tarkvara või seadistada teenuseid. Provisioner'id on aga pigem viimane abinõu - enamasti peaks infrastruktuurikood olema piisavalt deklaratiivne ilma nendeta.

### Provider süsteem

Provider'id on Terraform'i laiendused, mis lisavad toe konkreetsetele teenustele. Iga provider avaldab ressursse ja data source'e, mida saate oma konfiguratsioonis kasutada. Näiteks AWS provider pakub üle 900 erineva ressursi tüübi, alates lihtsatest S3 bucket'itest kuni keerukate EKS klastriteni.

Provider'ite installimine toimub automaatselt `terraform init` käsuga. Terraform loeb teie konfiguratsioonist, milliseid provider'eid vajate, laeb need alla Terraform Registry'st ja salvestab `.terraform` kausta. Versioonihalduks saate määrata, milliseid versioone lubada, mis tagab stabiilsuse ja aitab vältida ootamatuid muudatusi.

Meie kursusel keskendume local provider'ile, mis võimaldab hallata kohalikke faile ja katalooge. See on suurepärane õppimiseks, kuna ei vaja pilve kontot ega maksmist. Local provider pakub lihtsat viisi mõista Terraform'i põhimõtteid ilma keerukate cloud keskkondadeta. Hiljem saate samu põhimõtteid rakendada mis tahes teise provider'iga.

### State haldamine

State fail on JSON vormingus dokument, mis sisaldab täielikku pilti teie infrastruktuurist Terraform'i perspektiivist. Iga ressurss, mille Terraform on loonud, on state failis kirjas koos oma ID, atribuutide ja sõltuvustega. Kui käivitate `terraform plan`, võrdleb Terraform teie koodi state failiga, et kindlaks teha, mis on muutunud ja mida on vaja teha.

State faili asukoht on kriitiline otsus. Vaikimisi salvestatakse see kohalikku faili `terraform.tfstate`, mis on lihtne alustamiseks, aga ei toimi meeskonnatöös. Mitme inimese korral peab state olema jagatud asukohas, näiteks AWS S3 või Terraform Cloud'is. Remote state võimaldab ka state locking'ut, mis väldib samaaegseid muudatusi.

State faili turvalisus on oluline, kuna see võib sisaldada tundlikku informatsiooni. Näiteks andmebaasi paroolid või API võtmed võivad state failis nähtavad olla. Seetõttu peab state fail olema krüpteeritud ja juurdepääs piiratud. Ärge kunagi pange state faili Git repositooriumisse - see kuulub `.gitignore` faili.

---

## 3. HCL Konfiguratsioonikeel

HashiCorp Configuration Language (HCL) on Terraform'i konfiguratsioonikeel, mis ühendab inimloetavuse masinate parsitavusega. HCL on deklaratiivne keel, mis tähendab, et kirjeldate soovitud lõpptulemust, mitte samme sinna jõudmiseks.

### HCL süntaksi põhielemendid

HCL koosneb blokkidest, argumentidest ja avaldistest. Plokk algab võtmesõnaga, millele järgnevad sildid ja looksulud. Ploki sees on argumendid, mis määravad selle ploki omadused. Näiteks ressursi plokk kirjeldab infrastruktuuri komponenti, mida soovite luua.

Ressursi definitsioon algab võtmesõnaga `resource`, millele järgnevad kaks stringi: ressursi tüüp ja kohalik nimi. Ressursi tüüp määrab, mis liiki ressursiga on tegemist (näiteks `local_file`), ja kohalik nimi on teie valitud identifikaator, mida saate kasutada viitamiseks teistes kohtades. Ploki sees määrate argumendid, mis konfigureerivad seda konkreetset ressurssi.

```hcl
resource "local_file" "example" {
  content  = "Hello, Terraform!"
  filename = "${path.module}/example.txt"
}
```

Selles näites loome kohaliku faili. Argument `content` määrab faili sisu ja `filename` määrab kuhu see salvestada. `path.module` on sisseehitatud muutuja, mis viitab praeguse mooduli asukohale.

### Muutujad ja väljundid

Muutujad võimaldavad teha konfiguratsioonist dünaamilise. Selle asemel et kirjutada väärtusi otse koodi, saate need defineerida muutujatena ja anda väärtused eraldi failist või käsurea kaudu. See võimaldab sama koodi kasutada erinevates keskkondades, muutes ainult muutujate väärtusi.

Muutuja definitsioon sisaldab tüüpi, vaikeväärtust ja kirjeldust. Tüüp võib olla lihtne (string, number, bool) või keerukas (list, map, object). Vaikeväärtus on oluline, kui te ei anna muutujale väärtust teisest allikast. Kirjeldus aitab teistel mõista, mida see muutuja teeb.

```hcl
variable "environment" {
  description = "Deployment environment (development, staging, production)"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}
```

Validatsioon võimaldab kontrollida, et muutuja väärtus vastab teie nõuetele. Selles näites lubame ainult kolme spetsiifilist väärtust. Kui keegi proovib kasutada mõnda muud väärtust, annab Terraform veateate juba planeerimise faasis.

Väljundid on viis jagada informatsiooni pärast infrastruktuuri loomist. Näiteks kui loote serveri, tahate tõenäoliselt teada selle IP aadressi. Väljund võimaldab selle väärtuse kuvada pärast `terraform apply` või kasutada seda teistes moodulites.

```hcl
output "file_path" {
  description = "Path to the created file"
  value       = local_file.example.filename
}
```

### Avaldised ja funktsioonid

HCL toetab mitmesuguseid avaldisi ja funktsioone, mis võimaldavad dünaamilist konfiguratsiooni. Ternary operator võimaldab tingimuslikku loogikat: `condition ? true_value : false_value`. See on kasulik, kui vajate erinevaid väärtusi sõltuvalt keskkonnast või teistest tingimustest.

```hcl
resource "local_file" "config" {
  content = var.environment == "production" ? "prod_config" : "dev_config"
  filename = "${path.module}/config.txt"
}
```

Sisseehitatud funktsioonid pakuvad võimsaid töötlusvõimalusi. `jsonencode` ja `yamlencode` konverteerivad Terraform'i objekte JSON või YAML vormingusse. `file` funktsioon loeb faili sisu. `concat` ja `merge` võimaldavad nimekirju ja mape kombineerida. `lookup` otsib väärtust mapist vaikeväärtusega.

Stringide interpolatsioon võimaldab dünaamiliselt ehitada stringe, kombineerides staatilise teksti ja muutujaid. Kasutatakse `${}` süntaksit muutuja või avaldise sisestamiseks stringi sisse. See on eriti kasulik failinimede, tagide või sõnumite loomisel.

### Tsüklid ja iteratsioon

Terraform võimaldab luua mitut sarnast ressurssi kahe erineva lähenemisega: `count` ja `for_each`. Count on lihtsam, kasutades numbrilist indeksit, samas kui for_each on võimsam, lubades itereerida üle mapide või setide.

Count kasutamisel viitate konkreetsele instantsile `count.index` kaudu, mis on nullist algav täisarv. See on hea, kui vajate kindlat arvu sarnaseid ressursse ja järjekord ei ole oluline.

```hcl
resource "local_file" "example" {
  count    = 3
  content  = "File number ${count.index}"
  filename = "${path.module}/file_${count.index}.txt"
}
```

For_each on paindlikum, võimaldades kasutada nii mape kui sette. Viitate praegusele elemendile `each.key` ja `each.value` kaudu, mis teeb koodi loetavamaks ja haldatavamaks. For_each on eelistatud, kui ressursside identiteet on oluline või kui võite vajada ressursse hiljem eemaldada keskel.

```hcl
variable "files" {
  type = map(string)
  default = {
    "config"  = "Configuration file"
    "data"    = "Data file"
    "log"     = "Log file"
  }
}

resource "local_file" "files" {
  for_each = var.files
  content  = each.value
  filename = "${path.module}/${each.key}.txt"
}
```

---

## 4. Terraform Workflow

Terraform'i kasutamine järgib kindlat töövoogu, mis koosneb neljast põhilisest sammust. Iga samm täidab konkreetset rolli ja koos moodustavad need turvalise ja ennustatava viisi infrastruktuuri haldamiseks.

### Initialization (terraform init)

Esimene samm igal projektiga on initsialisatsioon. Käsuga `terraform init` ettevalmistame töökataloogi Terraform'i kasutamiseks. See käsk laeb alla vajalikud provider pluginad, seadistab backend'i state haldamiseks ja initsialiseerib moodulid.

Initsialisatsioon loeb teie konfiguratsiooni failidest, milliseid provider'eid ja mooduleid vajate. Seejärel kontrollib Terraform Registry'st nende viimaste versioone (või kasutab teie määratud versioone) ja laeb need alla. Pluginad salvestatakse `.terraform` kausta, mida tuleks lisada `.gitignore` faili.

Backend konfigureerimine määrab, kuhu state fail salvestatakse. Vaikimisi kasutatakse local backend'i, mis salvestab state faili samasse kausta. Tootmiskeskkondades tuleks kasutada remote backend'i, nagu AWS S3 või Terraform Cloud, mis võimaldab meeskonnatööd ja state locking'ut.

Initsialisatsioon on ohutu operatsioon, mida saate käivitada mitu korda. Kui lisate uue provider'i või mooduli, käivitage uuesti `terraform init`. See ei mõjuta teie olemasolevat infrastruktuuri ega state faili.

### Planning (terraform plan)

Planeerimise samm on Terraform'i võtmevõimalus - see näitab teile, mida käsk `terraform apply` teeks, ilma midagi tegelikult muutmata. Plan võrdleb teie konfiguratsiooni (soovitud olek) state failiga (praegune olek) ja määrab vajalikud muudatused.

Plan väljund kasutab sümboleid näitamaks operatsiooni tüüpi. Plussmärk tähendab uue ressursi loomist. Miinusmärk näitab kustutamist. Tilde märgib in-place uuendust, kus ressurss muudetakse ilma seda kustutamata. Miinus-pluss kombinatsioon tähendab, et ressurss kustutatakse ja luuakse uuesti.

Plan on oluline turvalisuse mehhanism. See laseb teil kontrollida muudatusi enne nende rakendamist, andes võimaluse avastada vigu või soovimatud mõjud. Tootmiskeskkonnas peaks plan alati review'tama enne apply käsu käivitamist, võimalusel teise inimese poolt.

Plani saate salvestada faili kasutades `-out` lippu. See loob binaarse faili, mis sisaldab täpset tegevuskava. Hiljem saate seda kasutada `terraform apply` käsuga, mis tagab, et rakendatakse täpselt see, mida planeeriti, isegi kui konfiguratsioon või state on vahepeal muutunud.

### Applying (terraform apply)

Apply samm viib muudatused ellu. See loob, muudab või kustutab ressursse vastavalt planeeritud tegevuskavale. Vaikimisi käivitab apply esmalt plani ja küsib seejärel kinnitust enne jätkamist, pakkudes viimast võimalust muudatusi üle vaadata.

Apply käib läbi ressursse kindlas järjekorras, austades sõltuvusi. Kui ressurss A sõltub ressursist B, loob Terraform esmalt B, seejärel A. Need sõltuvused tuvastatakse automaatselt koodist - kui viitate teise ressursi atribuudile, loob Terraform sõltuvuse. Vajadusel saate kasutada `depends_on` argumenti eksplitseetse sõltuvuse määramiseks.

Apply käigus näete reaalajas progressi. Terraform kuvab, milline ressurss on parasjagu töös ja kui kaua see on võtnud. Mõned operatsioonid, nagu suurte serverite käivitamine, võivad võtta mitu minutit. Terraform ootab, kuni ressurss on täielikult valmis enne järgmise juurde liikumist.

Kui apply ebaõnnestub pooleli, jääb teie infrastruktuur osaliselt rakendatud olekusse. Terraform salvestab state faili kõik edukalt loodud ressursid ja järgmine apply proovib jätkata sealt, kus pooleli jäi. Seetõttu on oluline hoida state fail kaitstud ja syncis.

### Destruction (terraform destroy)

Destroy käsk eemaldab kogu Terraform'i poolt hallatud infrastruktuuri. See loeb state faili, määrab kõik ressursid ja kustutab need vastupidises järjekorras võrreldes nende loomisega. Kui ressurss A sõltub B-st, kustutatakse esmalt A, seejärel B.

Enne kustutamist näitab Terraform, mida ta kavatseb eemaldada, ja küsib kinnitust. See on ohutu mehhanism juhusliku infrastruktuuri hävitamise vältimiseks. Tootmiskeskkondades võite kasutada lifecycle plokis `prevent_destroy = true`, mis keeldub ressurssi kustutamast isegi destroy käsuga.

Osalist kustutamist saate teha kasutades `-target` lippu, mis määrab konkreetsed ressursid eemaldamiseks. See on kasulik arenduses, kuid tootmises tuleks vältida, kuna võib tekitada sõltuvusprobleeme. Parem on eemaldada ressursi definitsioon koodist ja lasta apply'l see kustutada.

Pärast destroy on state fail tühi, aga fail ise jääb alles. Kui hiljem käivitate uuesti apply, loob Terraform kõik ressursid uuesti, aga need saavad uued ID'd ja algavad puhtalt lehelt.

---

## 5. Best Practices ja Levinud Mustrid

Terraform'i efektiivne kasutamine nõuab rohkemat kui ainult süntaksi tundmist. Aastaid kogunenud kogemus on välja kujundanud parimad praktikad, mis aitavad vältida levinud vigu ja teevad teie infrastruktuuri hallatavaks.

### Koodi organisatsioon

Failide struktuur peaks olema loogiline ja järjekindel. Algajatele sobib lihtne kolme faili muster: `main.tf` ressursside jaoks, `variables.tf` sisendite jaoks ja `outputs.tf` väljundite jaoks. See hoiab asju organiseerituna ilma üleliigse keerukuseta.

Kui projekt kasvab, tasub kaaluda temaatilist jaotust. Võrguseadistused võivad olla `network.tf` failis, andmebaasid `database.tf` failis ja nii edasi. See teeb spetsiifiliste komponentide leidmise lihtsamaks ja vähendab merge konfliktide tõenäosust meeskonnatöös.

Moodulite kasutamine võimaldab koodi taaskasutamist. Tavaline muster on luua `modules/` kaust, kus iga alamkaust esindab taaskasutatavat komponenti. Näiteks `modules/web-server/` võib sisaldada kõike vajalikku veebiserveri loomiseks, mida saate kasutada erinevates keskkondades või projektides.

Keskkondade eristamine on samuti oluline. Üks lähenemine on kasutada eraldi katalooge iga keskkonna jaoks: `environments/dev/`, `environments/staging/`, `environments/prod/`. Iga kaust sisaldab oma `terraform.tfvars` faili keskkonnaspetsiifiliste väärtustega, aga jagab sama põhikoodi läbi moodulite.

### Versioonihaldus

Terraform'i konfiguratsiooni peab hoidma versioonihalduses, kuid mitte kõik failid kuuluvad Git'i. State failid, `.terraform/` kaust ja plaanifailid tuleb lisada `.gitignore` faili. Need sisaldavad kas tundlikku informatsiooni või on masinloetavad binaarfailid, mis ei kuulu source control'i.

Git workflow peaks toetama review protsessi. Iga muudatus peaks tulema läbi pull request'i, kus vähemalt üks teine inimene vaatab üle. Pull request'i kirjelduses tuleks selgitada, miks muudatus on vajalik ja mida see mõjutab. Ideaalis peaks pull request sisaldama ka `terraform plan` väljundit, et reviewer näeks täpset mõju.

Commit sõnumid peaksid olema kirjeldavad. Selle asemel et kirjutada "update config", kirjutage "Add monitoring to production web servers". Hea commit sõnum vastab küsimusele "mida see commit teeb" ja annab konteksti.

Tagide kasutamine on soovitav production deploymentide jaoks. Iga kord kui midagi production'i viiakse, tehke Git tag vastava versiooninumbriga. See võimaldab vajadusel täpselt teada, mis versioon oli parasjagu production'is, ja hõlbustab rollback'i.

### Turvalisus

Tundlike andmete hoidmine on kriitiline teema. Paroolid, API võtmed ja muud saladused ei tohi kunagi olla koodis hard-coded. Kasutage keskkonna muutujaid, secrets management süsteeme (nagu AWS Secrets Manager või HashiCorp Vault) või Terraform'i encrypted variables.

State faili turvalisus on samuti oluline, kuna see võib sisaldada tundlikku teavet. Remote backend'id nagu S3 peaksid olema krüpteeritud rest'is ja transit'is. Juurdepääs state failile peaks olema piiratud ainult neile, kel seda tõesti vaja on.

Minimaalsete õiguste põhimõte kehtib ka infrastruktuurikoodi puhul. Terraform'i credentials peaksid andma ainult need õigused, mis on vajalikud konkreetsete ressursside haldamiseks. Ärge kasutage admin õigusi, kui piisab väiksematest.

Koodiskaneerimine peaks olema osa CI/CD pipeline'ist. Tööriistad nagu tfsec, checkov või Terraform Sentinel saavad leida turvalisuse probleeme enne production'i jõudmist. Need kontrollivad näiteks, kas S3 bucket on avalik, kas krüpteerimine on lubatud või kas logid on aktiveeritud.

### Testimine ja valideerimine

Koodi kvaliteedi kontrollimine peaks olema automatiseeritud. `terraform fmt` standardiseerib koodi vormindust. `terraform validate` kontrollib süntaksi ja sisemist loogikat. Need käsud peaksid käima enne iga commit'i või vähemalt pull request'i review's.

Planeerimise faas on osa testimisest. Iga pull request peaks sisaldama `terraform plan` väljundit. See annab reviewerile võimaluse näha täpset mõju ilma infrastruktuuri muutmata. Mõned meeskonnad isegi automaatpostitavad plani tulemuse pull request'i kommentaarina.

Integratsioonitestid infrastruktuuri jaoks on võimalikud, kuigi keerulisemad kui rakendustestid. Tööriistad nagu Terratest (Go) või kitchen-terraform (Ruby) võimaldavad kirjutada teste, mis loovad ajutise infrastruktuuri, kontrollivad selle tööd ja kustutavad pärast. Need testid on kallid aja ja raha poolest, aga tasuvad end ära kriitilistel komponentidel.

---

## 6. Terraform vs Teised IaC Tööriistad

Terraform ei ole ainus Infrastructure as Code tööriist turul. Igaühel on oma tugevused, nõrkused ja ideaalne kasutusjuht. Õige tööriista valimine sõltub teie konkreetsetest vajadustest, meeskonna oskustest ja tehnilisest keskkonnast.

### Ansible vs Terraform

Ansible on konfiguratsiooni halduse tööriist, mis sarnaneb Terraform'iga, aga on loodud teiste eesmärkide jaoks. Ansible on imperatiivne, mis tähendab, et kirjutate samme, mida täita. Terraform on deklaratiivne, kirjeldades soovitud lõpptulemust.

Ansible töötab agentless'ina üle SSH, mis teeb algseadistamise lihtsaks. Te ei pea installima midagi sihtmasinatele. Terraform vajab iga teenuse jaoks provider'it, mis lisab kompleksust, aga annab tüübi kontrolli ja parema integratsiooni.

Praktikas kasutatakse neid sageli koos. Terraform loob infrastruktuuri (serverid, võrgud, load balancer'id), samas kui Ansible konfigureerib tarkvara nendel serveritel. See kombinatsioon kasutab iga tööriista tugevusi: Terraform infrastruktuuri orkestreerimiseks, Ansible rakenduste deployment'iks.

Ansible'i õppimiskõver on laugem. YAML süntaks on tuttav ja playbook'ide kontseptsioon on intuitiivne. Terraform'i HCL ja state management võivad algul tunduda võõrad. Aga kui need on omandatud, pakub Terraform võimsamat infrastruktuuri haldust.

### CloudFormation vs Terraform

AWS CloudFormation on Amazon'i natiivne IaC tööriist. See on tihedalt integreeritud AWS teenustega ja toetab sageli uusi AWS funktsioone varem kui Terraform. CloudFormation template'id on JSON või YAML vormingus ja järgivad AWS spetsiifilist struktuuri.

CloudFormation'i suurim piirang on vendor lock-in. See töötab ainult AWS'iga, mis tähendab, et kui teil on multi-cloud strateegia või kasutate muid teenuseid, vajate erinevaid tööriistu. Terraform on multi-cloud vaikimisi, võimaldades hallata AWS, Azure, GCP ja sadu teisi teenuseid ühtse süntaksiga.

State haldamine erineb oluliselt. CloudFormation haldab state'd AWS'i poolel automaatselt läbi stack'ide, mis lihtsustab seadistamist. Terraform state nõuab rohkem tähelepanu, eriti meeskonnatöös, aga annab ka rohkem kontrolli.

Praktiline valik sõltub teie vajadusest. Kui olete 100% AWS'is ja ei plaani lahkuda, võib CloudFormation olla piisav ja lihtsam. Kui soovite paindlikkust, multi-cloud võimekust või kasutate juba Terraform't teiste teenuste jaoks, on mõistlik jääda Terraform'i juurde.

### Pulumi vs Terraform

Pulumi on uuem IaC tööriist, mis eristub sellega, et kasutab üldisi programmeerimiskeeli (Python, TypeScript, Go, C#) Domain Specific Language'i asemel. See tähendab, et saate kirjutada infrastruktuuri koodi keeles, mida juba tunnete, kasutades IDE'd, debugger'it ja teste, nagu tavakoodi puhul.

Pulumi tugevus on keerukuses. Kui teil on vaja keerukat loogikat või arvutusi infrastruktuuris, on üldised programmeerimiskeeled võimsamad kui HCL. Saate kasutada library'sid, kirjutada funktsioone, teha objektorienteeritud disaini. See on eriti kasulik suurte, keerukate infrastruktuuride puhul.

Terraform'i HCL on lihtsam ja deklaratiivsem, mis on eelis enamikus kasutusjuhtudes. Piiratud süntaks sunnib teid mõtlema deklaratiivselt ja hoiab koodi loetavana. Üldiste programmeerimiskeelte paindlikkus võib viia ka imperatiivsema ja raskemini hallatava koodini.

Community ja ökosüsteem on Terraform'il palju suurem. Rohkem dokumentatsiooni, näiteid, mooduleid ja Stack Overflow vastuseid. Pulumi on uuem ja väiksem, kuigi kasvav. Meeskonna oskuste vaade on samuti oluline - kui teie meeskonnal on tugevad programmeerimise oskused, võib Pulumi olla loomulik valik.

---

## Kokkuvõte

Infrastructure as Code muudab infrastruktuuri haldamise lähenemist fundamentaalselt. Kood võimaldab konsistentsust, korduvkasutamist, versioonihaldust ja automatiseerimist viisil, mis käsitsi konfiguratsiooniga võimatu on.

Terraform on üks populaarsemaid IaC tööriistu tänu oma deklaratiivsele lähenemusele, multi-cloud võimekusele ja tugevale provider ökosüsteemile. HCL keel pakub head tasakaalu loetavuse ja võimsuse vahel, samas kui state management võimaldab Terraform'il täpselt jälgida infrastruktuuri.

Selles moodulis õppisime Terraform'i põhikontseptsioone: kuidas HCL töötab, mis on provider'id ja state, kuidas Terraform workflow käib ning milliseid parimaid praktikaid järgida. Järgmises praktikas rakendame neid teadmisi konkreetsete ülesannete lahendamiseks, luues ja haldades infrastruktuuri Terraform'iga.

Infrastruktuuri kui koodi käsitlemine on oskus, mis kasvab praktikaga. Esimesed sammud võivad tunduda keerulised, aga põhimõtted muutuvad loomulikuks. Oluline on mõista, miks asju teatud viisil tehakse, mitte ainult kuidas. See arusaam aitab teid teha paremaid otsuseid ja vältida levinud lõkse.
