import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from langdetect import detect, LangDetectException

# Charger les données
with open('darab_comments.json', 'r', encoding='utf-8') as file:
    comments_data = json.load(file)

# Filtrer les commentaires en arabe et préparer les étiquettes, en excluant les commentaires neutres
arabic_comments = []
arabic_labels = []

for comment in comments_data:
    try:
        if detect(comment['filtered_comment']) == 'ar' and comment['labilise'] is not None and comment['labilise'] != -1:
            arabic_comments.append(comment['filtered_comment'])
            arabic_labels.append(int(comment['labilise']))
    except (LangDetectException, ValueError):
        continue

# Vérifiez si nous avons des commentaires et des labels après le filtrage
if len(arabic_comments) == 0 or len(arabic_labels) == 0:
    raise ValueError("Aucun commentaire arabe valide trouvé avec des labels 0 ou 1.")

# Transformer les données textuelles en vecteurs numériques
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(arabic_comments)
y = arabic_labels

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définir les classifieurs
classifiers = {
    'Logistic Regression': LogisticRegression(),
    'Support Vector Machine': SVC(),
    'Linear Discriminant Analysis': LinearDiscriminantAnalysis(),
    'Quadratic Discriminant Analysis': QuadraticDiscriminantAnalysis(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Decision Trees': DecisionTreeClassifier()
}

# Stocker les résultats dans un dictionnaire
results = {}

# Entraîner et évaluer chaque classifieur
for name, clf in classifiers.items():
    if name in ['Linear Discriminant Analysis', 'Quadratic Discriminant Analysis', 'K-Nearest Neighbors', 'Decision Trees']:
        # Convertir les matrices creuses en matrices denses
        X_train_dense = X_train.toarray()
        X_test_dense = X_test.toarray()
        clf.fit(X_train_dense, y_train)
        y_pred = clf.predict(X_test_dense)
    else:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    results[name] = {
        'accuracy': accuracy,
        'classification_report': report
    }

# Enregistrer les résultats dans un fichier JSON
with open('classification_results_arabic.json', 'w', encoding='utf-8') as result_file:
    json.dump(results, result_file, ensure_ascii=False, indent=4)

print("Les résultats des classifications ont été enregistrés dans 'classification_results_arabic.json'")
