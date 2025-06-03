class AutomatonValidator:
    def __init__(self):
        self.sigma = set()  # alfabet
        self.states = set()  # stari
        self.final_states = set()  # stari finale
        self.start_states = set()  # stari de start
        self.transitions = []  # tranzitii

    def parse_file(self, filename):
        """parsez fisierul de intrare pentru automat"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Eroare: Fișierul '{filename}' nu a fost găsit.")
            return False
        except Exception as e:
            print(f"Eroare la citirea fișierului: {e}")
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
                if line != "...":  # ignor
                    self.sigma.add(line)

            elif current_section == "states":
                if line != "...":  # ignor
                    # verific daca starea este finala (se termina cu ,F)
                    if line.endswith(',F'):
                        state = line[:-2]  # elimin ',F'
                        self.states.add(state)
                        self.final_states.add(state)
                    # verific daca starea este de start (se termina cu ,S)
                    elif line.endswith(',S'):
                        state = line[:-2]  # elimin ',S'
                        self.states.add(state)
                        self.start_states.add(state)
                    else:
                        self.states.add(line)

            elif current_section == "transitions":
                if line != "...":  # ignor
                    # parsez tranzactia: stateX, wordY, stateZ
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) == 3:
                        from_state, word, to_state = parts
                        self.transitions.append((from_state, word, to_state))
                    else:
                        print(f"Eroare la linia {line_num}: format tranziție invalid '{line}'")
                        return False

        return True

    def validate(self):
        """Validează automatul conform cerințelor"""
        errors = []

        print("=== INFORMAȚII DESPRE AUTOMAT ===")
        print(f"Alfabet (Sigma): {sorted(self.sigma)}")
        print(f"Stări: {sorted(self.states)}")
        print(f"Stări finale: {sorted(self.final_states)}")
        print(f"Stări de start: {sorted(self.start_states)}")
        print(f"Numărul de tranziții: {len(self.transitions)}")
        print()

        print("=== VALIDARE ===")

        # verific ca exista cel putin o stare de start
        if not self.start_states:
            errors.append("Nu există stări de start (marcate cu ,S)")

        # verific ca simbolul 'S' poate succede doar o stare
        s_successors = set()
        for from_state, word, to_state in self.transitions:
            if word == 'S':
                s_successors.add(from_state)

        if len(s_successors) > 1:
            errors.append(f"Simbolul 'S' poate succede mai mult de o stare: {s_successors}")

        # validez tranzitiile
        for i, (from_state, word, to_state) in enumerate(self.transitions):
            # verific ca starile din tranzitii exista
            if from_state not in self.states:
                errors.append(f"Tranziția {i + 1}: starea sursă '{from_state}' nu există în lista de stări")

            if to_state not in self.states:
                errors.append(f"Tranziția {i + 1}: starea destinație '{to_state}' nu există în lista de stări")

            # verific daca cuvintele din tranzitii exista in alfabet
            if word not in self.sigma:
                errors.append(f"Tranziția {i + 1}: cuvântul '{word}' nu există în alfabet")

        # raportez rezultatele
        if errors:
            print("❌ VALIDARE EȘUATĂ:")
            for error in errors:
                print(f"  • {error}")
            return False
        else:
            print("✅ VALIDARE REUȘITĂ: Automatul este valid!")
            return True

    def display_transitions(self):
        """Afișează toate tranzițiile"""
        print("\n=== TRANZIȚII ===")
        for i, (from_state, word, to_state) in enumerate(self.transitions, 1):
            print(f"{i:2d}. {from_state} --({word})--> {to_state}")


def main():
    # nume fix al fisierului din care se citeste
    filename = 'test_automat.txt'

    print(f"🔍 Citesc obligatoriu din fișierul: {filename}")
    print("=" * 50)

    # creez validatorul
    validator = AutomatonValidator()

    # parsez si valideaza fisierul
    if validator.parse_file(filename):
        is_valid = validator.validate()
        validator.display_transitions()

        if is_valid:
            print("\n🎉 Automatul este complet valid!")
        else:
            print("\n⚠️  Automatul conține erori.")
    else:
        print("❌ Parsarea fișierului a eșuat.")
        print(f"💡 Asigură-te că fișierul '{filename}' există și are formatul corect.")


if __name__ == "__main__":
    main()