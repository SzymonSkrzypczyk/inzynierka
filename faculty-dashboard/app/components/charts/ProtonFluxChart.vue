<template>
  <div class="panel sub-panel">
    <div class="flex justify-between items-start mb-6">
      <div>
        <h2 class="font-bold uppercase tracking-[0.2em] text-3xl" :style="{ color: DashboardColors.primaryText }">Solar Proton Flux</h2>
        <p class="text-dash-text-muted text-lg mt-2 font-mono uppercase tracking-widest">Radiation Intensity (pfu) | Logarithmic Scale | 24H</p>
      </div>
    </div>

    <div class="relative flex-1">
      <div class="absolute left-0 top-0 bottom-12 pr-4 z-10 w-20 h-full bg-dash-surface">
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 100%;">10⁴</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 83.33%;">10³</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 66.66%;">10²</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 50%;">10¹</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 33.33%;">10⁰</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 16.66%;">10⁻¹</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4 translate-y-1/2" style="bottom: 0%;">10⁻²</span>
      </div>

      <div class="absolute inset-0 left-20 bottom-12 border-l border-b border-dash-border-variant bg-grid overflow-hidden">
        <!-- Threshold -->
        <div class="absolute w-full border-t border-dash-caution/50 z-10" style="top: 50%;">
          <span class="absolute left-2 top-1 bg-dash-surface px-1 text-dash-caution text-sm font-bold">S1 THRESHOLD</span>
        </div>

        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Legend -->
    <div class="flex items-center gap-8 mt-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-1" :style="{ backgroundColor: DashboardColors.secondary }"></div>
        <span class="text-dash-text-muted text-lg font-mono tracking-widest">&gt;10 MeV ENERGY CHANNEL</span>
      </div>
      <div class="flex items-center gap-3">
        <div class="w-8 h-1" :style="{ backgroundColor: DashboardColors.secondaryVariant }"></div>
        <span class="text-dash-text-muted text-lg font-mono tracking-widest">&gt;100 MeV ENERGY CHANNEL</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import DashboardColors from '~/utils/colors'
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LogarithmicScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LogarithmicScale, PointElement, LineElement, Title, Tooltip, Legend)

const props = defineProps({
  labels: Array,
  p10: Array,
  p100: Array
})

const safe = (arr) => (arr || []).map(v => v > 0 ? v : 1e-3)

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: '>10 MeV',
      data: safe(props.p10),
      borderColor: DashboardColors.secondary,
      backgroundColor: DashboardColors.secondaryBg,
      tension: 0.4,
      pointRadius: 0,
      borderWidth: 3,
      fill: false,
      pointBackgroundColor: DashboardColors.secondary,
      pointBorderColor: DashboardColors.primaryText
    },
    {
      label: '>100 MeV',
      data: safe(props.p100),
      borderColor: DashboardColors.secondaryVariant,
      backgroundColor: DashboardColors.secondaryBg,
      tension: 0.4,
      pointRadius: 0,
      borderWidth: 2.5,
      fill: false,
      pointBackgroundColor: DashboardColors.secondaryVariant,
      pointBorderColor: DashboardColors.primaryText
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false }
  },
  scales: {
    x: { display: false },
    y: {
      type: 'logarithmic',
      display: false,
      min: 1e-2,
      max: 1e4
    }
  }
}
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(to right, v-bind('DashboardColors.border') 1px, transparent 1px),
    linear-gradient(to bottom, v-bind('DashboardColors.border') 1px, transparent 1px);
  background-size: 30px 30px;
}
</style>
