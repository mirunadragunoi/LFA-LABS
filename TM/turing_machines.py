#!/usr/bin/env python3
"""
    Turing Machine Implementation
    Implementeaza o biblioteca pentru incarcarea, validarea si executia masinilor Turing
"""

import json
import re
from typing import Dict, List, Tuple, Set, Optional
from enum import Enum


class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    STAY = 'S'


class TMState(Enum):
    RUNNING = "running"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HALTED = "halted"


class TuringMachine:
    """Implementarea unei masini Turing"""

    def __init__(self, config: Dict):
        self.states = set(config['states'])
        self.alphabet = set(config['alphabet'])
        self.tape_alphabet = set(config['tape_alphabet'])
        self.start_state = config['start_state']
        self.accept_states = set(config['accept_states'])
        self.reject_states = set(config['reject_states'])
        self.transitions = {}

        # construire tabel de tranzitii
        for transition in config['transitions']:
            key = (transition['from_state'], transition['read_symbol'])
            value = (transition['to_state'], transition['write_symbol'],
                     Direction(transition['direction']))
            self.transitions[key] = value

        # starea curenta a masinii
        self.current_state = self.start_state
        self.tape = []
        self.head_position = 0
        self.blank_symbol = config.get('blank_symbol', '_')
        self.status = TMState.RUNNING
        self.steps = 0
        self.max_steps = config.get('max_steps', 1000)

    def load_input(self, input_string: str):
        """Incarca input-ul pe banda"""
        self.tape = list(input_string) if input_string else [self.blank_symbol]
        self.head_position = 0
        self.current_state = self.start_state
        self.status = TMState.RUNNING
        self.steps = 0

    def get_current_symbol(self) -> str:
        """Returneaza simbolul curent de pe banda"""
        if self.head_position < 0 or self.head_position >= len(self.tape):
            return self.blank_symbol
        return self.tape[self.head_position]

    def write_symbol(self, symbol: str):
        """Scrie un simbol pe banda la pozitia curenta"""
        # extind banda daca e necesar
        while self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)

        if self.head_position < 0:
            # extind banda la stanga
            self.tape = [self.blank_symbol] * abs(self.head_position) + self.tape
            self.head_position = 0

        self.tape[self.head_position] = symbol

    def move_head(self, direction: Direction):
        """Muta capul de citire"""
        if direction == Direction.LEFT:
            self.head_position -= 1
        elif direction == Direction.RIGHT:
            self.head_position += 1
        # STAY nu schimba pozitia

    def step(self) -> bool:
        """Executa un pas al masinii Turing. Returneaza True daca poate continua"""
        if self.status != TMState.RUNNING:
            return False

        if self.steps >= self.max_steps:
            self.status = TMState.HALTED
            return False

        current_symbol = self.get_current_symbol()
        key = (self.current_state, current_symbol)

        if key not in self.transitions:
            # nu exista tranzitie - masina se opreste
            if self.current_state in self.accept_states:
                self.status = TMState.ACCEPTED
            elif self.current_state in self.reject_states:
                self.status = TMState.REJECTED
            else:
                self.status = TMState.HALTED
            return False

        # executa tranzitia
        to_state, write_symbol, direction = self.transitions[key]

        self.write_symbol(write_symbol)
        self.current_state = to_state
        self.move_head(direction)
        self.steps += 1

        # verifica daca am ajuns intr-o stare finala
        if self.current_state in self.accept_states:
            self.status = TMState.ACCEPTED
            return False
        elif self.current_state in self.reject_states:
            self.status = TMState.REJECTED
            return False

        return True

    def run(self, input_string: str = "") -> Tuple[TMState, str, int]:
        """Ruleaza masina Turing pe input-ul dat"""
        self.load_input(input_string)

        while self.step():
            pass

        # curata banda de simboluri blank la sfarsitul
        while self.tape and self.tape[-1] == self.blank_symbol:
            self.tape.pop()

        output = ''.join(self.tape) if self.tape else ""
        return self.status, output, self.steps

    def get_tape_content(self) -> str:
        """Returneaza continutul curent al benzii"""
        if not self.tape:
            return self.blank_symbol

        # curata simbolurile blank de la sfarsit
        tape_copy = self.tape.copy()
        while tape_copy and tape_copy[-1] == self.blank_symbol:
            tape_copy.pop()

        return ''.join(tape_copy) if tape_copy else ""


