# Ansible Alused

## Õpiväljundid

Pärast seda loengut õpilane:

- **Selgitab** miks automatiseerimine on vajalik ja kuidas Ansible probleemi lahendab
- **Kirjeldab** Ansible'i agentless arhitektuuri ja push-mudeli põhimõtteid
- **Eristab** idempotentseid operatsioone mitte-idempotentsetest
- **Loetleb** Ansible'i kolm põhikomponenti (inventory, ad-hoc, playbook)
- **Tunneb ära** millal kasutada ad-hoc käske vs playbook'e
- **Loeb** lihtsat YAML süntaksit ja mõistab playbook'i struktuuri

---

## Sissejuhatus

Tere tulemast teisele nädalale! Täna räägime Ansible'ist, mis on üks populaarsemaid serverite automat töötab. iseerimisvahendeid tänapäeval.

Ansible on oskus mis on otseselt kasutatav tööturul. Paljud suurettevõtted kasutavad Ansible'it oma infrastruktuuri haldamiseks. Õppides seda, omate te ühe olulise DevOps tööriistad oma arsenalis.

Alustame väikese ajalooga. Miks? Sest parim viis mõista miks mingi tööriist on loodud, on mõista millist probleemi see lahendab. Kui te mõistate probleemi, siis tööriist läheb palju paremini pähe.

## 1. Ajalugu ja probleem

### 1.1 Kuidas servereid haldati varem (90-ndad ja varajased 2000-ndad)

