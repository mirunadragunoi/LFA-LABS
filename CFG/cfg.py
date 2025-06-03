"""
    Acest program implementeaza un sistem pentru lucrul cu Context-Free Grammars (CFG)
- gramatici independente de context folosite in teoria limbajelor formale si compilatoare.
    Functionalitati principale:
        1. Incarcare si validare (load)
            Citeste CFG din fisiere JSON sau format text
            Valideaza ca toate simbolurile sunt definite corect
            Verifica ca variabila de start exista

        2. Creare interactiva (create)
            Permite utilizatorului sa defineasca pas cu pas o gramatica
            Introduce variabile, terminale, variabila de start si reguli
            Salveaza rezultatul in fisier

        3. Exemple predefinite (exemple)
        Genereaza exemple clasice din teoria limbajelor:
            Expresii aritmetice cu +, *, paranteze
            Paranteze balansate
            Palindroame din {0,1}
            Siruri cu numar egal de 0 si 1

        4. Testare derivare (test)
            Incearca sa derive un sir dat folosind regulile gramaticii
            Foloseste derivarea din stanga (leftmost derivation)
            Afiseaza pasii de derivare

    Exemplu de utilizare:
Creeaza exemple: python cfg.py exemple

Incarca o gramatica: python cfg.py load exemple_arithmetic.json

Testeaza daca "(a+a)" poate fi derivat: python cfg.py test exemple_arithmetic.json "(a+a)"
"""


import sys
import json
import re
from collections import defaultdict


