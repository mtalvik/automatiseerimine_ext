# Commit Sõnumite Juhend

**Kasutamine:** Kiire viide headeks commit sõnumiteks

---

## Conventional Commits Formaat

```
type(scope): description
```

### Type'id

| Type | Millal |
|------|--------|
| `feat` | Uus funktsioon |
| `fix` | Vea parandus |
| `docs` | Dokumentatsioon |
| `style` | Vormindus, tühikud |
| `refactor` | Koodi ümberkorraldamine |
| `test` | Testid |
| `chore` | Konfiguratsioon, dependency |

### Scope (valikuline)

Mis osa projektist: `(auth)`, `(api)`, `(ui)`, `(db)`

---

## Head Näited

```bash
feat(auth): add login endpoint
fix(api): handle null response in user query
docs(readme): add installation instructions
refactor(db): simplify query logic
test(calculator): add division by zero test
chore(deps): update Python to 3.11
style(app): fix indentation in main.py
```

---

## Halvad Näited

❌ **ÄRA tee nii:**
```
fix
update
asdf
changes
wip
final version
stuff
idk
```

✅ **Tee nii:**
```
fix(login): prevent empty username submission
feat(api): add user profile endpoint
docs: update README with usage examples
```

---

## Reeglid

1. **Kasuta käskivat kõneviisi:** "add" mitte "added"
2. **Alusta väikese tähega:** `feat: add` mitte `Feat: Add`
3. **Ära lõpeta punktiga**
4. **Max 50 tähemärki** first line'is
5. **Selgita MIDA tegid,** mitte kuidas

---

## Body (valikuline)

Kui vajad rohkem selgitust:

```
feat(auth): add JWT token authentication

Implemented JWT-based auth to replace session cookies.
Tokens expire after 1 hour, refresh tokens valid 30 days.

Closes #123
```

**Reeglid:**
- Tühi rida pärast first line'i
- Selgita MIKS, mitte MIS
- Viita issue'le kui on

---

## Kiire Kontroll

Enne commit'i küsi:

- [ ] Kas sõnum algab type'iga?
- [ ] Kas on selge, MIDA muutsin?
- [ ] Kas keegi 3 kuu pärast saab aru?
- [ ] Kas pole "fix" või "update"?

---

**Rohkem infot:**
- [Conventional Commits](https://www.conventionalcommits.org/)
- Vaata ka: `reference/whatthecommit.md` (kui tahad näha HALVAID näiteid 😄)