"""
TP2 - Exercice 4 : Système de réservation
"""

# Fonction fournie - ne pas modifier
def afficher_salle(salle):
    """Affiche la salle du restaurant de manière formatée."""
    print("\n=== Plan de la salle ===")
    print("   ", end="")
    for j in range(len(salle[0])):
        print(f" {j}", end="")
    print()
    for i, rangee in enumerate(salle):
        print(f"{i}: ", end="")
        for table in rangee:
            print(f" {table}", end="")
        print()
    print("=" * 25)


# PARTIE 1: Initialisation (2 points)
def initialiser_salle(nb_rangees, nb_colonnes, positions_tables):
    """
    Initialise la salle du restaurant.
    
    Args:
        nb_rangees (int): Nombre de rangées
        nb_colonnes (int): Nombre de colonnes
        positions_tables (list): Liste de tuples (rangee, colonne, taille_table)
                                taille_table: 2 pour petite, 4 pour grande
    
    Returns:
        list: Grille représentant la salle
            'L2'/'L4' = table libre pour 2/4 personnes
            'X' = espace non disponible
    """
    salle = [["X" for j in range(nb_colonnes)] for i in range(nb_rangees)]
    
    # TODO: Créer une grille remplie de 'X' (espaces non disponibles)
    # Puis placer les tables aux positions indiquées
    # Format: 'L2' pour table libre de 2, 'L4' pour table libre de 4
    
    for i in positions_tables:
        y,x,t = i
        salle[y][x] = "L2" if t == 2 else "L4"
    
    return salle


def marquer_reservation(salle, position, taille_groupe):
    """
    Marque une table comme réservée.
    
    Args:
        salle (list): Grille de la salle
        position (tuple): (rangee, colonne) de la table
        taille_groupe (int): Nombre de personnes
    
    Returns:
        list: Salle mise à jour avec 'R2' ou 'R4' pour table réservée
    """
    nouvelle_salle = [rangee[:] for rangee in salle]  # Copie profonde
    
    # TODO: Marquer la table à la position donnée comme réservée (vérifier 
    # qu'elle est libre, on pourra utiliser la méthode startswith())
    # 'R2' pour table de 2 réservée, 'R4' pour table de 4
    
    y,x = position
    if nouvelle_salle[y][x][0] == "L":
        nouvelle_salle[y][x] = "R2" if taille_groupe == 2 else "R4"
    
    return nouvelle_salle


# PARTIE 2: Recherche de table (3 points)
def calculer_score_table(position, taille_table, taille_groupe, nb_colonnes):
    """
    Calcule le score d'une table pour un groupe.
    
    Args:
        position (tuple): (rangee, colonne) de la table
        taille_table (int): Capacité de la table (2 ou 4)
        taille_groupe (int): Nombre de personnes dans le groupe
        nb_colonnes (int): Nombre total de colonnes (pour calculer proximité fenêtre)
    
    Returns:
        int: Score de la table (plus élevé = meilleur)
            -1 si la table ne convient pas
    """
    score = 100
    
    # TODO: Calculer le score selon:
    # - Si taille_table < taille_groupe: retourner -1 (ne convient pas)
    # - Base: 100 points
    # - Pénalité: -10 points par place vide (gaspillage)
    # - Bonus fenêtre: +20 points si colonne == 0 ou colonne == nb_colonnes-1
    # - Bonus position: +5 points si rangée < 3 (près de l'entrée)
    
    if taille_table < taille_groupe:
        score = -1
    else:
        y,x = position
        libre = taille_table - taille_groupe
        score -= libre*10
        score += 5 if x < 3 else 0
        score += 20 if y == 0 or y == nb_colonnes-1 else 0
    
    return score


def trouver_meilleure_table(salle, taille_groupe):
    """
    Trouve la meilleure table disponible pour un groupe.
    
    Args:
        salle (list): Grille de la salle
        taille_groupe (int): Nombre de personnes
    
    Returns:
        tuple: (position, taille_table) ou None si aucune table disponible
    """
    meilleure_table = None
    meilleur_score = -1
    
    # TODO: Parcourir toutes les tables libres ('L2' ou 'L4')
    # Calculer leur score et garder la meilleure
    
    for i in range(len(salle)):
        for j in range(len(salle[0])):
            if salle[i][j] == "L2" or salle[i][j] == "L4":
                score = calculer_score_table((i,j), 2 if salle[i][j] == "L2" else 4, taille_groupe, len(salle[0]))
                if score > meilleur_score:
                    meilleur_score = score
                    meilleure_table = ((i,j), 2 if salle[i][j] == "L2" else 4)
    
    return meilleure_table


