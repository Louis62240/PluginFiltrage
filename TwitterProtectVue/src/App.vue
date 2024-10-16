<script setup>
import homeComponent from './components/home/homeComponent.vue';
import headerComponent from './components/header/headerComponent.vue';
import searchComponent from './components/home/searchComponent.vue';

import { ref } from 'vue';

const loading = ref(false);

// Fonction pour gérer le changement du statut de chargement
const handleLoading = (isLoading) => {
  loading.value = isLoading;
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 p-8">
    <div :class="{ 'blur-lg': loading }">
      <headerComponent />
      <searchComponent @loading="handleLoading" />
      <homeComponent />
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
  border: 8px solid #f3f3f3; /* Couleur de fond du loader */
  border-top: 8px solid #3498db; /* Couleur de la bordure animée */
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

/* Couverture de l'écran avec opacité */
.fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8); /* Fond semi-transparent */
  z-index: 9999; /* S'assure que le loader est au-dessus de tout */
}
</style>
