# Importer les fonctions nécessaires depuis tweet_scraper.py
from tweet_scraper import scrape_tweet, parse_tweet

def main():
    query = input("Entrez un thème ou un mot-clé pour rechercher des tweets : ")
    tweet_count = int(input("Combien de tweets souhaitez-vous récupérer ? (ex: 10) "))
    
    tweets = scrape_tweets_from_search(query, tweet_count)
    
    if not tweets:
        print(f"Aucun tweet trouvé pour le mot-clé : {query}")
    else:
        for idx, tweet in enumerate(tweets, start=1):
            print(f"Tweet {idx}:")
            print(f"Texte : {tweet['text']}")
            print(f"Utilisateur : {tweet['user_handle']}")
            print(f"Date : {tweet['timestamp']}")
            print(f"Retweets : {tweet['retweets']}, Likes : {tweet['likes']}\n")

if __name__ == "__main__":
    main()
