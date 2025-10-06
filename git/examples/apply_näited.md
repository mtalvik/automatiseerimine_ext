#  Git Apply Näited

**Eesmärk:** Näidata, kuidas kasutada Git apply käsku praktikas  
**Kontekst:** Kasutage neid näiteid, kui õpite patch failide rakendamist

---

##  Mis on Patch?

Patch on fail, mis sisaldab muudatuste kirjeldust. Seda saab kasutada, et rakendada muudatusi olemasolevatele failidele.

**Lihtne näide:**
- Sul on fail `app.py`
- Keegi teine teeb muudatusi ja saadab sulle patch faili
- Sa rakendad patch'i ja sinu fail uueneb automaatselt

---

##  Patch'id ja Versioonihaldus

### Miks kasutame patch'e?

**Versioonihalduse kontekstis:**
- **Bug fix'id** - kiire paranduste rakendamine
- **Code review'de järel** - muudatuste tegemine vastavalt tagasisidele
- **Meeskonnatöö** - teiste arendajate muudatuste lisamine
- **Backup** - muudatuste salvestamine enne commit'i

### Patch vs Git

| Meetod | Eelised | Puudused |
|--------|---------|----------|
| **Patch fail** | Lihtne, ei vaja Git'i | Ei salvesta ajalugu |
| **Git commit** | Täielik ajalugu | Nõuab Git'i |

**Millal kasutada patch'e:**
- Kiire paranduste tegemine
- Kui pole Git'i kasutuses
- Muudatuste jagamine e-mailiga
- Backup enne suuri muudatusi

---

##  Kuidas Rakendada Patch'i?

### Kaks Lihtsat Viisi

#### 1. Kasuta `patch` käsku (lihtsam)

```bash
patch failinimi.py < muudatused.diff
```

#### 2. Kasuta `git apply` käsku (Git projektides)

```bash
git apply muudatused.patch
```

---

##  Praktiline Näide

### Samm 1: Sul on fail `cpu_usage.py`

```python
#!/usr/bin/env python3

import psutil

def check_cpu_usage(percent):
    usage = psutil.cpu_percent()
    return usage < percent

if not check_cpu_usage(75):
    print("ERROR! CPU is overloaded")
else:
    print("Everything ok")
```

### Samm 2: Saad patch faili `cpu_usage.diff`

```
--- cpu_usage.py	2019-06-23 08:16:04.666457429 -0700
+++ cpu_usage_fixed.py	2019-06-23 08:15:37.534370071 -0700
@@ -2,7 +2,8 @@
 import psutil
 
 def check_cpu_usage(percent):
-    usage = psutil.cpu_percent()
+    usage = psutil.cpu_percent(1)
+    print("DEBUG: usage: {}".format(usage))
     return usage < percent
 
 if not check_cpu_usage(75):
```

### Samm 3: Rakenda patch

```bash
patch cpu_usage.py < cpu_usage.diff
```

Vastus: `patching file cpu_usage.py`

### Samm 4: Kontrolli tulemust

```bash
cat cpu_usage.py
```

**Tulemus:**
```python
#!/usr/bin/env python3

import psutil

def check_cpu_usage(percent):
    usage = psutil.cpu_percent(1)
    print("DEBUG: usage: {}".format(usage))
    return usage < percent

if not check_cpu_usage(75):
    print("ERROR! CPU is overloaded")
else:
    print("Everything ok")
```

**Mida juhtus?**
- Lisati parameeter `1` funktsiooni sisse
- Lisati debug väljund
- Fail uuenes automaatselt!

---

##  Lihtne Harjutus

### Proovi Ise!

**Samm 1:** Loo fail `hello.py`
```python
def greet(name):
    print("Hello, " + name)
```

**Samm 2:** Loo patch fail `hello_fix.patch`
```
--- hello.py	2023-12-01 10:00:00 +0000
+++ hello_fixed.py	2023-12-01 10:01:00 +0000
@@ -1,2 +1,3 @@
 def greet(name):
-    print("Hello, " + name)
+    print("Hello, " + name + "!")
+    print("How are you?")
```

**Samm 3:** Rakenda patch
```bash
patch hello.py < hello_fix.patch
```

**Samm 4:** Kontrolli tulemust
```bash
cat hello.py
```

---

##  Kasulikud Käsud

```bash
# Lihtne patch rakendamine
patch fail.py < muudatused.diff

# Git projektides
git apply muudatused.patch

# Kontrolli patch'i enne rakendamist
git apply --check muudatused.patch
```

---

##  Kokkuvõte

### Mida õppisid?

- Mis on patch fail
- Kuidas rakendada lihtsaid muudatusi
- Kaks viisi patch'i rakendamiseks
- Praktiline näide CPU kasutuse kohta

### Järgmised Sammud

Kui oled valmis keerukamate asjade jaoks:
- Lugeda diff väljundit (vaata `git_diff_examples.md`)
- Lahendada konflikte
- Kasutada git am ja muid täpsemaid tööriistu

### Versioonihalduse Järgmised Sammud

Pärast patch'ide õppimist:
- **Git commit'id** - muudatuste salvestamine ajalukku
- **Git branch'id** - paralleelsete arendusliinide haldamine
- **Git merge** - harude ühendamine
- **Pull Request'id** - meeskonnatöö GitHub'is

**Patch'i rakendamine on lihtne ja kasulik oskus versioonihalduses!**

---

*Materjal põhineb Git'i ametlikul dokumentatsioonil*
