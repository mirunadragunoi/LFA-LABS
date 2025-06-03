# 🧠🚀 DFA Engine

Un program simplu în Python care permite încărcarea, validarea și rularea unui **automat finit determinist (DFA)**, pe baza unei configurații date într-un fișier text. Programul primește ca argumente în linia de comandă fișierul de configurare și un șir de caractere care trebuie verificat.

---

## 📁 Structura Proiectului
```bash
dfa.py # Codul sursă principal
dfa_input1.txt # Exemplu de fișier de configurare pentru un DFA
dfa_input2.txt
dfa_input3.txt
```

--- 

## 🧩 Formatul Fișierului de Configurare (ex: `dfa_input1.txt`, `dfa_input2.txt`, `dfa_input3.txt`)

Fișierul trebuie să respecte următorul format secvențial:
```bash
Sigma:
0
1
End

States:
q0,S
q1
q2,F
End

Transitions:
q0, 0, q1
q1, 1, q2
q2, 0, q0
End
```

- `Sigma:` ... `End` – definește alfabetul (simbolurile de intrare)
- `States:` ... `End` – definește stările:
  - `,S` marchează starea de start
  - `,F` marchează o stare finală
  - `,S,F` sau `,F,S` marchează o stare care este și de start și finală
- `Transitions:` ... `End` – definește tranzițiile în format: `stare_curentă, simbol, stare_următoare`

---

## ⚙️ Cum se rulează

```bash
python dfa.py <fisier_configurare> <string_de_testat>
```
---

## 🔍 Exemple:
```bash
python dfa.py dfa_input1.txt 010
python dfa.py dfa_input1.txt 1101
```

---

## 🛠️ Funcționalități
- ✅ Încarcă și validează un DFA din fișier

- ✅ Afișează informații detaliate despre DFA (stări, alfabet, tranziții etc.)

- ✅ Rulează un șir de intrare și indică dacă este acceptat sau respins

- ✅ Detectează și raportează erori de configurare:

  - ❗Lipsa stării de start

  - ❗Tranziții invalide

  - ❗Simboluri necunoscute

---

## 🔐 Validări efectuate
- 🧩 DFA-ul are exact o stare de start

- 🧩 Fiecare tranziție duce spre o stare existentă

- 🧩 Simbolurile din tranziții fac parte din alfabetul definit