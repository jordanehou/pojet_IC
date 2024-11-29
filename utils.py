from petri_net import (
    transitions, zone_securisee, rouge_ns, vert_ns, jaune_ns,
    rouge_oe, vert_oe, jaune_oe, trafic_intense, accident_detecte_ns,
    accident_detecte_oe, compteur_trafic_ns, compteur_trafic_oe
)

def reinitialiser_jetons():
    """Réinitialise les jetons pour commencer la simulation."""
    zone_securisee.jetons = 1
    rouge_ns.jetons = 1
    vert_ns.jetons = 0
    jaune_ns.jetons = 0
    rouge_oe.jetons = 1
    vert_oe.jetons = 0
    jaune_oe.jetons = 0
    trafic_intense.jetons = 0
    accident_detecte_ns.jetons = 0
    accident_detecte_oe.jetons = 0
    compteur_trafic_ns[0] = 0
    compteur_trafic_oe[0] = 0

def remise_a_1():
    if(rouge_ns.jetons > 1):
        rouge_ns.jetons = 1

def simuler_reseau_petri(etapes):
    """Simuler le réseau de Petri pour un cas spécifique."""
    for etape in range(1, etapes + 1):
        print(f"Étape {etape} :")

        # Gestion des compteurs de trafic intense
        if vert_ns.jetons > 0:
            compteur_trafic_ns[0] += 1
        else:
            compteur_trafic_ns[0] = 0

        if vert_oe.jetons > 0:
            compteur_trafic_oe[0] += 1
        else:
            compteur_trafic_oe[0] = 0

        for transition in transitions:
            if transition.est_active():
                activee = transition.activer()
                if activee:
                    print(f"  Transition activée : {transition.nom}")
                    break  # Une seule transition par étape
        # mise a 1 du jeton du feu rouge de la direction NS
        remise_a_1()
        # Afficher l'état actuel des places 
        print(f"  {rouge_ns}\n  {vert_ns}\n  {jaune_ns}")
        print(f"  {rouge_oe}\n  {vert_oe}\n  {jaune_oe}")
        print(f"  Trafic intense : {trafic_intense.jetons}")
        print(f"  Accident NS : {accident_detecte_ns.jetons}")
        print(f"  Accident OE : {accident_detecte_oe.jetons}\n")


def simuler_tous_les_cas():
    """Simuler les trois cas : normal, trafic intense, accident."""
    print("=== Cas normal ===")
    reinitialiser_jetons()
    simuler_reseau_petri(10)

    print("=== Cas de trafic intense (NS) ===")
    reinitialiser_jetons()
    trafic_intense.jetons = 1  # Prolonger le feu vert sur NS
    simuler_reseau_petri(10)

    print("=== Cas d'accident (NS) ===")
    reinitialiser_jetons()
    accident_detecte_ns.jetons = 1  # Bloquer NS en rouge
    simuler_reseau_petri(10)


def simuler_accident():
    print("=== Cas d'accident (NS) ===")
    reinitialiser_jetons()
    accident_detecte_ns.jetons = 1  # Bloquer NS en rouge
    remise_a_1()
    simuler_reseau_petri(10)
