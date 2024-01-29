import pandas as pd
import matplotlib.pyplot as plt

# Charger les données du fichier CSV
data = pd.read_csv('trading_data.csv')

# Créer un graphique avec les profits cumulés
plt.plot(data['Time'], data['Profit'], label='Profit', marker='o')

# Ajouter des titres et des étiquettes
plt.title("Evolution du profit au cours du temps")
plt.xlabel("Heure")
plt.ylabel("Profit (USDT)")

# Afficher la légende
plt.legend()

# Ajuster les étiquettes de l'axe des x pour éviter qu'elles se chevauchent
plt.xticks(rotation=45)

# Afficher le graphique
plt.show()