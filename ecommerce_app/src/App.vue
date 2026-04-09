<script setup>
import { RouterView } from 'vue-router'
import navbar from './components/navbar.vue';
</script>

<template>
  
  <div id="app" class="font-sans text-gray-800">
    <!-- You can place a global header or navbar here if needed -->
    <navbar />
    <!-- Router View -->
    <!-- <RouterView /> -->
    
    <!-- You can place a global footer here if needed -->
  </div>
</template>

<style>
/* Global styles, or leave empty if using Tailwind */
</style>
