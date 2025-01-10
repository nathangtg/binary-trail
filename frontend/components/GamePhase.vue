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

<script setup lang="ts">
    import type { Phase } from '~/interfaces/phase';
  
    const phases: Phase[] = [
    {
      id: 1,
      title: 'API Warrior',
      description: 'Uncover the secrets of headers and master the art of API requests. This phase challenges you to identify missing headers, debug API interactions, and handle HTTP status codes effectively. Hone your skills and unlock the first key!'
    },
    {
      id: 2,
      title: 'Crypto Maze',
      description: 'Decrypt encoded messages to find clues and make API calls. Use tools or write your own scripts to decode ciphertexts and convert them into actionable insights. Each solved message brings you closer to mastering cryptography and uncovering the next challenge!'
    },
    {
      id: 3,
      title: 'The Algorithm Network',
      description: 'Write an efficient algorithm, submit it via Gists, and pass the final test! You’ll be tasked with solving real-world coding problems and integrating your solutions with the provided API. Only the most optimal solutions will prevail. Prove your mettle and claim victory!'
    }
  ];

</script>