<template>
  <div class="panel hero-panel">
    <div class="flex justify-between items-start mb-8 z-20">
      <div>
        <h2 class="font-bold uppercase tracking-[0.03em] text-3xl" :style="{ color: DashboardColors.primaryText }">Planetary Kp Index</h2>
        <p class="text-white text-lg mt-2 font-mono">24-72H OBSERVATION WINDOW | STEP-BAR METRICS</p>
      </div>
      <div class="text-right">
        <div class="text-9xl font-bold leading-none" :style="{ color: `${DashboardColors.secondary}CC` }">{{ currentKp.toFixed(2) }}</div>
        <div class="text-white text-lg font-bold mt-4 bg-dash-surface-container px-4 py-2 inline-block rounded uppercase tracking-widest border border-dash-border-variant">
          CURRENT G-SCALE: {{ gScale }}
        </div>
      </div>
    </div>

    <div class="relative flex-1">
      <!-- Custom Y-Axis labels -->
      <div class="absolute left-0 top-0 bottom-12 flex flex-col justify-between items-end pr-4 z-10 w-16 h-full bg-dash-surface">
        <span v-for="val in [9, 7, 5, 3, 1, 0]" :key="val" class="text-dash-text-dim text-lg font-mono leading-none absolute right-4" :style="{ bottom: (val/9 * 100) + '%' }">{{ val }}</span>
      </div>

      <div class="absolute inset-0 left-12 bottom-12 border-l border-b border-dash-border-variant bg-grid overflow-hidden">
        <!-- Threshold Lines -->
        <div class="absolute w-full border-t border-dashed border-dash-danger/50 z-10" style="top: 0%;">
          <span class="absolute right-2 top-1 bg-dash-surface px-1 text-dash-danger text-[10px] font-bold whitespace-nowrap">G5 - EXTREME (Kp 9)</span>
        </div>
        <div class="absolute w-full border-t border-dashed border-dash-warning/50 z-10" style="top: 11.11%;">
          <span class="absolute right-[160px] top-1 bg-dash-surface px-1 text-dash-warning text-[10px] font-bold whitespace-nowrap">G4 - SEVERE (Kp 8)</span>
        </div>
        <div class="absolute w-full border-t border-dashed border-dash-caution/50 z-10" style="top: 22.22%;">
          <span class="absolute right-[320px] top-1 bg-dash-surface px-1 text-dash-caution text-[10px] font-bold whitespace-nowrap">G3 - STRONG (Kp 7)</span>
        </div>

        <!-- Bars -->
        <div class="flex items-end h-full w-full justify-around px-2 relative">
          <!-- Observed data -->
          <div
            v-for="(val, i) in observedData"
            :key="'obs-' + i"
            class="w-[3%] rounded-t-sm transition-all duration-500"
            :class="getBarColor(val)"
            :style="{ height: (val / 9 * 100) + '%' }"
          ></div>
          <!-- Divider between observed and predicted -->
          <div v-if="observedData.length > 0 && predictedData.length > 0" 
               class="absolute w-0.5 h-full bg-dash-text-dim opacity-50"
               :style="{ left: (observedData.length * 3.3) + '%' }">
          </div>
          <!-- Predicted data -->
          <div
            v-for="(val, i) in predictedData"
            :key="'pred-' + i"
            class="w-[3%] rounded-t-sm transition-all duration-500 opacity-60"
            :class="getPredictedBarColor(val)"
            :style="{ height: (val / 9 * 100) + '%' }"
          ></div>
        </div>
      </div>

      <!-- X-Axis -->
      <div class="absolute left-20 right-0 bottom-0 grid grid-cols-5 pt-4 px-8 bg-dash-surface text-lg font-mono text-dash-text-dim">
        <span class="text-center">-72h</span>
        <span class="text-center">-48h</span>
        <span class="text-center">-24h</span>
        <span class="text-center text-primary font-bold tracking-widest">CURRENT</span>
        <span class="text-center">PREDICTED</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import DashboardColors from '~/utils/colors'
import { computed } from 'vue'

const props = defineProps({
  observedData: {
    type: Array,
    default: () => []
  },
  observedLabels: {
    type: Array,
    default: () => []
  },
  predictedData: {
    type: Array,
    default: () => []
  },
  predictedLabels: {
    type: Array,
    default: () => []
  }
})

const currentKp = computed(() => props.observedData[props.observedData.length - 1] || 0)

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
  if (val >= 7) return 'bg-dash-danger'
  if (val >= 5) return 'bg-dash-caution'
  return 'bg-dash-secondary/80'
}

function getPredictedBarColor(val) {
  if (val >= 7) return 'bg-dash-danger/60'
  if (val >= 5) return 'bg-dash-caution/60'
  return 'bg-dash-secondary/40'
}
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(to right, v-bind('DashboardColors.border') 1px, transparent 1px),
    linear-gradient(to bottom, v-bind('DashboardColors.border') 1px, transparent 1px);
  background-size: 50px 50px;
}
</style>
