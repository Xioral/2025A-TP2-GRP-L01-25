"""
TP2 - Exercice 5 : Analyse de la satisfaction client
"""

def analyser_commentaire(commentaire, mots_cles):
    """
    Analyse un commentaire client et calcule un score de satisfaction.
    
    Args:
        commentaire (str): Le commentaire du client
        mots_cles (dict): Dictionnaire {mot: score}
                         Positif si score > 0, négatif si score < 0
    
    Returns:
        tuple: (score_total, mots_trouves)
    """
    score_total = 5  # Score de base
    mots_trouves = []
    
    # On convertit le commentaire en minuscules
    commentaire_lower = commentaire.lower()
    
    # On crée une version du commentaire avec espaces autour pour faciliter la recherche, donc on remplace la ponctuation par des espaces
    commentaire_modifie = commentaire_lower
    for char in '.,!?;:()[]{}"\'-':
        commentaire_modifie = commentaire_modifie.replace(char, ' ')
    
    # On divise en mots pour une recherche plus précise
    mots_commentaire = commentaire_modifie.split()
    
    #TODO : Rechercher chaque mot-clé dans le commentaire
        # D'abord, vérifier la correspondance exacte dans la liste des mots
        # Sinon, vérifier si le mot-clé est le début d'un mot du commentaire 
        # (cela permet de trouver "froid" dans "froide" ou "froids"), pour cela utiliser la méthode startswith().
    # Borner le score final entre 0 et 10
    
    liste = mots_cles.keys()
    for mot in mots_commentaire:
        if mot in liste:
            mots_trouves.append(mot)
            score_total += mots_cles[mot]
        else:
            for i in liste:
                if i in mot:
                    mots_trouves.append(i)
                    score_total += mots_cles[i]
    
    if score_total > 10:
        score_total = 10
    if score_total < 0:
        score_total = 0
    
    return score_total, mots_trouves


def categoriser_commentaires(liste_commentaires, mots_cles):
    """
    Catégorise les commentaires selon leur score de satisfaction.
    
    Args:
        liste_commentaires (list): Liste de commentaires
        mots_cles (dict): Dictionnaire des mots-clés avec scores
    
    Returns:
        dict: Commentaires groupés par catégorie
              'positifs' (score >= 7), 'neutres' (4-6), 'negatifs' (<4)
    """
    categories = {'positifs': [], 'neutres': [], 'negatifs': []}
    
    # TODO: Analyser chaque commentaire
    # Catégoriser selon le score obtenu
    # Stocker le commentaire et son score dans la bonne catégorie
    
    for i in liste_commentaires:
        score, mots = analyser_commentaire(i,mots_cles)
        if score >= 7:
            categories["positifs"].append((i,score))
        elif score < 4:
            categories["negatifs"].append((i,score))
        else:
            categories["neutres"].append((i,score))
    
    return categories


def identifier_problemes(commentaires_negatifs, mots_cles_negatifs):
    """
    Identifie les problèmes récurrents dans les commentaires négatifs.
    
    Args:
        commentaires_negatifs (list): Liste de commentaires avec score < 4
        mots_cles_negatifs (dict): Mots-clés négatifs uniquement
    
    Returns:
        dict: Fréquence de chaque problème identifié (nombre d'apparitions)
    """
    frequence_problemes = {}
    
    # TODO: Pour chaque commentaire négatif
    # Compter le nombre d'apparition de chaque mot-clé négatif
    # Retourner un dictionnaire trié par fréquence décroissante
    
    temp = {}
    for i in commentaires_negatifs:
        score, mots = analyser_commentaire(i, mots_cles_negatifs)
        for j in mots:
            if j not in temp.keys():
                temp[j] = 1
            else:
                temp[j] += 1
    
    frequence_problemes = dict(sorted(temp.items(), key=lambda item:item[1], reverse=True))
    
    return frequence_problemes


def generer_rapport_satisfaction(categories, frequence_problemes):
    """
    Génère un rapport complet de satisfaction client.
    
    Args:
        categories (dict): Commentaires catégorisés
        frequence_problemes (dict): Problèmes identifiés et leur fréquence (nombre d'apparitions)
    
    Returns:
        dict: Rapport avec statistiques et recommandations
    """
    rapport = {
        'satisfaction_moyenne': 0.0,
        'distribution': {},
        'points_forts': [],
        'points_amelioration': [],
    }
    
    # TODO: Calculer la satisfaction moyenne
    # Calculer la distribution (% positifs, neutres, négatifs)
    # Identifier les 3 principaux points d'amélioration (les 3 problèmes les plus fréquents)
    
    nbr = 0
    total = 0
    distri = []
    for i in categories.values():
        distri.append(len(i))
        for j in i:
            com, score = j
            total += score
            nbr += 1
    
    rapport["satisfaction_moyenne"] = total/nbr
    rapport["distribution"]["positifs"] = str(distri[0]/sum(distri)) + "%"
    rapport["distribution"]["neutres"] = str(distri[1]/sum(distri)) + "%"
    rapport["distribution"]["negatifs"] = str(distri[2]/sum(distri)) + "%"
    
    if len(categories["positifs"]) > len(categories["negatifs"]):
        rapport["points_forts"] = ["Service apprécié", "Qualité reconnnue"]
    
    
    rapport["points_amelioration"] = [list(frequence_problemes.keys())[i] for i in range(3)]
    
    return rapport


