<template>
    <section class="py-16 px-4">
      <div class="container mx-auto">
        <h2 class="text-3xl font-bold text-green-100 text-center mb-12">Why Choose Binary Trails?</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <FeatureCard
            v-for="feature in features"
            :key="feature.title"
            v-bind="feature"
          />
        </div>
      </div>
    </section>
  </template>
  
  <script setup lang="ts">
  import { Code, Trophy, Users } from 'lucide-react'
  
  const features = [
    {
      icon: Code,
      title: 'Real-World API Challenges',
      description: 'Practice with authentic scenarios that mirror professional development tasks.'
    },
    {
      icon: Trophy,
      title: 'Competitive Learning',
      description: 'Compete with other developers and climb the global leaderboard.'
    },
    {
      icon: Users,
      title: 'Developer Community',
      description: 'Join a community of passionate developers and share solutions.'
    }
  ]
  </script>