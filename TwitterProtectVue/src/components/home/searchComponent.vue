<template>
  <div class="flex justify-center items-center my-10">
    <div class="relative w-full max-w-md">
      <input
        v-model="query"
        @input="handleInput"
        type="text"
        placeholder="Rechercher un thème sur Twitter"
        class="w-full py-3 px-4 pr-12 text-gray-700 placeholder-gray-500 bg-white rounded-full shadow-md border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 ease-in-out"
      />
      <button
        @click="searchTwitter"
        class="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-blue-500 text-white rounded-full shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300 ease-in-out"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          class="w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M14.752 11.168l-1.414-1.414a4 4 0 10-1.414 1.414l1.414 1.414a2 2 0 101.414-1.414z"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'; // Assurez-vous d'avoir installé axios avec `npm install axios`

const query = ref('');

// Fonction pour appeler l'API FastAPI pour la recherche de tweets
const searchTwitter = async () => {
  try {
    const response = await axios.post('http://localhost:8000/search_tweets', {
      query: query.value,  // La requête entrée par l'utilisateur
      tweet_count: 10      // Nombre de tweets à récupérer
    });
    console.log(response.data.tweets);  // Affiche les tweets récupérés dans la console
  } catch (error) {
    console.error('Erreur lors de la recherche de tweets:', error);
  }
};

const handleInput = () => {
  // Vous pouvez ajouter ici des fonctionnalités comme une auto-suggestion
};
</script>

<style scoped>
/* Vous pouvez ajuster les styles ici pour plus de personnalisation */
</style>
