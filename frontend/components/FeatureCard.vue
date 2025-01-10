<template>
    <div class="bg-green-950/50 backdrop-blur p-6 rounded-xl">
      <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
        <component :is="icon" class="w-6 h-6 text-green-400" />
      </div>
      <h3 class="text-xl font-semibold text-green-200 mb-2">{{ title }}</h3>
      <p class="text-green-300">{{ description }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
  interface Props {
    icon: any;
    title: string;
    description: string;
  }
  
  defineProps<Props>()
  </script>
  