import json
from transformers import pipeline

# Charger le modèle de détection de toxicité
detoxify = pipeline("text-classification", model="unitary/toxic-bert")

# Fonction pour détecter la toxicité dans les tweets
def check_toxicity(tweets):
    for tweet in tweets:
        result = detoxify(tweet["text"])[0]
        text = "connard"
        result2 = detoxify(text)[0]
        print (result2)
        
        print(f"Tweet: {tweet['text']}")
        print(f"Toxicity Score: {result['score']}, Label: {result['label']}\n")

# Lire le fichier JSON avec l'encodage approprié
with open('tweets.json', 'r', encoding='utf-8') as file:
    tweets = json.load(file)

# Vérification de la toxicité dans les tweets
check_toxicity(tweets)
