import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
import model
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

file = 'grille_montagne_5.csv'

data = pd.read_csv(file)

df = data[[col for col in data.columns.values if col != 'faisabilite']]

X_train = df.values
y_train = (data['faisabilite'].values == 'possible').astype(int).tolist()

mlp = MLPClassifier(hidden_layer_sizes=(20, 20, 20), max_iter=1000)
mlp.fit(X_train, y_train)

X_test = []
y_test = []

for i in range(100):

    grille = model.Grille()
    grille.remplir()

    probleme = model.Probleme(grille=grille)

    X_test.append([])

    for pos in model.POSITIONS:
        for ind in range(model.COTE):
            X_test[-1].append(probleme[pos][ind])

    try:
        solution = probleme.resoudre()
        y_test.append(1)
    except Exception as e:
        y_test.append(0)

y_pred = mlp.predict(X_test)

precision = accuracy_score(y_pred, y_test)

contingences = confusion_matrix(y_test, y_pred)

print(str(contingences))
