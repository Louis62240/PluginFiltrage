import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from tweet_scraper_v2 import scrape_tweets_from_search
from verificationTweet import process_json_file, process_tweets

app = Flask(__name__)
CORS(app)

# Fonction pour charger les tweets existants depuis le fichier JSON
def load_existing_tweets(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON dans le fichier {filename}.")
            return []  # Fichier vide ou corrompu
        except IOError as e:
            print(f"Erreur d'entrée/sortie : {e}")
            return []
    else:
        print(f"Le fichier {filename} n'existe pas.")
        return []
    
# Nouvelle fonction pour effacer le contenu du fichier JSON
def clear_tweets_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)  # Sauvegarder une liste vide

# Fonction pour sauvegarder des tweets dans le fichier JSON
def save_tweets_to_json(tweets, filename):
    existing_tweets = load_existing_tweets(filename)
    
    # Ajouter les nouveaux tweets aux anciens
    updated_tweets = existing_tweets + tweets

    # Sauvegarder tous les tweets (anciens + nouveaux)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(updated_tweets, f, ensure_ascii=False, indent=4)
# Nouvelle route pour effacer le fichier tweets.json
@app.route('/api/clear_tweets', methods=['POST'])
def clear_tweets():
    try:
        # Chemin relatif vers le fichier tweets.json dans le projet Vue.js
        filename = os.path.join('TwitterProtectVue', 'src', 'assets', 'json', 'tweets.json')

        # Effacer le contenu du fichier tweets.json
        clear_tweets_file(filename)

        return jsonify({"message": "Les tweets ont été effacés avec succès."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tweets', methods=['POST'])
def get_tweets():
    try:
        # Récupérer les données de la requête
        data = request.json
        query = data.get('query', '')
        tweet_count = data.get('tweet_count', 10)  # nombre par défaut de tweets

        # Vérifier que la requête contient un query
        if not query:
            return jsonify({"error": "Le paramètre 'query' est requis."}), 400

        # Scraper les tweets
        tweets = scrape_tweets_from_search(query, tweet_count)

        if not tweets:
            return jsonify({"message": f"Aucun tweet trouvé pour le mot-clé : {query}."}), 404

        # Processus de vérification des tweets
        verified_tweets = process_tweets(tweets)

        # Chemin relatif vers le fichier tweets.json dans le projet Vue.js
        filename = os.path.join('TwitterProtectVue', 'src', 'assets', 'json', 'tweets.json')

        # Sauvegarder les tweets vérifiés dans le fichier JSON
        save_tweets_to_json(verified_tweets, filename)

        # Retourner les tweets vérifiés sous forme de JSON
        return jsonify(verified_tweets), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