def generer_rapport_occupation(salle):
    """
    Génère un rapport sur l'occupation de la salle.
    
    Args:
        salle (list): Grille de la salle
    
    Returns:
        dict: Statistiques d'occupation
    """
    rapport = {
        'tables_libres_2': 0,
        'tables_libres_4': 0,
        'tables_reservees_2': 0,
        'tables_reservees_4': 0,
        'tables_occupees_2': 0,
        'tables_occupees_4': 0,
        'taux_occupation': 0.0
    }
    
    # TODO: Compter les différents types de tables
    # Calculer le taux d'occupation (réservées + occupées) / total
    
    nbr_tables = 0
    
    for i in range(len(salle)):
        for j in range(len(salle[0])):
            if salle[i][j] == "L2":
                rapport["tables_libres_2"] += 1
                nbr_tables += 1
            elif salle[i][j] == "L4":
                rapport["tables_libres_4"] += 1
                nbr_tables += 1
            elif salle[i][j] == "R2":
                rapport["tables_reservees_2"] += 1
                nbr_tables += 1
            elif salle[i][j] == "R4":
                rapport["tables_reservees_4"] += 1
                nbr_tables += 1
            elif salle[i][j] == "O2":
                rapport["tables_occupees_2"] += 1
                nbr_tables += 1
            elif salle[i][j] == "O4":
                rapport["tables_occupees_4"] += 1
                nbr_tables += 1
    
    rapport["taux_occupation"] = (rapport["tables_reservees_2"] + rapport["tables_reservees_4"] + rapport["tables_occupees_2"] + rapport["tables_occupees_4"]) / nbr_tables
    
    return rapport


if __name__ == '__main__':
    # Configuration de la salle
    nb_rangees = 5
    nb_colonnes = 6
    
    # Positions des tables: (rangée, colonne, taille)
    positions_tables = [
        (0, 0, 2), (0, 2, 2), (0, 5, 2),  # Rangée 0: tables de 2 près fenêtres
        (1, 1, 4), (1, 4, 4),              # Rangée 1: tables de 4
        (2, 0, 2), (2, 2, 4), (2, 5, 2),  # Rangée 2: mixte
        (3, 1, 4), (3, 3, 4),              # Rangée 3: tables de 4
        (4, 0, 2), (4, 2, 2), (4, 4, 2), (4, 5, 2)  # Rangée 4: tables de 2
    ]
    
    # Partie 1: Initialisation
    print("=== PARTIE 1: Initialisation ===")
    salle = initialiser_salle(nb_rangees, nb_colonnes, positions_tables)
    afficher_salle(salle)
    
    # Test de réservation
    print("\nRéservation d'une table pour 4 personnes en position (1, 1):")
    salle = marquer_reservation(salle, (1, 1), 4)
    afficher_salle(salle)
    
    # Partie 2: Recherche de table
    print("\n=== PARTIE 2: Recherche de table ===")
    
    # Test de calcul de score
    score_test = calculer_score_table((0, 0), 2, 2, nb_colonnes)
    print(f"Score table (0,0) pour 2 personnes: {score_test}")
    
    # Test de recherche
    groupes_test = [2, 3, 4, 6]
    for taille in groupes_test:
        resultat = trouver_meilleure_table(salle, taille)
        if resultat:
            pos, taille_table = resultat
            print(f"Groupe de {taille}: Meilleure table en {pos} (capacité {taille_table})")
        else:
            print(f"Groupe de {taille}: Aucune table disponible")
    
    # Test du rapport
    print("\n=== Rapport d'occupation ===")
    rapport = generer_rapport_occupation(salle)
    for cle, valeur in rapport.items():
        if 'taux' in cle:
            print(f"  {cle}: {valeur:.1%}")
        else:
            print(f"  {cle}: {valeur}")
