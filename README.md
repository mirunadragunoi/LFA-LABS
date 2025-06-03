# 🤖 LFA Labs - Limbaje Formale și Automate

Un repository complet cu implementări practice ale conceptelor fundamentale din **Limbaje Formale și Automate (LFA)**. Toate implementările sunt realizate în Python și includ exemple interactive și documentație detaliată.

---

### 🎓 Concepte Acoperite

- **Automate Finite** (DFA/NFA)
- **Conversii între Automate**
- **Gramatici Context-Free (CFG)**
- **Automate cu Stivă (PDA)**
- **Mașini Turing**
- **Aplicații Interactive**

---

## 🚀 Instalare și Configurare

### Cerințe de Sistem
- **Python 3.8+**
- **pip** (Python package manager)
- **Git** (pentru clonare)

### Instalare Rapidă
```bash
# Clonează repository-ul
git clone https://github.com/mirunadragunoi/LFA-LABS.git
cd LFA-LABS

# Creează environment virtual (recomandat)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# SAU
venv\Scripts\activate     # Windows

# Instalează dependențele
pip install -r requirements.txt
```

### Verificare Instalare
```bash
# Rulează toate testele
python -m pytest tests/

# Testează un modul specific
python lab1-dfa/dfa_examples.py
```

## 🔬 Laboratoare și Implementări

### 🔄 DFA (Deterministic Finite Automaton)
**Funcționalități:**
- Definirea și simularea DFA
- Validarea cuvintelor
- Minimizarea automatelor
- Vizualizare grafică

### 🌟 NFA (Nondeterministic Finite Automaton)
**Funcționalități:**
- Implementare completă NFA
- Suport pentru ε-tranziții
- Simularea nedeterministă
- Comparații cu DFA

### 🔄 Conversie NFA → DFA
**Funcționalități:**
- Algoritm de construcție a submulțimilor
- Eliminarea ε-tranzițiilor
- Optimizări pentru performanță
- Compararea automatelor rezultate

### 📝 CFG (Context-Free Grammar)
**Funcționalități:**
- Parsarea gramaticilor context-free
- Generarea derivărilor
- Eliminarea recursiei stângi

### ⚙️ Automat Finit Generic
**Funcționalități:**
- Implementare generalizată
- Conversii între reprezentări
- Operații pe automate (uniune, intersecție)
- Construcția din expresii regulate

### 🖥️ Mașina Turing
**Funcționalități:**
- Simularea completă a Mașinii Turing
- Suport pentru multiple benzi
- Mașina Turing Universală
- Exemple de calcule clasice

### 🎮 Joc cu Automat cu Stivă (PDA)
**Funcționalități:**
- Joc interactiv text-based
- Implementare completă PDA
- Operații pe stivă (push/pop)

**Caracteristici joc:**
- 🗺️ Navigare prin camere
- 🎒 Sistem de inventar cu stivă
- 🎯 Obiective multiple
- 📊 Statistici detaliate

---
