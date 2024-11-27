class Transition:
    def __init__(self, nom, places_entrée, places_sortie, condition=None):
        self.nom = nom
        self.places_entrée = places_entrée
        self.places_sortie = places_sortie
        self.condition = condition or (lambda: True)

    def est_active(self):
        return all(place.jetons > 0 for place in self.places_entrée) and self.condition()

    def activer(self):
        if self.est_active():
            for place in self.places_entrée:
                place.jetons -= 1
            for place in self.places_sortie:
                place.jetons += 1
            return True
        return False
