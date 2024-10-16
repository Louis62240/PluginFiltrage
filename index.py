# Importer les fonctions du fichier tweet_scraper_v2.py
from tweet_scraper_v2 import scrape_tweets_from_search, save_tweets_to_json

def main():
    query = input("Entrez un thème ou un mot-clé pour rechercher des tweets : ")
    tweet_count = int(input("Combien de tweets souhaitez-vous récupérer ? (ex: 10) "))
    
    tweets = scrape_tweets_from_search(query, tweet_count)
    
    if not tweets:
        print(f"Aucun tweet trouvé pour le mot-clé : {query}")
    else:
        filename = f"tweets_{query}.json"
        save_tweets_to_json(tweets, filename)
        print(f"{len(tweets)} tweets ont été sauvegardés dans le fichier '{filename}'.")

if __name__ == "__main__":
    main()
