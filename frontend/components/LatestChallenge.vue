<template>
    <section class="py-16 px-4">
        <div class="container mx-auto">
          <h2 class="text-3xl font-bold text-green-100 mb-8 justify-center self-center text-center">Latest Challenges</h2>
          <div class="grid md:grid-cols-1 lg:grid-cols-3 gap-6">
            <div v-for="challenge in challenges" :key="challenge.id" 
                 class="bg-green-950/40 rounded-xl p-6 border border-green-800/50 hover:border-green-600/50 transition-colors">
              <div class="flex items-center justify-between mb-4">
                <span :class="[ 'px-3 py-1 rounded-full text-sm font-medium', difficultyColors[challenge.difficulty] ]">
                  {{ challenge.difficulty }}
                </span>
                <span class="text-green-400">{{ challenge.points }} pts</span>
              </div>
              <h3 class="text-xl font-semibold text-green-100 mb-2">{{ challenge.title }}</h3>
              <p class="text-green-300 mb-4">{{ challenge.description }}</p>
            </div>
          </div>
        </div>
      </section>
</template>

<script setup lang="ts">
import type { Challenge } from '~/interfaces/challenge';
const difficultyColors = {
        'Beginner': 'bg-green-500/20 text-green-400',
        'Intermediate': 'bg-yellow-500/20 text-yellow-400',
        'Advanced': 'bg-red-500/20 text-red-400'
    }
    
    const challenges: Challenge[] = [
        {
        id: 1,
        title: 'Decode the Headers',
        description: 'Figure out which headers are needed for the request.',
        difficulty: 'Beginner',
        points: 50
        },
        {
        id: 2,
        title: 'Decrypt the Message',
        description: 'Use the cipher provided to decode the message.',
        difficulty: 'Intermediate',
        points: 100
        },
        {
        id: 3,
        title: 'Algorithm Submission',
        description: 'Solve the algorithm problem and submit your solution via a Gist link.',
        difficulty: 'Advanced',
        points: 150
        }
    ]
</script>