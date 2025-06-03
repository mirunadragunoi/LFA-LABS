# 📘 CFG System - Lucru cu Gramatica Independență de Context

Acest proiect oferă un sistem interactiv pentru încărcarea, crearea, validarea și testarea gramaticilor independente de context (CFG), utile în teoria limbajelor formale, limbaje de programare și compilatoare.

---

## 🔧 Funcționalități principale

### ✅ 1. **Încărcare și validare (`load`)**
   - Încarcă o gramatică din fișiere `.json` sau format text simplificat.
   - Verifică dacă simbolurile sunt definite corect.
   - Asigură că variabila de start există.

### ✅ 2. **Creare interactivă (`create`)**
   - Permite utilizatorului să introducă pas cu pas:
     - Variabile (non-terminali)
     - Terminali
     - Variabila de start
     - Reguli de producție
   - Gramatica poate fi salvată în format `.json` sau `.txt`.

### ✅ 3. **Generare exemple (`exemple`)**
   - Creează automat gramatici pentru:
     - Expresii aritmetice (`+`, `*`, paranteze)
     - Paranteze balansate
     - Palindroame peste `{0,1}`
     - Șiruri cu număr egal de `0` și `1`

### ✅ 4. **Testare derivare (`test`)**
   - Verifică dacă un șir dat poate fi derivat din gramatică (derivare din stânga).
   - Afișează pașii de derivare.

---

## ▶️ Exemple de utilizare

```bash
# 1. Crează exemple predefinite
python cfg.py exemple

# 2. Încarcă o gramatică și valideaz-o
python cfg.py load exemple_arithmetic.json

# 3. Creează o gramatică nouă (salvată automat)
python cfg.py create nou_cfg.json

# 4. Testează derivarea unui șir
python cfg.py test exemple_balanced.json "(())"
```

---

## 📁 Format fișier JSON pentru CFG
```json
{
  "variables": ["S", "A"],
  "terminals": ["a", "b"],
  "start_variable": "S",
  "rules": {
    "S": ["a A", "b"],
    "A": ["a", "b"]
  }
}
```

---

## 📃 Format alternativ (text)
```bash
Variables:
S
A
End

Terminals:
a
b
End

Start:
S
End

Rules:
S -> a A | b
A -> a | b
End
```
---

## ✅ Output validare CFG
```bash
✅ CFG validation successful!
Variables (Non-terminals): ['S']
Terminals: ['(', ')']
Start Variable: S
Number of Production Rules: 3
S -> ( S ) | S S | epsilon
```

---

## 📄 Fișiere generate
- **exemple_arithmetic.json** – Expresii aritmetice

- **exemple_balanced.json** – Paranteze balansate

- **exemple_palindromes.json** – Palindroame

- **exemple_equal.json** – Număr egal de 0 și 1

---