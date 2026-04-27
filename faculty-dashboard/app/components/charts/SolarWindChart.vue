<template>
  <div class="panel sub-panel">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h2 class="text-secondary font-bold uppercase tracking-wider text-base">Solar Wind</h2>
        <p class="text-[#c8c6ca] text-sm mt-1 font-mono uppercase">Speed (km/s) & Bz (nT) | 24H</p>
      </div>
    </div>

    <div class="relative flex-1">
      <div class="absolute left-0 top-0 bottom-6 flex flex-col justify-between items-end pr-2 z-10 w-12 h-full bg-[#141313]">
        <span v-for="val in [900, 600, 300, 0]" :key="val" class="text-[#7e7d7f] text-sm font-mono leading-none absolute right-2" :style="{ bottom: (val/1000 * 100) + '%' }">{{ val }}</span>
      </div>

      <div class="absolute inset-0 left-8 bottom-6 border-l border-b border-[#353434] bg-grid overflow-hidden">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Legend -->
    <div class="flex items-center gap-4 mt-2">
      <div class="flex items-center gap-2">
        <div class="w-6 h-0.5 bg-[#06bb63]"></div>
        <span class="text-[#c8c6ca] text-xs font-mono">Speed (km/s)</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-6 h-0 relative">
          <div class="absolute top-1/2 w-full border-t-2 border-dashed border-[#eab308]"></div>
        </div>
        <span class="text-[#c8c6ca] text-xs font-mono">Bz (nT)</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps({
  labels: Array,
  speed: Array,
  bz: Array
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: 'Speed',
      data: props.speed,
      borderColor: '#06bb63',
      backgroundColor: 'rgba(6, 187, 99, 0.1)',
      fill: true,
      tension: 0.4,
      pointRadius: 0,
      borderWidth: 2
    },
    {
      label: 'Bz',
      data: props.bz.map(v => v * 20 + 300), // Scale Bz to fit on same axis for visualization
      borderColor: '#eab308',
      borderDash: [5, 5],
      tension: 0.4,
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
    linear-gradient(to right, #1C1C1E 1px, transparent 1px),
    linear-gradient(to bottom, #1C1C1E 1px, transparent 1px);
  background-size: 30px 30px;
}
</style>
