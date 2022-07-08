from jeu_de_donnees import remplir_jeu_donnees
import dao

problemes = dao.get_problemes_possibles(cote=4)

probleme = problemes[0]

problemes_moins_donnees = probleme.get_problemes_moins_donnees()

for pb in problemes_moins_donnees:
    print(str(pb))
