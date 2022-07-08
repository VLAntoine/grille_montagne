import model
import csv


def remplir_jeu_donnees(cote, nb_problemes_faisables):

    fichier = 'grille_montagne_' + str(cote) + '.csv'

    with open(fichier, 'w', newline='') as csvfile:
        fieldnames = ['faisabilite']
        fieldnames.extend([pos + str(i) for pos in model.POSITIONS for i in range(cote)])
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        problemes = []

        i = 0
        info = 0

        while i != nb_problemes_faisables:

            info += 1
            print(info)

            grille = model.Grille(cote)
            grille.remplir()

            probleme = model.Probleme(grille=grille)
            problemes_semblables = probleme.get_problemes_semblables()

            if len([pb for pb in problemes if pb in problemes_semblables]) == 0:
                row = {}
                for pos in model.POSITIONS:
                    for ind in range(cote):
                        row[pos + str(ind)] = probleme[pos][ind]

                try:
                    probleme.resoudre()
                    row['faisabilite'] = 'possible'
                    writer.writerow(row)
                    i += 1
                    print(str(i))
                except Exception as e:
                    row['faisabilite'] = 'impossible'
                    writer.writerow(row)



