<template>
  <div class="min-h-screen bg-gradient-to-b from-black to-green-900">
    <nav class="bg-green-950/90 backdrop-blur-sm fixed w-full z-50 border-b border-green-800/30">
      <div class="container mx-auto px-6 py-5 flex justify-between items-center">
        <NuxtLink 
          to="/" 
          class="text-green-300 text-2xl font-bold tracking-tight hover:text-green-200 transition-colors flex items-center gap-2"
        >
          <div class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
          Binary Trails
        </NuxtLink>
        
        <div class="flex items-center gap-8">
          <NuxtLink 
            v-for="item in navItems" 
            :key="item.path" 
            :to="item.path"
            class="text-green-100/90 hover:text-green-300 transition-all duration-200 text-sm font-medium relative py-1
                   after:content-[''] after:absolute after:w-0 after:h-0.5 after:bg-green-400/70 
                   after:left-0 after:-bottom-1 after:transition-all after:duration-200
                   hover:after:w-full"
          >
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