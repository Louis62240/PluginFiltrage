import json
import re
from typing import List, Dict, Any
import requests
from PIL import Image
from io import BytesIO
import torch
from torchvision.models import detection
from torchvision.transforms import functional as F

def contains_profanity(text: str) -> bool:
    # Liste simple de mots inappropriés (à étendre selon les besoins)
    profanity_list = ["merde", "putain", "connard", "salope", "fuck", "bitch", "ass"]
    return any(word in text.lower() for word in profanity_list)

def is_image_appropriate(url: str) -> bool:
    try:
        # Télécharger l'image
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        
        # Charger le modèle pré-entraîné
        model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
        model.eval()
        
        # Préparer l'image pour le modèle
        img_tensor = F.to_tensor(img).unsqueeze(0)
        
        # Faire la prédiction
        with torch.no_grad():
            prediction = model(img_tensor)
        
        # Liste des classes potentiellement inappropriées
        inappropriate_classes = [
            'person', 'wine glass', 'bottle', 'gun', 'knife'
        ]
        
        # Vérifier les prédictions
        for element in prediction[0]['labels']:
            if detection.coco_names[element] in inappropriate_classes:
                return False
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'image: {e}")
        return False

def verify_tweet(tweet: Dict[str, Any]) -> Dict[str, Any]:
    # Vérifier le texte pour les insultes
    if contains_profanity(tweet['text']):
        tweet['isCorrect'] = False
        return tweet

    # Vérifier les images
    for image_url in tweet.get('tweet_images', []):
        if not is_image_appropriate(image_url):
            tweet['isCorrect'] = False
            return tweet

    # Si aucun problème n'est trouvé, le tweet est considéré comme correct
    tweet['isCorrect'] = True
    return tweet

def process_tweets(tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [verify_tweet(tweet) for tweet in tweets]

def main():
    # Charger les tweets depuis un fichier JSON
    try:
        with open('tweets.json', 'r') as file:
            tweets = json.load(file)
    except FileNotFoundError:
        print("Erreur : Le fichier 'tweets.json' n'a pas été trouvé.")
        return
    except json.JSONDecodeError:
        print("Erreur : Le fichier 'tweets.json' n'est pas un JSON valide.")
        return

    # Traiter les tweets
    verified_tweets = process_tweets(tweets)

    # Sauvegarder les tweets vérifiés dans un nouveau fichier JSON
    try:
        with open('verified_tweets.json', 'w') as file:
            json.dump(verified_tweets, file, indent=2)
        print("Vérification des tweets terminée. Résultats sauvegardés dans 'verified_tweets.json'.")
    except IOError:
        print("Erreur : Impossible d'écrire dans le fichier 'verified_tweets.json'.")

if __name__ == "__main__":
    main()