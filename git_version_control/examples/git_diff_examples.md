# Git Diff ja Diff Väljundi Lugemine

**Kestus:** 30 minutit  
**Eesmärk:** Õppida lugema diff väljundit ja mõistma, mida iga sümbol tähendab

---

## 📖 Sissejuhatus Diff'i Lugemisse

Diff on tööriist, mis näitab failide vahelisi erinevusi. Git kasutab sama formaati, mis Unix/Linux `diff` käsk.

### Miks on oluline diff'i lugeda?

- **Code Review** - mõista, mida teised arendajad muutsid
- **Debugging** - leida, mis muutus ja tekitas vea
- **Version Control** - jälgida koodi ajalugu
- **Merge Conflicts** - lahendada konflikte

---

## 📖 Diff Väljundi Formaat

### Põhiline Struktuur

```
@@ -algusrida,read +algusrida,read @@
- eemaldatud rida
+ lisatud rida
  muutmata rida
```

### Sümbolite Tähendused

| Sümbol | Tähendus | Näide |
|--------|----------|-------|
| `-` | Eemaldatud rida | `- vana_kood = True` |
| `+` | Lisatud rida | `+ uus_kood = False` |
| ` ` (tühi) | Muutmata rida | `  print("tere")` |
| `@@` | Kontekst marker | `@@ -5,3 +5,4 @@` |

---

## 📖 Praktilised Näited

### Näide 1: Lihtne Rida Muutmine

**Fail 1 (rearrange1.py):**
```python
#!/usr/bin/env python3
import re

def rearrange_name(name):
    result = re.search(r"^([\w .]*), ([\w .]*)$", name)
    if result == None:
        return name
    return "{} {}".format(result[2], result[1])
```

**Fail 2 (rearrange2.py):**
```python
#!/usr/bin/env python3
import re

def rearrange_name(name):
    result = re.search(r"^([\w .-]*), ([\w .-]*)$", name)
    if result == None:
        return name
    return "{} {}".format(result[2], result[1])
```

**Diff väljund:**
```bash
$ diff rearrange1.py rearrange2.py
```

```
6c6
<     result = re.search(r"^([\w .]*), ([\w .]*)$", name)
---
>     result = re.search(r"^([\w .-]*), ([\w .-]*)$", name)
```

**Selgitus:**
- `6c6` = rida 6 esimeses failis muudeti rida 6 teises failis
- `<` = esimese faili sisu (eemaldatud)
- `---` = eraldaja
- `>` = teise faili sisu (lisatud)
- Muutus: lisati `-` sümbol regex'i `[\w .-]` sisse

### Näide 2: Mitme Rea Muutmine

**Fail 1 (validations1.py):**
```python
def validate_user(username, minlen):
    assert type(username) == str, "username must be a string"
    if minlen < 1:
        raise ValueError("minlen must be at least 1")
    
    if len(username) < minlen:
        return False
    if not username.isalnum():
        return False
    return True
```

**Fail 2 (validations2.py):**
```python
def validate_user(username, minlen):
    if type(username) != str:
        raise TypeError("username must be a string")
    if minlen < 1:
        raise ValueError("minlen must be at least 1")
    
    if len(username) < minlen:
        return False
    if not username.isalnum():
        return False
    # Usernames can't begin with a number
    if username[0].isnumeric():
        return False
    return True
```

**Diff väljund:**
```bash
$ diff validations1.py validations2.py
```

```
5c5,6
<	assert (type(username) == str), "username must be a string"
--
>	if type(username != str: 
> 	    raise TypeError("username must be a string"

11a13,15
>	    return False
>	# Usernames can't begin with a number
>	if username[0].isnumeric():
```

**Selgitus:**
- `5c5,6` = rida 5 muudeti ridadeks 5-6
- `11a13,15` = pärast rida 11 lisati read 13-15
- `assert` asendati `if` kontrolliga
- Lisati uus kontroll kasutajanime alguse kohta

### Näide 3: Unified Diff Formaat (-u)

**Sama diff unified formaadis:**
```bash
$ diff -u validations1.py validations2.py
```

```
--- validations1.py	2019-06-06 14:28:49.639209499 +0200
+++ validations2.py	2019-06-06 14:30:48.019360890 +0200
@@ -2,7 +2,8 @@
 
 def validate_user(username, minlen):
-    assert type(username) == str, "username must be a string"
+    if type(username) != str:
+        raise TypeError("username must be a string")
     if minlen < 1:
         raise ValueError("minlen must be at least 1")
     
@@ -10,5 +11,8 @@
         return False
     if not username.isalnum():
         return False
+    # Usernames can't begin with a number
+    if username[0].isnumeric():
+        return False
     return True
```

**Selgitus:**
- `---` ja `+++` = failide nimed ja ajamärgid
- `@@ -2,7 +2,8 @@` = kontekst: 7 rida esimesest failist, 8 rida teisest
- `-` ja `+` = eemaldatud ja lisatud read
- Tühjad read = kontekst (muutmata)

---

## 📖 Git Diff Näited

### Git Diff Töökausta vs Staging

```bash
$ git diff
```

```
diff --git a/app.py b/app.py
index a1b2c3d..e4f5g6h 100644
--- a/app.py
+++ b/app.py
@@ -10,7 +10,7 @@ def main():
     print("Tere maailm!")
     
     # Lisa uus funktsioon
-    old_function()
+    new_function()
     
     return 0
```

**Selgitus:**
- `diff --git` = Git'i diff formaat
- `index a1b2c3d..e4f5g6h` = Git'i sisemised hash'id
- `100644` = faili õigused
- `a/app.py` ja `b/app.py` = võrdlusfailid

