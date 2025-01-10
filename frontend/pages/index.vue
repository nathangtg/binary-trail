<template>
    <div class="min-h-screen">
        <section class="relative overflow-hidden">
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,#064e3b_0%,transparent_70%)]"></div>
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_70%,#065f46_0%,transparent_70%)]"></div>
            <div class="relative">
            <HeroSection />
            </div>
        </section>
        <GamePhase />  
        <AboutProject />
        <LatestChallenge />
        <CTASection />
    </div>
</template>

<style scoped>
.container {
    max-width: 960px;
}
</style>