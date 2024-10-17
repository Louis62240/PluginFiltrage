<template>
    <!-- Bouton Clear situé en haut à droite -->
    <div class="fixed top-4 right-4">
      <button
        @click="clearTweets"
        class="p-2 bg-red-500 text-white rounded-full shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-300 ease-in-out"
      >
        Clear Tweets
      </button>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios'; // Importer axios pour effectuer des requêtes HTTP
  
  // Fonction pour vider les tweets via l'API Flask
  const clearTweets = async () => {
    try {
      // Requête POST pour appeler l'API /api/clear_tweets et vider le fichier tweets.json
      const response = await axios.post('http://localhost:8000/api/clear_tweets');
  
      if (response.status === 200) {
        alert('Les tweets ont été effacés avec succès.');
      } else {
        alert('Une erreur s\'est produite lors de l\'effacement des tweets.');
      }
    } catch (error) {
      console.error('Erreur lors de la suppression des tweets :', error);
      alert('Erreur lors de la suppression des tweets. Veuillez réessayer.');
    }
  };
  </script>
  
  <style scoped>
  /* Styles pour le bouton Clear */
  .fixed {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 1000;
  }
  
  button {
    padding: 10px;
    background-color: #e3342f;
    color: white;
    border-radius: 50%;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease-in-out;
  }
  
  button:hover {
    background-color: #cc1f1a;
  }
  </style>
  