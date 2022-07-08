import csv
import model


def get_problemes_possibles(cote: int):
    fichier = 'grille_montagne_' + str(cote) + '.csv'

    with open(fichier, 'r', newline='') as csvfile:
        fieldnames = ['faisabilite']
        fieldnames.extend([pos + str(i) for pos in model.POSITIONS for i in range(cote)])
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        possibles = [row for row in reader if row['faisabilite'] == 'possible']

        problemes = []

        for possible in possibles:
            probleme = model.Probleme(cote=cote)
            possible.pop("faisabilite")
            for key in possible.keys():
                position = key[:-1]
                indice = int(key[-1])
                probleme[position][indice] = int(possible[key])
            problemes.append(probleme)

        return problemes
