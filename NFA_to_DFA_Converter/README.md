# 🧩 NFA to DFA Converter

Acest script Python convertește un automat finit nedeterminist (NFA) într-un automat finit determinist (DFA), utilizând algoritmul de construcție a subseturilor.

---

## 📄 Descriere

Scriptul primește ca argumente:

- ▶️ Fișierul de configurare al NFA-ului (`.json`), care poate conține un singur NFA sau mai multe exemple.
- ▶️ Un fișier gol sau nou în care va fi salvat automatul determinist (DFA) rezultat.
- ▶️ (Opțional) Numele unui exemplu specific de NFA dacă fișierul conține mai multe configurații.

Conversia se face prin determinarea **closure-ului epsilon** și construirea tranzițiilor deterministe între stări echivalente cu mulțimi de stări NFA.

---

## ▶️ Utilizare

```bash
python nfa_to_dfa_converter.py <nfa_input_file.json> <dfa_output_file.json> [nfa_example_key]
```

## 🔁 Exemple:
```bash
# Conversie NFA cu un singur exemplu
python nfa_to_dfa_converter.py single_nfa.json dfa_output.json

# Conversie NFA dintr-un fișier cu mai multe exemple
python nfa_to_dfa_converter.py nfa_examples.json dfa_output.json nfa_example_1
```

## 📁 Structura fișierului de intrare (NFA)
Un NFA valid trebuie să conțină următoarele câmpuri:
```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b", "ε"],
  "start_state": "q0",
  "final_states": ["q2"],
  "transitions": {
    "q0": { "a": ["q0"], "ε": ["q1"] },
    "q1": { "b": ["q2"] },
    "q2": {}
  }
}
```
Dacă sunt mai multe exemple în același fișier .json, ele pot fi împărțite astfel:

```json
{
  "nfa_example_1": {
    "description": "Un NFA simplu pentru testare",
    "states": [...],
    ...
  },
  "nfa_example_2": { ... }
}
```

## ✅ Structura fișierului de ieșire (DFA)
Exemplu de fișier generat:

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q2"],
  "transitions": {
    "q0": { "a": "q1" },
    "q1": { "b": "q2" }
  }
}
```

---


## 🔧 Funcționalități implementate
- ✅ Detectare și tratament automat pentru epsilon sau ε în tranziții.

- ✅ Identificarea stărilor finale în DFA pe baza celor din NFA.

- ✅ Afișare detaliată a procesului de conversie în terminal.

- ✅ Suport pentru multiple exemple într-un singur fișier .json.


## 📌 Erori posibile
- ⚠️ Fișierul de intrare nu există sau nu este valid JSON.

- ⚠️ Cheia nfa_example_key nu este găsită dacă este specificată.

- ⚠️ Fișierul conține mai multe exemple dar cheia nu este specificată.