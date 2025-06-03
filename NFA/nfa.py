"""
    Acest program se va rula in terminal si va primi ca argumente numele acestui fisier (dnfa.py),
un fisier ce contine un automat finit nondeterminist (nfa_input1.txt) si un string ce va fi verificat de NFA.
    Programul va incarca nfa-ul primit si il va valida sau respinge in cazul in care nu are o
configuratie corecta. In plus, va afisa pentru string daca este acceptat sau respins.
"""


import sys
from collections import defaultdict, deque


class NFA:
    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = defaultdict(lambda: defaultdict(list))  # state -> symbol -> [next_states]

    def load_from_file(self, filename):
        """incarcam NFA-ul din fisierul de configurare"""
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

            # procesez continutul sectiunilor
            if current_section == "sigma":
                # adaug simbolul in alfabet (inclusiv epsilon dacă este specificat)
                if line in ['ε', 'epsilon', 'eps']:
                    self.alphabet.add('ε')
                else:
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
                # pentru NFA, pot avea multiple tranzitii pentru aceeasi combinatie
                parts = [part.strip() for part in line.split(',')]
                if len(parts) == 3:
                    from_state, symbol, to_state = parts
                    # convertesc epsilon in forma standard
                    if symbol in ['epsilon', 'eps']:
                        symbol = 'ε'
                    self.transitions[from_state][symbol].append(to_state)
                else:
                    print(f"❌ Eroare la linia {line_num}: format tranziție invalid '{line}'")
                    return False

        return self.validate_nfa()

    def validate_nfa(self):
        """validez ca automatul este un NFA valid"""
        errors = []

        # verific ca exista exact o stare de start
        if not self.start_state:
            errors.append("Nu există stare de start (marcată cu ,S)")

        # verific ca toate tranzitiile sunt valide
        for from_state, transitions in self.transitions.items():
            if from_state not in self.states:
                errors.append(f"Starea sursă '{from_state}' nu există")

            for symbol, to_states in transitions.items():
                if symbol != 'ε' and symbol not in self.alphabet:
                    errors.append(f"Simbolul '{symbol}' nu există în alfabet")

                for to_state in to_states:
                    if to_state not in self.states:
                        errors.append(f"Starea destinație '{to_state}' nu există")

        if errors:
            print("❌ NFA INVALID:")
            for error in errors:
                print(f"  • {error}")
            return False

        print("✅ NFA valid încărcat cu succes!")
        return True

    def epsilon_closure(self, states):
        """calculez epsilon-closure pentru un set de stari"""
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            # verific pentru tranzitii epsilon
            if 'ε' in self.transitions[state]:
                for next_state in self.transitions[state]['ε']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    def move(self, states, symbol):
        """calculez multimea starilor accesibile din starile date pe simbol"""
        result = set()
        for state in states:
            if symbol in self.transitions[state]:
                result.update(self.transitions[state][symbol])
        return result

    def accepts(self, input_string):
        """verific daca NFA accepta string-ul de intrare"""
        if not self.start_state:
            return False

        print(f"\n🔍 Procesez string-ul: '{input_string}'")

        # calculez epsilon-closure pentru starea initială
        current_states = self.epsilon_closure({self.start_state})
        print(f"📍 Stări inițiale (cu ε-closure): {sorted(current_states)}")

        # procesez fiecare simbol din string
        for i, symbol in enumerate(input_string):
            if symbol not in self.alphabet or symbol == 'ε':
                if symbol == 'ε':
                    print(f"❌ Simbolul epsilon nu poate fi în input!")
                else:
                    print(f"❌ Simbolul '{symbol}' nu există în alfabet!")
                return False

            # calculez move pentru simbolul curent
            moved_states = self.move(current_states, symbol)
            if not moved_states:
                print(
                    f"❌ Pas {i + 1}: Nu există tranziții pentru simbolul '{symbol}' din stările {sorted(current_states)}")
                return False

            # calculez epsilon-closure pentru starile rezultate
            current_states = self.epsilon_closure(moved_states)
            print(f"Pas {i + 1}: {symbol} → {sorted(moved_states)} → ε-closure: {sorted(current_states)}")

        # verific daca vreo stare finala este in setul curent
        final_intersection = current_states.intersection(self.final_states)
        is_accepted = len(final_intersection) > 0

        print(f"📍 Stări finale: {sorted(current_states)}")
        if final_intersection:
            print(f"🎯 Stări finale acceptante: {sorted(final_intersection)}")

        if is_accepted:
            print(f"✅ String-ul '{input_string}' este ACCEPTAT!")
        else:
            print(f"❌ String-ul '{input_string}' este RESPINS!")

        return is_accepted

    def display_info(self):
        """afișez informatii despre NFA"""
        print("\n=== INFORMAȚII NFA ===")
        print(f"Alfabet: {sorted(self.alphabet)}")
        print(f"Stări: {sorted(self.states)}")
        print(f"Stare de start: {self.start_state}")
        print(f"Stări finale: {sorted(self.final_states)}")

        # numar total de tranzitii
        total_transitions = sum(len(transitions) for transitions in self.transitions.values())
        print(f"Numărul de tranziții: {total_transitions}")

        print("\n=== TRANZIȚII ===")
        transition_count = 1
        for from_state in sorted(self.transitions.keys()):
            for symbol in sorted(self.transitions[from_state].keys()):
                to_states = self.transitions[from_state][symbol]
                for to_state in sorted(to_states):
                    print(f"{transition_count:2d}. {from_state} --({symbol})--> {to_state}")
                    transition_count += 1

        # afisez si informatii despre nondeterminism
        print("\n=== ANALIZA NONDETERMINISMULUI ===")
        nondeterministic_transitions = 0
        epsilon_transitions = 0

        for from_state, transitions in self.transitions.items():
            for symbol, to_states in transitions.items():
                if symbol == 'ε':
                    epsilon_transitions += len(to_states)
                elif len(to_states) > 1:
                    nondeterministic_transitions += 1
                    print(f"🔀 Nondeterminism: {from_state} --({symbol})--> {to_states}")

        print(f"📊 Tranziții nondeterministice: {nondeterministic_transitions}")
        print(f"📊 Tranziții epsilon: {epsilon_transitions}")

    def get_computation_tree(self, input_string, max_depth=10):
        """generez arborele de computatie pentru un string (pentru debugging)"""
        if not self.start_state:
            return []

        # structura: (stare_curenta, poziție_in_string, istoric_path)
        initial_states = self.epsilon_closure({self.start_state})
        queue = [(state, 0, [state]) for state in initial_states]
        all_paths = []

        while queue and len(all_paths) < 100:  # limitez numarul de cai pentru performanta
            current_state, pos, path = queue.pop(0)

            # daca am procesat tot string-ul
            if pos == len(input_string):
                is_accepting = current_state in self.final_states
                all_paths.append((path, is_accepting))
                continue

            # daca am depasit adancimea maxima
            if len(path) > max_depth:
                continue

            symbol = input_string[pos]
            if symbol in self.transitions[current_state]:
                for next_state in self.transitions[current_state][symbol]:
                    # calculez epsilon-closure pentru urmatoarea stare
                    epsilon_closure = self.epsilon_closure({next_state})
                    for eps_state in epsilon_closure:
                        new_path = path + [f"--{symbol}-->", eps_state]
                        queue.append((eps_state, pos + 1, new_path))

        return all_paths


