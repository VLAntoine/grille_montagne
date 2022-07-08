import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

file = 'grille_montagne_6.csv'

data = pd.read_csv(file)

df = data[[col for col in data.columns.values if col != 'faisabilite']]

scaling = StandardScaler()

scaling.fit(df)
Scaled_data = scaling.transform(df)

principal = PCA(n_components=3)
principal.fit(Scaled_data)
x = principal.transform(Scaled_data)

print(x.shape)

print(principal.components_)

faisabilites = (data['faisabilite'].values == 'possible').tolist()

print(principal.explained_variance_ratio_)

plt.figure(figsize=(10, 10))
plt.scatter(x[:, 0], x[:, 1], c=faisabilites, cmap='plasma')
plt.xlabel('pc1')
plt.ylabel('pc2')


fig = plt.figure(figsize=(10, 10))

axis = fig.add_subplot(111, projection='3d')

axis.scatter(x[:, 0], x[:, 1], x[:, 2], c=faisabilites, cmap='plasma')
axis.set_xlabel("PC1", fontsize=10)
axis.set_ylabel("PC2", fontsize=10)
axis.set_zlabel("PC3", fontsize=10)

plt.show()

