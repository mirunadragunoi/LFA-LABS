"""
    Acest program se va rula in terminal si va primi ca argumente numele acestui fisier (dfa.py),
un fisier ce contine un automat finit determinist (dfa_input1.txt) si un string ce va fi verificat de DFA.
    Programul va incarca dfa-ul primit si il va valida sau respinge in cazul in care nu are o
configuratie corecta. In plus, va afisa pentru string daca este acceptat sau respins.
"""


import sys


class DFA:
    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = {}  # (state, symbol) -> next_state

    def load_from_file(self, filename):
        """incarcam DFA ul din fisierul de configurare"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"❌ Eroare: Fișierul '{filename}' nu a fost găsit.")
            return False
        except Exception as e:
            print(f"❌ Eroare la citirea fișierului: {e}")
            return False

        current_section = None

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # ignor liniile goale si comentariile
            if not line or line.startswith('#'):
                continue

            # detectez sectiunile
            if line == "Sigma:":
                current_section = "sigma"
                continue
            elif line == "End":
                current_section = None
                continue
            elif line == "States:":
                current_section = "states"
                continue
            elif line == "Transitions:":
                current_section = "transitions"
                continue

            # procesez continutul secțtunilor
            if current_section == "sigma":
                self.alphabet.add(line)

            elif current_section == "states":
                # verific daca starea este finala (se termina cu ,F)
                if line.endswith(',F'):
                    state = line[:-2]
                    self.states.add(state)
                    self.final_states.add(state)
                # verific daca starea este de start (se termina cu ,S)
                elif line.endswith(',S'):
                    state = line[:-2]
                    self.states.add(state)
                    self.start_state = state
                # verific daca starea este si de start si finala
                elif ',S,F' in line or ',F,S' in line:
                    state = line.replace(',S,F', '').replace(',F,S', '')
                    self.states.add(state)
                    self.start_state = state
                    self.final_states.add(state)
                else:
                    self.states.add(line)

            elif current_section == "transitions":
                # parsez tranzitia: stateX, symbolY, stateZ
                parts = [part.strip() for part in line.split(',')]
                if len(parts) == 3:
                    from_state, symbol, to_state = parts
                    self.transitions[(from_state, symbol)] = to_state
                else:
                    print(f"❌ Eroare la linia {line_num}: format tranziție invalid '{line}'")
                    return False

        return self.validate_dfa()

    def validate_dfa(self):
        """validez ca automatul este un DFA valid"""
        errors = []

        # verific ca exista exact o stare de start
        if not self.start_state:
            errors.append("Nu există stare de start (marcată cu ,S)")

        # verific ca toate tranzitiile sunt valide
        for (from_state, symbol), to_state in self.transitions.items():
            if from_state not in self.states:
                errors.append(f"Starea sursă '{from_state}' nu există")
            if to_state not in self.states:
                errors.append(f"Starea destinație '{to_state}' nu există")
            if symbol not in self.alphabet:
                errors.append(f"Simbolul '{symbol}' nu există în alfabet")

        if errors:
            print("❌ DFA INVALID:")
            for error in errors:
                print(f"  • {error}")
            return False

        print("✅ DFA valid încărcat cu succes!")
        return True

    def accepts(self, input_string):
        """Verific daca DFA accepta string-ul de intrare"""
        if not self.start_state:
            return False

        current_state = self.start_state

        print(f"\n🔍 Procesez string-ul: '{input_string}'")
        print(f"📍 Stare inițială: {current_state}")

        for i, symbol in enumerate(input_string):
            if symbol not in self.alphabet:
                print(f"❌ Simbolul '{symbol}' nu există în alfabet!")
                return False

            if (current_state, symbol) not in self.transitions:
                print(f"❌ Nu există tranziție din starea '{current_state}' cu simbolul '{symbol}'")
                return False

            next_state = self.transitions[(current_state, symbol)]
            print(f"Pas {i + 1}: {current_state} --({symbol})--> {next_state}")
            current_state = next_state

        is_accepted = current_state in self.final_states
        print(f"📍 Stare finală: {current_state}")

        if is_accepted:
            print(f"✅ String-ul '{input_string}' este ACCEPTAT!")
        else:
            print(f"❌ String-ul '{input_string}' este RESPINS!")

        return is_accepted

    def display_info(self):
        """Afișează informații despre DFA"""
        print("\n=== INFORMAȚII DFA ===")
        print(f"Alfabet: {sorted(self.alphabet)}")
        print(f"Stări: {sorted(self.states)}")
        print(f"Stare de start: {self.start_state}")
        print(f"Stări finale: {sorted(self.final_states)}")
        print(f"Numărul de tranziții: {len(self.transitions)}")

        print("\n=== TRANZIȚII ===")
        for i, ((from_state, symbol), to_state) in enumerate(sorted(self.transitions.items()), 1):
            print(f"{i:2d}. {from_state} --({symbol})--> {to_state}")


def main():
    if len(sys.argv) != 3:
        print("❌ Utilizare incorectă!")
        print("📖 Sintaxa corectă:")
        print("python dfa.py dfa_config_file input_string")
        print("\n📋 Exemple:")
        print("python dfa.py dfa_input1.txt 1001")
        print("python dfa.py dfa_input2.txt 1101")
        return

    config_file = sys.argv[1]
    input_string = sys.argv[2]

    print(f"🚀 DFA Engine")
    print("=" * 50)

    # creeaza si incarca DFA
    dfa = DFA()
    if not dfa.load_from_file(config_file):
        return

    # afisez informatii despre DFA
    dfa.display_info()

    print("\n" + "=" * 50)

    # testez string-ul
    result = dfa.accepts(input_string)

    print("\n" + "=" * 50)
    if result:
        print("🎉 REZULTAT: ACCEPT")
    else:
        print("🚫 REZULTAT: REJECT")


if __name__ == "__main__":
    main()