#!/usr/bin/env python3
"""
Program principal pentru testarea mașinilor Turing
Exemplu de utilizare a bibliotecii TM
"""

from turing_machines import TuringMachine, TMConfigLoader, TMConfigValidator
import json


def load_and_test_tm(config_file, test_inputs):
    """Încarcă o configurație TM și o testează cu diverse input-uri"""
    print(f"\n=== Testare {config_file} ===")
    print("-" * 50)

    # Exemplu de utilizare - exact cum ai cerut
    loader = TMConfigLoader()
    is_valid, config, errors = loader.load_from_file(config_file)

    if is_valid:
        print(f"✓ Configurația '{config_file}' este validă")
        print(f"Descriere: {config.get('description', 'N/A')}")

        tm = TuringMachine(config)

        print("\nRezultate teste:")
        for input_string in test_inputs:
            status, output, steps = tm.run(input_string)
            print(f"Input: '{input_string}' -> Status: {status.value}, Output: '{output}', Steps: {steps}")

    else:
        print(f"✗ Erori în configurația '{config_file}':")
        for error in errors:
            print(f"  - {error}")


def create_individual_config_files():
    """Creează fișiere JSON individuale din examples.json"""

    # Încarcă toate exemplele
    try:
        with open('examples.json', 'r', encoding='utf-8') as f:
            all_examples = json.load(f)

        # Salvează fiecare exemplu în fișier separat
        for name, config in all_examples.items():
            filename = f"{name}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✓ Salvat {filename}")

    except FileNotFoundError:
        print("Fișierul examples.json nu a fost găsit!")
        return False
    except Exception as e:
        print(f"Eroare la procesarea examples.json: {e}")
        return False

    return True


def interactive_tm_test():
    """Mod interactiv pentru testarea TM-urilor"""
    print("\n=== Mod Interactiv ===")
    print("Introduceți calea către fișierul de configurație TM:")

    while True:
        config_file = input("\nFișier configurație (sau 'exit' pentru ieșire): ").strip()

        if config_file.lower() == 'exit':
            break

        if not config_file:
            continue

        loader = TMConfigLoader()
        is_valid, config, errors = loader.load_from_file(config_file)

        if is_valid:
            print(f"✓ Configurația încărcată cu succes!")
            print(f"Nume: {config.get('name', 'N/A')}")
            print(f"Descriere: {config.get('description', 'N/A')}")

            tm = TuringMachine(config)

            while True:
                test_input = input("\nInput pentru TM (sau 'back' pentru alt fișier): ").strip()

                if test_input.lower() == 'back':
                    break

                status, output, steps = tm.run(test_input)
                print(f"Rezultat: {status.value}")
                print(f"Output: '{output}'")
                print(f"Pași executați: {steps}")

        else:
            print(f"✗ Erori în configurație:")
            for error in errors:
                print(f"  - {error}")


def main():
    """Funcția principală"""
    print("=== Sistem de Testare Mașini Turing ===")

    # 1. Creează fișierele individuale din examples.json
    print("\n1. Crearea fișierelor de configurație...")
    if create_individual_config_files():
        print("✓ Fișierele de configurație au fost create cu succes!")
    else:
        print("✗ Eroare la crearea fișierelor de configurație")
        return

    # 2. Testează fiecare TM cu exemple predefinite
    print("\n2. Testare automată a TM-urilor...")

    # Test palindrome checker
    load_and_test_tm("palindrome_checker.json",
                     ["101", "1001", "11011", "110", "1", ""])

    # Test unary incrementer
    load_and_test_tm("unary_incrementer.json",
                     ["1", "11", "111", ""])

    # Test copy machine
    load_and_test_tm("copy_machine.json",
                     ["01", "10", "101", "0", "1", ""])

    # 3. Exemplu manual de utilizare
    print("\n3. Exemplu manual de încărcare și testare...")

    # Exemplu exact cum ai cerut
    loader = TMConfigLoader()
    is_valid, config, errors = loader.load_from_file("palindrome_checker.json")

    if is_valid:
        tm = TuringMachine(config)
        status, output, steps = tm.run("1001")  # input_string = "1001"
        print(f"Rezultat: {status.value}, Output: {output}, Steps: {steps}")
    else:
        print("Erori:", errors)

    # 4. Mod interactiv (opțional)
    print("\n4. Doriți să intrați în modul interactiv? (y/n)")
    choice = input().strip().lower()
    if choice == 'y':
        interactive_tm_test()

    print("\n=== Testare completă! ===")


if __name__ == "__main__":
    main()