<template>
  <section class="py-20 px-6">
    <div class="container mx-auto">
      <div class="max-w-4xl mx-auto bg-green-950/30 rounded-2xl p-8 border border-green-800/30 backdrop-blur-sm">
        <!-- Header -->
        <div class="text-center mb-8">
          <span class="text-green-400 text-sm font-medium px-4 py-1.5 rounded-full bg-green-950/50 border border-green-800/30">
            Just For Fun!
          </span>
          <h2 class="text-4xl font-bold text-green-50 mt-4">
            About Binary Trails
          </h2>
        </div>

        <!-- Main content -->
        <div class="space-y-6 text-green-200 text-lg leading-relaxed">
          <p>
            Hey there! Binary Trails is a fun playground I created to test and improve my dev skills. No pressure, no formal learning paths - just a collection of interesting challenges involving different aspects of modern development.
          </p>
          
          <p>
            You'll get to mess around with:
          </p>

          <!-- Tech tags -->
          <TechTags />

          <p>
            Think of it as a sandbox where you can experiment with different dev tools and concepts. No rigid structure - just pick what interests you and dive in. It's all about hands-on experience and having fun while coding!
          </p>

          <!-- Fun note -->
          <div class="mt-8 p-4 bg-green-950/50 rounded-xl border border-green-800/30">
            <p class="text-green-400 text-base">
              💡 Pro tip: Don't worry about getting everything perfect. This is a space to experiment, break things, and learn from the process!
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>