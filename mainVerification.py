from verificationTweet import process_json_file

def main():
    # Utiliser 'tweets.json' par défaut
    json_file_path = 'tweets.json'

    # Appeler la fonction de traitement avec le chemin du fichier
    process_json_file(json_file_path)

if __name__ == "__main__":
    main()
