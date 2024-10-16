# main.py

# Importer la fonction main depuis le fichier tweet_scraper_v2.py
from tweet_scraper_v2 import main

if __name__ == "__main__":
    # Définir les paramètres ici
    query = "python"
    tweet_count = 10
    
    # Appeler la fonction main en passant les paramètres
    main(query, tweet_count)
