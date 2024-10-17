<template>
  <div class="flex flex-col justify-center items-center my-10 space-y-4">
    <!-- Barre pour entrer le thème -->
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

    <!-- Barre pour entrer le nombre de tweets -->
    <div class="relative w-full max-w-md">
      <input
        v-model="tweetCount"
        type="number"
        placeholder="Nombre de tweets à traiter"
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

const emit = defineEmits(['loading']);

const query = ref('');
const tweets = ref([]);  // Stocker les tweets récupérés
const error = ref('');   // Stocker les erreurs
const loadingValue = ref(false);  
const tweetCount = ref(20);  // Nombre de tweets à récupérer
// Fonction pour appeler l'API Flask pour la recherche de tweets
const searchTwitter = async () => {
  if (!query.value || tweetCount.value <= 0) {
    alert('Veuillez entrer un thème et un nombre de tweets valide.');
    return;
  }
  
  try {
    emit('loading', true);
    error.value = '';  // Réinitialiser l'erreur avant chaque nouvelle recherche
    const response = await axios.post('http://localhost:5000/api/tweets', {
      query: query.value,  // La requête entrée par l'utilisateur
      tweet_count: 20     // Nombre de tweets à récupérer
    });
    console.log(response.data)
    emit('loading', false);
    tweets.value = response.data;  // Mettre à jour les tweets
  } catch (err) {
    console.error('Erreur lors de la recherche de tweets:', err);
    error.value = 'Erreur lors de la récupération des tweets. Veuillez réessayer.';  // Message d'erreur utilisateur
  }
};

const handleInput = () => {
  // Vous pouvez ajouter ici des fonctionnalités comme une auto-suggestion
};
</script>

<style scoped>
/* Vous pouvez ajuster les styles ici pour plus de personnalisation */
.tweets-container {
  max-width: 600px;
  margin: 0 auto;
}
.tweet {
  background-color: #f8fafc;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
