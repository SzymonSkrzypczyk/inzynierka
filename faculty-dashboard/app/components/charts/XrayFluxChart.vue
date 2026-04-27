<template>
  <div class="panel sub-panel">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h2 class="text-secondary font-bold uppercase tracking-wider text-base">GOES X-ray Flux</h2>
        <p class="text-[#c8c6ca] text-sm mt-1 font-mono uppercase">Flux (W/m²) | Log Scale | 24H</p>
      </div>
    </div>

    <div class="relative flex-1">
      <div class="absolute left-0 top-0 bottom-6 flex flex-col justify-between items-end pr-2 z-10 w-12 h-full bg-[#141313]">
        <span class="text-[#ef4444] text-sm font-bold absolute right-2" style="bottom: 83.33%;">X</span>
        <span class="text-orange-500 text-sm font-bold absolute right-2" style="bottom: 66.66%;">M</span>
        <span class="text-yellow-500 text-sm font-bold absolute right-2" style="bottom: 50%;">C</span>
        <span class="text-[#7e7d7f] text-sm font-mono absolute right-2" style="bottom: 33.33%;">B</span>
        <span class="text-[#7e7d7f] text-sm font-mono absolute right-2" style="bottom: 16.66%;">A</span>
      </div>

      <div class="absolute inset-0 left-8 bottom-6 border-l border-b border-[#353434] bg-grid overflow-hidden">
        <!-- Thresholds -->
        <div class="absolute w-full border-t border-[#ef4444]/20" style="top: 16.66%;">
          <span class="absolute right-2 top-1 bg-[#141313] px-1 text-[#ef4444] text-sm font-bold">X</span>
        </div>
        <div class="absolute w-full border-t border-orange-500/20" style="top: 33.33%;">
          <span class="absolute right-2 top-1 bg-[#141313] px-1 text-orange-500 text-sm font-bold">M</span>
        </div>
        <div class="absolute w-full border-t border-yellow-500/20" style="top: 50%;">
          <span class="absolute right-2 top-1 bg-[#141313] px-1 text-yellow-500 text-sm font-bold">C</span>
        </div>

        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Legend -->
    <div class="flex items-center gap-4 mt-2">
      <div class="flex items-center gap-2">
        <div class="w-6 h-0.5 bg-[#06bb63]"></div>
        <span class="text-[#c8c6ca] text-xs font-mono">X-ray Flux (W/m²)</span>
      </div>
    </div>
  </div>
</template>

<script setup>
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
      borderColor: '#06bb63',
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
    linear-gradient(to right, #1C1C1E 1px, transparent 1px),
    linear-gradient(to bottom, #1C1C1E 1px, transparent 1px);
  background-size: 30px 30px;
}
</style>
