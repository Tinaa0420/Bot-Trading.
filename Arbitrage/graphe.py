import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data = pd.read_csv('trading_data.csv', parse_dates=['Date'], index_col='Date')

daily_data = data.groupby(data.index.date)['Profit_last_tx'].sum()

# Créer une nouvelle figure et un axe pour le graphique
fig, ax = plt.subplots(figsize=(10, 6))

# Tracer les données quotidiennes (index : dates, valeurs : somme des profits_last_tx) avec des marqueurs ronds et une ligne continue
ax.plot(daily_data.index, daily_data.values, marker='o', linestyle='-')

# Configurer l'axe des x pour afficher les dates correctement avec le format 'jour-mois'
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

# Définir les emplacements des étiquettes de l'axe des x avec un intervalle d'un jour
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

# Faire pivoter les étiquettes de l'axe des x de 45 degrés pour une meilleure lisibilité
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Profit')
plt.title('Profit par jour')
plt.grid(True)

plt.show()
