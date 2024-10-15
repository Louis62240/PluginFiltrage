import tweepy

# Clés d'API
api_key = "7I3I3F9G0c2NKGJLPZ6BS2g0P"  # API Key
api_secret_key = "2sPGLRpZEsdGnEvQEMJRizdpfegjhT21pGrsffkRNl2ZlgbRib"  # API Secret Key
access_token = "793352095869140992-50DgNyJxT61IM8w4eVaUnfoDpUEkUCx"  # Access Token
access_token_secret = "D0i0HnJ45v6aiRHNmO61ySdgAnOXtUE4oqXgtbz0z9qP5"  # Access Token Secret

# Authentification avec l'API Twitter
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

# Création de l'objet API
api = tweepy.API(auth)

# Test de récupération de tweets à partir d'un mot-clé
query = "cyberharcèlement"
tweets = api.search_tweets(q=query, lang="fr", count=10)

# Affichage des tweets récupérés
for tweet in tweets:
    print(f"Tweet de @{tweet.user.screen_name}: {tweet.text}")
