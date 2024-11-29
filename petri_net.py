from place import Place
from transition import Transition

# Places
zone_securisee = Place("ZoneSécurisée", 1)
rouge_ns = Place("Rouge_NS", 1)
vert_ns = Place("Vert_NS")
jaune_ns = Place("Jaune_NS")
rouge_oe = Place("Rouge_OE", 1)
vert_oe = Place("Vert_OE")
jaune_oe = Place("Jaune_OE")
trafic_intense = Place("Trafic_Intense")  # Indique un trafic intense
accident_detecte_ns = Place("Accident_NS")  # Indique un accident sur NS
accident_detecte_oe = Place("Accident_OE")  # Indique un accident sur oe

# Compteurs pour trafic intense (pour prolonger le feu vert)
compteur_trafic_ns = [0]
compteur_trafic_oe = [0]

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
t1_oe = Transition(
    "T1_OE", [rouge_oe, zone_securisee], [vert_oe, rouge_ns],
    lambda: accident_detecte_oe.jetons == 0 and compteur_trafic_oe[0] == 0
)
t2_oe = Transition(
    "T2_OE", [vert_oe], [jaune_oe],
    lambda: trafic_intense.jetons == 0 or compteur_trafic_oe[0] == 3
)
t3_oe = Transition(
    "T3_OE", [jaune_oe], [zone_securisee, rouge_oe]
)

# Liste des transitions
transitions = [t1_ns, t2_ns, t3_ns, t1_oe, t2_oe, t3_oe]

places = {
    "ZoneSécurisée": zone_securisee,
    "Rouge_NS": rouge_ns,
    "Vert_NS": vert_ns,
    "Jaune_NS": jaune_ns,
    "Rouge_OE": rouge_oe,
    "Vert_OE": vert_oe,
    "Jaune_OE": jaune_oe,
    "Trafic_Intense": trafic_intense,
    "Accident_NS": accident_detecte_ns,
    "Accident_OE": accident_detecte_oe,
}
