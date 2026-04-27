<template>
  <div class="panel hero-panel">
    <div class="flex justify-between items-start mb-6 z-20">
      <div>
        <h2 class="text-secondary font-bold uppercase tracking-wider text-base">Planetary Kp Index</h2>
        <p class="text-[#c8c6ca] text-sm mt-1 font-mono">24-72H OBSERVATION WINDOW | STEP-BAR METRICS</p>
      </div>
      <div class="text-right">
        <div class="text-secondary text-7xl font-bold leading-none">{{ currentKp.toFixed(2) }}</div>
        <div class="text-[#c8c6ca] text-sm font-bold mt-2 bg-[#201f1f] px-2 py-1 inline-block rounded uppercase tracking-widest">
          CURRENT G-SCALE: {{ gScale }}
        </div>
      </div>
    </div>

    <div class="relative flex-1">
      <!-- Custom Y-Axis labels -->
      <div class="absolute left-0 top-0 bottom-8 flex flex-col justify-between items-end pr-3 z-10 w-12 h-full bg-[#141313]">
        <span v-for="val in [9, 7, 5, 3, 1, 0]" :key="val" class="text-[#7e7d7f] text-sm font-mono leading-none absolute right-3" :style="{ bottom: (val/9 * 100) + '%' }">{{ val }}</span>
      </div>

      <div class="absolute inset-0 left-8 bottom-8 border-l border-b border-[#353434] bg-grid overflow-hidden">
        <!-- Threshold Lines -->
        <div class="absolute w-full border-t border-dashed border-[#ef4444]/50 z-10" style="top: 0%;">
          <span class="absolute right-2 top-1 bg-[#141313] px-1 text-[#ef4444] text-sm font-bold">G5 - EXTREME (Kp 9)</span>
        </div>
        <div class="absolute w-full border-t border-dashed border-orange-500/50 z-10" style="top: 11.11%;">
          <span class="absolute right-2 top-1 bg-[#141313] px-1 text-orange-500 text-sm font-bold">G4 - SEVERE (Kp 8)</span>
        </div>
        <div class="absolute w-full border-t border-dashed border-yellow-500/50 z-10" style="top: 22.22%;">
          <span class="absolute right-2 top-1 bg-[#141313] px-1 text-yellow-500 text-sm font-bold">G3 - STRONG (Kp 7)</span>
        </div>

        <!-- Bars -->
        <div class="flex items-end h-full w-full justify-around px-2">
          <div
            v-for="(val, i) in data"
            :key="i"
            class="w-[3%] rounded-t-sm transition-all duration-500"
            :class="getBarColor(val)"
            :style="{ height: (val / 9 * 100) + '%' }"
          ></div>
        </div>
      </div>

      <!-- X-Axis -->
      <div class="absolute left-8 right-0 bottom-0 grid grid-cols-4 pt-2 px-2 bg-[#141313]">
        <span class="text-[#7e7d7f] text-sm font-mono pl-1">-72h</span>
        <span class="text-[#7e7d7f] text-sm font-mono text-center">-48h</span>
        <span class="text-[#7e7d7f] text-sm font-mono text-center">-24h</span>
        <span class="text-secondary text-sm font-bold font-mono text-right pr-1">CURRENT</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const currentKp = computed(() => props.data[props.data.length - 1] || 0)

const gScale = computed(() => {
  const kp = currentKp.value
  if (kp >= 9) return 'G5'
  if (kp >= 8) return 'G4'
  if (kp >= 7) return 'G3'
  if (kp >= 6) return 'G2'
  if (kp >= 5) return 'G1'
  return 'G0'
})

function getBarColor(val) {
  if (val >= 7) return 'bg-[#ef4444]'
  if (val >= 5) return 'bg-yellow-500'
  return 'bg-[#4ae183]/80'
}
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(to right, #1C1C1E 1px, transparent 1px),
    linear-gradient(to bottom, #1C1C1E 1px, transparent 1px);
  background-size: 50px 50px;
}
</style>
