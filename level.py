# Soll die Platformen aus einer JSON oder ähnlichem laden, wenn ein neues Level erstellt wird.

class Level:
    def __init__(self, id):
        self.id = id

    def load(self):
        print(f"Level {self.id} geladen")