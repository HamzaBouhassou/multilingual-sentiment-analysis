import json
import matplotlib.pyplot as plt

# Charger les résultats depuis le fichier JSON
with open('classification_results1.json', 'r', encoding='utf-8') as file:
    results = json.load(file)

# Extraire les noms des classifieurs et leurs précisions
classifier_names = list(results.keys())
accuracies = [results[name]['accuracy'] for name in classifier_names]

# Créer le bar chart
plt.figure(figsize=(10, 6))
plt.bar(classifier_names, accuracies, color='skyblue')
plt.xlabel('Classifieurs')
plt.ylabel('Précision')
plt.title('Précision des différents classifieurs')
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid(axis='y')

# Sauvegarder le diagramme
plt.savefig('classification_results_bar_chart.png')
plt.show()
