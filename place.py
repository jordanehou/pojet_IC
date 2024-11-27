# place.py
class Place:
    def __init__(self, nom, jetons=0):
        self.nom = nom
        self.jetons = jetons

    def __str__(self):
        return f"{self.nom} : {self.jetons} jetons"
