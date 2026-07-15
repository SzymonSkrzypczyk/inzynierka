<template>
  <div class="panel flex flex-col items-center justify-center relative overflow-hidden h-full border-none bg-dash-bg">
    <!-- Background subtle effect -->
    <div class="absolute inset-0 bg-grid opacity-20"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-dash-bg/50 to-dash-bg"></div>

    <!-- Main Title -->
    <div class="relative z-10 flex flex-col items-center">
      <div class="w-24 h-1 bg-primary mb-8 animate-pulse shadow-[0_0_15px_var(--tw-shadow-color)] shadow-primary"></div>
      <h1 class="text-8xl md:text-9xl font-bold uppercase tracking-[0.3em] font-mono text-center" :style="{ color: DashboardColors.primaryText }">
        Space<br>Weather
      </h1>
      <div class="w-24 h-1 bg-primary mt-8 animate-pulse shadow-[0_0_15px_var(--tw-shadow-color)] shadow-primary"></div>
    </div>

    <!-- Bottom Right Credit -->
    <div class="absolute bottom-12 right-12 z-10 animate-fade-in-delayed">
      <span class="text-dash-text-dim font-mono text-sm tracking-wider">Created by Szymon Skrzypczyk</span>
    </div>
  </div>
</template>

<script setup>
import DashboardColors from '~/utils/colors'
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(to right, v-bind('DashboardColors.border') 1px, transparent 1px),
    linear-gradient(to bottom, v-bind('DashboardColors.border') 1px, transparent 1px);
  background-size: 60px 60px;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in-delayed {
  0% { opacity: 0; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}

.animate-fade-in {
  animation: fade-in 1.5s ease-out forwards;
}

.animate-fade-in-delayed {
  animation: fade-in-delayed 3s ease-out forwards;
}
</style>
