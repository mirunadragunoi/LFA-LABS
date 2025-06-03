"""
    Acest program se va rula in terminal si va primi ca argumente numele acestui fisier (nfa_to_dfa_converter.py),
un fisier ce contine un automat finit nondeterminist (nfa_input1.json) si un fisier gol in care se va incarca
conversia intr un automat finit determinist (dfa_output1.json).

"""



import sys
import json
from collections import defaultdict, deque


class NFAToDFAConverter:
    def __init__(self, nfa_config_file, nfa_example_key=None):
        """Initializeaza convertorul cu fișierul NFA de configuratie"""
        self.nfa = self.load_nfa_config(nfa_config_file, nfa_example_key)
        self.dfa_states = {}
        self.dfa_transitions = {}
        self.dfa_final_states = set()

    def load_nfa_config(self, filename, nfa_example_key=None):
        """Incarca configuratia NFA din fisier"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # daca fisierul contine multiple exemple de NFA
            if nfa_example_key:
                if nfa_example_key not in data:
                    print(f"Error: NFA example '{nfa_example_key}' not found in file")
                    available_keys = [k for k in data.keys() if k != 'comment']
                    print(f"Available examples: {available_keys}")
                    sys.exit(1)
                return data[nfa_example_key]

            # daca este un singur NFA direct în fisier
            elif 'states' in data and 'alphabet' in data:
                return data

            # daca fisierul contine exemple multiple, afisează optiunile
            else:
                available_examples = [k for k in data.keys() if k != 'comment']
                print(f"Error: Multiple NFA examples found. Please specify which one to use:")
                for example in available_examples:
                    if example in data and isinstance(data[example], dict) and 'description' in data[example]:
                        print(f"  - {example}: {data[example]['description']}")
                    else:
                        print(f"  - {example}")
                sys.exit(1)

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{filename}'")
            sys.exit(1)

    def epsilon_closure(self, states):
        """Calculeaza epsilon-closure pentru un set de stari"""
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            # verific pentru tranzitii epsilon
            if state in self.nfa.get('transitions', {}):
                for symbol, next_states in self.nfa['transitions'][state].items():
                    if symbol == 'ε' or symbol == 'epsilon':
                        for next_state in next_states:
                            if next_state not in closure:
                                closure.add(next_state)
                                stack.append(next_state)

        return frozenset(closure)

    def move(self, states, symbol):
        """Calculeaza multimea starilor accesibile din starile date pe simbol"""
        result = set()
        for state in states:
            if state in self.nfa.get('transitions', {}):
                if symbol in self.nfa['transitions'][state]:
                    result.update(self.nfa['transitions'][state][symbol])
        return result

    def convert_to_dfa(self):
        """Conversia NFA in DFA folosind algoritmul de construcție a subseturilor"""
        print(f"Converting NFA to DFA...")
        print(f"NFA States: {self.nfa['states']}")
        print(f"NFA Alphabet: {self.nfa['alphabet']}")
        print(f"NFA Start State: {self.nfa['start_state']}")
        print(f"NFA Final States: {self.nfa['final_states']}")
        print()

        start_closure = self.epsilon_closure({self.nfa['start_state']})
        print(f"Initial epsilon-closure of {self.nfa['start_state']}: {set(start_closure)}")

        # folosesc o coada pentru BFS prin starile DFA
        queue = deque([start_closure])
        processed = set()

        # DFA counter de stari
        dfa_state_counter = 0

        # harta de la seturi de stari la nume de stari DFA
        state_mapping = {start_closure: f'q{dfa_state_counter}'}
        dfa_state_counter += 1

        dfa_transitions = defaultdict(dict)
        dfa_final_states = set()

        while queue:
            current_state_set = queue.popleft()

            if current_state_set in processed:
                continue
            processed.add(current_state_set)

            current_dfa_state = state_mapping[current_state_set]
            print(f"Processing DFA state {current_dfa_state} = {set(current_state_set)}")

            # verific daca aceasta stare DFA contine stari finale NFA
            if any(state in self.nfa['final_states'] for state in current_state_set):
                dfa_final_states.add(current_dfa_state)
                print(f"  -> {current_dfa_state} is a final state")

            # pentru fiecare simbol din alfabet (exclud epsilon)
            alphabet_without_epsilon = [sym for sym in self.nfa['alphabet']
                                        if sym not in ['ε', 'epsilon']]

            for symbol in alphabet_without_epsilon:
                moved_states = self.move(current_state_set, symbol)
                if moved_states:
                    next_state_set = self.epsilon_closure(moved_states)
                    print(
                        f"  On symbol '{symbol}': {set(current_state_set)} -> {set(moved_states)} -> {set(next_state_set)}")

                    # creeaza o noua stare in DFA daca este nevoie
                    if next_state_set not in state_mapping:
                        state_mapping[next_state_set] = f'q{dfa_state_counter}'
                        dfa_state_counter += 1
                        queue.append(next_state_set)

                    # adaugam tranzitia
                    dfa_transitions[current_dfa_state][symbol] = state_mapping[next_state_set]
                else:
                    print(f"  On symbol '{symbol}': no transition from {set(current_state_set)}")

        print()

        # creez configuratia DFA
        dfa_config = {
            'states': list(state_mapping.values()),
            'alphabet': [sym for sym in self.nfa['alphabet'] if sym not in ['ε', 'epsilon']],
            'transitions': dict(dfa_transitions),
            'start_state': state_mapping[start_closure],
            'final_states': list(dfa_final_states)
        }

        return dfa_config

    def save_dfa_config(self, dfa_config, filename):
        """Salveaza configuratia DFA intr-un fisier"""
        with open(filename, 'w') as f:
            json.dump(dfa_config, f, indent=2)
        print(f"DFA configuration saved to '{filename}'")

    def print_dfa_info(self, dfa_config):
        """Printez informatiile despre DFA"""
        print("=== DFA Configuration ===")
        print(f"States: {dfa_config['states']}")
        print(f"Alphabet: {dfa_config['alphabet']}")
        print(f"Start State: {dfa_config['start_state']}")
        print(f"Final States: {dfa_config['final_states']}")
        print("\nTransitions:")
        for state, transitions in dfa_config['transitions'].items():
            for symbol, next_state in transitions.items():
                print(f"  {state} --{symbol}--> {next_state}")
        print()


def main():
    if len(sys.argv) < 3:
        print("Usage: python nfa_to_dfa_converter.py nfa_config_file converted_dfa_config_file [nfa_example_key]")
        print("Examples:")
        print("  python nfa_to_dfa_converter.py nfa_examples.json output.json nfa_example_1")
        print("  python nfa_to_dfa_converter.py single_nfa.json output.json")
        sys.exit(1)

    nfa_config_file = sys.argv[1]
    dfa_config_file = sys.argv[2]
    nfa_example_key = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        # creez convertorul si convertesc NFA-ul la DFA
        converter = NFAToDFAConverter(nfa_config_file, nfa_example_key)
        dfa_config = converter.convert_to_dfa()

        # afisez informatiile despre DFA
        converter.print_dfa_info(dfa_config)

        # salvez configuratia DFA-ului
        converter.save_dfa_config(dfa_config, dfa_config_file)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()