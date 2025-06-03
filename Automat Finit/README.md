# 🔦 Automaton Validator

Un validator pentru automate finite care verifică corectitudinea structurii și definițiilor unui automat pe baza unui fișier de intrare.

---

## 📖 Descriere

Această aplicație Python validează automate finite prin analiza următoarelor componente:
- Alfabetul (Sigma) - simbolurile acceptate
- Stările automatului
- Stările finale și de start
- Tranzițiile între stări

---

## 📝 Funcționalități

- ✅ Parsarea fișierelor de definire a automatelor
- ✅ Validarea corectitudinii structurale a automatului
- ✅ Verificarea existenței stărilor de start
- ✅ Validarea unicității succesorului pentru simbolul 'S'
- ✅ Verificarea consistenței tranzițiilor
- ✅ Raportare detaliată a erorilor
- ✅ Afișarea informațiilor complete despre automat

---

## 🛠️ Utilizare

### 🚀 1. Pregătirea fișierului de intrare

Creează un fișier numit `test_automat.txt` în același director cu scriptul. Fișierul trebuie să aibă următorul format:

```
Sigma:
a
b
S
End

States:
q0,S
q1
q2,F
End

Transitions:
q0, a, q1
q1, b, q2
q0, S, q0
End
```

### 🚀 2. Rularea aplicației

```bash
python automaton_validator.py
```
---

## 🧩 Format fișier de intrare

### 🚀 Structura fișierului

Fișierul este împărțit în secțiuni delimitate de cuvinte cheie:

#### Secțiunea `Sigma:`
Definește alfabetul automatului (simbolurile acceptate).
```
Sigma:
a
b
S
End
```

#### Secțiunea `States:`
Definește stările automatului cu marcatori speciali:
- `,S` - stare de start
- `,F` - stare finală

```
States:
q0,S
q1
q2,F
End
```

#### Secțiunea `Transitions:`
Definește tranzițiile în formatul: `stare_sursa, simbol, stare_destinatie`

```
Transitions:
q0, a, q1
q1, b, q2
q0, S, q0
End
```

---

### 🎮 Reguli de format

- Liniile goale și comentariile (care încep cu `#`) sunt ignorate
- Fiecare secțiune se termină cu `End`
- Liniile cu `...` sunt ignorate (pot fi folosite ca placeholder)
- Spațiile din jurul virgulelor în tranziții sunt eliminate automat

---

## 🎯 Exemplu de ieșire

```
🔍 Citesc obligatoriu din fișierul: test_automat.txt
==================================================

=== INFORMAȚII DESPRE AUTOMAT ===
Alfabet (Sigma): ['S', 'a', 'b']
Stări: ['q0', 'q1', 'q2']
Stări finale: ['q2']
Stări de start: ['q0']
Numărul de tranziții: 3

=== VALIDARE ===
✅ VALIDARE REUȘITĂ: Automatul este valid!

=== TRANZIȚII ===
 1. q0 --(a)--> q1
 2. q1 --(b)--> q2
 3. q0 --(S)--> q0

🎉 Automatul este complet valid!
```
---

## ❗Validări efectuate

Aplicația verifică următoarele condiții:

1. **Existența stărilor de start**: Trebuie să existe cel puțin o stare marcată cu `,S`
2. **Unicitatea succesorului pentru 'S'**: Simbolul 'S' poate fi succedat de maximum o stare
3. **Consistența tranzițiilor**: 
   - Stările sursă și destinație trebuie să existe în lista de stări
   - Simbolurile din tranziții trebuie să existe în alfabet

---

## ⚔️ Mesaje de eroare comune

### ❗ Fișier lipsă
```
Eroare: Fișierul 'test_automat.txt' nu a fost găsit.
```
**Soluție**: Creează fișierul `test_automat.txt` în același director cu scriptul.

### ❗Format tranziție invalid
```
Eroare la linia X: format tranziție invalid 'linia_problematică'
```
**Soluție**: Verifică că tranzițiile respectă formatul `stare_sursa, simbol, stare_destinatie`.

### ❗Stare inexistentă
```
Tranziția X: starea sursă 'nume_stare' nu există în lista de stări
```
**Soluție**: Verifică că toate stările din tranziții sunt definite în secțiunea `States:`.

---

## 🧩 Structura codului

### 🛠️ Clasa `AutomatonValidator`

- `__init__()`: Inițializează structurile de date
- `parse_file(filename)`: Parsează fișierul de intrare
- `validate()`: Efectuează validările și raportează rezultatele
- `display_transitions()`: Afișează toate tranzițiile într-un format lizibil