def calculer_tendance(historique_scores):
    """
    Calcule la tendance de satisfaction sur plusieurs périodes.
    
    Args:
        historique_scores (list): Liste de listes [periode, score_moyen]
    
    Returns:
        str: 'amélioration', 'stable', ou 'dégradation'
    """
    tendance = "stable"
    
    # TODO: Analyser l'évolution des scores
    # Si augmentation constante: 'amélioration'
    # Si diminution constante: 'dégradation'
    # Sinon: 'stable'
    
    liste = []
    present = 0
    precedent = 0
    
    for i in range(1,len(historique_scores)):
        present = historique_scores[i][1]
        precedent = historique_scores[i-1][1]
        liste.append(present-precedent)
    
    if all(x > 0 for x in liste):
        tendance = "amélioration"
    elif all(x < 0 for x in liste):
        tendance = "dégradation"
    else:
        tendance = "stable"
    
    return tendance


if __name__ == '__main__':
    # Dictionnaire des mots-clés et leurs scores
    mots_cles = {
        # Positifs
        'excellent': 3, 'délicieux': 2, 'parfait': 3,
        'rapide': 1, 'frais': 2, 'savoureux': 2,
        'accueillant': 1, 'propre': 1, 'recommande': 2,
        
        # Négatifs  
        'froid': -2, 'lent': -3, 'décevant': -2,
        'cher': -1, 'sale': -3, 'impoli': -2,
        'insipide': -2, 'attente': -1, 'déçu': -2
    }
    
    # Exemples de commentaires
    commentaires_test = [
        "Service excellent et plats délicieux! Je recommande vivement.",
        "Attente trop longue, et les plats étaient froids.",
        "Restaurant propre mais un peu cher pour la qualité.",
        "Très déçu, service lent et nourriture insipide.",
        "Accueil chaleureux, plats frais et savoureux!",
        "Correct, sans plus. Prix raisonnables.",
        "Parfait! Rapide, délicieux et accueillant.",
        "Sale et impoli, vraiment décevant.",
        "Bonne ambiance mais l'attente était longue.",
        "Les plats sont excellents mais le service est lent."
    ]
    
    # Test analyse de commentaire
    print("=== Analyse de commentaires individuels ===")
    for i, comm in enumerate(commentaires_test[:3], 1):
        score, mots = analyser_commentaire(comm, mots_cles)
        print(f"Commentaire {i}:")
        print(f"  Texte: '{comm[:50]}...'")
        print(f"  Score: {score}/10")
        print(f"  Mots-clés: {mots}")
    
    # Test catégorisation
    print("\n=== Catégorisation des commentaires ===")
    categories = categoriser_commentaires(commentaires_test, mots_cles)
    for cat, comms in categories.items():
        print(f"{cat.capitalize()}: {len(comms)} commentaires")
        if comms and len(comms) > 0:
            print(f"  Exemple: '{comms[0][0][:40]}...' (score: {comms[0][1]})")
    
    # Test identification problèmes
    print("\n=== Problèmes identifiés ===")
    mots_negatifs = {k: v for k, v in mots_cles.items() if v < 0}
    commentaires_negatifs = [c[0] for c in categories.get('negatifs', [])]
    problemes = identifier_problemes(commentaires_negatifs, mots_negatifs)
    
    if problemes:
        print("Problèmes récurrents (fréquence en %):")
        for probleme, freq in list(problemes.items())[:5]:
            print(f"  - {probleme}: {freq:.1f}% des commentaires négatifs")
    
    # Test rapport
    print("\n=== Rapport de satisfaction ===")
    rapport = generer_rapport_satisfaction(categories, problemes)
    print(f"Satisfaction moyenne: {rapport['satisfaction_moyenne']:.1f}/10")
    print(f"Distribution: {rapport['distribution']}")
    if rapport['points_forts']:
        print(f"Points forts: {rapport['points_forts']}")
    if rapport['points_amelioration']:
        print(f"Points d'amélioration prioritaires: {rapport['points_amelioration']}")
    
    # Test tendance
    print("\n=== Analyse de tendance ===")
    historique = [
        ['Janvier', 6.5],
        ['Février', 6.8],
        ['Mars', 7.1],
        ['Avril', 7.3]
    ]
    tendance = calculer_tendance(historique)
    print(f"Tendance sur 4 mois: {tendance}")
