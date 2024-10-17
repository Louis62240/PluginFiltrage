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
  const emit = defineEmits(['clear']);
  
  // Fonction qui émet l'événement 'clear' lorsqu'on clique sur le bouton
  const clearTweets = () => {
    emit('clear'); // Émettre un événement pour que le parent réinitialise les tweets
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
  