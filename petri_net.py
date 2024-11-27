from place import Place
from transition import Transition

# Places
zone_securisee = Place("ZoneSécurisée", 1)
rouge_ns = Place("Rouge_NS", 1)
vert_ns = Place("Vert_NS")
jaune_ns = Place("Jaune_NS")
rouge_ew = Place("Rouge_EW", 1)
vert_ew = Place("Vert_EW")
jaune_ew = Place("Jaune_EW")
trafic_intense = Place("Trafic_Intense")  # Indique un trafic intense
accident_detecte_ns = Place("Accident_NS")  # Indique un accident sur NS
accident_detecte_ew = Place("Accident_EW")  # Indique un accident sur EW

# Compteurs pour trafic intense (pour prolonger le feu vert)
compteur_trafic_ns = [0]
compteur_trafic_ew = [0]

# Transitions pour Nord-Sud
t1_ns = Transition(
    "T1_NS", [rouge_ns, zone_securisee], [vert_ns],
    lambda: accident_detecte_ns.jetons == 0 and compteur_trafic_ns[0] == 0
)
t2_ns = Transition(
    "T2_NS", [vert_ns], [jaune_ns],
    lambda: trafic_intense.jetons == 0 or compteur_trafic_ns[0] == 3
)
t3_ns = Transition(
    "T3_NS", [jaune_ns], [zone_securisee]
)

# Transitions pour Est-Ouest
t1_ew = Transition(
    "T1_EW", [rouge_ew, zone_securisee], [vert_ew, rouge_ns],
    lambda: accident_detecte_ew.jetons == 0 and compteur_trafic_ew[0] == 0
)
t2_ew = Transition(
    "T2_EW", [vert_ew], [jaune_ew],
    lambda: trafic_intense.jetons == 0 or compteur_trafic_ew[0] == 3
)
t3_ew = Transition(
    "T3_EW", [jaune_ew], [zone_securisee, rouge_ew]
)

# Liste des transitions
transitions = [t1_ns, t2_ns, t3_ns, t1_ew, t2_ew, t3_ew]

places = {
    "ZoneSécurisée": zone_securisee,
    "Rouge_NS": rouge_ns,
    "Vert_NS": vert_ns,
    "Jaune_NS": jaune_ns,
    "Rouge_EW": rouge_ew,
    "Vert_EW": vert_ew,
    "Jaune_EW": jaune_ew,
    "Trafic_Intense": trafic_intense,
    "Accident_NS": accident_detecte_ns,
    "Accident_EW": accident_detecte_ew,
}
