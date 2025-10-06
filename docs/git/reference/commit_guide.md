# WhatTheCommit Viitematerjal

**Kasutamine:** Kasutage seda viidet, kui vajate inspiratsiooni commit sõnumite jaoks

---

##  Mis see *tegelikult* on?

[WhatTheCommit.com](https://whatthecommit.com/) on sait, mis viskab sulle suvalisi commit-sõnumeid, sest sa oled ilmselt liiga laisk, et mõelda ise midagi paremat kui “update” või “asdfasdkjf”.

Kasuta seda ainult **kohalikes projektides**, muidu keegi vaatab su Git-ajalugu ja valandab kogemata.

## Kiire Seadistus, sest sul on kannatust umbes 6 sekundiks

**Lisa oma `~/.bashrc`-i:**

```bash
alias gitcommit='git commit -m "$(curl -s https://whatthecommit.com/index.txt)"'
```

**Või kui sa tahad teha seda "nagu proff":**

```bash
git config --global alias.commit-fun '!f() { git commit -m "$(curl -s https://whatthecommit.com/index.txt)"; }; f'
```

##  Kuidas see töötab? Ei tööta, see *toimib*… umbes.

```bash
$ git add .
$ gitcommit
[main a1b2c3d] i have no idea what i’m doing
 1 file changed, 1 panic attack triggered
```

## Mõned pärlid masinast, kes mõistab su hingevalu

* “commit before i break more shit” – väga ennetav
* “oops, forgot to add that file” – klassika
* “that last commit? oh, forget it” – Git-zen
* “trust me, it’s working” – valede tippvorm

## Mitte kasutada töö juures… kui sa tahad töökohta hoida

---

See tööriist sobib hästi:
 Prototüüpideks
 Kodukoodiks
 Identiteedikriisideks
 Projektideks, kus keegi päriselt loeb su commit-ajalugu