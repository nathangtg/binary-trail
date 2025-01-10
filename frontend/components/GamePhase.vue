<template>
    <section class="py-12 px-4">
        <div class="container mx-auto">
          <h2 class="text-3xl font-bold text-green-100 mb-8 text-center">Game Phases</h2>
          <div class="grid md:grid-cols-1 lg:grid-cols-3 gap-6">
            <div 
              v-for="phase in phases" 
              :key="phase.id" 
              class="bg-green-950/40 rounded-xl p-6 border border-green-800/50 hover:border-green-600/50 transition-colors"
            >
              <h3 class="text-xl font-semibold text-green-100 mb-2">{{ phase.title }}</h3>
              <p class="text-green-300 mb-4">{{ phase.description }}</p>
            </div>
          </div>
        </div>
      </section>
</template>

<script lang="ts">
    import type { Phase } from '~/interfaces/phase';
  
    const phases: Phase[] = [
        { id: 1, title: 'API Warrior', description: 'Uncover the secrets of headers and master the art of API requests.' },
        { id: 2, title: 'Crypto Maze', description: 'Decrypt encoded messages to find clues and make API calls.' },
        { id: 3, title: 'The Algorithm Network', description: 'Write an algorithm, submit it via Gists, and pass the final test!' }
    ]</script>