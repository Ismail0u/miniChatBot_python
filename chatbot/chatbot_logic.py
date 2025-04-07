import nltk
import random
import string
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔹 Définir un répertoire spécifique pour NLTK
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Spécifier à NLTK d'utiliser ce répertoire
nltk.data.path.append(nltk_data_path)

# Vérifie si 'punkt' est téléchargé, sinon le télécharger dans le répertoire personnalisé
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Téléchargement du tokenizer 'punkt'...")
    nltk.download('punkt', download_dir=nltk_data_path)

# Télécharge 'stopwords' si nécessaire
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Téléchargement des 'stopwords'...")
    nltk.download('stopwords', download_dir=nltk_data_path)

# Afficher les chemins de recherche de NLTK pour confirmer où il cherche les données
print("Chemins de recherche des données NLTK:", nltk.data.path)

class Chatbot:
    def __init__(self, response_file='chatbot_responses.json'):
        # 📂 Obtenir le chemin absolu vers le fichier JSON
        current_dir = os.path.dirname(__file__)
        response_path = os.path.join(current_dir, response_file)

        # 📄 Charger les réponses depuis le fichier JSON
        with open(response_path, 'r', encoding='utf-8') as f:
            self.responses = json.load(f)

        # ⚙️ Préparer les questions pour la vectorisation TF-IDF
        self.vectorizer = TfidfVectorizer()
        self.questions = list(self.responses.keys())
        self.vectorized_questions = self.vectorizer.fit_transform(self.questions)

    def get_response(self, user_input):
        # 🔡 Normaliser l'entrée utilisateur (minuscule, sans ponctuation)
        user_input = user_input.lower()
        user_input = ''.join([c for c in user_input if c not in string.punctuation])

        # 🧠 Essayer de tokeniser, et re-télécharger punkt si besoin
        try:
            tokens = nltk.word_tokenize(user_input)
        except LookupError:
            print("Erreur de tokenisation, téléchargement de 'punkt'...")
            nltk.download('punkt', download_dir=nltk_data_path)
            tokens = nltk.word_tokenize(user_input)

        if not tokens:
            return "Je n'ai pas compris. Peux-tu reformuler ?"

        # 📊 Vectoriser la question utilisateur
        user_vector = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vector, self.vectorized_questions)

        # 🔍 Trouver la meilleure correspondance
        best_match = similarities.argmax()
        score = similarities[0, best_match]

        if score > 0.3:
            return random.choice(self.responses[self.questions[best_match]])
        else:
            return random.choice([
                "Désolé, je ne comprends pas.",
                "Peux-tu reformuler ?",
                "Je ne sais pas répondre à ça."
            ])
