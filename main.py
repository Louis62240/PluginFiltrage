from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tweet_scraper_v2 import main  # Importer la fonction main de ton script de scraping

app = FastAPI()

# Configurer le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origine autorisée (URL de ton frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

# Modèle de données pour la requête
class QueryRequest(BaseModel):
    query: str
    tweet_count: int = 10  # Par défaut, on récupère 10 tweets

# Route API pour chercher les tweets
@app.post("/search_tweets")
async def search_tweets(request: QueryRequest):
    try:
        # Appeler la fonction main avec les paramètres de la requête
        print(request.query)
        tweets = main(request.query, request.tweet_count)
        return {"tweets": tweets}  # Retourne les tweets sous forme de JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lancer l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
