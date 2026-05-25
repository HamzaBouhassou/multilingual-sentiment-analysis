import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Charger le fichier JSON
input_file_path = 'filtered3_comments.json'

with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Calculer les pourcentages positifs et négatifs par langue
language_stats = defaultdict(lambda: {'positive': 0, 'negative': 0})
video_language_stats = defaultdict(lambda: defaultdict(lambda: {'positive': 0, 'negative': 0}))

for comment in data:
    video_id = comment.get('video_id', None)
    language = comment.get('language', None)
    label = comment.get('label', None)

    if video_id is not None and language is not None and label is not None:
        if label == 1:
            language_stats[language]['positive'] += 1
            video_language_stats[video_id][language]['positive'] += 1
        elif label == 0:
            language_stats[language]['negative'] += 1
            video_language_stats[video_id][language]['negative'] += 1

# Préparer les données pour le graphique global par langue
languages = list(language_stats.keys())
positive_counts_global = [language_stats[lang]['positive'] for lang in languages]
negative_counts_global = [language_stats[lang]['negative'] for lang in languages]

# Préparer les données pour le graphique par vidéo par langue
video_ids = list(video_language_stats.keys())
language_counts_video = defaultdict(lambda: defaultdict(list))

for video_id, stats in video_language_stats.items():
    for language in languages:
        language_counts_video[video_id][language] = [
            stats[language]['positive'],
            stats[language]['negative']
        ]

# Créer le graphique à barres groupées pour les comptages globaux par langue
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

bar_width = 0.35  # Largeur des barres
index = np.arange(len(languages))  # Indices des positions des barres

bar1_global = ax1.bar(index, positive_counts_global, bar_width, label='Positive', color='green', alpha=0.6)
bar2_global = ax1.bar(index + bar_width, negative_counts_global, bar_width, label='Negative', color='red', alpha=0.6)

ax1.set_xlabel('Languages')
ax1.set_ylabel('Counts')
ax1.set_title('Global Positive and Negative Sentiment Counts by Language')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels(languages)
ax1.legend()

# Ajouter les valeurs au-dessus des barres (globales)
def autolabel_global(bars, ax):
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Décalage vertical
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel_global(bar1_global, ax1)
autolabel_global(bar2_global, ax1)

# Créer le graphique à barres groupées pour les comptages par vidéo par langue
video_index = np.arange(len(video_ids))  # Indices des positions des barres pour les vidéos
video_bar_width = 0.2  # Largeur des barres pour chaque vidéo

for i, language in enumerate(languages):
    positive_counts_video = [language_counts_video[video_id][language][0] for video_id in video_ids]
    negative_counts_video = [language_counts_video[video_id][language][1] for video_id in video_ids]

    ax2.bar(video_index + i * video_bar_width, positive_counts_video, video_bar_width,
            label=f'{language} Positive', alpha=0.6)
    ax2.bar(video_index + i * video_bar_width, negative_counts_video, video_bar_width,
            bottom=positive_counts_video, label=f'{language} Negative', alpha=0.6)

ax2.set_xlabel('Video IDs')
ax2.set_ylabel('Counts')
ax2.set_title('Positive and Negative Sentiment Counts by Video and Language')
ax2.set_xticks(video_index + len(languages) * video_bar_width / 2)
ax2.set_xticklabels(video_ids)
ax2.legend()

plt.tight_layout()
plt.show()
