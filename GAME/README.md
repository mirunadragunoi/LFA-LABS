# 🎮 Joc de Aventură - Automat Finit cu Stivă

Un joc text-based de aventură implementat ca un **Pushdown Automaton** (automat finit cu stivă) în Python. Jocul demonstrează conceptele de teoria automatelor și structuri de date prin gameplay interactiv.

---

## 📋 Cuprins

- [Descriere](#-descriere)
- [Caracteristici](#-caracteristici)
- [Instalare și Rulare](#-instalare-și-rulare)
- [Cum să Joci](#-cum-să-joci)
- [Teoria Automatelor](#-teoria-automatelor)
- [Structura Codului](#-structura-codului)
- [Harta Jocului](#️-harta-jocului)

---

## 🎯 Descriere

Acest joc implementează un labirint interactiv unde jucătorul trebuie să navigheze prin diferite camere pentru a scăpa. Jucătorul începe la intrare și trebuie să găsească lingura din bucătărie pentru a putea ieși prin **Mega Exit** și a obține victoria supremă.

### Obiectivul Jocului
- 🎯 **Obiectiv Principal**: Scapă prin Mega Exit cu lingura
- 🥄 **Obiectiv Secundar**: Găsește și colectează lingura din bucătărie
- 🚪 **Alternativă**: Ieși prin Exit normal (fără lingură)

## ✨ Caracteristici

### 🤖 Implementare ca Automat Finit
- **Pushdown Automaton** (PDA) cu două stive
- Tranziții de stare deterministe
- Validare automată a mișcărilor
- Gestionarea inventarului prin operații PUSH/POP

### 🎮 Gameplay Features
- Interface text-based intuitivă
- Sistem de inventar cu stivă
- Istoric complet al mișcărilor
- Validare inteligentă a comenzilor
- Statistici detaliate la sfârșitul jocului

### 📊 Estruturi de Date
- **Inventory Stack**: Gestionează obiectele colectate
- **Move History Stack**: Păstrează istoricul navigării
- **State Transitions**: Dicționar pentru tranziții valide

## 🚀 Instalare și Rulare

### Cerințe de Sistem
- Python 3.6 sau mai nou
- Nu sunt necesare biblioteci externe

### Instalare
```bash
# Clonează sau descarcă fișierul
git clone <repository-url>
cd adventure-game

# SAU descarcă direct fișierul adventure_game.py
```

### Rulare
```bash
python adventure_game.py
```

## 🎮 Cum să Joci

### Comenzi Disponibile
- **UP**: Mergi în sus
- **DOWN**: Mergi în jos  
- **LEFT**: Mergi la stânga
- **RIGHT**: Mergi la dreapta
- **PICKUP**: Ia un obiect (doar în bucătărie)
- **HELP**: Afișează ajutorul
- **QUIT**: Ieși din joc

### Strategia de Joc
1. **Explorează** - Începe de la intrare și explorează camerele
2. **Găsește Bucătăria** - Mergi LEFT din hallway
3. **Ia Lingura** - Folosește PICKUP în bucătărie
4. **Găsește Camera Secretă** - Mergi UP din hallway
5. **Scapă** - Mergi la Mega Exit cu lingura

### Exemple de Comenzi
```
👉 Introdu acțiunea ta: UP
👉 Introdu acțiunea ta: LEFT  
👉 Introdu acțiunea ta: PICKUP
👉 Introdu acțiunea ta: RIGHT
👉 Introdu acțiunea ta: UP
👉 Introdu acțiunea ta: UP
```

## 🤖 Teoria Automatelor

### Tipul de Automat
Acest joc implementează un **Pushdown Automaton (PDA)** cu următoarele componente:

#### Componente Formale
- **Q** (Stări): `{entrance, hallway, kitchen, library, secret_room, exit, mega_exit, win}`
- **Σ** (Alfabet de intrare): `{UP, DOWN, LEFT, RIGHT, PICKUP}`
- **Γ** (Alfabet stivă): `{spoon, move_states}`
- **δ** (Funcția de tranziție): Definită în `transitions`
- **q₀** (Starea inițială): `entrance`
- **F** (Stări finale): `{win}`

#### Operații pe Stivă
```python
def push_to_stack(self, stack, item):
    """Operație PUSH pentru stivă"""
    stack.append(item)
    
def pop_from_stack(self, stack):
    """Operație POP pentru stivă"""
    if stack:
        return stack.pop()
    return None
```

#### Funcția de Tranziție
```python
transitions = {
    'entrance': {'UP': 'hallway'},
    'hallway': {
        'DOWN': 'entrance',
        'LEFT': 'kitchen', 
        'RIGHT': 'library',
        'UP': 'secret_room'
    },
    # ... alte tranziții
}
```

## 🏗️ Structura Codului

### Clasa Principală: `AdventureGameAutomaton`

#### Atribute Principale
```python
self.states          # Dicționar cu toate stările
self.current_state   # Starea curentă a automatului
self.inventory_stack # Stiva pentru inventar
self.move_history    # Stiva pentru istoric mișcări
self.transitions     # Tranziții de stare valide
```

#### Metode Principale
- `__init__()`: Inițializează automatul
- `process_action()`: Procesează comenzile jucătorului
- `push_to_stack()`: Operație PUSH pe stivă
- `pop_from_stack()`: Operație POP de pe stivă
- `display_status()`: Afișează starea curentă
- `play()`: Bucla principală a jocului

### Fluxul de Execuție
```
Inițializare → Afișare Status → Input Jucător → 
Procesare Acțiune → Verificare Condiții → 
Actualizare Stare → Repetă
```

## 🗺️ Harta Jocului

```
                   ┌─────────────┐
                   │ SECRET ROOM │
                   │     🔐      │
                   └──────┬──────┘
                          │ UP/DOWN
          ┌───────────────┼───────────────┐
          │               │               │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │  KITCHEN  │   │  HALLWAY  │   │  LIBRARY  │
    │     🍳    │◄──┤     🏛️     ├──►│     📚    │
    │  (spoon)  │   │           │   │           │
    └───────────┘   └─────┬─────┘   └─────┬─────┘
                          │               │
                          │ UP/DOWN       │ UP/DOWN
                          │               │
                    ┌─────▼─────┐   ┌─────▼─────┐
                    │ ENTRANCE  │   │   EXIT    │
                    │     🚪    │   │     🚪    │
                    └───────────┘   └───────────┘
                          
                   ┌─────────────┐
                   │ MEGA EXIT   │
                   │     ✨      │
                   │ (needs 🥄)  │
                   └─────────────┘
```

### Legendă
- 🚪 **ENTRANCE**: Punctul de start
- 🏛️ **HALLWAY**: Centrul de navigare
- 🍳 **KITCHEN**: Aici găsești lingura (🥄)
- 📚 **LIBRARY**: Camera cu cărți
- 🔐 **SECRET ROOM**: Camera secretă
- 🚪 **EXIT**: Ieșirea normală
- ✨ **MEGA EXIT**: Ieșirea supremă (necesită lingura)

## 🎯 Exemple de Gameplay

### Scenariul 1: Victoria prin Mega Exit
```
📍 ENTRANCE → UP → HALLWAY → LEFT → KITCHEN → PICKUP → 
RIGHT → HALLWAY → UP → SECRET ROOM → UP → MEGA EXIT
🌟 VICTORIE SUPREMĂ!
```

### Scenariul 2: Victoria prin Exit Normal  
```
📍 ENTRANCE → UP → HALLWAY → RIGHT → LIBRARY → UP → EXIT
🎉 Victorie normală!
```

### Scenariul 3: Încercare Eșuată la Mega Exit
```
📍 ENTRANCE → UP → HALLWAY → UP → SECRET ROOM → UP → MEGA EXIT
🔒 BLOCAT! Lipsește lingura!
```

## 📈 Statistici și Tracking

Jocul urmărește:
- **Numărul total de mișcări**
- **Obiecte colectate**
- **Istoricul complet al traseului**
- **Starea finală**

### Exemplu Output Statistici
```
📊 STATISTICI FINALE:
   🏃 Mișcări totale: 8
   🎒 Obiecte colectate: 1
   📍 Starea finală: win
   🛤️  Traseul tău: entrance → hallway → kitchen → hallway → secret_room → mega_exit
```
---

**Enjoy the adventure! 🎮✨**

*Învață teoria automatelor prin joc!*