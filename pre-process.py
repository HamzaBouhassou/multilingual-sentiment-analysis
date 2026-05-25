import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Fonction pour nettoyer et filtrer les comment aires
def clean_comment(comment):
    # Supprimer les emojis

    # Supprimer la ponctuation
    comment = re.sub(r'[^\w\s]', '', comment)

    # Supprimer les répétitions de lettres (comme saaaaaaaaalaaaaaaaam -> salam)
    comment = re.sub(r'(.)\1+', r'\1', comment)

    # Supprimer les liens (http://... ou https://...)
    comment = re.sub(r'http\S+', '', comment)

    # Remplacer les balises <br>, <br/>, <br /> par une chaîne vide
    cleaned_text = re.sub(r'<br\s*/?>', '', comment, flags=re.IGNORECASE).replace("br","" )

    return comment.strip()

# Charger les stopwords pour le français et l'arabe
stop_words_fr = set(stopwords.words('french'))
stop_words_ar = set(stopwords.words('arabic'))

# Charger les commentaires depuis le fichier JSON
with open('extracted_comments.json', 'r', encoding='utf-8') as file:
    comments = json.load(file)

filtered_comments = []

# Parcourir chaque commentaire et le nettoyer
for comment in comments:
    if 'comment' in comment:  # Vérifier si la clé 'text' existe dans le commentaire
        cleaned_comment = clean_comment(comment['comment'])
        
        # Tokenization et filtrage des stopwords par langue
        words = word_tokenize(cleaned_comment)
        filtered_words = [word for word in words if word.lower() not in stop_words_fr and word.lower() not in stop_words_ar]

        # Reconstruire le commentaire filtré
        filtered_comment = ' '.join(filtered_words)
        
        # Ajouter le commentaire filtré à la liste
        filtered_comments.append({
            'video_id' : comment['video_id'],
            'original_comment': comment['comment'],
            'filtered_comment': filtered_comment
        })
    else:
        print(f"Commentaire sans 'text' trouvé: {comment}")

# Enregistrer les commentaires filtrés dans un fichier JSON
with open('filtered_comments.json', 'w+', encoding='utf-8') as f:
    json.dump(filtered_comments, f, ensure_ascii=False, indent=4)

print("Filtrage et sauvegarde des commentaires filtrés terminés.")
