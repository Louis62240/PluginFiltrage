import json
from playwright.sync_api import sync_playwright
from typing import List, Dict

def convert_to_int(number_str: str) -> int:
    """Convertit les nombres abrégés (ex: 1.5K, 2K) en entiers."""
    if not number_str or number_str == "":
        return 0  # Retourne 0 si la chaîne est vide ou None
    number_str = number_str.replace(",", "")
    if "K" in number_str:
        return int(float(number_str.replace("K", "")) * 1000)
    elif "M" in number_str:
        return int(float(number_str.replace("M", "")) * 1000000)
    else:
        return int(number_str)

def scrape_tweets_from_search(query: str, tweet_count: int = 10) -> List[Dict]:
    tweets = []

    def parse_tweet_element(tweet_element):
        """Récupère les informations pertinentes d'un tweet affiché sur la page."""
        try:
            tweet_text = tweet_element.query_selector("div[lang]").inner_text() if tweet_element.query_selector("div[lang]") else ""
            timestamp = tweet_element.query_selector("time").get_attribute("datetime") if tweet_element.query_selector("time") else ""
            profile_image_url = tweet_element.query_selector("div > div > div > a > div > div > img").get_attribute("src") if tweet_element.query_selector("div > div > div > a > div > div > img") else ""
            user_handle = tweet_element.query_selector("div > div > div > a > div > div > span").inner_text() if tweet_element.query_selector("div > div > div > a > div > div > span") else ""
            retweet_count_str = tweet_element.query_selector("[data-testid='retweet']").inner_text() if tweet_element.query_selector("[data-testid='retweet']") else "0"
            like_count_str = tweet_element.query_selector("[data-testid='like']").inner_text() if tweet_element.query_selector("[data-testid='like']") else "0"

            # Récupérer les images
            image_elements = tweet_element.query_selector_all("div[aria-label='Image'] img")
            tweet_images = [img.get_attribute("src") for img in image_elements] if image_elements else []

            # Récupérer les vidéos : essayer avec <video>, <iframe>, ou d'autres balises possibles
            video_elements = tweet_element.query_selector_all("video")
            iframe_elements = tweet_element.query_selector_all("iframe")
            
            # Récupérer les vidéos depuis les balises vidéo ou iframe
            tweet_videos = [video.get_attribute("src") for video in video_elements if video.get_attribute("src")] if video_elements else []
            tweet_iframes = [iframe.get_attribute("src") for iframe in iframe_elements if iframe.get_attribute("src")] if iframe_elements else []

            # Convertir les retweets et likes en entiers en tenant compte des abréviations
            retweet_count = convert_to_int(retweet_count_str)
            like_count = convert_to_int(like_count_str)
            
            return {
                "text": tweet_text,
                "timestamp": timestamp,
                "user_handle": user_handle,
                "profile_image_url": profile_image_url,
                "retweets": retweet_count,
                "likes": like_count,
                "tweet_images": tweet_images,
                "tweet_videos": tweet_videos + tweet_iframes  # Ajouter les vidéos et les iframes potentiellement contenant des vidéos
            }
        except Exception as e:
            print(f"Erreur lors du parsing d'un tweet : {e}")
            return None

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Aller à la page de recherche des tweets "Top" de Twitter
            search_url = f"https://twitter.com/search?q={query}&f=top"
            print(f"Accès à l'URL : {search_url}")
            page.goto(search_url)

            # Augmenter le délai pour attendre que les tweets soient visibles
            page.wait_for_selector("article[data-testid='tweet']", timeout=30000)

            tweet_selector = "article[data-testid='tweet']"
            scroll_attempts = 0
            max_scroll_attempts = 10  # Limiter le nombre de scrolls pour éviter la boucle infinie

            while len(tweets) < tweet_count and scroll_attempts < max_scroll_attempts:
                try:
                    # Récupérer tous les tweets visibles sur la page
                    tweet_elements = page.query_selector_all(tweet_selector)
                    
                    if not tweet_elements:
                        print(f"Aucun tweet trouvé, tentative de scrolling... ({scroll_attempts+1}/{max_scroll_attempts})")
                        scroll_attempts += 1
                    else:
                        print(f"{len(tweet_elements)} tweets trouvés lors du scroll {scroll_attempts+1}")

                    for tweet_element in tweet_elements:
                        tweet_data = parse_tweet_element(tweet_element)
                        if tweet_data and tweet_data not in tweets:
                            print(f"Ajout d'un tweet : {tweet_data['text'][:30]}...")
                            tweets.append(tweet_data)
                            if len(tweets) >= tweet_count:
                                break

                    # Scrolling vers le bas pour charger plus de tweets
                    page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                    page.wait_for_selector(tweet_selector, timeout=5000)
                    scroll_attempts += 1

                except Exception as e:
                    print(f"Erreur lors du scrolling ou de la récupération des tweets : {e}")
                    scroll_attempts += 1

            # Trier les tweets par nombre de retweets et de likes en ordre décroissant
            if tweets:
                tweets = sorted(tweets, key=lambda x: (x['retweets'], x['likes']), reverse=True)

        except Exception as e:
            print(f"Erreur lors de la navigation : {e}")

        finally:
            # Toujours fermer le navigateur pour éviter les fuites de mémoire
            browser.close()

    return tweets[:tweet_count]  # Retourner les tweets récupérés, limités au nombre requis

def save_tweets_to_json(tweets: List[Dict], filename: str):
    """Enregistre les tweets dans un fichier JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)

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
