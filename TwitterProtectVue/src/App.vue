<script setup>
import homeComponent from './components/home/homeComponent.vue';
import headerComponent from './components/header/headerComponent.vue';
import searchComponent from './components/home/searchComponent.vue';
import clearComponent from './components/home/clearComponent.vue'; // Importer le clearComponent

import { ref } from 'vue';

const loading = ref(false);
const tweets = ref([]); // Pour stocker les tweets récupérés

// Fonction pour gérer le changement du statut de chargement
const handleLoading = (isLoading) => {
  loading.value = isLoading;
};

// Fonction pour effacer les tweets
const clearTweets = () => {
  tweets.value = []; // Efface les tweets
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 p-8">


    <!-- Cette section sera floutée en fonction de l'état de chargement -->
    <div :class="{ 'blur-lg': loading }">
      <headerComponent />


      <!-- Barre de recherche sans effet de flou -->
      <searchComponent @loading="handleLoading" />
      <div class="flex justify-end">
        <clearComponent @clear="clearTweets" />
      </div>
      <!-- Affichage des tweets dans homeComponent -->
      <homeComponent :tweets="tweets" />
    </div>

    <!-- Loader au centre si la page est en train de charger -->
    <div v-if="loading" class="fixed inset-0 flex items-center justify-center bg-white bg-opacity-50 z-50">
      <div class="loader"></div>
    </div>
  </div>
</template>

<style scoped>
/* Effet de flou */
.blur-lg {
  backdrop-filter: blur(10px);
  transition: backdrop-filter 0.3s ease-in-out;
}

/* Style du loader */
.loader {
  border: 8px solid #f3f3f3;
  /* Couleur de fond du loader */
  border-top: 8px solid #3498db;
  /* Couleur de la bordure animée */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

</style>