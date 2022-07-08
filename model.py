import itertools
import numpy as np
import random
import copy
import utils
import statistics

POSITIONS = ["NORD", "EST", "SUD", "OUEST"]


class Grille:
    """
    La classe qui représente les solutions des problèmes et qui sert à les générer.
    """

    def __init__(self, cote: int):
        self.__cote = cote
        self.__cases = np.zeros((self.__cote, self.__cote), dtype=int)

    def remplir(self):
        """
        Remplit une grille au hasard en respectant la seule règle : un nombre ne peut pas apparaître deux fois ou plus
        la même ligne ni dans la même colonne
        """

        error = True
        cote = self.__cote

        # tant que les grilles ne se remplissent pas, i.e tant que le programme lève une exception. Cela se produit
        # parce qu'en fonction des choix de remplissage qui sont faits, il n'y a plus de case disponible pour un nombre
        # sans que cela n'enfreigne la règle.
        while error:
            error = False
            try:
                # remplit la première ligne de manière aléatoire
                self.__cases[0, :] = [i for i in range(1, cote + 1)]
                random.shuffle(self.__cases[0, :])

                # chaque nombre est une entrée dans le dictionnaire "rempli" auquel correspond la liste des indices des
                # colonnes qu'il occupe déjà
                rempli = {}
                for indice, nombre in enumerate(self.__cases[0]):
                    rempli[nombre] = [indice]
                # remplit les lignes suivantes
                for ligne in range(1, cote):
                    nombres_a_placer = list(range(1, cote + 1))
                    occupe = []
                    while len(nombres_a_placer) != 0:
                        choix = {}
                        # associe chaque nombre à la liste des indices des cases qu'il peut prendre sur la ligne (i.e
                        # celles qu'il n'occupe pas dans "rempli" et celles qui ne sont pas déjà prises dans la ligne)
                        for nombre in nombres_a_placer:
                            choix[nombre] = [i for i in range(cote) if i not in occupe and i not in rempli[nombre]]
                        # garde un nombre parmi ceux qui ont le moins de choix de cases
                        min_choix = min([len(choix[n]) for n in choix])
                        nombre_choisi = random.choice(
                            list({key: value for key, value in choix.items() if len(value) == min_choix}))
                        # place le nombre choisi sur une case qu'il peut occuper au hasard
                        indice_choisi = random.choice(choix[nombre_choisi])
                        self.__cases[ligne][indice_choisi] = nombre_choisi
                        # met à jour les différentes listes et dictionnaires
                        occupe.append(indice_choisi)
                        rempli[nombre_choisi].append(indice_choisi)
                        nombres_a_placer.remove(nombre_choisi)
            # si le programme lève une exception, on recommence à boucler
            except Exception:
                error = True

    @property
    def cases(self):
        return self.__cases

    def __getitem__(self, pos):
        # pos se présente sous la forme d'un tuple qui représente les coordonnées dans la grille
        x, y = pos
        return self.__cases[x, y]

    def __setitem__(self, pos, value):
        # pos se présente sous la forme d'un tuple qui représente les coordonnées dans la grille
        x, y = pos
        self.__cases[x, y] = value

    def __contains__(self, item):
        return item in self.__cases

    def __str__(self):
        str_grille = ""
        cote = self.__cote

        for i in range(cote):
            for j in range(cote):
                str_grille += str(self[i, j]) + " "
            str_grille += "\n"

        return str_grille

    def __eq__(self, other):
        return np.array_equal(self.__cases, other.cases)


