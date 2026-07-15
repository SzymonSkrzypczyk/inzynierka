<template>
  <div class="panel sub-panel">
    <div class="flex justify-between items-start mb-6">
      <div>
        <h2 class="font-bold uppercase tracking-[0.2em] text-3xl" :style="{ color: DashboardColors.primaryText }">GOES X-ray Flux</h2>
        <p class="text-dash-text-muted text-lg mt-2 font-mono uppercase tracking-widest">Electromagnetic Flux (W/m²) | Logarithmic Scale | 24H</p>
      </div>
    </div>

    <div class="relative flex-1">
      <div class="absolute left-0 top-0 bottom-12 flex flex-col justify-between items-end pr-4 z-10 w-20 h-full bg-dash-surface">
        <span class="text-dash-danger text-xl font-bold absolute right-4" style="bottom: 83.33%;">X</span>
        <span class="text-dash-warning text-xl font-bold absolute right-4" style="bottom: 66.66%;">M</span>
        <span class="text-dash-caution text-xl font-bold absolute right-4" style="bottom: 50%;">C</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4" style="bottom: 33.33%;">B</span>
        <span class="text-dash-text-dim text-lg font-mono absolute right-4" style="bottom: 16.66%;">A</span>
      </div>

      <div class="absolute inset-0 left-20 bottom-12 border-l border-b border-dash-border-variant bg-grid overflow-hidden">
        <!-- Thresholds -->
        <div class="absolute w-full border-t border-dash-danger/80" style="top: 16.66%;"></div>
        <div class="absolute w-full border-t border-dash-warning/80" style="top: 33.33%;"></div>
        <div class="absolute w-full border-t border-dash-caution/80" style="top: 50%;"></div>

        <Line :data="chartData" :options="chartOptions" />
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
  flux: Array
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      data: props.flux,
      borderColor: DashboardColors.secondaryVariant,
      tension: 0.2,
      pointRadius: 0,
      borderWidth: 1.5,
      fill: false
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
      min: 1e-9,
      max: 1e-3
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
