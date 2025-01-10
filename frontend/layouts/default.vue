<template>
    <div class="min-h-screen bg-gradient-to-b from-black to-green-900">
      <nav class="bg-green-950/90 backdrop-blur-sm fixed w-full z-50">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
          <NuxtLink to="/" class="text-green-300 text-2xl font-bold">Binary Trails</NuxtLink>
          <div class="space-x-6">
            <NuxtLink 
              v-for="item in navItems" 
              :key="item.path" 
              :to="item.path"
              class="text-green-100 hover:text-green-300 transition-colors">
              {{ item.name }}
            </NuxtLink>
          </div>
        </div>
      </nav>
      <slot />
    </div>
  </template>
  
  <script setup lang="ts">
  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Challenges', path: '/challenges' },
    { name: 'Leaderboard', path: '/leaderboard' },
    { name: 'Documentation', path: '/docs' }
  ]
  </script>
  