![IT admin füüsiliselt serveri juures, käsitsi töö](https://www.pacw.org/wp-content/uploads/2024/11/Figure-14.jpg)

Alustame 1990-ndatest. Sel ajal oli IT maailmas palju lihtsam. Tüüpiline firma võis omada viis kuni kümme serverit. Need serverid asusid serverisaalis ja IT administraator läks füüsiliselt nende juurde. Ta ühendas klaviatuuri ja monitori, logi sisse ja seadistas asju käsitsi. Kui midagi vaja oli muuta, tuli jälle füüsiliselt kohale minna.

See meetod töötas sel ajal suhteliselt hästi. Miks? Sest servereid oli vähe ja muudatusi tehti harva. Võibolla kord kuus või isegi harvem tuli midagi uuendada või muuta. Serverid töötasid stabiilselt ja neid eriti ei puututud.

Aga juba siis hakkasid tekkima esimesed probleemid. Esiteks, iga server muutus ajapikku natuke erinevaks. Kuidas see juhtus? No näiteks IT admin konfigureeris server1 esmaspäeval ja server2 neljapäeval. Esmaspäeval ta meenutas kõiki samme, aga neljapäeval juba unustas ühe sammu vahele. Või tegi midagi pisut erinevalt sest vahepeal oli õppinud paremat viisi.

Teiseks, dokumentatsiooni ei olnud. Või kui oli, siis see oli aegunud. Kõik teadmised - kuidas täpselt serverid on seadistatud, mis järjekorras asjad installitud, millised erandid tehti - kõik see oli IT administraatori peas. Kui see inimene lahkus firmast, siis lahkusid ka teadmised. Uus inimene pidi hakkama nullist tuvastama kuidas asjad on seadistatud.

### 1.2 2000-ndad: Serverite arv kasvab ja shell skriptid ilmuvad

![Serverite arvu kasv ajas](https://www.nextplatform.com/wp-content/uploads/2019/01/google-datacenter-servers-dalles-bw-1030x438.jpg)

2000-ndate alguses hakkas olukord muutuma. Internetibuum tõi kaasa vajaduse rohkemate serverite järele. Firmal ei olnud enam 10 serverit vaid võibolla 50 või 100. Füüsiliselt iga serveri juurde minek ei olnud enam mõistlik - see võttis liiga palju aega.

IT administraatorid hakkasid kasutama SSH-d - Secure Shell protokolli. SSH võimaldas kaugühendust serveritesse, nii et sa ei pidanud enam füüsiliselt kohale minema. Võisid oma laua tagant serveritesse sisse logida. See oli suur samm edasi.

Aga probleem püsis - kui sul on 50 serverit ja pead igasse käsitsi sisse logima, kirjutama käsud ja välja logima, siis see võtab ikka tunde. Siis hakkasid inimesed kirjutama shell skripte.

Shell skript on lihtsalt tekstifail kus on kirjas käsud mis sa tahaksid käivitada. Näiteks:

```bash
#!/bin/bash
for server in server1 server2 server3; do
  ssh admin@$server "apt update && apt install nginx"
done
```

See skript loob läbi serverite nimekirja ja käivitab igas käsu. See oli juba parem - ühe käsu käivitamine asemel 50 käsu käivitamist. Aga shell skriptidel olid oma probleemid.

Esimene probleem oli see, et skriptid ei olnud "nutikad". Kui sa käivitasid skripti esimest korda, paigaldas ta nginx'i. Okei, hea. Aga kui sa käivitasid sama skripti teist korda? Ta üritab nginx'i uuesti paigaldada. Olenevalt käsust võis see põhjustada erroreid või isegi midagi katki teha.

Teine probleem oli järjestikune töö. Skript ühendus server1, tegi töö, logi välja. Siis server2, tegi töö, logi välja. Järjestikku. Kui ühe serveriga läks 2 minutit, siis 50 serveriga läks 100 minutit. See ei olnud eriti efektiivne.

Kolmas probleem oli vigade käsitlemine. Kui server23 ühendus ebaõnnestus, siis skript kas jooksis edasi (ja sa ei teadnud et see server jäi vahele) või peatus (ja ülejäänud 27 serverit ei saanud uuendust). Mõlemad variandid olid halvad.

### 1.3 2005-2009: Puppet ja Chef - esimesed suured automatiseerimisvahendid

![Puppet ja Chef logod](https://media.licdn.com/dms/image/v2/D4D12AQFhrjy0ozGShQ/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1690917230934?e=2147483647&v=beta&t=5yNZoMKZbOz-vJ9ENMP6DduR8Yywb1Utls07ajfRz8s)

2005. aastal ilmus Puppet ja 2009. aastal Chef. Need olid esimesed suured, professionaalsed konfiguratsioonihalduse tööriistad. Need olid mõeldud täpselt selle probleemi lahendamiseks - kuidas hallata sadu või tuhandeid servereid.

Need tööriistad tõid kaasa palju uuendusi. Nad kasutasid deklaratiivset süntaksit - sa kirjeldasid MIDA sa tahad, mitte KUIDAS seda teha. Nad olid nutikad - kontrollisid enne muutmist kas see on vajalik. Nad toetasid keerukat loogikat ja korduvkasutatavaid komponente.

Aga nende arhitektuur oli keeruline. Mõlemad kasutasid "agent-based" mudelit. See tähendab, et igasse serverisse tuli installida väike programm - agent. See agent töötas kogu aeg taustal, kasutades mälu ja CPU'd. Agent oli programmeeritud küsima iga 15-30 minuti tagant keskserverilt: "Tere, kas on midagi teha?" Keskserver vastas kas jah või ei, ja agent tegi mis kästi.

See arhitektuur töötas, aga tõi kaasa oma probleeme. Esiteks, agent oli veel üks asi mida tuli hallata. Pidi agent'i installima, uuendama, kontrollima kas töötab. Teiseks, agent kasutas ressursse. Vähe, aga kui sul on 1000 serverit, siis see summeerub. Kolmandaks, oli latentsuse probleem - muudatus võis võtta kuni 30 minutit sõltuvalt millal agent viimati küsis.

Lisaks kasutasid need tööriistad oma spetsiaalseid keeli. Puppet kasutas Ruby DSL-i, Chef kasutas Ruby't. Need keeled ei olnud eriti intuitiivsed. Õppimiskõver oli väga järsk - võttis nädalaid või kuid enne kui said aru kuidas need tööriistad toimivad ja said midagi kasulikku teha.

### 1.4 2012: Ansible sünnib - lihtne idee mis muutis mängu

![Michael DeHaan (Ansible looja)](https://image.slidesharecdn.com/devopswithansible-170120102347/75/DevOps-with-Ansible-4-2048.jpg)

2012. aastal lõi Michael DeHaan Ansible'i. DeHaan oli varem töötanud Puppet ja teiste automatiseerimisvahendite kallal, nii et ta teadis nende probleeme. Ta mõtles - miks me teeme seda nii keeruliseks? 

Tal oli väga lihtne idee: SSH on juba igas Linux serveris. Python on juba igas Linux serveris. Miks me peame installima veel midagi? Lihtsalt kasutame SSH-d!

Selle asemel et kirjutada keeruline konfiguratsioonisüsteem oma keerulises keeles, otsustas ta kasutada YAML-i. YAML on väga lihtne andmeformaat mis näeb välja nagu taandega tekst. Igaüks saab aru.

Selle asemel et kasutada agent'e, otsustas ta teha "push" mudeli. Sa käivitad käsu oma arvutist ja Ansible lükkab muudatused serveritesse. Kohe. Mitte kunagi hiljem, vaid kohe.

Ansible esimene versioon oli väga lihtne. Aga see lihtsus oli tema tugevus. Inimesed said aru kiiresrti. Võisid tunni jooksul õppida põhitõed ja hakata kasutama. Võrreldes Puppet või Chefiga, kus võttis nädalaid enne kui said midagi toodetud, oli see ulmeline erinevus.

Ansible hakkas kiiresti populaarsust koguma. 2015. aastal ostis Red Hat Ansible'i 150 miljoni dollari eest. See oli märk, et Ansible oli muutunud tõsiseks, ettevõtte-tasemel tööriistaks. Red Hat nägi et see on nende ökosüsteemi oluline osa.

2019. aastal ostis IBM Red Hati 34 miljardi dollari eest. See oli üks suuremaid tehinguid tehnoloogiasektoris. Ansible oli nüüd osa IBM-ist, ühest maailma suuremast tehnoloogiafirmast.

### 1.5 Tänapäev: Miks Ansible on tähtis

![Ansible kasutus](https://spacelift.io/_next/image?url=https%3A%2F%2Fspaceliftio.wpcomstaging.com%2Fwp-content%2Fuploads%2F2024%2F04%2Fansible-use-cases.png&w=3840&q=75)

Täna, 2024. aastal on Ansible üks populaarsemaid automatiseerimisvahendeid maailmas. Vaatame mõnda numbrit. GitHubis on Ansible projektil üle 62,000 tähe - see näitab kui paljud arendajad peavad seda oluliseks. Ansible Galaxy, mis on Ansible'i kogukonna jagatud komponentide repositoorium, sisaldab üle 25,000 valmis komponenti mida igaüks saab kasutada.

Suur enamus DevOps meeskondadest kasutab Ansible'it. Hinnanguliselt 70% DevOps praktikutest on Ansible'iga kokku puutunud. See on de facto standard serverite automatiseerimises. Kui lähete tööintervjuule DevOps või süsteemiadministraatori kohale, on väga suur tõenäosus et teilt küsitakse Ansible'i kogemuse kohta.

Miks Ansible nii populaarseks sai? Mitu põhjust. Esiteks, see on lihtne. Te ei pea olema programmeerija et Ansible'it kasutada. Te ei pea õppima uut programmeerimiskeelt. Kui te teate kuidas SSH töötab ja oskate kirjutada YAML faile (mis on väga lihtne), siis olete 80% teel.

Teiseks, see on võimas. Lihtsus ei tähenda piiratud võimekust. Ansible'iga saab teha väga keerulisi asju - hallata tuhandeid servereid, orkesteerida keerulisi deployment'e, integreerida pilve teenustega. Aga te ei pea kohe keerulistega alustama. Võite alustada lihtsast ja järk-järgult liikuda keerulisemate asjadeni.

Kolmandaks, see on tasuta ja avatud lähtekoodiga. Te ei pea maksma litsentse et kasutada. Saate alla laadida, installida ja hakata kohe kasutama. On olemas ka maksulised tooted (Ansible Tower, nüüd Ansible Automation Platform) mis annavad lisavõimalusi, aga põhiline Ansible on täiesti tasuta.

## 2. Ansible põhiidee

### 2.1 Mis on Ansible - suur pilt

![Ansible high-level overview](https://miro.medium.com/v2/resize:fit:1358/1*yg1Ey8E2Xdl14HiBsRKLyA.gif)

Nüüd kui me mõistame ajaloolist konteksti, vaatame mis Ansible täpselt on. Kõige lihtsamalt öeldes on Ansible automatiseerimisvahend. Aga see ei ütle veel palju. Täpsemalt - Ansible on tööriist mis laseb teil hallata mitmeid arvuteid korraga.

Mõelge sellele nagu kaugjuhtimispuldile. Kui teil on kaugjuhtimispult, siis te ei pea füüsiliselt televiisori juurde minema et kanalit vahetada. Vajutate nuppu ja televiisor teeb mis käsite. Ansible on sarnane - ainult et te juhite mitte televisiooni vaid servereid. Ja mitte ühte vaid kümneid või sadu servereid korraga.

Ansible'i põhiline ülesanne on väga lihtne. Te kirjeldate YAML failides mida te tahate. Näiteks: "Tahan et nginx veebiserver oleks installitud ja töötaks kõikides minu veebiserveritest." Ansible võtab selle kirjelduse, vaatab mis praegu serverites on, ja teeb kõik vajaliku et teie kirjeldus muutuks reaalsuseks.

Oluline punkt - te ei pea ütlema KUIDAS seda teha. Te ei pea kirjutama: "Esiteks käivita apt update, siis apt install nginx, siis kontrolli kas installis, siis systemctl start nginx..." Ansible teab ise kuidas nginx'i paigaldada. Te lihtsalt ütlete MIDA te tahate.

### 2.2 Agentless arhitektuur - miks see on revolutsiooniline

![Agentless vs Agent-based architecture](https://www.aquasec.com/wp-content/uploads/2023/03/large-Agents-charts.jpg)

Nüüd räägime arhitektuurist. See on üks põhjusi miks Ansible on nii populaarne. Vaatame diagrammi.

Ekraanil näete vasakul "agent-based" arhitektuuri, mis on see mida Puppet ja Chef kasutavad. Iga serveris on agent - väike programm. See agent töötab kogu aeg taustal. Paremal näete Ansible'i "agentless" arhitektuuri. Serverites ei ole midagi. Lihtsalt SSH.

Mis on agent? Agent on programm mis on installitud serverisse ja töötab seal koguaeg. See on nagu väike robot kes istub serveris ja ootab käske. Iga 15 või 30 minuti tagant ta küsib keskserverilt: "Tere, kas on midagi teha?" Kui on, siis ta teeb. Kui ei ole, siis ta ootab edasi.

See kõlab mõistlikuna, aga toob kaasa kompleksust. Mõelge sellele nii - kui te paigaldate 100 serverit, siis te peate esimese asjana igasse paigaldama agendi. See on "chicken and egg" probleem - kuidas te paigaldate agendi kui te veel ei saa automatiseerida sest agent ei ole veel seal?

Agent vajab hooldust. Ta peab olema õiges versioonis. Vahel läheb katki ja peate tuvastama miks. Agent kasutab ressursse - vähe, aga kasutab. Kui teil on 1000 serverit ja iga agent kasutab 50 MB RAM-i, siis see on kokku 50 GB RAM-i mis läheb lihtsalt "ootamisele".

Ansible läks teist teed. Nad mõtlesid - SSH on juba olemas. SSH on Secure Shell protokoll mis võimaldab turvalist kaugühendust. See on praktiliselt igas Linux serveris vaikimisi installitud. Miks me ei kasuta lihtsalt seda?

Ansible'i puhul te ei pea serveritesse MIDAGI installima. SSH on seal. Python on seal (ja nagunii kasutatakse seda paljudes asjades). Olete valmis. See on uskumatult lihtne.

Kuidas see töötab? Kui te käivitate Ansible käsu, siis Ansible avab SSH ühenduse serverisse. Sama ühendus mida te kasutate kui kirjutate `ssh user@server` käsu käsitsi. Ansible saadab üle SSH väikese Pythoni skripti. Server käivitab selle skripti. Skript kontrollib mis on praegu, teeb vajalikud muudatused, saadab tulemuse tagasi. SSH ühendus suletakse. Kõik.

Agent ei tööta taustal. Kui Ansible ei tee midagi, siis server ei tee Ansible'i jaoks ka midagi. Ei mingit ressursi kasutust, ei mingit taustal töötamist. See on väga elegant lahendus.

### 2.3 Push vs Pull mudel - kontroll vs automaatsus

![Push vs Pull model comparison](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*-chzBHbzBA1BbBQo7a-q3w.png)

Nüüd vaatame kuidas automatiseerimisvahendid otsustavad MILLAL muudatusi teha. On kaks põhilist mudelit - pull ja push.

Pull mudel on see mida Puppet ja Chef kasutavad. "Pull" tähendab et server tõmbab informatsiooni. Kuidas see töötab? Vaatame diagrammi. On keskserver, Puppet Master. Ja on serverid kus töötab agent. Agent on programmeeritud küsima iga 30 minuti tagant: "Tere Puppet Master, kas on midagi teha?" Master vaatab konfiguratsiooni ja vastab: "Jah, paigalda nginx" või "Ei, kõik korras."

See mudel töötab, aga on üks suur probleem - latentsus. Kujutage ette - teie ülemus tuleb kell 9:00 hommikul ja ütleb: "Leiti turvaprobleem! Peame KOHE uuendama nginx'i kõikides serverites!" Te teete Puppet Master serveris konfiguratsiooni muudatuse. Aga nüüd peate ootama.

Server1 küsis viimati kell 8:50. Ta küsib järgmine kord kell 9:20. Seega server1 saab uuenduse alles pool tundi hiljem. Server2 küsis kell 9:05 - tal oli õnne, ta saab uuenduse 25 minutiga. Aga Server3 küsis just kell 8:58, ta saab uuenduse alles kell 9:28. Kogu protsess võtab 30 minutit enne kui kõik serverid on uuendatud.

Push mudel on see mida Ansible kasutab. "Push" tähendab et teie lükkate muudatused välja. Kuidas see töötab? Te käivitate käsu: `ansible-playbook update.yml`. Sel hetkel - kohe - Ansible avab ühendused kõikidesse serveritesse ja hakkab tööd tegema. Mitte 30 minutit hiljem, vaid kohe. Kolme minuti pärast on kõik serverid uuendatud.

Te olete kontrolli all. Te otsustate MILLAL muudatused juhtuvad. Kui on turvaprobleem - te saate kohe reageerida. Kui on plaaniline muudatus - te saate teha keset ööd kui kasutajaid ei ole. Kontroll on teie kätes.

Mõlemad mudelid on tehniliselt võimalikud ja mõlemal on oma kohad. Pull on hea kui te tahate et süsteem hoiab end ise soovitud seisundis ilma teie sekkumiseta. Push on hea kui te tahate täpset kontrolli millal asjad juhtuvad. Ansible valis push mudeli ja see on osutunud väga populaarseks.

### 2.4 Idempotentsus - turvaline automatiseerimine

![Idempotent vs non-idempotent operations](https://media.licdn.com/dms/image/v2/D5612AQEp3iL1Zn9Czg/article-inline_image-shrink_1000_1488/article-inline_image-shrink_1000_1488/0/1718953580431?e=2147483647&v=beta&t=CDRoZci-6-ezcoShpWvtnwk8bhxHM3oO9hgE84ngg8k)

Nüüd tuleb üks kõige tähtsamaid kontseptsioone - idempotentsus. See on veidi keeruline sõna aga mõiste on väga oluline. Idempotentsus tuleb matemaatikast. See tähendab operatsiooni mida sa võid teha mitu korda ja tulemus on alati sama.

Vaatame lihtsat matemaatilist näidet. Kui te korrutate arvu nulliga, saate alati null. 5 korda 0 on 0. Kui te korrutate veel kord nulliga, on ikka 0. Võite korrutada kümme korda - tulemus ei muutu. See on idempotentne operatsioon.

Või võtame abs() funktsiooni - absoluutväärtus. abs(-5) on 5. abs(5) on ka 5. Kui te rakendade abs() funktsiooni numbr ile kaks korda - abs(abs(-5)) - saate ikkagi 5. Idempotentne.

Ansible'i kontekstis tähendab idempotentsus järgmist: kui te käivitate sama playbook'i kaks korda, siis teine kord ei muutu midagi. Ansible kontrollib igal käivitusel: "Mis on praegu? Mis peaks olema? Kas on sama?" Kui jah, siis Ansible ütleb "OK, kõik juba õige" ja ei tee midagi. Kui ei, siis ta teeb muudatuse.

Vaatame praktilist näidet. Shell skript mis EI OLE idempotent:

```bash
echo "port 8080" >> config.txt
```

See lisab rea config.txt faili lõppu. Esimesel käivitusel - okei, lisatakse "port 8080". Teisel käivitusel - lisatakse uuesti. Nüüd on kaks rida. Kolmandal - kolm rida. See on probleem.

Ansible versioon mis ON idempotent:

```yaml
- lineinfile:
    path: config.txt
    line: "port 8080"
```

Esimesel käivitusel Ansible vaatab: "Kas config.txt sisaldab rida 'port 8080'? Ei sisalda. Lisan." Teisel käivitusel: "Kas config.txt sisaldab rida 'port 8080'? Jah, sisaldab juba. Ei tee midagi." Kolmandal korral sama. Failis on alati täpselt üks rida.

Miks see on NII oluline? Sest see teeb automatiseerimise turvaliseks. Kujutage ette - teie ülemus küsib: "Kas sa oled kindel et kõik 50 serverit on õigesti seadistatud?" Ilma idempotentsuseta te kardaksite playbook'i uuesti käivitada. Mis siis kui see muudab midagi mis ei tohiks muutuda? Äkki läheb midagi sassi?

Idempotentsusega saate julgelt käivitada mitu korda. Kui midagi on valesti, Ansible parandab. Kui kõik on õige, Ansible ei puutu. Võite käivitada iga päev - kui midagi vahepeal muutus (näiteks keegi muutis käsitsi faili), siis Ansible parandab tagasi. Kui midagi ei muutunud, siis Ansible lihtsalt kontrollib ja kinnitab.

See on nagu turvapiir. Te ei pea muretsema et automation läheb hulluks ja muudab kõike. Ansible kontrollib alati enne kui muudab.

### 2.5 Execution flow - kuidas Ansible käivitamine välja näeb

![Ansible execution steps](https://toptechtips.github.io/img/ansible-parallel/default.png)

Lõpuks vaatame sammhaaval kuidas Ansible töövoog välja näeb. See aitab mõista mis päriselt juhtub kui te käivitate Ansible käsu.

**Samm 1:** Te kirjutate playbook faili. See on YAML vormingus tekstifail. Seal te kirjeldate mida tahate. Näiteks "tahan et kõikides veebiserveritest oleks nginx installitud ja töötaks."

**Samm 2:** Te avate terminali ja kirjutate käsu: `ansible-playbook install_nginx.yml`

**Samm 3:** Ansible program teie arvutis loeb seda playbook faili. Ta parsib YAML-i ja mõistab mis te tahate teha.

**Samm 4:** Ansible loeb inventory faili. Inventory on teine fail kus on kõikide teie serverite nimekiri - nende IP aadressid, kasutajanimed, grupid. Ansible vaatab playbook'ist et see on mõeldud "webservers" grupile ja vaatab inventory'st kes on selles grupis. "Okei, mul on 50 veebiservit, nende aadressid on need ja need."

**Samm 5:** Ansible hakkab avama SSH ühendusi. Vaikimisi avab ta 5 ühendust paralleelselt. Seega esimesed 5 serverit saavad ühenduse kohe. Kui teil on 50 serverit, siis Ansible teeb esimesed 5, siis järgmised 5, jne. Te saate konfigureerida kui palju paralleelseid ühendusi lubada - rohkem on kiirem aga kasutab rohkem ressursse.

**Samm 6:** Iga serveri jaoks - ja see on oluline - Ansible EI ALUSTA kohe muutmisega. Esimene asi mida ta teeb on "gathering facts". Ta kogub informatsiooni serveri kohta. Mis operatsioonisüsteem? Mis versioon? Kui palju mälu? Mis IP aadress? Kas nginx on juba installitud? Mis versioon?

**Samm 7:** Nüüd Ansible võrdleb. "Praegu on nginx versioon 1.18. Playbook ütleb et peaks olema 'latest'. Kontrollin repository'st - latest on 1.20. Seega pean uuendama." Või "Praegu ei ole nginx'i üldse. Pean paigaldama." Või "Praegu on juba nginx 1.20, mis on latest. Ei pea midagi tegema."

**Samm 8:** Ansible teeb ainult vajalikud muudatused. Server1 vajab uuendust - uuendab. Server2 on juba õige - jätab vahele. Server3 ei ole nginx'i - paigaldab. Iga server saab täpselt seda mis talle vaja.

**Samm 9:** Ansible näitab teile raportit. Ekraanil ilmub väljund: "server1: changed, server2: ok, server3: changed" jne. Lõpus on kokkuvõte: "50 serverit, 47 muudetud, 3 juba õiged, 0 ebaõnnestus."

Kogu see protsess võtab võibolla 3 minutit 50 serverile. Võrrelge seda 4+ tunniga kui teeksite käsitsi.

## 3. Kolm põhikomponenti

### 3.1 Inventory - kellele me käske saadame

![inventory.ini file structure](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Ywp-CLRXKEGiRyvFCqRQUw.png)

Alustame esimesest komponendist - inventory. Inventory on lihtne tekstifail kus on kirjas kõikide teie serverite nimekiri. See on nagu telefoniraamat - kui Ansible peab teadma kellega ühendust võtta, ta vaatab inventory'st.

Vaatame lihtsat inventory faili:

```ini
[webservers]
web1 ansible_host=10.0.0.10 ansible_user=ubuntu
web2 ansible_host=10.0.0.11 ansible_user=ubuntu

[databases]
db1 ansible_host=10.0.0.20 ansible_user=admin
db2 ansible_host=10.0.0.21 ansible_user=admin
```

Lahti seletades: Kandilised sulud tähistavad gruppi. `[webservers]` on grupi nimi. Te võite selle nimetada kuidas soovite - nimi on lihtsalt meelde jätmiseks.

All on grupi liikmed. Iga rida on üks server. `web1` on serveri alias - lühinimi mida te kasutate käskudes. `ansible_host=10.0.0.10` on serveri tegelik IP aadress või hostname. `ansible_user=ubuntu` ütleb millise kasutajanimega Ansible peaks sisse logima.

Miks grupid on kasulikud? Sest siis saate käske suunata ainult teatud tüüpi serveritele. Näiteks käsk:

```bash
ansible webservers -m ping
```

See pingib ainult veebiserveid. Andmebaasid jäävad puutumata. See on väga oluline kui teil on sadu servereid erinevate rollidega. Te ei taha ju kogemata käivitada veebiserveri konfiguratsioon i andmebaasi serverites.

Inventory võib olla palju keerulisem. Saate teha hierarhilisi gruppe:

```ini
[ubuntu]
web1 ansible_host=10.0.0.10
web2 ansible_host=10.0.0.11

[alma]
db1 ansible_host=10.0.0.20
db2 ansible_host=10.0.0.21

[webservers:children]
ubuntu

[databases:children]
alma
```

Siin me ütleme et `webservers` grupp SISALDAB `ubuntu` gruppi. `:children` tähendab alamgruppe. Miks see on kasulik? Sest võite sihtida kas OS põhiselt (`ansible ubuntu -m command -a "apt update"`) või rolli põhiselt (`ansible webservers -m service -a "name=nginx state=restarted"`).

Võite lisada ka muutujaid:

```ini
[webservers:vars]
nginx_port=80
ssl_enabled=yes
```

Need muutujad on automaatselt kättesaadavad kõigis webservers grupi serverites. Playbook'is saate kasutada `{{ nginx_port }}` ja see asendatakse väärtusega 80.

Inventory on väga paindlik. Võite seda kirjutada ka YAML vormingus, võite kasutada dünaamilisi inventory skripte mis genereerivad serverite nimekirja (näiteks küsides AWS-st kõik serverid), võite kasutada mitut inventory faili korraga. Aga alustame lihtsast - lihtne INI fail on täiesti piisav.

### 3.2 Ad-hoc käsud - kiired testid ja ühekordsed toimingud

![Ad-hoc command examples](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GJP11bPQkG5ng30X-8wTDw.png)

Teine asi mida Ansible võimaldab on ad-hoc käsud. "Ad-hoc" tähendab "selleks juhtuks" - need on ühekordsed käsud mis te käivitate otse terminal'ist ilma playbook'i kirjutamata.

Millal ad-hoc käske kasutada? Nad on ideaalsed kiireks testimiseks, info kogumiseks või väikeste ühekordsete toimingute jaoks. Näiteks te tahate kontrollida kas kõik serverid on üleval - lihtsam on käivitada ad-hoc ping kui kirjutada playbook. Või te tahate näha kõikide serverite uptime'i - jälle, ad-hoc on kiirem.

Ad-hoc käsu struktuur on lihtne:

```bash
ansible <sihtmärk> -m <moodul> -a "<argumendid>"
```

Sihtmärk on kellele - võib olla grupi nimi nagu `webservers` või `all` mis tähendab kõiki. Moodul on MIS tegevust te tahate teha. Argumendid on mooduli parameetrid.

Vaatame mõnda praktilist näidet:

```bash
ansible all -m ping
```

See on kõige lihtsam käsk. Ta "pingib" kõiki servereid. See ei ole ICMP ping (nagu `ping` käsklus normaalses terminalis) vaid Ansible'i oma ping. See kontrollib kas SSH ühendus töötab, kas Python on olemas, kas Ansible saab käske käivitada. Väljund näeb välja umbes nii:

```
web1 | SUCCESS => {"ping": "pong"}
web2 | SUCCESS => {"ping": "pong"}
```

SUCCESS tähendab et ühendus töötab. "pong" on Ansible'i vastus "ping"-ile - nagu lauatennises.

Teine näide:

```bash
ansible all -m command -a "uptime"
```

See käivitab `uptime` käsu kõikides serverites. Väljund näitab kui kaua iga server on töötanud:

```
web1 | CHANGED | rc=0 >>
 14:30:15 up 2 days,  5:23,  1 user,  load average: 0.00

web2 | CHANGED | rc=0 >>
 14:30:15 up 5 days, 12:45,  2 users,  load average: 0.15
```

CHANGED tähendab et käsk käivitati (kuigi midagi ei muutunud). rc=0 on return code - 0 tähendab õnnestumist.

Kolmas näide - paketi paigaldamine:

```bash
ansible webservers -m apt -a "name=htop state=present" --become
```

See paigaldab `htop` programmi kõikidesse veebiserveritest. `apt` moodul on Debian/Ubuntu paketihaldur. `state=present` tähendab "veendu et see on olemas". `--become` tähendab et kasuta sudo õigusi (sest paketi paigaldamine vajab admin õigusi).

Neljast näide - faili kopeerimine:

```bash
ansible all -m copy -a "src=test.txt dest=/tmp/test.txt"
```

See kopeerib faili `test.txt` teie arvutist kõikidesse serveritesse `/tmp/` kausta.

Ad-hoc käsud on väga võimsad ja kiired. Aga kui te hakkate tegema midagi keerukamat - näiteks paigaldama nginx'i, kopeerima konfiguratsiooni, restartima teenust - siis on parem kirjutada playbook. Playbook on korduvkasutatav, dokumenteeritud ja saate seda versioonikontrolli panna.

### 3.3 Playbooks - automatiseeritud töövood

![Simple playbook structure](https://hkrtrainings.com/storage/photos/843/Playbook%20structure.png)

Nüüd jõuame Ansible'i südamikuni - playbook'id. Playbook on YAML vormingus fail mis sisaldab ülesannete jada. See on põhiline viis kuidas te Ansible'iga töötate.

Miks nimetatakse seda "playbook"? Mõelge spordile - näiteks korvpall või jalgpall. Meeskondadel on "playbook" kus on kirjas erinevad taktikad ja strateegiad. "Kui olukord X, siis tee Y." Ansible playbook on sarnane - seal on kirjas mida teha, mis järjekorras, mis tingimustel.

Vaatame lihtsat playbook'i:

```yaml
---
- name: Install and start nginx
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes
```

Lahti seletades rea-realt. Kolm kriipsu `---` on YAML standard - see tähistab dokumendi algust. Kriipsuga algavad read on loendi elemendid. Siin on meil üks element - üks "play".

`name: Install and start nginx` on kirjeldus. See on inimestele - et te näeksite ekraanil mis toimub. Ansible ise seda ei kasuta.

`hosts: webservers` ütleb millistes serverites see play jookseb. Sel juhul kõikides serverites mis on `webservers` grupis inventory's.

`become: yes` tähendab et kasuta sudo õigusi. Paljud toimingud nagu pakettide paigaldamine või teenuste käivitamine vajavad admin õigusi.

`tasks:` alustab ülesannete loendit. Iga task on eraldi element loendis (kriipsuga).

Esimene task: `name: Install nginx` on jälle kirjeldus. `apt:` on mooduli nimi. Apt on Debian/Ubuntu paketihaldur. `name: nginx` ja `state: present` on mooduli parameetrid. See ütleb: "Veendu et nginx pakett on installitud."

Teine task käivitab nginx'i teenuse. `service:` moodul haldab süsteemi teenuseid. `state: started` tähendab "veendu et teenus töötab". `enabled: yes` tähendab "veendu et teenus käivitub automaatselt boot'imisel".

Playbook'i käivitate nii:

```bash
ansible-playbook -i inventory.ini install_nginx.yml
```

`-i` määrab inventory faili. Käsu käivitamisel näete väljundit:

```
PLAY [Install and start nginx] ***************

TASK [Gathering Facts] ***********************
ok: [web1]
ok: [web2]

TASK [Install nginx] *************************
changed: [web1]
ok: [web2]

TASK [Start nginx service] *******************
changed: [web1]
ok: [web2]

PLAY RECAP ***********************************
web1    : ok=3    changed=2    unreachable=0    failed=0
web2    : ok=3    changed=0    unreachable=0    failed=0
```

Siin näeme et web1 serveris nginx paigaldati ja käivitati (changed=2). Web2 serveris oli juba kõik õige (changed=0). See on idempotentsus tööl!

### 3.4 YAML süntaks - minimaalne vajalik

![YAML syntax examples](https://thedeveloperstory.com/wp-content/uploads/2021/12/yaml-syntax.png)

Kuna playbook'id on YAML vormingus, peate teadma YAML-i põhitõdesid. YAML on väga lihtne - see on lihtsalt struktureeritud tekst kus struktuur näidatakse taandetega.

YAML tähendab "YAML Ain't Markup Language" (jah, see on rekursiivne akronüüm). YAML loodi olema inimloetav. See ei ole programmeerimiskeel - see on lihtsalt andmeformaat, nagu JSON, aga palju lihtsamini loetav.

Põhireeglid:

**Võti-väärtus paarid:**
```yaml
key: value
name: nginx
port: 80
enabled: true
```

Väga oluline - pärast koolonit PEAB olema tühik! `key:value` ei tööta. `key: value` töötab. See on üks tavaline viga.

**Loendid:**
```yaml
packages:
  - nginx
  - php
  - mysql
```

Loendi elemendid algavad kriipsuga ja tühikuga. Taanded peavad olema õiged - kõik elemendid peavad olema sama taseme.

**Pesastatud struktuurid:**
```yaml
server:
  name: web1
  ip: 10.0.0.10
  port: 80
```

Siin on `server` mis sisaldab kolme võtit. Taanded näitavad pesastust.

**Kommentaarid:**
```yaml
# See on kommentaar
name: nginx  # See ka
```

Kommentaarid algavad `#` sümboliga.

**Kriitilised reeglid:**

1. Kasutage AINULT tühikuid, MITTE tab'e. YAML ei luba tab'e. Kui proovite, saate vea. Tavaliselt kasutatakse 2 või 4 tühikut per taandus tase.

2. Taanded peavad olema järjepidevad. Kui alustate 2 tühikuga, siis kasutage kõikjal 2 tühikut.

3. Pärast koolonit peab olema tühik.

4. Stringid ei vaja tavaliselt jutumärke, aga kui string sisaldab erisümbole, siis võib vaja minna.

See on kõik mida te peate YAML-ist teadma et alustada. YAML on disainitud olema lihtne ja kui te järgite neid põhireegel, siis läheb hästi.

### 3.5 Moodulid - Ansible'i tööriistad

![Popular Ansible modules list](https://www.middlewareinventory.com/wp-content/uploads/2022/11/ansible-uri-module-parameters-1024x906.png)

Viimane asi mida peame põhikomponentide juures mainima on moodulid. Moodulid on Ansible'i "tööriistad" - igaüks teeb ühe konkreetse asja.

Ansible'is on üle 3000 mooduli. See kõlab hirmutavalt palju aga ära kartke - te ei pea kõiki teadma. On võibolla 20-30 moodulit mida kasutatakse 90% ajast. Ülejäänud on spetsiaalsed juh tud jaoks.

Mõned kõige tavalisemad moodulid:

**`apt` ja `yum`** - paketihaldus. `apt` on Debian/Ubuntu jaoks, `yum` (või uuem `dnf`) on RedHat/CentOS/Alma jaoks. Kui te tahate kirjutada OS-agnostiliselt, võite kasutada `package` moodulit mis automaatselt valib õige.

**`service` (või `systemd`)** - teenuste haldamine. Käivitamine, peatamine, restartamine. `systemd` on täpsemalt systemd spetsiifiline, `service` töötab mitmete init süsteemidega.

**`copy`** - failide kopeerimine teie control node'st serveritesse. Lihtne faili üle kandmine.

**`template`** - failide genereerimine template'idest. Template võib sisaldada muutujaid mis asendatakse väärtustega. Näiteks konfiguratsioonifail kus port number tuleb muutujast.

**`file`** - failide ja kaustade haldamine. Saate luua kaustu, muuta õigusi, kustutada faile, luua symlinke.

**`user` ja `group`** - kasutajate ja gruppide haldamine. Luua, muuta, kustutada kasutajaid.

**`command` ja `shell`** - käskude käivitamine. `command` on turvalisem aga piiratum - ei luba pipe'e, redirection'i. `shell` lubab kõike aga on vähem turvaline. Kasutage `command` kui võimalik.

**`git`** - Git repositooriumite haldamine. Saate kloonida, pullida, checkoutida.

**`docker_container`, `docker_image`** - Dockeri haldamine kui te kasutate konteinereid.

Iga mooduli kohta saate vaadata dokumentatsiooni:

```bash
ansible-doc apt
```

See näitab kõiki parameetreid, näiteid, selgitusi. Ansible'i dokumentatsioon on väga hea - peaaegu iga küsimuse vastus on seal.

Oluline mõista - moodulid on idempotentsed. Näiteks `apt` moodul ei ürita paigaldada paketti kui see on juba olemas. `service` moodul ei ürita käivitada teenust kui see juba töötab. See on see mis teeb Ansible'i turvaliseks.

---

## 4. Praktilene demo

### 4.1 Setup kontroll


Nüüd vaatame koos kiire demo läbi. See ei ole veel labor - see on lihtsalt illustratsioon. Te ei pea detaile jälgima või märkmeid tegema. Labor on kohe pärast seda ja seal te teete kõike ise samm-sammult.

Eeldame et meil on töökeskkond valmis. Proxmox'is on meil Windows jumpbox kus on VS Code, on WSL2 kus on Ansible, ja on 4 Linux serverit - 2 Ubuntu ja 2 Alma. Inventory fail on kirjutatud.

Avame terminali...

### 4.2 Ping test - kas ühendus töötab?

Esimene asi mida alati teeme on ping test:

```bash
ansible -i inventory.ini all -m ping
``

Näete ekraanil väljundit. Iga serveri kohta näete "SUCCESS" ja "ping: pong". See tähendab et SSH ühendus töötab, Python on olemas ja Ansible saab käske käivitada. Kui näeksite "UNREACHABLE" või "FAILED", siis on mingi probleem - võibolla SSH võti pole õigesti seadistatud või IP aadress on vale.

### 4.3 Ad-hoc command - hostname ja uptime

Nüüd käivitame lihtsa käsu:

```bash
ansible -i inventory.ini all -m command -a "hostname && uptime"
```

Siin näete et iga server tagastab oma hostname'i ja uptime'i. Ubuntu1 on töötanud 2 päeva, Alma1 on töötanud 5 päeva jne. See on kasulik kiire ülevaate saamiseks.

### 4.4 Lihtne playbook - faktide väljastamine

Lõpuks vaatame playbook'i. Ekraanil on fail `demo.yml`:

```yaml
---
- name: Demo playbook
  hosts: all
  tasks:
    - name: Show system info
      debug:
        msg: |
          Hostname: {{ ansible_hostname }}
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          IP: {{ ansible_default_ipv4.address }}
```

`debug` moodul lihtsalt prindib teksti. Need kaksikud looksulud on muutujad - need on faktid (facts) mida Ansible automaatselt kogub. Ansible kogub iga serveri kohta tohutult informatsiooni - hostname, OS, IP aadress, mälu, CPU, kettad jne. Need on kõik kättesaadavad muutujatena.

Käivitame:

```bash
ansible-playbook -i inventory.ini demo.yml
```


Väljundis näete "PLAY [Demo playbook]" - see alustab. Siis "TASK [Gathering Facts]" - see käivitub automaatselt ja kogub informatsiooni. Siis meie task "Show system info" mis prindib iga serveri kohta info. Lõpus on "PLAY RECAP" - kokkuvõte.

Pange tähele - kui käivitate seda playbook'i uuesti, on tulemus sama. See on idempotentsus. Playbook ei muuda midagi, lihtsalt näitab infot, seega võite käivitada nii palju kordi kui tahate.

## Kokkuvõte ja küsimused

### Kokkuvõte

Oleme jõudnud loengu lõppu. Teeme kiire kokkuvõtte.

Täna õppisime Ansible'i põhitõdesid. Alustasime ajaloost - kuidas serverite haldamine on aastate jooksul arenenud käsitsist shell skriptideks, sealt Puppet ja Chef agentide juurde ja lõpuks Ansible'i lihtsale agentless lahendusele.

Rääkisime Ansible'i põhiideedest. Ansible on agentless - kasutab SSH-d mis on nagunii olemas. See on push-based - teie otsustate millal muudatused juhtuvad. See on idempotent - turvaline käivitada mitu korda.

Vaatasime kolme põhikomponenti. Inventory ütleb KELLELE käsud lähevad. Ad-hoc käsud on kiired testid. Playbook'id on automatiseeritud töövood kus kirjeldate soovitud seisundit.

Õppisime YAML põhitõdesid - see on lihtne andmeformaat. Rääkisime moodulitest - need on Ansible'i tööriistad igaks ülesandeks.


### Ressursid

Kui hiljem tahate rohkem õppida:

**docs.ansible.com** - ametlik dokumentatsioon. Seal on kõik. Iga mooduli täpne kirjeldus, näited, best practices.

**galaxy.ansible.com** - Ansible Galaxy. See on kogukonna jagatud komponentide repositoorium. Tuhanded valmis playbook'id ja rollid mida saate kasutada. Kui te tahate paigaldada midagi keerukat - näiteks Kubernetes cluster - on seal tõenäoliselt juba keegi selle teinud.

**yamllint.com** - kui te ei ole kindel kas teie YAML süntaks on õige, kleepige see siia. Ta kontrollib ja näitab vigu.

**VS Code Ansible extension** - kui kasutate VS Code't, installige Red Hati Ansible extension. See annab teile syntax highlighting'u, auto-complete'i, veasõnumid. Muudab playbook'ide kirjutamise palju lihtsamaks.