### Git Diff Staging vs Commit

```bash
$ git diff --staged
```

```
diff --git a/config.py b/config.py
index f7g8h9i..j1k2l3m 100644
--- a/config.py
+++ b/config.py
@@ -5,6 +5,7 @@
 DATABASE_URL = "postgresql://localhost/mydb"
 DEBUG = True
 LOG_LEVEL = "INFO"
+API_KEY = "secret123"
 
 # Server settings
 PORT = 8000
```

**Selgitus:**
- `--staged` = võrdleb staging area'ga viimase commit'iga
- Lisati uus rida `API_KEY = "secret123"`

### Git Diff Kahe Commit'i Vahel

```bash
$ git diff HEAD~1 HEAD
```

```
diff --git a/main.py b/main.py
index x1y2z3a..b4c5d6e 100644
--- a/main.py
+++ b/main.py
@@ -15,8 +15,9 @@ def process_data(data):
     for item in data:
         if item.is_valid():
             processed.append(item)
-        else:
-            print(f"Invalid item: {item}")
+        elif item.has_warning():
+            print(f"Warning for item: {item}")
+            processed.append(item)
     return processed
```

**Selgitus:**
- `HEAD~1` = eelmine commit
- `HEAD` = praegune commit
- Muudeti `else` tingimus `elif` tingimuseks

---

## 📖 Diff'i Lugemise Sammud

### 1. Vaata Konteksti
```
@@ -5,3 +5,4 @@
```
- Mitu rida on muudetud?
- Millised read on kontekstis?

### 2. Tuvasta Muudatuste Tüübid
- **Eemaldamine** (`-`): vana kood
- **Lisamine** (`+`): uus kood
- **Kontekst** (tühi): muutmata read

### 3. Mõista Loogikat
- Miks tehti muudatus?
- Kas on breaking change?
- Kas on bug fix või feature?

### 4. Kontrolli Järgnevust
- Kas kõik muudatused on seotud?
- Kas on puuduvaid muudatusi?

---

## 📖 Harjutused

### Harjutus 1: Loe Diff'i

```bash
$ git diff
```

```
diff --git a/utils.py b/utils.py
index a1b2c3d..e4f5g6h 100644
--- a/utils.py
+++ b/utils.py
@@ -20,5 +20,6 @@ def format_name(first, last):
     if not first or not last:
         return "Unknown"
-    return f"{first} {last}"
+    return f"{first.capitalize()} {last.capitalize()}"
```

**Küsimused:**
1. Mida muudeti?
2. Miks tehti muudatus?
3. Kas on breaking change?

### Harjutus 2: Analüüsi Suuremat Diff'i

```bash
$ git diff HEAD~2
```

```
diff --git a/app.py b/app.py
index x1y2z3a..b4c5d6e 100644
--- a/app.py
+++ b/app.py
@@ -10,12 +10,15 @@ def main():
     config = load_config()
     
-    if config.debug:
-        print("Debug mode enabled")
-    
     try:
         app = create_app(config)
+        if config.debug:
+            print("Debug mode enabled")
+            app.debug = True
+        
         app.run(host='0.0.0.0', port=config.port)
+    except Exception as e:
+        print(f"Error starting app: {e}")
+        return 1
     
     return 0
```

**Küsimused:**
1. Mitu muudatust tehti?
2. Millised on peamised muudatused?
3. Kas on lisatud error handling?

---

## 📖 Kasulikud Diff Käsud

### Git Diff Variandid

```bash
# Töökausta vs staging
git diff

# Staging vs viimane commit
git diff --staged

# Töökausta vs viimane commit
git diff HEAD

# Kahe commit'i vahel
git diff commit1..commit2

# Kahe branch'i vahel
git diff main..feature

# Konkreetse faili muudatused
git diff -- app.py

# Word-level diff (sõnade tasemel)
git diff --word-diff

# Side-by-side diff
git diff --side-by-side
```

### Regulaar Diff Käsud

```bash
# Unified diff
diff -u fail1.txt fail2.txt

# Context diff (3 rida konteksti)
diff -c fail1.txt fail2.txt

# Ignore whitespace
diff -w fail1.txt fail2.txt

# Ignore case
diff -i fail1.txt fail2.txt

# Recursive diff kaustadele
diff -r kaust1/ kaust2/
```

---

## 📖 Kokkuvõte

### Olulised Punktid

1. **Diff formaat** on standardne Unix/Linux maailmas
2. **Git diff** kasutab sama formaati
3. **Sümbolid** `-`, `+`, ` ` on võtmed lugemiseks
4. **Kontekst** aitab mõista muudatuste tähendust
5. **Unified diff** (-u) on kõige loetavam

### Parimad Praktikad

- **Alusta kontekstist** - vaata @@ rida
- **Tuvasta muudatuste tüübid** - lisamine/eemaldamine
- **Mõista loogikat** - miks tehti muudatus
- **Kontrolli järgnevust** - kas kõik on seotud
- **Kasuta graafilisi tööriistu** - vajaduse korral

### Järgmised Sammud

Pärast seda materjali peaksite oskama:
- Lugeda diff väljundit
- Mõista muudatuste tähendust
- Analüüsida koodi muudatusi
- Kasutada erinevaid diff käske
- Teha code review'e

**Harjutage diff'i lugemist iga päev - see on oluline oskus arendaja karjääris!**

---

*Materjal põhineb Unix diff standarditel ja Git'i dokumentatsioonil*
