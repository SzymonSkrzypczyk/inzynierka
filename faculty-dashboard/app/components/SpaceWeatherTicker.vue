<template>
  <div class="ticker-panel flex items-center gap-4 h-16 px-6 bg-[#141313] border border-[#1C1C1E] rounded-sm">
    <div class="flex items-center gap-3 border-r border-[#353434] pr-6">
      <div class="w-2 h-2 bg-[#4ae183] rounded-full animate-pulse shadow-[0_0_8px_#4ae183]"></div>
      <h1 class="text-[#4ae183] font-bold uppercase tracking-[0.2em] text-base whitespace-nowrap font-mono">
        Space Weather
      </h1>
    </div>

    <div class="flex-1 overflow-hidden px-4">
      <transition name="fade" mode="out-in">
        <p :key="currentIndex" class="text-[#c8c6ca] font-mono text-xs md:text-sm uppercase tracking-wider">
          <span class="text-[#4ae183] mr-2">>>></span>
          {{ messages[currentIndex] }}
        </p>
      </transition>
    </div>

    <div class="text-[#7e7d7f] font-mono text-[10px] uppercase tracking-widest border-l border-[#353434] pl-6 whitespace-nowrap">
      Live Feed // MISSION-CTRL-{{ (currentIndex + 1).toString().padStart(2, '0') }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const messages = [
  "GEOMAGNETIC STORM: G3-STRONG level reached. Impact: Power grid fluctuations at high latitudes, potential GPS signal degradation, and vibrant auroras.",
  "SOLAR WIND: High-speed stream (>600 km/s) detected. Impact: Compression of Earth's magnetosphere, potentially disrupting satellite orbital stability.",
  "X-RAY FLUX: Class M5.2 flare observed. Impact: R2-Moderate radio blackout on sunlit side, affecting high-frequency radio communications.",
  "PROTON FLUX: Elevated S1 radiation storm in progress. Impact: Increased radiation risk for astronauts and potential spacecraft electronics upsets."
]

const currentIndex = ref(0)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % messages.length
  }, 45000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
