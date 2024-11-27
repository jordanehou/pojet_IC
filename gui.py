import tkinter as tk
from tkinter import messagebox

# Classe représentant l'état des feux de circulation
# test
class FeuxCirculation:
    def __init__(self, zone_dessin):
        self.zone_dessin = zone_dessin
        # Création des cercles pour chaque feu
        self.rouge_ns = zone_dessin.create_oval(50, 50, 150, 150, fill="gray")  # Rouge pour le Nord-Sud
        self.orange_ns = zone_dessin.create_oval(50, 160, 150, 260, fill="gray")  # Orange pour le Nord-Sud
        self.vert_ns = zone_dessin.create_oval(50, 270, 150, 370, fill="gray")  # Vert pour le Nord-Sud

        self.rouge_oe = zone_dessin.create_oval(250, 50, 350, 150, fill="gray")  # Rouge pour l'Est-Ouest
        self.orange_oe = zone_dessin.create_oval(250, 160, 350, 260, fill="gray")  # Orange pour l'Est-Ouest
        self.vert_oe = zone_dessin.create_oval(250, 270, 350, 370, fill="gray")  # Vert pour l'Est-Ouest

        # Ajouter les étiquettes des directions
        zone_dessin.create_text(100, 20, text="Nord-Sud", font=("Arial", 14), fill="black")
        zone_dessin.create_text(300, 20, text="Est-Ouest", font=("Arial", 14), fill="black")

    def mettre_a_jour_feux(self, direction, couleur):
        # Mise à jour des couleurs en fonction de la direction et de l'état
        if direction == "NS":
            self.zone_dessin.itemconfig(self.rouge_ns, fill="red" if couleur == "red" else "gray")
            self.zone_dessin.itemconfig(self.orange_ns, fill="yellow" if couleur == "yellow" else "gray")
            self.zone_dessin.itemconfig(self.vert_ns, fill="green" if couleur == "green" else "gray")
        elif direction == "OE":
            self.zone_dessin.itemconfig(self.rouge_oe, fill="red" if couleur == "red" else "gray")
            self.zone_dessin.itemconfig(self.orange_oe, fill="yellow" if couleur == "yellow" else "gray")
            self.zone_dessin.itemconfig(self.vert_oe, fill="green" if couleur == "green" else "gray")

# Classe pour la gestion des transitions et de l'état des feux
class SystemeCirculation:
    def __init__(self, zone_dessin):
        self.feux_circulation = FeuxCirculation(zone_dessin)
        self.courant_ns = "red"  # Feu de circulation pour le Nord-Sud
        self.courant_oe = "red"  # Feu de circulation pour l'Est-Ouest

    def declencher_transition(self, direction):
        # Logique des transitions des feux
        if direction == "NS":
            if self.courant_ns == "red":
                self.courant_ns = "green"
                self.courant_oe = "red"
            elif self.courant_ns == "green":
                self.courant_ns = "yellow"
            elif self.courant_ns == "yellow":
                self.courant_ns = "red"
                self.courant_oe = "green"
        elif direction == "OE":
            if self.courant_oe == "red":
                self.courant_oe = "green"
                self.courant_ns = "red"
            elif self.courant_oe == "green":
                self.courant_oe = "yellow"
            elif self.courant_oe == "yellow":
                self.courant_oe = "red"
                self.courant_ns = "green"

        self.feux_circulation.mettre_a_jour_feux("NS", self.courant_ns)
        self.feux_circulation.mettre_a_jour_feux("OE", self.courant_oe)

    def gerer_traffic(self, scenario, direction):
        if scenario == "dense":
            if direction == "NS" and self.courant_ns != "green":
                self.courant_ns = "green"
                self.courant_oe = "red"
                self.feux_circulation.mettre_a_jour_feux("NS", "green")
                self.feux_circulation.mettre_a_jour_feux("OE", "red")
            elif direction == "OE" and self.courant_oe != "green":
                self.courant_oe = "green"
                self.courant_ns = "red"
                self.feux_circulation.mettre_a_jour_feux("OE", "green")
                self.feux_circulation.mettre_a_jour_feux("NS", "red")
            messagebox.showinfo("Trafic dense", f"Maintien du vert pour {direction} en raison du trafic dense.")
        elif scenario == "accident":
            if direction == "NS":
                if self.courant_oe == "red":
                    self.courant_oe = "green"
                    self.feux_circulation.mettre_a_jour_feux("OE", "green")
                self.courant_ns = "red"
                self.feux_circulation.mettre_a_jour_feux("NS", "red")
            elif direction == "OE":
                if self.courant_ns == "red":
                    self.courant_ns = "green"
                    self.feux_circulation.mettre_a_jour_feux("NS", "green")
                self.courant_oe = "red"
                self.feux_circulation.mettre_a_jour_feux("OE", "red")
            messagebox.showinfo("Accident", f"Feux bloqués au rouge pour {direction} en raison d'un accident.")

# Fonction principale de l'interface graphique
def creer_interface():
    racine = tk.Tk()
    racine.title("Système de feux de circulation")

    # Crée un Canvas pour afficher les feux de circulation
    zone_dessin = tk.Canvas(racine, width=400, height=500)
    zone_dessin.pack()

    # Créer un système de feux de circulation
    systeme_circulation = SystemeCirculation(zone_dessin)

    # Fonction pour passer au feu suivant
    def transition_suivante():
        if systeme_circulation.courant_ns == "green":
            systeme_circulation.declencher_transition("NS")
        elif systeme_circulation.courant_oe == "green":
            systeme_circulation.declencher_transition("OE")
        else:
            if systeme_circulation.courant_ns == "red":
                systeme_circulation.declencher_transition("NS")
            elif systeme_circulation.courant_oe == "red":
                systeme_circulation.declencher_transition("OE")

    # Fonction pour gérer les scénarios de trafic
    def gerer_scenario(scenario, direction):
        systeme_circulation.gerer_traffic(scenario, direction)

    # Ajouter les boutons
    bouton_suivant = tk.Button(racine, text="Suivant", command=transition_suivante)
    bouton_suivant.pack(pady=10)

    # Boutons pour gérer le trafic dense
    bouton_dense_ns = tk.Button(racine, text="Trafic dense Nord-Sud", command=lambda: gerer_scenario("dense", "NS"))
    bouton_dense_ns.pack(pady=5)

    bouton_dense_oe = tk.Button(racine, text="Trafic dense Est-Ouest", command=lambda: gerer_scenario("dense", "OE"))
    bouton_dense_oe.pack(pady=5)

    # Boutons pour gérer les accidents
    bouton_accident_ns = tk.Button(racine, text="Accident Nord-Sud", command=lambda: gerer_scenario("accident", "NS"))
    bouton_accident_ns.pack(pady=5)

    bouton_accident_oe = tk.Button(racine, text="Accident Est-Ouest", command=lambda: gerer_scenario("accident", "OE"))
    bouton_accident_oe.pack(pady=5)

    racine.after(1000, transition_suivante)

    racine.mainloop()

if __name__ == "__main__":
    creer_interface()
