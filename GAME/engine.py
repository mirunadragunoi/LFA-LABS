class AdventureGameAutomaton:
    def __init__(self):
        # starile automatului
        self.states = {
            'ENTRANCE': 'entrance',
            'HALLWAY': 'hallway',
            'KITCHEN': 'kitchen',
            'LIBRARY': 'library',
            'SECRET_ROOM': 'secret_room',
            'EXIT': 'exit',
            'MEGA_EXIT': 'mega_exit',
            'WIN': 'win',
            'GAME_OVER': 'game_over'
        }

        # starea curenta
        self.current_state = self.states['ENTRANCE']

        # inventarul (stiva pentru obiecte)
        self.inventory_stack = []

        # istoric miscari (stiva pentru navigare)
        self.move_history = []

        # actiuni posibile
        self.valid_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'PICKUP']

        # tranzitii de stare - definim automatul
        self.transitions = {
            'entrance': {
                'UP': 'hallway'
            },
            'hallway': {
                'DOWN': 'entrance',
                'LEFT': 'kitchen',
                'RIGHT': 'library',
                'UP': 'secret_room'
            },
            'kitchen': {
                'RIGHT': 'hallway',
                'PICKUP': 'kitchen'  # pentru a lua lingura
            },
            'library': {
                'LEFT': 'hallway',
                'UP': 'exit'
            },
            'secret_room': {
                'DOWN': 'hallway',
                'UP': 'mega_exit'
            },
            'exit': {
                'DOWN': 'library'
            },
            'mega_exit': {
                'DOWN': 'secret_room'
            }
        }

        # descrierea camerelor
        self.room_descriptions = {
            'entrance': "🚪 Ești la INTRARE. Poți merge UP către hallway.",
            'hallway': "🏛️ Ești în HALLWAY (holul principal).\n   LEFT: Kitchen | RIGHT: Library | UP: Secret Room | DOWN: Entrance",
            'kitchen': "🍳 Ești în KITCHEN (bucătărie).\n   Aici poți lua o LINGURĂ (PICKUP) | RIGHT: înapoi la Hallway",
            'library': "📚 Ești în LIBRARY (bibliotecă).\n   LEFT: înapoi la Hallway | UP: Exit",
            'secret_room': "🔐 Ești în SECRET ROOM (camera secretă).\n   DOWN: înapoi la Hallway | UP: Mega Exit",
            'exit': "🚪 Ești la EXIT normal.\n   DOWN: înapoi la Library\n   (Poți ieși fără lingură)",
            'mega_exit': "✨ Ești la MEGA EXIT!\n   DOWN: înapoi la Secret Room\n   (Ai nevoie de LINGURĂ pentru a scăpa!)",
            'win': "🎉 FELICITĂRI! Ai scăpat cu succes prin Mega Exit!",
            'game_over': "💀 Game Over!"
        }

    def push_to_stack(self, stack, item):
        """Operatie PUSH pentru stiva"""
        stack.append(item)

    def pop_from_stack(self, stack):
        """Operatie POP pentru stiva"""
        if stack:
            return stack.pop()
        return None

    def peek_stack(self, stack):
        """Priveste varful stivei fara sa fie sters"""
        if stack:
            return stack[-1]
        return None

    def has_spoon(self):
        """Verifica daca jucatorul are lingura in inventar"""
        return 'spoon' in self.inventory_stack

    def display_status(self):
        """Afișeaza starea curenta a jocului"""
        print("\n" + "=" * 60)
        print(f"📍 LOCAȚIA CURENTĂ: {self.current_state.upper()}")
        print("=" * 60)
        print(self.room_descriptions[self.current_state])

        # afiseaza inventarul (stiva de obiecte)
        if self.inventory_stack:
            print(f"\n🎒 INVENTAR: {', '.join(self.inventory_stack).upper()}")
        else:
            print(f"\n🎒 INVENTAR: gol")

        # afiseaza istoricul miscarilor (stiva de navigare)
        if self.move_history:
            print(f"📝 ISTORIC MIȘCĂRI: {' → '.join(self.move_history[-5:])}")  # ultimele 5

        print(f"\n⌨️  ACȚIUNI DISPONIBILE: {', '.join(self.valid_actions)}")

    def process_action(self, action):
        """Proceseaza o actiune - logica automatului"""
        action = action.upper().strip()

        if action not in self.valid_actions:
            print(f"❌ Acțiune invalidă: {action}")
            return False

        # salveaza starea anterioara in stiva de navigare
        self.push_to_stack(self.move_history, self.current_state)

        # logica speciala pentru PICKUP
        if action == 'PICKUP':
            if self.current_state == 'kitchen':
                if not self.has_spoon():
                    self.push_to_stack(self.inventory_stack, 'spoon')
                    print("✅ Ai luat LINGURA din bucătărie!")
                    return True
                else:
                    print("❌ Ai deja lingura!")
                    return True
            else:
                print("❌ Nu există nimic de luat aici!")
                return True

        # verifica daca tranzitia este valida
        if self.current_state not in self.transitions:
            print("❌ Nu poți face această acțiune aici!")
            return True

        if action not in self.transitions[self.current_state]:
            print(f"❌ Nu poți merge {action} de aici!")
            return True

        # efectueaza tranzitia
        new_state = self.transitions[self.current_state][action]

        # logica speciala pentru iesiri
        if new_state == 'exit':
            self.current_state = 'win'
            print("🎉 Ai ieșit prin Exit normal! Joc câștigat!")
            return False  # jocul se termina

        elif new_state == 'mega_exit':
            if self.has_spoon():
                self.current_state = 'win'
                print("🌟 Ai scăpat prin MEGA EXIT cu lingura! VICTORIE SUPREMĂ!")
                return False  # jocul se termina
            else:
                print("🔒 Mega Exit este blocat! Ai nevoie de LINGURĂ pentru a scăpa!")
                print("   Întoarce-te și găsește lingura din bucătărie!")
                return True  # continua jocul
        else:
            self.current_state = new_state

        return True

    def play(self):
        """Bucla principala a jocului"""
        print("🎮 BINE AI VENIT LA JOCUL DE AVENTURĂ!")
        print("🎯 OBIECTIV: Scapă din labirint! Găsește lingura pentru Mega Exit!")
        print("📜 REGULILE AUTOMATULUI:")
        print("   - Starea curentă determină acțiunile posibile")
        print("   - Inventarul funcționează ca o STIVĂ (LIFO)")
        print("   - Istoricul mișcărilor este salvat într-o STIVĂ")
        print("   - Automat finit cu stivă (Pushdown Automaton)")

        game_running = True

        while game_running:
            self.display_status()

            # verifica conditiile de caștig
            if self.current_state == 'win':
                print("\n🏆 FELICITĂRI! AI CÂȘTIGAT JOCUL!")
                break

            print(f"\n💭 Gândește-te strategic! Ai nevoie de lingură pentru Mega Exit.")
            action = input("👉 Introdu acțiunea ta: ").strip()

            if action.upper() == 'QUIT':
                print("👋 Mulțumesc că ai jucat!")
                break

            if action.upper() == 'HELP':
                self.show_help()
                continue

            game_running = self.process_action(action)

        print("\n🎮 JOCUL S-A TERMINAT!")
        self.show_final_stats()

    def show_help(self):
        """Afiseaza ajutorul"""
        print("\n📖 AJUTOR - COMENZI DISPONIBILE:")
        print("   UP/DOWN/LEFT/RIGHT - Mișcare în direcțiile respective")
        print("   PICKUP - Ia un obiect (doar în bucătărie)")
        print("   HELP - Afișează acest mesaj")
        print("   QUIT - Ieși din joc")
        print("\n🗺️  HARTA:")
        print("   ENTRANCE → HALLWAY → KITCHEN (lingură aici!)")
        print("                  ↓")
        print("              LIBRARY → EXIT (ieșire normală)")
        print("                  ↓")
        print("            SECRET ROOM → MEGA EXIT (necesită lingură!)")

    def show_final_stats(self):
        """Afișeaza statisticile finale"""
        print(f"\n📊 STATISTICI FINALE:")
        print(f"   🏃 Mișcări totale: {len(self.move_history)}")
        print(f"   🎒 Obiecte colectate: {len(self.inventory_stack)}")
        print(f"   📍 Starea finală: {self.current_state}")
        if self.move_history:
            print(f"   🛤️  Traseul tău: {' → '.join(self.move_history)}")


# ruleaza jocul
if __name__ == "__main__":
    game = AdventureGameAutomaton()
    game.play()