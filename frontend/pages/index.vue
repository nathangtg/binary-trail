<template>
    <div class="min-h-screen">
      <section class="relative overflow-hidden">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,#064e3b_0%,transparent_70%)]"></div>
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_70%,#065f46_0%,transparent_70%)]"></div>
        <div class="relative">
          <HeroSection />
        </div>
      </section>
  
      <!-- Game Phases Section -->
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
  
      <!-- About the Project -->
      <section class="py-12 px-4">
        <div class="container mx-auto text-center">
          <h2 class="text-3xl font-bold text-green-100 mb-4">About This Project</h2>
          <p class="text-green-300 max-w-3xl mx-auto">
            Welcome to Binary Trails! The goal is simple: challenge your coding and problem-solving skills through three exciting phases. This project is meant to be a fun way for developers to engage in hands-on tasks like working with APIs, decoding encrypted messages, and solving algorithm challenges. It's not about leaderboards or stats—just you, the challenges, and a bit of fun.
          </p>
        </div>
      </section>
  
      <!-- Latest Challenges Section -->
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
  
      <!-- CTA Section -->
      <section class="py-16 px-4">
        <div class="container mx-auto">
          <div class="bg-gradient-to-r from-green-950/80 to-green-900/80 rounded-2xl p-8 md:p-12 text-center">
            <h2 class="text-4xl font-bold text-green-100 mb-4">Try It Out for Fun!</h2>
            <p class="text-green-200 mb-8 max-w-2xl mx-auto">
              Think you've got what it takes to solve the three phases? Jump in, experiment, and hone your skills. This project is entirely for fun—no scores, no pressure!
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <button class="px-8 py-3 bg-green-500 hover:bg-green-400 text-green-950 rounded-lg font-semibold transition-colors">
                Start Playing
              </button>
              <button class="px-8 py-3 border-2 border-green-500 text-green-400 hover:bg-green-500/10 rounded-lg font-semibold transition-colors">
                View Documentation
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script setup lang="ts">
    import type { Phase } from '~/interfaces/phase';
    import type { Challenge } from '~/interfaces/challenge';
  
    const phases: Phase[] = [
        { id: 1, title: 'API Warrior', description: 'Uncover the secrets of headers and master the art of API requests.' },
        { id: 2, title: 'Crypto Maze', description: 'Decrypt encoded messages to find clues and make API calls.' },
        { id: 3, title: 'The Algorithm Network', description: 'Write an algorithm, submit it via Gists, and pass the final test!' }
    ]
    
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
  
  <style scoped>
  .container {
    max-width: 960px;
  }
  </style>
  