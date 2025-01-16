// pages/challenges.vue
<template>
  <div class="min-h-screen pt-24 px-6 pb-16">
    <div class="container mx-auto">
      <!-- Header -->
      <div class="mb-12">
        <h1 class="text-4xl font-bold text-green-50 mb-4">Challenges</h1>
        <div class="flex flex-wrap items-center gap-4">
          <!-- Search -->
          <div class="relative flex-grow max-w-md">
            <input 
              type="text" 
              v-model="searchQuery"
              placeholder="Search challenges..." 
              class="w-full bg-green-950/50 border border-green-800/30 rounded-xl px-4 py-2.5 
                     text-green-100 placeholder-green-700 focus:outline-none focus:border-green-600
                     transition-colors"
            />
          </div>
          
          <!-- Filters -->
          <div class="flex gap-3">
            <select 
              v-model="difficultyFilter"
              class="bg-green-950/50 border border-green-800/30 rounded-xl px-4 py-2.5 
                     text-green-300 focus:outline-none focus:border-green-600 transition-colors"
            >
              <option value="">All Difficulties</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
            
            <select 
              v-model="categoryFilter"
              class="bg-green-950/50 border border-green-800/30 rounded-xl px-4 py-2.5 
                     text-green-300 focus:outline-none focus:border-green-600 transition-colors"
            >
              <option value="">All Categories</option>
              <option value="API">API Integration</option>
              <option value="Encryption">Encryption</option>
              <option value="Algorithm">Algorithm</option>
              <option value="Testing">Testing</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Challenges Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="challenge in filteredChallenges" 
          :key="challenge.id"
          class="bg-green-950/30 border border-green-800/30 rounded-xl overflow-hidden hover:border-green-600/50 transition-all duration-300"
        >
        <ChallengeCard :challenge="challenge" :difficultyColors="difficultyColors" />
      </div>
    </div>

      <!-- Empty State -->
      <div 
        v-if="filteredChallenges.length === 0"
        class="text-center py-12"
      >
        <p class="text-green-300 text-lg">No challenges found matching your criteria.</p>
      </div>
    </div>
  </div>
  <div />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Challenge } from '../interfaces/challenge'

const searchQuery = ref('')
const difficultyFilter = ref('')
const categoryFilter = ref('')

const difficultyColors = {
  'Beginner': 'bg-green-500/20 text-green-400',
  'Intermediate': 'bg-yellow-500/20 text-yellow-400',
  'Advanced': 'bg-red-500/20 text-red-400'
}

// Sample challenges data (in a real app, this would come from an API)
const challenges = ref<Challenge[]>([
  {
    id: 1,
    title: 'GitHub API Integration',
    description: 'Create a client to fetch and display repository information using the GitHub REST API.',
    difficulty: 'Beginner',
    category: 'API',
    points: 100,
    completionRate: 78,
    tags: ['REST API', 'OAuth', 'GitHub']
  },
  {
    id: 2,
    title: 'Message Encryption',
    description: 'Implement a simple encryption/decryption system using various cryptographic algorithms.',
    difficulty: 'Intermediate',
    category: 'Encryption',
    points: 200,
    completionRate: 65,
    tags: ['Cryptography', 'Security', 'Algorithms']
  },
  {
    id: 3,
    title: 'API Testing Suite',
    description: 'Build a comprehensive testing suite for RESTful APIs using Postman and Newman.',
    difficulty: 'Intermediate',
    category: 'Testing',
    points: 150,
    completionRate: 72,
    tags: ['Postman', 'Testing', 'Automation']
  },
  {
    id: 4,
    title: 'Binary Search Trees',
    description: 'Implement and optimize operations on a binary search tree data structure.',
    difficulty: 'Advanced',
    category: 'Algorithm',
    points: 300,
    completionRate: 45,
    tags: ['DSA', 'Trees', 'Optimization']
  }
])

const filteredChallenges = computed(() => {
  return challenges.value.filter(challenge => {
    const matchesSearch = challenge.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         challenge.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesDifficulty = !difficultyFilter.value || challenge.difficulty === difficultyFilter.value
    const matchesCategory = !categoryFilter.value || challenge.category === categoryFilter.value
    
    return matchesSearch && matchesDifficulty && matchesCategory
  })
})

const startChallenge = (challengeId: number) => {
  // Navigate to the specific challenge page
  navigateTo(`/challenges/${challengeId}`)
}
</script>