class CFG:
    def __init__(self):
        self.variables = set()  # non-terminals (uppercase letters)
        self.terminals = set()  # terminals (lowercase letters, digits, symbols)
        self.rules = defaultdict(list)  # variable -> [list of productions]
        self.start_variable = None

    def load_from_file(self, filename):
        """Partea 1: Incarca si valideaza un CFG dintr un fisier de configuratie"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # incarcam variabilele
            if 'variables' in data:
                self.variables = set(data['variables'])

            if 'terminals' in data:
                self.terminals = set(data['terminals'])

            # incarcam variabila de start
            if 'start_variable' in data:
                self.start_variable = data['start_variable']

            # incarcam regulile
            if 'rules' in data:
                for variable, productions in data['rules'].items():
                    self.rules[variable] = productions

            return self.validate_cfg()

        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format - {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading CFG: {e}")
            return False

    def load_from_text_format(self, filename):
        """ incarcator de formate de text alternative"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found")
            return False

        current_section = None

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line == "Variables:":
                current_section = "variables"
                continue
            elif line == "Terminals:":
                current_section = "terminals"
                continue
            elif line == "Start:":
                current_section = "start"
                continue
            elif line == "Rules:":
                current_section = "rules"
                continue
            elif line == "End":
                current_section = None
                continue

            if current_section == "variables":
                self.variables.add(line)
            elif current_section == "terminals":
                self.terminals.add(line)
            elif current_section == "start":
                self.start_variable = line
            elif current_section == "rules":
                # Parse rule: A -> α | β
                if '->' in line:
                    left, right = line.split('->', 1)
                    variable = left.strip()
                    productions = [p.strip() for p in right.split('|')]
                    self.rules[variable].extend(productions)
                else:
                    print(f"❌ Error at line {line_num}: Invalid rule format '{line}'")
                    return False

        return self.validate_cfg()

    def validate_cfg(self):
        """validam daca CFG este bine format"""
        errors = []

        # verific daca variabila de start exista
        if not self.start_variable:
            errors.append("No start variable specified")
        elif self.start_variable not in self.variables:
            errors.append(f"Start variable '{self.start_variable}' not in variables set")

        # verific regulile
        for variable in self.rules.keys():
            if variable not in self.variables:
                errors.append(f"Rule variable '{variable}' not declared in variables")

        # verific toate simbolurile
        for variable, productions in self.rules.items():
            for production in productions:
                if production == 'ε' or production == 'epsilon':
                    continue

                symbols = self.parse_production(production)
                for symbol in symbols:
                    if symbol not in self.variables and symbol not in self.terminals:
                        errors.append(f"Unknown symbol '{symbol}' in production '{variable} -> {production}'")

        if errors:
            print("❌ CFG VALIDATION FAILED:")
            for error in errors:
                print(f"  • {error}")
            return False

        print("✅ CFG validation successful!")
        return True

    def parse_production(self, production):
        """ analizarea unui sir de productie in simboluri individuale"""
        symbols = []
        i = 0
        while i < len(production):
            if production[i].isupper():
                symbol = production[i]
                j = i + 1
                while j < len(production) and (production[j].isalnum() or production[j] == "'"):
                    symbol += production[j]
                    j += 1
                symbols.append(symbol)
                i = j
            else:
                symbols.append(production[i])
                i += 1
        return symbols

    def create_from_input(self):
        """Partea 2: crearea unui CFG interactiv din datele introduse de utilizator"""
        print("🏗️  CFG CREATOR")
        print("=" * 50)

        print("Enter variables (non-terminals) separated by spaces:")
        print("Example: S A B")
        variables_input = input("Variables: ").strip()
        self.variables = set(variables_input.split())

        print("\nEnter terminals separated by spaces:")
        print("Example: a b 0 1")
        terminals_input = input("Terminals: ").strip()
        self.terminals = set(terminals_input.split())

        print(f"\nAvailable variables: {sorted(self.variables)}")
        while True:
            start = input("Enter start variable: ").strip()
            if start in self.variables:
                self.start_variable = start
                break
            else:
                print(f"❌ '{start}' is not in the variables list. Try again.")

        print(f"\nEnter production rules (one per line):")
        print("Format: A -> α | β  (use | for multiple productions)")
        print("Use 'ε' or 'epsilon' for empty string")
        print("Type 'done' when finished")
        print("Examples:")
        print("  S -> aSb | epsilon")
        print("  A -> aA | a")

        while True:
            rule = input("Rule: ").strip()
            if rule.lower() == 'done':
                break

            if '->' not in rule:
                print("❌ Invalid format. Use: Variable -> production")
                continue

            left, right = rule.split('->', 1)
            variable = left.strip()

            if variable not in self.variables:
                print(f"❌ Variable '{variable}' not declared. Available: {sorted(self.variables)}")
                continue

            productions = [p.strip() for p in right.split('|')]
            self.rules[variable].extend(productions)
            print(f"✅ Added rule: {variable} -> {' | '.join(productions)}")

        if self.validate_cfg():
            print("\n🎉 CFG created successfully!")
            return True
        else:
            return False

    def save_to_file(self, filename, format_type='json'):
        """salveaza CFG ul"""
        try:
            if format_type == 'json':
                cfg_data = {
                    'variables': list(self.variables),
                    'terminals': list(self.terminals),
                    'start_variable': self.start_variable,
                    'rules': dict(self.rules)
                }

                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(cfg_data, file, indent=2, ensure_ascii=False)

            elif format_type == 'text':
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("Variables:\n")
                    for var in sorted(self.variables):
                        file.write(f"{var}\n")

                    file.write("End\n\nTerminals:\n")
                    for term in sorted(self.terminals):
                        file.write(f"{term}\n")

                    file.write(f"End\n\nStart:\n{self.start_variable}\nEnd\n\nRules:\n")
                    for variable in sorted(self.rules.keys()):
                        productions = ' | '.join(self.rules[variable])
                        file.write(f"{variable} -> {productions}\n")
                    file.write("End\n")

            print(f"✅ CFG saved to '{filename}'")
            return True

        except Exception as e:
            print(f"❌ Error saving CFG: {e}")
            return False

    def display_info(self):
        """ afiseaza informatiile despre CFG """
        print("\n=== CFG INFORMATION ===")
        print(f"Variables (Non-terminals): {sorted(self.variables)}")
        print(f"Terminals: {sorted(self.terminals)}")
        print(f"Start Variable: {self.start_variable}")
        print(f"Number of Production Rules: {sum(len(prods) for prods in self.rules.values())}")

        print("\n=== PRODUCTION RULES ===")
        for variable in sorted(self.rules.keys()):
            productions = ' | '.join(self.rules[variable])
            print(f"{variable} -> {productions}")

    def derive_string(self, target_string, max_steps=20):
        """incercare de a deriva un sir de caractere folosind CFG (derivare simpls din stanga)"""
        print(f"\n🎯 Attempting to derive: '{target_string}'")

        # se incepe cu variabila de start
        current = [self.start_variable]
        steps = 0

        print(f"Step 0: {' '.join(current)}")

        while steps < max_steps and current != list(target_string):
            steps += 1

            # gasiti cel mai din stanga neterminal
            leftmost_var = None
            var_index = -1

            for i, symbol in enumerate(current):
                if symbol in self.variables:
                    leftmost_var = symbol
                    var_index = i
                    break

            if leftmost_var is None:
                break

            # obtineti productiile posibile pentru aceasta variabila
            if leftmost_var not in self.rules:
                print(f"❌ No rules for variable '{leftmost_var}'")
                return False

            # se incearca fiecare productie (euristica simpla: se prefera mai intai cele mai scurte)
            productions = sorted(self.rules[leftmost_var], key=len)

            for production in productions:
                # se creaza o noua derivare
                new_current = current[:var_index]

                if production == 'ε' or production == 'epsilon':
                    pass
                else:
                    # se adauga simbolul in productie
                    new_current.extend(list(production))

                new_current.extend(current[var_index + 1:])

                print(
                    f"Step {steps}: {' '.join(current)} -> {' '.join(new_current)} (using {leftmost_var} -> {production})")
                current = new_current
                break
            else:
                print(f"❌ No suitable production found for '{leftmost_var}'")
                return False

        # verific daca am derivat sirul
        derived_string = ''.join(current)
        if derived_string == target_string:
            print(f"✅ Successfully derived '{target_string}'!")
            return True
        else:
            print(f"❌ Could not derive '{target_string}'. Got: '{derived_string}'")
            return False

    def is_in_language(self, test_string):
        """verificam daca un sir de caractere ar putea fi in limbaj (verificare euristica simpla)"""
        for char in test_string:
            if char not in self.terminals:
                return False, f"Character '{char}' not in terminals"

        return True, "String uses only terminal symbols"


