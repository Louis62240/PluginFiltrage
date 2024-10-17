import json
import requests
from PIL import Image
from io import BytesIO
import torch
from torchvision.models import detection
from torchvision.transforms import functional as F
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from typing import Dict, List, Any

# Liste des noms des classes COCO
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter',
    'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
    'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle',
    'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
    'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
    'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Utilisation du modèle "facebook/dino-vits16" pour des tâches générales de classification d'images
model_name = "facebook/dino-vits16"
extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

def is_image_nsfw(image: Image.Image) -> bool:
    """
    Cette fonction utilise un modèle pour vérifier si l'image contient de la nudité ou du contenu explicite.
    """
    try:
        # Préparer l'image pour le modèle
        inputs = extractor(images=image, return_tensors="pt")
        
        # Prédire le contenu
        with torch.no_grad():
            logits = model(**inputs).logits
        
        # Extraire la classe avec la probabilité la plus élevée
        probabilities = torch.softmax(logits, dim=1)[0]
        nsfw_prob = probabilities[1].item()  # La probabilité que l'image soit NSFW (classe 1)

        print(f"Probabilité de contenu NSFW : {nsfw_prob:.2f}")

        # Seuil de probabilité pour considérer une image comme NSFW (ici, 0.7 ou 70%)
        return nsfw_prob >= 0.7
    except Exception as e:
        print(f"Erreur lors de la détection NSFW : {e}")
        return False

def is_image_appropriate(url: str, inappropriate_classes: list = None, confidence_threshold: float = 0.5) -> bool:
    # Définit les classes par défaut à vérifier si elles ne sont pas spécifiées
    if inappropriate_classes is None:
        inappropriate_classes = ['person', 'wine glass', 'bottle', 'gun', 'knife']

    try:
        # Télécharger l'image avec gestion des erreurs
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Erreur lors du téléchargement de l'image: statut {response.status_code}")
            return False
        
        img = Image.open(BytesIO(response.content)).convert("RGB")
        
        # Vérifier si l'image est potentiellement NSFW (nudité ou contenu explicite)
        if is_image_nsfw(img):
            print("L'image contient du contenu NSFW (nudité ou autre).")
            return False

        # Charger le modèle pré-entraîné pour la détection d'objets
        model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
        model.eval()
        
        # Préparer l'image pour le modèle
        img_tensor = F.to_tensor(img).unsqueeze(0)
        
        # Faire la prédiction
        with torch.no_grad():
            prediction = model(img_tensor)
        
        # Parcourir les prédictions et vérifier la pertinence
        for i, label in enumerate(prediction[0]['labels']):
            class_name = COCO_INSTANCE_CATEGORY_NAMES[label]
            confidence = prediction[0]['scores'][i]
            
            # Si la classe est inappropriée et que la confiance dépasse le seuil
            if class_name in inappropriate_classes and confidence >= confidence_threshold:
                print(f"Objet inapproprié détecté : {class_name} avec une confiance de {confidence:.2f}")
                return False
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return False
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