class TMConfigValidator:
    """Validator pentru configuratii de masini Turing"""

    @staticmethod
    def validate(config: Dict) -> Tuple[bool, List[str]]:
        """Valideaza o configuratie TM. Returneaza (is_valid, errors)"""
        errors = []

        # verificam campurile obligatorii
        required_fields = ['states', 'alphabet', 'tape_alphabet', 'start_state',
                           'accept_states', 'reject_states', 'transitions']

        for field in required_fields:
            if field not in config:
                errors.append(f"Câmpul obligatoriu '{field}' lipsește")

        if errors:
            return False, errors

        # validari specifice
        states = set(config['states'])
        alphabet = set(config['alphabet'])
        tape_alphabet = set(config['tape_alphabet'])

        # alfabetul de intrare trebuie sa fie subset al alfabetului benzii
        if not alphabet.issubset(tape_alphabet):
            errors.append("Alfabetul de intrare trebuie să fie subset al alfabetului benzii")

        # starea de start trebuie sa existe
        if config['start_state'] not in states:
            errors.append(f"Starea de start '{config['start_state']}' nu există în mulțimea starilor")

        # starile de accept trebuie sa existe
        accept_states = set(config['accept_states'])
        if not accept_states.issubset(states):
            errors.append("Una sau mai multe stări de accept nu există în mulțimea starilor")

        # starile de reject trebuie sa existe
        reject_states = set(config['reject_states'])
        if not reject_states.issubset(states):
            errors.append("Una sau mai multe stări de reject nu există în mulțimea starilor")

        # starile de accept si reject trebuie sa fie disjuncte
        if accept_states.intersection(reject_states):
            errors.append("Stările de accept și reject nu pot avea elemente comune")

        # validare tranzitii
        for i, transition in enumerate(config['transitions']):
            required_trans_fields = ['from_state', 'read_symbol', 'to_state', 'write_symbol', 'direction']

            for field in required_trans_fields:
                if field not in transition:
                    errors.append(f"Tranziția {i}: câmpul '{field}' lipsește")
                    continue

            if len([f for f in required_trans_fields if f in transition]) == len(required_trans_fields):
                # validari doar daca toate campurile exista
                if transition['from_state'] not in states:
                    errors.append(f"Tranziția {i}: starea sursă '{transition['from_state']}' nu există")

                if transition['to_state'] not in states:
                    errors.append(f"Tranziția {i}: starea destinație '{transition['to_state']}' nu există")

                if transition['read_symbol'] not in tape_alphabet:
                    errors.append(
                        f"Tranziția {i}: simbolul de citit '{transition['read_symbol']}' nu există în alfabetul benzii")

                if transition['write_symbol'] not in tape_alphabet:
                    errors.append(
                        f"Tranziția {i}: simbolul de scris '{transition['write_symbol']}' nu există în alfabetul benzii")

                if transition['direction'] not in ['L', 'R', 'S']:
                    errors.append(f"Tranziția {i}: direcția '{transition['direction']}' trebuie să fie L, R sau S")

        return len(errors) == 0, errors