def create_sipser_examples():
    # exemplu 1: gramatica pentru expresii aritmetice
    cfg_arithmetic = {
        "description": "Arithmetic expressions",
        "variables": ["E", "T", "F"],
        "terminals": ["a", "+", "*", "(", ")"],
        "start_variable": "E",
        "rules": {
            "E": ["E + T", "T"],
            "T": ["T * F", "F"],
            "F": ["( E )", "a"]
        }
    }

    # exemplu 2: gramatica pentru paranteze balansate
    cfg_balanced = {
        "description": "Balanced parentheses",
        "variables": ["S"],
        "terminals": ["(", ")"],
        "start_variable": "S",
        "rules": {
            "S": ["( S )", "S S", "epsilon"]
        }
    }

    # exemplu 3: gramatica pentru string uri palindrom formate din {0, 1}
    cfg_palindromes = {
        "description": "Palindromes over {0,1}",
        "variables": ["S"],
        "terminals": ["0", "1"],
        "start_variable": "S",
        "rules": {
            "S": ["0 S 0", "1 S 1", "0", "1", "epsilon"]
        }
    }

    # exemplu 4: gramatica pentru string uri ce au acelasi numar de 0 si de 1
    cfg_equal = {
        "description": "Equal number of 0s and 1s",
        "variables": ["S"],
        "terminals": ["0", "1"],
        "start_variable": "S",
        "rules": {
            "S": ["0 S 1", "1 S 0", "S S", "epsilon"]
        }
    }

    examples = {
        "arithmetic": cfg_arithmetic,
        "balanced": cfg_balanced,
        "palindromes": cfg_palindromes,
        "equal": cfg_equal
    }

    # salveaza exemplele in fisiere
    for name, cfg_data in examples.items():
        filename = f"exemple_{name}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(cfg_data, file, indent=2, ensure_ascii=False)
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")

    return examples


def main():
    if len(sys.argv) < 2:
        print("🚀 CFG SYSTEM")
        print("=" * 50)
        print("Usage options:")
        print("1. python cfg.py load <config_file>           # Exercise 1: Load and validate")
        print("2. python cfg.py create [output_file]         # Exercise 2: Create interactively")
        print("3. python cfg.py exemple                      # Exercise 3: Create examples")
        print("4. python cfg.py test <config_file> <string>  # Test string derivation")
        print("\nExamples:")
        print("python cfg.py load exemple_arithmetic.json")
        print("python cfg.py create my_cfg.json")
        print("python cfg.py exemple")
        print("python cfg.py test exemple_balanced.json '(())'")
        return

    command = sys.argv[1].lower()

    if command == "load":
        # exemplu 1: incarca si valideaza un CFG
        if len(sys.argv) != 3:
            print("❌ Usage: python cfg.py load <config_file>")
            return

        config_file = sys.argv[2]
        cfg = CFG()

        if config_file.endswith('.json'):
            success = cfg.load_from_file(config_file)
        else:
            success = cfg.load_from_text_format(config_file)

        if success:
            cfg.display_info()

    elif command == "create":
        # exercitiu 2: creaza un CFG de la un input
        output_file = sys.argv[2] if len(sys.argv) > 2 else "created_cfg.json"

        cfg = CFG()
        if cfg.create_from_input():
            cfg.display_info()
            cfg.save_to_file(output_file)

    elif command == "exemple":
        # exemplu 3: creaza exemple
        print("🏗️  Creating CFG Examples")
        print("=" * 50)
        examples = create_sipser_examples()

        print(f"\n✅ Created {len(examples)} example files:")
        for name in examples.keys():
            print(f"  • exemple_{name}.json")

        print("\nTo test these examples:")
        print("python cfg.py load exemple_arithmetic.json")
        print("python cfg.py test exemple_balanced.json '(())'")

    elif command == "test":
        # se testeaza string ul
        if len(sys.argv) != 4:
            print("❌ Usage: python cfg.py test <config_file> <string>")
            return

        config_file = sys.argv[2]
        test_string = sys.argv[3]

        cfg = CFG()
        if cfg.load_from_file(config_file):
            cfg.display_info()

            valid, message = cfg.is_in_language(test_string)
            print(f"\n📋 String validation: {message}")

            if valid:
                cfg.derive_string(test_string)

    else:
        print(f"❌ Unknown command: {command}")
        print("Use: load, create, exemple, or test")


if __name__ == "__main__":
    main()