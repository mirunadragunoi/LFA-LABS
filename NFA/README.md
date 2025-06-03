# 🌀 NFA String Verifier (Automat Finit Nondeterminist)

Acest program permite încărcarea unui **automat finit nedeterminist (NFA)** dintr-un fișier de configurare și verificarea unui string pentru a determina dacă este **acceptat** sau **respins** de automat.

---

## 📦 Caracteristici

- Încărcarea și validarea automatelor din fișiere.
- Procesarea stringurilor pas cu pas, cu log detaliat.
- Suport pentru tranziții epsilon (`ε`).
- Detectarea stărilor de start și finale.
- Analiză pentru tranziții nedeterministe și epsilon.
- Generarea unui **arbore de computație** pentru stringuri scurte.

---

## ▶️ Cum se rulează

```bash
python nfa.py <fisier_config_nfa> <string_de_verificat>
```
### 🔁 Exemple:
```bash
python nfa.py nfa_input1.txt 1001
python nfa.py nfa_input2.txt ab
```
---

## 📝 Structura fișierului de configurare
Fișierul de intrare (ex: nfa_input1.txt) trebuie să respecte următorul format:

```text
Sigma:
0
1
ε
End

States:
q0,S
q1
q2,F
End

Transitions:
q0, 0, q0
q0, 1, q0
q0, 1, q1
q1, 0, q2
q0, ε, q1
End
```
---
## 🔹 Legenda:
- Sigma: – simbolurile din alfabet (inclusiv ε pentru tranziții epsilon).

- States: – lista stărilor. Adaugă ,S pentru starea de start, ,F pentru stările finale.

- Transitions: – fiecare tranziție este pe formatul stare_sursă, simbol, stare_destinație.

---

## ✅ Output-ul programului
Programul va afișa:

- Informații despre automat (alfabet, stări, tranziții).

- Pas cu pas verificarea stringului.

- Rezultatul final (ACCEPT sau REJECT).

- Arborele de computație pentru stringuri scurte (≤ 5 simboluri).

---

## ⚠️ Erori comune
- Lipsa stării de start (qX,S).

- Tranziții către stări inexistente.

- Simboluri din input care nu apar în alfabet.

- Simbolul ε în stringul de input (nu este permis).

## 🧠 Exemplu de arbore de computație
Pentru stringuri scurte, programul afișează toate căile posibile prin care NFA-ul poate ajunge la un rezultat (acceptare sau respingere).