<template>
    <div class="challenge-card">
      <!-- Challenge Card Header -->
      <div class="p-6 border-b border-green-800/30">
        <div class="flex justify-between items-start mb-4">
          <span 
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              difficultyColors[challenge.difficulty]
            ]"
          >
            {{ challenge.difficulty }}
          </span>
          <span class="text-green-400">{{ challenge.points }} pts</span>
        </div>
        <h3 class="text-xl font-semibold text-green-100 mb-2">{{ challenge.title }}</h3>
        <p class="text-green-300 text-sm mb-4">{{ challenge.description }}</p>
        
        <!-- Tags -->
        <div class="flex flex-wrap gap-2">
          <span 
            v-for="tag in challenge.tags" 
            :key="tag"
            class="px-2 py-0.5 bg-green-950/50 rounded-md text-green-400 text-xs border border-green-800/30"
          >
            {{ tag }}
          </span>
        </div>
      </div>
  
      <!-- Challenge Card Footer -->
      <div class="px-6 py-4 bg-green-950/50 flex items-center justify-between">
        <div class="flex items-center gap-4 text-sm text-green-400">
          <div class="flex items-center">
            <CheckCircleIcon class="w-4 h-4 mr-1" />
            {{ challenge.completionRate }}%
          </div>
        </div>
        <button 
          @click="startChallenge(challenge.id)"
          class="px-4 py-1.5 bg-green-500 hover:bg-green-400 text-green-950 rounded-lg 
                 font-medium text-sm transition-colors"
        >
          Start
        </button>
      </div>
    </div>
  </template>
  
  <script>
import { CheckCircleIcon } from 'lucide-react'
  
  export default {
    name: 'ChallengeCard',
    props: {
      challenge: {
        type: Object,
        required: true,
      },
      difficultyColors: {
        type: Object,
        required: true,
      },
    },
    methods: {
      startChallenge(challengeId) {
        this.$emit('start-challenge', challengeId);
      },
    },
  };
  </script>
  
  <style scoped>
  .challenge-card {
    background-color: #1a202c; 
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  </style>
  