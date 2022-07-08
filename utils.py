import itertools


def get_nombres_a_placer(liste):
    """
    Retourne la liste des nombres qu'il reste à placer dans la liste donnée en paramètre
    """
    return [i for i in range(1, len(liste) + 1) if i not in liste]


def get_indices_cases_vides(liste):
    """
    Retourne la liste des indices de la liste en paramètre où la valeur est nulle (= case vide)
    """
    return [i for i in range(len(liste)) if liste[i] == 0]


def get_nombre_sommets_visibles(liste):
    """
    Retourne le nombre de sommets visibles de la liste en entrée à l'exclusion des zéros.
    [0,3,1,0,4] -> 2
    """
    max_hauteur = 0
    nb_sommets = 0
    for nombre in liste:
        if nombre > max_hauteur:
            max_hauteur = nombre
            nb_sommets += 1
    return nb_sommets


def get_nombres_sommets_visibles_possibles(liste):
    """
    Retourne les nombres possibles de sommets visibles de la liste, sous forme de liste.
    0 1 0 4 6 7 5
    -> 3, 4, 6 et 7 seront forcément visibles donc la liste retournée contient 4.
    -> 2 peut être visible s'il est placé avant le 3, la liste retournée contient donc également 5 (2,3,4,6,7)
    -> 1 ne sera par contre pas visible car il sera devant un nombre plus grand que lui.
    -> retour : [4, 5]
    """

    indices_cases_vides = get_indices_cases_vides(liste)
    set_nombres_sommets_visibles = set()
    # pour chaque permutation possible des nombres à placer dans la liste donnée en paramètre
    # (si 2, 3, 5 sont à placer dans la liste, boucle sur les 6 permutations possibles de ces nombres):
    for nombres in itertools.permutations(get_nombres_a_placer(liste)):
        liste_complete = liste.copy()
        # complète la liste avec les nombres à placer dans l'ordre donné par la permutation
        for i, indice in enumerate(indices_cases_vides):
            liste_complete[indice] = list(nombres)[i]
        # compte le nombre de sommets visibles et l'ajoute à la liste des nombres de sommets pouvant être visibles
        set_nombres_sommets_visibles.add(get_nombre_sommets_visibles(liste_complete))

    return set_nombres_sommets_visibles

