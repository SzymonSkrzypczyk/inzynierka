<template>
  <div class="panel sub-panel">
    <div class="flex justify-between items-start mb-6">
      <div>
        <h2 class="font-bold uppercase tracking-[0.2em] text-3xl" :style="{ color: DashboardColors.primaryText }">Solar Wind</h2>
        <p class="text-dash-text-muted text-lg mt-2 font-mono uppercase tracking-widest">Particle Velocity (km/s) | 24H Real-time Telemetry</p>
      </div>
    </div>

    <div class="relative flex-1">
      <div class="absolute left-0 top-0 bottom-12 flex flex-col justify-between items-end pr-4 z-10 w-20 h-full bg-dash-surface">
        <span v-for="val in [1000, 750, 500, 250, 0]" :key="val" class="text-dash-text-dim text-lg font-mono leading-none absolute right-4" :style="{ bottom: (val/1000 * 100) + '%' }">{{ val }}</span>
      </div>

      <div class="absolute inset-0 left-20 bottom-12 border-l border-b border-dash-border-variant bg-grid overflow-hidden">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

  </div>
</template>

<script setup>
import DashboardColors from '~/utils/colors'
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps({
  labels: Array,
  speed: Array
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: 'Speed',
      data: props.speed,
      borderColor: DashboardColors.secondaryVariant,
      backgroundColor: DashboardColors.secondaryBg,
      fill: true,
      tension: 0.4,
      pointRadius: 0,
      borderWidth: 2
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
      display: false,
      min: 0,
      max: 1000
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
