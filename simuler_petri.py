import tkinter as tk
from petri_net import transitions, rouge_ns, vert_ns, jaune_ns, rouge_ew, vert_ew, jaune_ew
from utils import reinitialiser_jetons, remise_a_1, simuler_reseau_petri


class PetriNetUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation de Réseau de Petri")

        # Canvas pour dessiner le réseau
        self.canvas = tk.Canvas(root, width=600, height=700, bg="white")
        self.canvas.pack()

        # Boutons pour gérer les cas
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        self.normal_button = tk.Button(self.control_frame, text="Cas Normal", command=self.start_normal_case)
        self.normal_button.grid(row=0, column=0, padx=10, pady=10)

        self.traffic_intense_button = tk.Button(self.control_frame, text="Cas Trafic Intense", command=self.start_traffic_case)
        self.traffic_intense_button.grid(row=0, column=1, padx=10, pady=10)

        self.accident_button = tk.Button(self.control_frame, text="Cas Accident", command=self.start_accident_case)
        self.accident_button.grid(row=0, column=2, padx=10, pady=10)

        # Variables pour représenter le réseau
        self.places = {
            "Rouge_NS": rouge_ns,
            "Vert_NS": vert_ns,
            "Jaune_NS": jaune_ns,
            "Rouge_EW": rouge_ew,
            "Vert_EW": vert_ew,
            "Jaune_EW": jaune_ew,
        }
        self.transitions = transitions
        self.place_positions = {}

        # Dessiner le réseau
        self.draw_petri_net()

    def draw_petri_net(self):
        """Dessine les places et transitions sur le canvas."""
        # Places
        x_offset, y_offset = 100, 50
        spacing_x, spacing_y = 150, 100

        self.place_positions = {
            "Rouge_NS": (x_offset, y_offset),
            "Vert_NS": (x_offset, y_offset + spacing_y),
            "Jaune_NS": (x_offset, y_offset + 2 * spacing_y),
            "Rouge_EW": (x_offset + spacing_x, y_offset),
            "Vert_EW": (x_offset + spacing_x, y_offset + spacing_y),
            "Jaune_EW": (x_offset + spacing_x, y_offset + 2 * spacing_y),
        }

        self.place_shapes = {}
        for name, (x, y) in self.place_positions.items():
            place_id = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightgray")
            text_id = self.canvas.create_text(x, y, text=self.places[name].jetons)
            self.place_shapes[name] = (place_id, text_id)

        # Transitions
        transition_x = x_offset + spacing_x / 2
        transition_y = y_offset + spacing_y / 2
        for i, transition in enumerate(self.transitions):
            x, y = transition_x, transition_y + i * spacing_y
            self.canvas.create_rectangle(x - 10, y - 20, x + 10, y + 2, fill="black")
            self.canvas.create_text(x, y, text=transition.nom, fill="white")

    def update_places(self):
        """Met à jour les places et les jetons sur l'interface graphique."""
        for name, (x, y) in self.place_positions.items():
            _, text_id = self.place_shapes[name]
            self.canvas.itemconfig(text_id, text=self.places[name].jetons)

    def step_simulation(self):
        """Effectue une étape de simulation."""
        for transition in self.transitions:
            if transition.est_active():
                transition.activer()
                remise_a_1()
                break
        self.update_places()
        self.root.after(3000, self.step_simulation)  # Répéter toutes les 3 secondes

    def start_normal_case(self):
        """Démarre la simulation pour le cas normal."""
        reinitialiser_jetons()
        self.update_places()
        self.step_simulation()

    def start_traffic_case(self):
        """Démarre la simulation pour le cas de trafic intense."""
        reinitialiser_jetons()
        rouge_ns.jetons = 2  # Exemple : Modifier les jetons pour simuler le trafic intense
        self.update_places()
        self.step_simulation()

    def start_accident_case(self):
        """Démarre la simulation pour le cas d'accident."""
        reinitialiser_jetons()
        rouge_ns.jetons = 1
        vert_ns.jetons = 0
        self.update_places()
        self.step_simulation()


if __name__ == "__main__":
    root = tk.Tk()
    app = PetriNetUI(root)
    root.mainloop()