def main():
    if len(sys.argv) != 3:
        print("❌ Utilizare incorectă!")
        print("📖 Sintaxa corectă:")
        print("python nfa.py nfa_config_file input_string")
        print("\n📋 Exemple:")
        print("python nfa.py nfa_input1.txt 1001")
        print("python nfa.py nfa_input2.txt ab")
        print("\n📝 Format fișier configurare:")
        print("Sigma:")
        print("0")
        print("1")
        print("ε")
        print("End")
        print("States:")
        print("q0,S")
        print("q1")
        print("q2,F")
        print("End")
        print("Transitions:")
        print("q0, 0, q0")
        print("q0, 1, q0")
        print("q0, 1, q1")
        print("q1, 0, q2")
        print("q0, ε, q1")
        print("End")
        return

    config_file = sys.argv[1]
    input_string = sys.argv[2]

    print(f"🚀 NFA Engine")
    print("=" * 50)

    # creez si incarc NFA
    nfa = NFA()
    if not nfa.load_from_file(config_file):
        return

    # afisez informatii despre NFA
    nfa.display_info()

    print("\n" + "=" * 50)

    # testez string-ul
    result = nfa.accepts(input_string)

    print("\n" + "=" * 50)
    if result:
        print("🎉 REZULTAT: ACCEPT")
    else:
        print("🚫 REZULTAT: REJECT")

    # optional: afisez arborele de computatie pentru string-uri scurte
    if len(input_string) <= 5:
        print(f"\n🌳 ARBORE DE COMPUTAȚIE pentru '{input_string}':")
        paths = nfa.get_computation_tree(input_string)
        for i, (path, is_accepting) in enumerate(paths[:10], 1):  # afisez primele 10 cai
            status = "✅ ACCEPT" if is_accepting else "❌ REJECT"
            print(f"{i:2d}. {' '.join(map(str, path))} → {status}")
        if len(paths) > 10:
            print(f"    ... și încă {len(paths) - 10} căi")


if __name__ == "__main__":
    main()