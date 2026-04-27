<template>
  <div class="aspect-16-9-container">
    <ChartsKpIndexChart v-if="kpData" :data="kpData.data" />
    <div v-else class="panel hero-panel animate-pulse flex items-center justify-center">
      <span class="text-[#c8c6ca] font-mono">LOADING MISSION DATA...</span>
    </div>

    <ChartsSolarWindChart v-if="solarWindData" :labels="solarWindData.labels" :speed="solarWindData.speed" :bz="solarWindData.bz" />
    <div v-else class="panel sub-panel animate-pulse"></div>

    <ChartsXrayFluxChart v-if="xrayData" :labels="xrayData.labels" :flux="xrayData.flux" />
    <div v-else class="panel sub-panel animate-pulse"></div>

    <ChartsProtonFluxChart v-if="protonData" :labels="protonData.labels" :p10="protonData.p10" :p100="protonData.p100" />
    <div v-else class="panel sub-panel animate-pulse"></div>
  </div>
</template>

<script setup>
const { data: kpData } = useFetch('/api/kp-index')
const { data: solarWindData } = useFetch('/api/solar-wind')
const { data: xrayData } = useFetch('/api/xray-flux')
const { data: protonData } = useFetch('/api/proton-flux')
</script>