class Probleme:
    """
    La classe qui définit les problèmes des montagnes.
    """

    def __init__(self, cote=0, pdv=None, grille: Grille = None):
        """
        Le constructeur de Problème. Un problème peut être initialisé à partir d'une grille ou directement à partir de
        ses listes de points de vue.
        Chaque problème est constitué de 4 points de vue qui sont des entrées du dictionnaire points_de_vue.
        Les clés de ces entrées sont les positions : NORD, EST, SUD, OUEST.
        Les valeurs de ces entrées sont la liste des sommets visibles (pour NORD et SUD, de gauche à droite ; pour EST
        et OUEST de haut en bas.
        """
        self.__points_de_vue = {}
        self.__cote = cote

        # si une grille est donnée en paramètre, on calcule, pour chaque ligne et colonne, le nombre de sommets visibles
        if grille is not None:
            self.__cote = len(grille[0, :])
            for position in POSITIONS:
                for i in range(self.__cote):
                    liste = []

                    if position == "NORD":
                        liste = grille[:, i]
                    elif position == "SUD":
                        # retourne la liste car ce sont les sommets visibles par le bas de la grille
                        liste = np.flip(grille[:, i])
                    elif position == "OUEST":
                        liste = grille[i, :]
                    elif position == "EST":
                        # retourne la liste car ce sont les sommets visibles par la droite de la grille
                        liste = np.flip(grille[i, :])

                    nb_sommets = utils.get_nombre_sommets_visibles(liste)
                    self.__points_de_vue[position].append(nb_sommets)
        # si le point_de_vue donné en paramètre est None, remplit un problème de 0
        elif pdv is None:
            for position in POSITIONS:
                self.__points_de_vue[position] = [0 for i in range(self.__cote)]
        else:
            self.__points_de_vue = pdv
            # le coté est la longueur d'une des listes de points de vue, on choisit arbitrairement NORD
            self.__cote = len(pdv["NORD"])

    def resoudre(self):
        """
        Retourne la grille solution unique du problème.
        Plus on monte en taille de problèmes, plus il y a des cas où un problème a plusieurs solutions. Dans ce cas,
        lève une exception.
        """
        cote = self.__cote
        grille_solution = Grille(cote)
        grille_des_possibles = np.empty((cote, cote), dtype=list)  # chaque case contient la liste des valeurs possibles

        # retire des possibles les nombres trop grands par rapport aux valeurs indiquées dans les marges
        for ran in range(cote):
            for col in range(cote):
                grille_des_possibles[ran, col] = [i for i in [p for p in range(1, cote + 1)]
                                                  if i <= cote - self["OUEST"][ran] + col + 1
                                                  and i <= 2 * cote - self["EST"][ran] - col
                                                  and i <= cote - self["NORD"][col] + ran + 1
                                                  and i <= 2 * cote - self["SUD"][col] - ran]

        resolu = False
        identique = 0  # indique depuis combien d'itérations sur toute la grille, cette dernière n'a pas été modifiée

        while not resolu:
            for ran in range(cote):
                for col in range(cote):
                    if grille_solution[ran, col] == 0:
                        # retire des possibles de la case les nombres déjà présents dans la même colonne ou la même
                        # ligne
                        possibles = [i for i in grille_des_possibles[ran, col]
                                     if i not in grille_solution[:, col]
                                     and i not in grille_solution[ran, :]]
                        if possibles != grille_des_possibles[ran, col]:
                            grille_des_possibles[ran, col] = possibles.copy()
                            identique = 0
                        # si un nombre des possibles de la case n'apparaît dans aucun des autres possibles de la
                        # même rangée ou dans aucun des possibles de la même colonne, il doit être mis dans la case
                        nombre_isole = [i for i in grille_des_possibles[ran, col]
                                        if
                                        [j for possible in grille_des_possibles[ran, :] for j in possible].count(i) == 1
                                        or
                                        [j for possible in grille_des_possibles[:, col] for j in possible].count(i) == 1
                                        ]
                        if len(nombre_isole) > 0:
                            grille_solution[ran, col] = nombre_isole[0]
                            grille_des_possibles[ran, col] = [nombre_isole[0]]
                            identique = 0
                        # s'il n'y a plus qu'un nombre possible pour la case, le met dans la grille résolue
                        elif len(grille_des_possibles[ran, col]) == 1:
                            grille_solution[ran, col] = grille_des_possibles[ran, col][0]
                            identique = 0
                        # si on ne peut voir qu'un sommet depuis un des points de vue, il s'agit forcément du plus grand
                        elif (ran == 0 and self["NORD"][col] == 1) or (ran == cote - 1 and self["SUD"][col] == 1) \
                                or (col == 0 and self["OUEST"][ran] == 1) or (
                                col == cote - 1 and self["EST"][ran] == 1):
                            grille_solution[ran, col] = cote
                            grille_des_possibles[ran, col] = [cote]
                            identique = 0
                        # si la boucle a déjà été parcourue sans être modifiée, on brute force en testant pour la case
                        # toutes les possibilités et en enlevant les nombres impossibles
                        elif identique == 2:
                            # on teste, pour chaque nombre possible de la case, si, en mettant ce nombre dans la case,
                            # on arrive, pour toutes les configurations de grille, à un nombre de sommets impossibles
                            for nombre in grille_des_possibles[ran, col]:
                                liste = []
                                sommets_visibles = 0
                                grille_copie = copy.deepcopy(grille_solution)
                                # affecte le nombre à la case dans la copie de la grille
                                grille_copie[ran, col] = nombre
                                # pour chaque position, teste la valeur du nombre dans la grille
                                for position in POSITIONS:
                                    if position == "NORD":
                                        liste = grille_copie[:, col].tolist()
                                        sommets_visibles = self["NORD"][col]
                                    elif position == "SUD":
                                        liste = grille_copie[:, col].tolist()
                                        liste.reverse()
                                        sommets_visibles = self["SUD"][col]
                                    elif position == "OUEST":
                                        liste = grille_copie[ran, :].tolist()
                                        sommets_visibles = self["OUEST"][ran]
                                    elif position == "EST":
                                        liste = grille_copie[ran, :].tolist()
                                        liste.reverse()
                                        sommets_visibles = self["EST"][ran]
                                    if sommets_visibles != 0 and \
                                            sommets_visibles not in utils.get_nombres_sommets_visibles_possibles(liste):
                                        grille_des_possibles[ran, col].remove(nombre)
                                        identique = 0
                                        # TODO: tester si le programme est plus rapide sans ce break
                                        break
            # si on a fait 2 itérations de la grille (on a brute forcé), il n'y a pas de solution unique
            if identique == 2:
                raise Exception("Ce problème n'a pas de solution unique")

            identique += 1
            # s'il n'y a plus de zéros dans la grille solution, elle est résolue
            if 0 not in grille_solution:
                resolu = True

        return grille_solution

    def get_problemes_moins_donnees(self):
        """
        Teste d'enlever chaque combinaison de valeurs du problème et retourne la liste de tous les problèmes qui peuvent
        être résolus avec ces valeurs en moins
        """
        problemes = []
        liste_pdv = self.get_liste_pdv()
        liste_impossibles = []
        # boucle sur le nombre de zéros présents dans le problème (lorsque ce nombre vaut zéro, le problème est
        # identique à self)
        for nb_zeros in range(len(liste_pdv)):
            # boucle sur toutes les combinaisons possibles d'indices de longueur valant le nombre de zéros
            for indices_zeros in itertools.combinations(range(len(liste_pdv)), nb_zeros):
                impossible_bool = False
                # si la liste des indices des zéros contient un des sets de nombres qui, s'ils sont nuls en même temps,
                # rendent le problème impossible, alors la liste rend le problème impossible.
                for set_impossible in liste_impossibles:
                    if set_impossible.issubset(set(indices_zeros)):
                        impossible_bool = True
                        break
                # si le problème n'est pas impossible, le résout
                if not impossible_bool:
                    probleme = copy.deepcopy(self)
                    # place, sur la copie de self, des 0 aux endroits de la combinaison d'indices "indices_zeros"
                    for indice in indices_zeros:
                        probleme[indice] = 0
                    # si le problème peut être résolu, l'ajoute à la liste des problèmes
                    try:
                        probleme.resoudre()
                        problemes.append(probleme)
                    # s'il ne peut pas être résolu, ajoute le set des indices où le problème vaut zéro à la liste des
                    # sets imporssibles
                    except Exception:
                        liste_impossibles.append(set(indices_zeros))

        return problemes

    def get_problemes_semblables(self):
        """
        Retourne la liste des problèmes identiques à une rotation, où à une symétrie près.
        """
        problemes_semblables = []
        cote = self.__cote

        for i in range(2):
            probleme = copy.deepcopy(self)
            # applique une symétrie d'axe verticale
            if i == 1:
                probleme["NORD"].reverse()
                probleme["SUD"].reverse()
                probleme["EST"], probleme["OUEST"] = probleme["OUEST"], probleme["EST"]

            liste_nb_sommets = probleme["NORD"] + probleme["EST"] + probleme["SUD"][::-1] + probleme["OUEST"][::-1]

            # applique des rotations de 0, 90, 180 et 270 degrés au problème
            for j in range(4):
                new_indice = j * cote
                for k in range(new_indice):
                    liste_nb_sommets.insert(0, liste_nb_sommets.pop())
                probleme["NORD"] = liste_nb_sommets[0: cote]
                probleme["EST"] = liste_nb_sommets[cote: 2 * cote]
                probleme["SUD"] = liste_nb_sommets[2 * cote: 3 * cote]
                probleme["OUEST"] = liste_nb_sommets[3 * cote: 4 * cote]

                problemes_semblables.append(probleme)

        return problemes_semblables

    def get_liste_pdv(self):
        """
        Retourne la liste des points de vue du problème dans le sens horaire : NORD, EST, SUD, OUEST
        """
        points_de_vue = []
        for pos in POSITIONS:
            points_de_vue.extend(self[pos])
        return points_de_vue

    def get_moyenne(self):
        """
        Retourne la moyenne des valeurs du problème
        """
        return statistics.mean([self[pos][i] for pos in POSITIONS for i in range(self.__cote)])

    def __eq__(self, other):
        for pos in POSITIONS:
            if self[pos] != other[pos]:
                return False
        return True

    def __getitem__(self, index):
        # si l'index est un string qui indique la position, renvoie la liste des valeurs des sommets visibles de la
        # position
        if isinstance(index, str):
            return self.__points_de_vue[index]
        # si l'index est un int, renvoie la valeur de la liste des points de vue à l'indice en entrée
        else:
            # (index // cote) permet de déterminer dans quel quartile se trouve l'indice en paramètre et donc position
            # correspondante
            pos = POSITIONS[index // self.__cote]
            # index % cote donne l'indice sur la liste des points de vue de la position
            return self.__points_de_vue[pos][index % self.__cote]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.__points_de_vue[key] = value
        else:
            pos = POSITIONS[key // self.__cote]
            self.__points_de_vue[pos][key % self.__cote] = value

    def __str__(self):
        str_probleme = ""
        for position in POSITIONS:
            str_probleme += position + " : "
            for i in range(self.__cote):
                str_probleme += str(self[position][i]) + " "
            str_probleme += "\n"

        return str_probleme
