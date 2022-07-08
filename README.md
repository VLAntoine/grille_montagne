# Grille Montagne

Ce programme vise à produire des grilles réalisables de grilles-montagnes (comme j'ai surnommé ce jeu). Ce jeu, plus communément appelé jeu du gratte-ciel, est un jeu mathématique de logique (à la manière du sudoku) qui se joue sur des grilles carrées de 3x3 à 8x8.

## Règles du jeu

Le but est de remplir une grille qui se présente sous la forme suivante :

   1   2   3   2
|1|   |   |   |   |3
|-|---|---|---|---|
|2|   |   |   |   |3
|2|   |   |   |   |1
|3|   |   |   |   |2
   3   2   1   2

Dans l'exemple ci-dessus, on doit y inscrire des nombres de 1 à 4. Pour cela on doit respecter quelques règles :
- chaque ligne et chaque colonne ne peuvent qu'une seule fois chaque nombre ;
- les numéros sur les côtés indiquent le nombre de sommets (ou gratte-ciels) visibles depuis ce point de vue. Par exemple, dans la suite 2,1,3,4, il y a 3 sommets visibles : 2, 3 et 4. Le 1, caché par le 2, n'est pas visibles.

La grille précédente a donc pour solution :

   1   2   3   2
1| 4 | 3 | 1 | 2 |3
 |---|---|---|---|
2| 2 | 4 | 3 | 1 |3
2| 3 | 1 | 2 | 4 |1
3| 1 | 2 | 4 | 3 |2
   3   2   1   2
   
Il est possible de retirer des numéros pour augmenter la difficulté. Par exemple, la grille ci-dessus peut être retrouvée avec seulement les informations suivantes :

      2   3    
| 4 | 3 | 1 | 2 |3
|---|---|---|---|
| 2 | 4 | 3 | 1 |
| 3 | 1 | 2 | 4 |1
| 1 | 2 | 4 | 3 |
   
## Fonctionnement du code et difficultés

L'objectif est de générer des problèmes réalisables. La méthode employée consiste à générer une grille, à en trouver le problème correspondant et à tester sa résolution. On enlève ensuite des éléments petit à petit, en testant à chaque fois si le problème est réalisable.
En faisant ainsi, on est vite confronté à une difficulté : les problèmes, ainsi générés, peuvent retourner de multiples solutions : ils ne sont donc pas faisables (le code retourne alors une erreur).

Lorsque c'est une grille 3x3 ou 4x4, cela ne pose pas de problème étant donné que les problèmes réalisables sont en majorité. Mais plus on monte, moins c'est le cas. Au bout de 13000 grilles testées, seules 8 étaient faisables. Comme l'algorithme de résolution est lent (on est vite amené à tester toutes les combinaisons possibles), cela représente un temps déraisonnables pour générer si peu de grilles.
À partir de là j'ai testé des méthodes de classification sur les données du problème (clustering, k-means, régressions logistiques et linéaires, réseaux neuronaux) pour déterminer a priori si les problèmes étaient faisables ou non. Ce ne fut pas un succès : 70% était bien classées, mais avec beaucoup de faux positifs.

Une fois que l'on a récupéré les problèmes faisables, on teste pour chacune des combinaisons de valeurs de chaque problème si, en les retirant, le problème reste faisable. Encore une fois les temps de calculs sont très longs. 
Néanmoins, cela m'a permis de me rendre compte que, pour un problème réalisable, on trouve de nombreux sous-problèmes, dont certains avec très peu d'informations. Cela donne envie de tester une autre approche.

## Améliorations

- On pourrait tenter une approche différente : partir des problèmes vides et ajouter petit à petit les numéros. Dès qu'on trouve un problème qui fonctionne, on ne cherche pas plus loin (les problèmes avec plus de données seront faciles à déterminer avec la grille solution). On retire également de la recherche tous les problèmes semblables (identiques par symétrie et rotation).

- Améliorer les algorithmes de recherche de solutions : il brute force très rapidement. L'ajout de certaines conditions logiques leur permettraient sûrement d'être plus rapide.

- Améliorer les algorithmes de génération de grilles : 1 grille sur 5 générée par l'algorithme retourne une exception. On peut faire tomber ce résultat à 0.

- Faire une couche DAO propre avec une vraie base de données (pas des fichiers CSV qui se baladent)

- Faire une interface graphique correcte (sous Qt par exemple)
