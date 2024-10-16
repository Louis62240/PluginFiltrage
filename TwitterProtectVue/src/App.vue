<script setup>
import homeComponent from './components/home/homeComponent.vue';
import headerComponent from './components/header/headerComponent.vue';
import searchComponent from './components/home/searchComponent.vue';
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 p-8">
    <headerComponent />
    <searchComponent />
    <homeComponent />
  </div>
</template>