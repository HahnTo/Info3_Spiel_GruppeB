# Soll die Platformen aus einer JSON oder ähnlichem laden, wenn ein neues Level erstellt wird.

class Level:
    def __init__(self, level_id):
        self.level_id = level_id

    def load(self):
        print(f"Level {self.level_id} geladen")