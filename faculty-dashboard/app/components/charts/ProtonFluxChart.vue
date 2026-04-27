<template>
  <div class="panel sub-panel">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h2 class="text-secondary font-bold uppercase tracking-wider text-sm">Proton Flux</h2>
        <p class="text-[#c8c6ca] text-[10px] mt-1 font-mono uppercase">Radiation Events | 24H</p>
      </div>
    </div>

    <div class="relative flex-1">
      <div class="absolute left-0 top-0 bottom-6 flex flex-col justify-between items-end pr-2 z-10 w-8 h-full">
        <span class="text-[#7e7d7f] text-[10px] font-mono absolute right-2" style="bottom: 80%;">10³</span>
        <span class="text-[#7e7d7f] text-[10px] font-mono absolute right-2" style="bottom: 60%;">10²</span>
        <span class="text-[#7e7d7f] text-[10px] font-mono absolute right-2" style="bottom: 40%;">10¹</span>
        <span class="text-[#7e7d7f] text-[10px] font-mono absolute right-2" style="bottom: 20%;">10⁰</span>
        <span class="text-[#7e7d7f] text-[10px] font-mono absolute right-2" style="bottom: 0%;">10⁻¹</span>
      </div>

      <div class="absolute inset-0 left-8 bottom-6 border-l border-b border-[#353434] bg-grid overflow-hidden">
        <!-- Threshold -->
        <div class="absolute w-full border-t border-yellow-500/50 z-10" style="top: 50%;">
          <span class="absolute left-2 -top-4 text-yellow-500 text-[8px] font-bold">S1 THRESHOLD</span>
        </div>

        <Line :data="chartData" :options="chartOptions" />
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
  p10: Array,
  p100: Array
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: '>10 MeV',
      data: props.p10,
      borderColor: '#c8c6c8',
      tension: 0.4,
      pointRadius: 0,
      borderWidth: 2,
      fill: false
    },
    {
      label: '>100 MeV',
      data: props.p100,
      borderColor: '#47464a',
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
      type: 'logarithmic',
      display: false,
      min: 0.1,
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
