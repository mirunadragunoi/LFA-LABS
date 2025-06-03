# 🤖 Turing Machine Simulator
_Implementare completă a unui simulator de mașini Turing în Python, cu încărcare din fișiere JSON, validare automată și execuție pas cu pas._

---

## 📖 Descriere
Acest proiect implementează un simulator complet pentru mașini Turing care poate:

- Încărca configurații din fișiere JSON
- Valida automat configurațiile pentru erori
- Simula execuția pas cu pas sau completă
- Gestiona banda infinită cu extensie automată
- Detecta stări finale (accept/reject/halt)

Proiectul este compus din 3 componente principale:

- **tm_engine.py** - Engine-ul principal cu clasele TM
- **main.py** - Program de testare și exemple
- **examples.json** - Colecție de configurații TM predefinite

---

## ✨ Caracteristici

- ✅ Simulare completă TM - Implementare conform definiției teoretice
- ✅ Bandă infinită - Extensie automată în ambele direcții
- ✅ Validare configurații - Verificare automată pentru erori de sintaxă/logică
- ✅ Import/Export JSON - Încărcare și salvare configurații
- ✅ Execuție controlată - Limită de pași pentru evitarea buclelor infinite
- ✅ Status tracking - Monitorizare stare (running/accepted/rejected/halted)

---

## ✨ Exemplu de utilizare
```bash
loader = TMConfigLoader()
is_valid, config, errors = loader.load_from_file("palindrome_checker.json")

if is_valid:
    tm = TuringMachine(config)
    status, output, steps = tm.run("1001")
    print(f"Rezultat: {status.value}, Output: {output}")
else:
    print("Erori:", errors)
```
# 🚀 _Testare Batch_
```bash
# Testează multiple input-uri
test_cases = ["101", "1001", "11011", "110"]
for input_str in test_cases:
    status, output, steps = tm.run(input_str)
    print(f"'{input_str}' -> {status.value} ({steps} pași)")
```
# 🚀 _Execuție Pas cu Pas_
```bash
tm = TuringMachine(config)
tm.load_input("101")

while tm.step():
    print(f"Stare: {tm.current_state}, Poziție: {tm.head_position}")
    print(f"Bandă: {tm.get_tape_content()}")

print(f"Status final: {tm.status.value}")
```

# 🚀 _Creare TM Personalizat_
```bash
# Definiție TM care schimbă 0->1
my_tm_config = {
    "name": "0 to 1 converter",
    "states": ["q0", "q1", "done"],
    "alphabet": ["0", "1"],
    "tape_alphabet": ["0", "1", "_"],
    "start_state": "q0",
    "accept_states": ["done"],
    "reject_states": [],
    "transitions": [
        {"from_state": "q0", "read_symbol": "0", 
         "to_state": "q1", "write_symbol": "1", "direction": "R"},
        {"from_state": "q1", "read_symbol": "0", 
         "to_state": "q1", "write_symbol": "1", "direction": "R"},
        {"from_state": "q1", "read_symbol": "_", 
         "to_state": "done", "write_symbol": "_", "direction": "S"}
    ]
}
```

# 🚀 _Salvează și testează_
```bash
TMConfigLoader.save_to_file(my_tm_config, "my_converter.json")
```

---

# 📝 Format Configurație JSON
## _Structura Completă_
```bash
json{
  "name": "Nume descriptiv",
  "description": "Descriere funcționalitate",
  "states": ["q0", "q1", "accept", "reject"],
  "alphabet": ["0", "1"],
  "tape_alphabet": ["0", "1", "X", "_"],
  "blank_symbol": "_",
  "start_state": "q0",
  "accept_states": ["accept"],
  "reject_states": ["reject"],
  "max_steps": 1000,
  "transitions": [
    {
      "from_state": "q0",
      "read_symbol": "0",
      "to_state": "q1",
      "write_symbol": "X",
      "direction": "R"
    }
  ]
}
```

---

## 📌 Câmpuri Obligatorii

- states: Lista toate stările TM
- alphabet: Alfabetul de intrare
- tape_alphabet: Alfabetul benzii (include alphabet + simboluri auxiliare)
- start_state: Starea inițială
- accept_states: Stări de acceptare
- reject_states: Stări de respingere
- transitions: Lista tranzițiilor

## 📌 Câmpuri Opționale

- name: Nume descriptiv
- description: Descriere funcționalitate
- blank_symbol: Simbolul blank (default: "_")
- max_steps: Limită pași execuție (default: 1000)

## 📌 Direcții Valide

- "L": Stânga (Left)
- "R": Dreapta (Right)
- "S": Rămâne (Stay)

# 📌 Metode principale
- ✅ **tm.run(input_string: str)** -> (TMState, str, int)
- ✅ **tm.step()** -> bool
- ✅ **tm.load_input(input_string: str)**
- ✅ **tm.get_tape_content()** -> str

---

## 🎯 Exemple TM Incluse
### 🧩 **1. Palindrome Checker (palindrome_checker.json)**

- Funcție: Verifică dacă un string binar este palindrom
- Input: Stringuri binare (ex: "101", "1001")
- Output: Accept/Reject
- Exemplu: "101" → ACCEPTED, "110" → REJECTED

### 🧩 2. Unary Incrementer (unary_incrementer.json)

- Funcție: Incrementează un număr în reprezentare unară
- Input: Stringuri de "1" (ex: "111" = numărul 3)
- Output: String cu un "1" în plus
- Exemplu: "111" → "1111" (3 → 4)

### 🧩 3. Copy Machine (copy_machine.json)

- Funcție: Dublează un string binar
- Input: String binar (ex: "01")
- Output: String dublat
- Exemplu: "01" → "0101"

---

## 🔍 Testare și Debugging
### ❗Mod Testare Automată
```bash
main.py
```
### ❗ Rulează toate testele predefinite
### _Mod Interactiv_
```bash 
# În main.py, alege opțiunea interactivă
# Poți încărca orice fișier JSON și testa cu input-uri personalizate
```
### _Debugging Pas cu Pas_
```bash 
tm = TuringMachine(config)
tm.load_input("test_input")
```
