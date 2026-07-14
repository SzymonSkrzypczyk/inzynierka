<template>
  <div class="aspect-16-9-container">
    <!-- Centered Header Title (Hidden on Title Page) -->
    <transition name="fade">
      <div v-if="currentSlide !== 'title'" class="flex justify-center items-center py-4">
        <h1 class="text-dash-secondary font-bold uppercase tracking-[0.4em] text-7xl font-mono">
          Space Weather
        </h1>
      </div>
    </transition>

    <!-- Main Content Carousel -->
    <div class="flex-1 relative overflow-hidden">
      <transition :name="transitionName">
        <div :key="currentSlide" class="absolute inset-0">
          <TitlePage v-if="currentSlide === 'title'" />

          <ChartsKpIndexChart
            v-else-if="currentSlide === 'kpIndex' && kpData"
            :observed-data="kpData.observedData"
            :observed-labels="kpData.observedLabels"
            :predicted-data="kpData.predictedData"
            :predicted-labels="kpData.predictedLabels"
            class="h-full"
          />

          <ChartsSolarWindChart
            v-else-if="currentSlide === 'solarWind' && solarWindData"
            :labels="solarWindData.labels"
            :speed="solarWindData.speed"
            :bz="solarWindData.bz"
            class="h-full"
          />

          <ChartsXrayFluxChart
            v-else-if="currentSlide === 'xrayFlux' && xrayData"
            :labels="xrayData.labels"
            :flux="xrayData.flux"
            class="h-full"
          />

          <ChartsProtonFluxChart
            v-else-if="currentSlide === 'protonFlux' && protonData"
            :labels="protonData.labels"
            :p10="protonData.p10"
            :p100="protonData.p100"
            class="h-full"
          />

          <!-- Loading States -->
          <div v-else class="panel hero-panel animate-pulse flex items-center justify-center h-full">
            <span class="text-dash-text-muted font-mono">RETRIEVING DATA STREAM FOR {{ currentSlide.toUpperCase() }}...</span>
          </div>
        </div>
      </transition>
    </div>

    <!-- Ticker Section at Bottom (Hidden on Title Page) -->
    <transition name="fade">
      <SpaceWeatherTicker
        v-if="currentSlide !== 'title'"
        :kp-data="kpData"
        :solar-wind-data="solarWindData"
        :xray-data="xrayData"
        :proton-data="protonData"
        :active-mode="currentSlide"
      />
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const { data: kpData, refresh: refreshKp } = useFetch('/api/kp-index')
const { data: solarWindData, refresh: refreshSolarWind } = useFetch('/api/solar-wind')
const { data: xrayData, refresh: refreshXray } = useFetch('/api/xray-flux')
const { data: protonData, refresh: refreshProton } = useFetch('/api/proton-flux')

const slides = ['title', 'kpIndex', 'solarWind', 'xrayFlux', 'protonFlux']
const currentSlideIndex = ref(0)
const currentSlide = computed(() => slides[currentSlideIndex.value])
const transitionName = ref('slide-left')

let timer = null

const refreshNextSlideData = () => {
  const nextIndex = (currentSlideIndex.value + 1) % slides.length
  const nextSlideName = slides[nextIndex]

  if (nextSlideName === 'kpIndex') refreshKp()
  else if (nextSlideName === 'solarWind') refreshSolarWind()
  else if (nextSlideName === 'xrayFlux') refreshXray()
  else if (nextSlideName === 'protonFlux') refreshProton()
}

const nextSlide = () => {
  transitionName.value = 'slide-left'
  currentSlideIndex.value = (currentSlideIndex.value + 1) % slides.length

  // Refresh data for the slide AFTER the one we just switched to
  refreshNextSlideData()

  // Set next timeout based on the new slide
  const duration = currentSlide.value === 'title' ? 10000 : 40000
  timer = setTimeout(nextSlide, duration)
}

onMounted(() => {
  // Pre-fetch data for the first data slide (kpIndex) while on Title
  refreshNextSlideData()

  // Start the first transition after the initial slide duration (Title is first)
  timer = setTimeout(nextSlide, 10000)
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
})
</script>

<style>
/* Horizontal Sliding Transitions */
.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-left-enter-from {
  transform: translateX(100%);
}

.slide-left-leave-to {
  transform: translateX(-100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