class TMConfigLoader:
    """Incarcator de configuratii pentru masini Turing"""

    @staticmethod
    def load_from_file(filename: str) -> Tuple[bool, Dict, List[str]]:
        """Incarca configuratia dintr-un fisier JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)

            is_valid, errors = TMConfigValidator.validate(config)
            return is_valid, config, errors

        except FileNotFoundError:
            return False, {}, [f"Fișierul '{filename}' nu a fost găsit"]
        except json.JSONDecodeError as e:
            return False, {}, [f"Eroare de parsing JSON: {str(e)}"]
        except Exception as e:
            return False, {}, [f"Eroare la încărcarea fișierului: {str(e)}"]

    @staticmethod
    def save_to_file(config: Dict, filename: str) -> Tuple[bool, List[str]]:
        """Salveaza configuratia intr-un fisier JSON"""
        try:
            # valideaza configuratia inainte de salvare
            is_valid, errors = TMConfigValidator.validate(config)
            if not is_valid:
                return False, errors

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            return True, []

        except Exception as e:
            return False, [f"Eroare la salvarea fișierului: {str(e)}"]


def create_example_configs():
    """Creeaza exemple de configuratii TM pentru testare"""

    # exemplu 1: TM care accepta stringuri de forma a^n b^n
    anbn_config = {
        "name": "a^n b^n acceptor",
        "description": "Acceptă stringuri de forma a^n b^n pentru n >= 1",
        "states": ["q0", "q1", "q2", "q3", "q4", "accept", "reject"],
        "alphabet": ["a", "b"],
        "tape_alphabet": ["a", "b", "X", "Y", "_"],
        "blank_symbol": "_",
        "start_state": "q0",
        "accept_states": ["accept"],
        "reject_states": ["reject"],
        "transitions": [
            {"from_state": "q0", "read_symbol": "a", "to_state": "q1", "write_symbol": "X", "direction": "R"},
            {"from_state": "q1", "read_symbol": "a", "to_state": "q1", "write_symbol": "a", "direction": "R"},
            {"from_state": "q1", "read_symbol": "Y", "to_state": "q1", "write_symbol": "Y", "direction": "R"},
            {"from_state": "q1", "read_symbol": "b", "to_state": "q2", "write_symbol": "Y", "direction": "L"},
            {"from_state": "q2", "read_symbol": "Y", "to_state": "q2", "write_symbol": "Y", "direction": "L"},
            {"from_state": "q2", "read_symbol": "a", "to_state": "q2", "write_symbol": "a", "direction": "L"},
            {"from_state": "q2", "read_symbol": "X", "to_state": "q0", "write_symbol": "X", "direction": "R"},
            {"from_state": "q0", "read_symbol": "Y", "to_state": "q3", "write_symbol": "Y", "direction": "R"},
            {"from_state": "q3", "read_symbol": "Y", "to_state": "q3", "write_symbol": "Y", "direction": "R"},
            {"from_state": "q3", "read_symbol": "_", "to_state": "accept", "write_symbol": "_", "direction": "S"}
        ]
    }

    # Exemplu 2: TM care inverseaza un string binar
    reverse_config = {
        "name": "Binary string reverser",
        "description": "Inversează un string binar",
        "states": ["start", "scan_right", "scan_left", "done"],
        "alphabet": ["0", "1"],
        "tape_alphabet": ["0", "1", "_"],
        "blank_symbol": "_",
        "start_state": "start",
        "accept_states": ["done"],
        "reject_states": [],
        "transitions": [
            {"from_state": "start", "read_symbol": "0", "to_state": "scan_right", "write_symbol": "_",
             "direction": "R"},
            {"from_state": "start", "read_symbol": "1", "to_state": "scan_right", "write_symbol": "_",
             "direction": "R"},
            {"from_state": "start", "read_symbol": "_", "to_state": "done", "write_symbol": "_", "direction": "S"},
            {"from_state": "scan_right", "read_symbol": "0", "to_state": "scan_right", "write_symbol": "0",
             "direction": "R"},
            {"from_state": "scan_right", "read_symbol": "1", "to_state": "scan_right", "write_symbol": "1",
             "direction": "R"},
            {"from_state": "scan_right", "read_symbol": "_", "to_state": "scan_left", "write_symbol": "0",
             "direction": "L"},
            {"from_state": "scan_left", "read_symbol": "0", "to_state": "scan_left", "write_symbol": "0",
             "direction": "L"},
            {"from_state": "scan_left", "read_symbol": "1", "to_state": "scan_left", "write_symbol": "1",
             "direction": "L"},
            {"from_state": "scan_left", "read_symbol": "_", "to_state": "start", "write_symbol": "_", "direction": "R"}
        ]
    }

    return anbn_config, reverse_config


def test_turing_machines():
    """Testeaza implementarea cu diverse exemple"""
    print("=== Test Turing Machines ===\n")

    # creez exemple de configuratii
    anbn_config, reverse_config = create_example_configs()

    # salvez configuratiile in fisiere
    TMConfigLoader.save_to_file(anbn_config, "anbn_tm.json")
    TMConfigLoader.save_to_file(reverse_config, "reverse_tm.json")
    print("Configurații salvate în 'anbn_tm.json' și 'reverse_tm.json'\n")

    # test 1: a^n b^n
    print("1. Test TM pentru a^n b^n:")
    print("-" * 30)

    tm1 = TuringMachine(anbn_config)
    test_cases = ["ab", "aabb", "aaabbb", "aab", "abb", ""]

    for test_input in test_cases:
        status, output, steps = tm1.run(test_input)
        print(f"Input: '{test_input}' -> Status: {status.value}, Steps: {steps}")

    print()

    # test 2: Inversare string binar
    print("2. Test TM pentru inversarea stringurilor binare:")
    print("-" * 50)

    tm2 = TuringMachine(reverse_config)
    test_cases = ["101", "1100", "0", "1", ""]

    for test_input in test_cases:
        status, output, steps = tm2.run(test_input)
        print(f"Input: '{test_input}' -> Output: '{output}', Status: {status.value}, Steps: {steps}")

    print()

    # test 3: incarcare si validare din fisier
    print("3. Test încărcare și validare din fișier:")
    print("-" * 40)

    is_valid, config, errors = TMConfigLoader.load_from_file("anbn_tm.json")
    if is_valid:
        print("✓ Configurația 'anbn_tm.json' este validă")
        tm3 = TuringMachine(config)
        status, output, steps = tm3.run("aabb")
        print(f"Test cu 'aabb': Status = {status.value}, Steps = {steps}")
    else:
        print("✗ Erori în configurație:")
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    test_turing_machines()