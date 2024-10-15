# Importer les fonctions nécessaires depuis tweet_scraper.py
from tweet_scraper import scrape_tweet, parse_tweet

def main():
    # Demander à l'utilisateur un lien de tweet
    tweet_url = input("Entrez l'URL du tweet : ")

    # Appel de la fonction scrape_tweet pour récupérer les données du tweet
    tweet_data = scrape_tweet(tweet_url)

    if tweet_data:
        # Parser les données du tweet
        parsed_tweet = parse_tweet(tweet_data)
        # Afficher les résultats
        print(parsed_tweet)
    else:
        print("Aucune donnée n'a pu être récupérée pour ce tweet.")

if __name__ == "__main__":
    main()
