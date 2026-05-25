import json
from textblob import TextBlob  # Utilisation de TextBlob pour l'analyse de sentiment
from langdetect import detect, LangDetectException  # Importer langdetect

def labelise_commentaire(commentaire):
    # Fonction pour labelliser le commentaire en fonction de son sentiment global
    analyse_sentiment = TextBlob(commentaire)
    polarite = analyse_sentiment.sentiment.polarity
    
    if polarite > 0.2:
        return 1  # positif
    elif polarite < -0.2:
        return 0  # négatif
    else:
        return -1  # neutre

def filtrer_et_labelliser(fichier_entree, fichier_sortie):
    with open(fichier_entree, 'r', encoding='utf-8') as f_entree:
        data = json.load(f_entree)
    
    frang_comments = []
    
    for commentaire in data:
        if 'filtered_comment' in commentaire:
            texte_commentaire = commentaire['filtered_comment']
            # Vérifier la langue du commentaire
            if est_francais(texte_commentaire) or est_anglais(texte_commentaire):
                # Labelliser le commentaire
                label = labelise_commentaire(texte_commentaire)
                if label != -1:  # Ne pas inclure les commentaires neutres
                    frang_comments.append({
                        "video_id": commentaire["video_id"],
                        "original_comment": commentaire["original_comment"],
                        "filtered_comment": commentaire["filtered_comment"],
                        "label": label
                    })
    
    # Écrire les commentaires dans le fichier frang_comments.json
    with open(fichier_sortie, 'w', encoding='utf-8') as f_sortie:
        json.dump(frang_comments, f_sortie, ensure_ascii=False, indent=4)

def est_francais(texte):
    # Fonction pour déterminer si le texte est en français
    try:
        langue = detect(texte)
        return langue == 'fr'
    except LangDetectException:
        return False

def est_anglais(texte):
    # Fonction pour déterminer si le texte est en anglais
    try:
        langue = detect(texte)
        return langue == 'en'
    except LangDetectException:
        return False

# Exemple d'utilisation du script
if __name__ == "__main__":
    fichier_entree = 'filtered2_comments.json'
    fichier_sortie = 'frang1_comments.json'
    
    filtrer_et_labelliser(fichier_entree, fichier_sortie)
