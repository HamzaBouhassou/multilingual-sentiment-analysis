import json
from langdetect import detect, LangDetectException

def filtrer_et_labelliser(fichier_entree, fichier_sortie, stopwords_arabe_path, stopwords_darija_path):
    with open(fichier_entree, 'r', encoding='utf-8') as f_entree:
        data = json.load(f_entree)
    
    darab_comments = []
    
    for commentaire in data:
        if 'filtered_comment' in commentaire:
            texte_commentaire = commentaire['filtered_comment']
            if est_arabe(texte_commentaire) or est_darija(texte_commentaire, stopwords_arabe_path, stopwords_darija_path):
                darab_comments.append({
                    "video_id": commentaire["video_id"],
                    "original_comment": commentaire["original_comment"],
                    "filtered_comment": commentaire["filtered_comment"],
                    "labilise": commentaire.get("labilise")  # Include the manual label
                })
    
    with open(fichier_sortie, 'w', encoding='utf-8') as f_sortie:
        json.dump(darab_comments, f_sortie, ensure_ascii=False, indent=4)

def est_arabe(texte):
    try:
        langue = detect(texte)
        return langue == 'ar'
    except LangDetectException:
        return False

def est_darija(texte, stopwords_arabe_path, stopwords_darija_path):
    try:
        langue = detect(texte)
        if langue == 'ar':
            with open(stopwords_arabe_path, 'r', encoding='utf-8') as f_arabe:
                stopwords_arabe = f_arabe.read().splitlines()
            with open(stopwords_darija_path, 'r', encoding='utf-8') as f_darija:
                stopwords_darija = f_darija.read().splitlines()
            return any(word in texte.split() for word in stopwords_darija) or all(word in texte.split() for word in stopwords_arabe)
    except LangDetectException:
        return False

if __name__ == "__main__":
    fichier_entree = 'filtered_comments.json'
    fichier_sortie = 'darab_comments.json'
    stopwords_arabe_path = r'C:\Users\hamza\OneDrive\Documents\youtube\stopwordsarab.txt'
    stopwords_darija_path = r'C:\Users\hamza\OneDrive\Documents\youtube\stopwords.txt'
    
    filtrer_et_labelliser(fichier_entree, fichier_sortie, stopwords_arabe_path, stopwords_darija_path)

    
    
    