def contains_profanity(text: str) -> bool:
    # Liste simple de mots inappropriés (à étendre selon les besoins)
    profanity_list = [
        # Français (variantes et mots courants sur les réseaux sociaux)
        "merde", "putain", "connard", "salope", "enculé", "fils de pute", "bordel", "bite", "couille", "nique", "niquer", "enfoiré", "batard", "pédé", "chier", "dégueulasse", "grognasse", 
        "fdp", "tg", "ntm", "ptn", "zgeg", "pd", "racli", "raclure", "trouduc", "baltringue", "abruti", "gueule", "pétasse", "clochard", "charogne", "foutre", "cramé", "michto",
        
        # Anglais (variantes et mots couramment utilisés sur Twitter)
        "fuck", "shit", "bitch", "asshole", "cunt", "dick", "pussy", "bastard", "slut", "whore", "fucker", "motherfucker", "cock", "jerk", "crap", "douchebag", "nigger", "nigga", 
        "twat", "prick", "cum", "suck", "gaylord", "fgt", "lmfao", "lmao", "wtf", "stfu", "gtfo", "ass", "bs", "butthurt", "dumbass", "dipshit", "retard", "idiot", "moron", "loser", 
        "skank", "scumbag", "hoe", "fck", "fckn", "fk", "kys", "dyke", "simp", "boomer", "ratchet", "thot", "trash", "karen", "bussy", "thicc", "creep", "twat", "f***", "fuq", "goddamn", 
        "wanker", "bollocks", "arsehole", "nonce", "tosser", "bloody", "wank", "bugger", "knobhead", "shag", "pillock", "scrub", "troll", "noob", "cringe", "soyboy", 
        
        # Espagnol (variantes et termes courants)
        "mierda", "puta", "gilipollas", "pendejo", "cabron", "chingar", "coño", "joder", "verga", "carajo", "culero", "pajero", "puto", "zorra", "maricón", "pito", "madre", 
        "chingado", "culiao", "huevon", "concha", "conchatumadre", "putazo", "gordo", "guey", "malparido", "culillo", "hijueputa",
        
        # Allemand (termes courants et insultes en ligne)
        "scheisse", "arschloch", "fick", "hure", "wichser", "dummkopf", "fotze", "schlampe", "hurensohn", "verdammt", "arsch", "schwein", "trottel", "idiot", "blödmann", "spasti",
        
        # Italien
        "cazzo", "stronzo", "merda", "puttana", "bastardo", "vaffanculo", "porca", "culo", "troia", "figa", "coglione", "frocio", "ricchione", "testa di cazzo", "cornuto", 
        "figlio di puttana", "rompicoglioni", "stupido", "deficiente",
        
        # Portugais
        "merda", "puta", "caralho", "foder", "porra", "filho da puta", "vai se foder", "bosta", "cu", "otário", "boceta", "xoxota", "pinto", "fodido", "cuzão", "arrombado", "burro", 
        "viadinho", "putona", "babaca", "babacão", "desgraçado",
        
        # Arabe (translittération)
        "sharmouta", "kos omak", "ibn el kalb", "khara", "zamel", "3ars", "fuck", "siba", "kos omak", "kos omak", "kos omok", "kos",
        
        # Polonais
        "kurwa", "suka", "jebac", "chuj", "zajebisty", "spierdalaj", "pizda", "ciota", "pierdol", "dziwka",
        
        # Russe
        "suka", "blyat", "ebat", "mudak", "pidor", "govno", "zhopa", "dolboeb", "chmo", "blyad", "dermo", "mraz",
        
        # Hindi
        "mamaa ka bhosda", "chutiya", "bhosdike", "madarchod", "behenchod", "gandu", "kamina", "jhant", "bhenchod", "launde", "lavde",
        
        # Coréen (romanisé)
        "ssi-bal", "gaesaekki", "nom", "nyeon", "gae", "ssibal", "ddong", "dokkaebi",
        
        # Japonais (romanisé)
        "baka", "kusottare", "yarou", "temee", "aho", "shine", "kuso", "chikushou", "hentai",
        
        # Indonésien
        "bajingan", "bangsat", "anjing", "goblok", "kampret", "perek", "memek", "tai", "bego",
        
        # Abréviations populaires et leet speak
        "wtf", "stfu", "lmao", "lmfao", "omg", "gtfo", "fml", "mf", "f.u.", "fk", "fck", "b.s.", "bs", "dickhead", "turd", "biatch", "buttface", 
        "f*ck", "sh*t", "b!tch", "a$$", "f@ck", "c*nt", "n*gga", "f***", "b****", "fckn", "fkkn", "b*tch", "p*ssy", "f@ggot", "n1gga", "n!gga"
    ]

    return any(word in text.lower() for word in profanity_list)

def process_tweets(tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [verify_tweet(tweet) for tweet in tweets]

def process_json_file(file_path: str) -> None:
    # Charger les tweets depuis un fichier JSON passé en paramètre
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tweets = json.load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' n'a pas été trouvé.")
        return
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier '{file_path}' n'est pas un JSON valide.")
        return

    # Traiter les tweets
    verified_tweets = process_tweets(tweets)

    # Sauvegarder les tweets vérifiés dans un nouveau fichier JSON
    output_file = 'verified_tweets.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(verified_tweets, file, indent=2, ensure_ascii=False)
        print(f"Vérification des tweets terminée. Résultats sauvegardés dans '{output_file}'.")
    except IOError:
        print(f"Erreur : Impossible d'écrire dans le fichier '{output_file}'.")