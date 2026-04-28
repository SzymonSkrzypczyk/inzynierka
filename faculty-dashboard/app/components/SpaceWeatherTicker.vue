<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  kpData: Object,
  solarWindData: Object,
  xrayData: Object,
  protonData: Object
})

const messages = {
  xrayFlux: [
    "X-RAY FLUX: Class A flare observed. Impact: Very low background levels, negligible effects on ionosphere or communications.",
    "X-RAY FLUX: Class B flare observed. Impact: Moderate background radiation, minimal disruption to radio communications.",
    "X-RAY FLUX: Class C flare observed. Impact: R1-Minor radio blackout on sunlit side, brief degradation of HF radio communications.",
    "X-RAY FLUX: Class M flare observed. Impact: R2-Moderate radio blackout, affecting high-frequency radio communications on sunlit side.",
    "X-RAY FLUX: Class X flare observed. Impact: R3-Strong radio blackout, widespread HF communication blackout and GPS degradation."
  ],
  
  solarWind: [
    "SOLAR WIND: Slow speed (300-400 km/s) detected. Impact: Nominal magnetospheric conditions, minimal geomagnetic activity.",
    "SOLAR WIND: Moderate speed (400-500 km/s) detected. Impact: Slight compression of magnetosphere, minor enhancements to auroral activity.",
    "SOLAR WIND: High speed (500-600 km/s) detected. Impact: Moderate magnetospheric compression, increased auroral activity at high latitudes.",
    "SOLAR WIND: Very high speed (600-800 km/s) detected. Impact: Significant magnetospheric compression, potential satellite drag effects and G1 geomagnetic storms.",
    "SOLAR WIND: Extreme speed (>800 km/s) detected. Impact: Severe magnetospheric disturbance, prolonged satellite drag and G2+ geomagnetic storms."
  ],
  
  protonFlux: [
    "PROTON FLUX: <10 pfu detected. Impact: Background radiation levels, no significant effects on spacecraft or aviation.",
    "PROTON FLUX: 10-100 pfu (S1-Minor). Impact: Minor radiation storm, slight risk to astronauts, possible single event upsets in satellites.",
    "PROTON FLUX: 100-1000 pfu (S2-Moderate). Impact: Moderate radiation storm, increased radiation risk for high-altitude flights over poles.",
    "PROTON FLUX: 1000-10,000 pfu (S3-Strong). Impact: Strong radiation storm, significant risk to astronauts and satellite electronics.",
    "PROTON FLUX: >10,000 pfu (S4-Severe). Impact: Severe radiation storm, mission-threatening radiation levels for space operations."
  ],
  
  kpIndex: [
    "KP INDEX: Kp=3 (Unsettled). Impact: Weak auroras at high latitudes, minor fluctuations in power systems.",
    "KP INDEX: Kp=5 (Storm). Impact: G1-Minor geomagnetic storm, auroras visible in northern US/Canada, intermittent HF radio communication issues.",
    "KP INDEX: Kp=6 (Strong Storm). Impact: G2-Moderate geomagnetic storm, power grid voltage corrections needed, satellite navigation degradation.",
    "KP INDEX: Kp=7 (Severe Storm). Impact: G3-Strong geomagnetic storm, widespread voltage control issues, low-frequency radio navigation problems.",
    "KP INDEX: Kp=8 (Extreme Storm). Impact: G4-Severe geomagnetic storm, pipeline corrosion risks, widespread HF radio blackouts."
  ]
};

const activeMessages = computed(() => {
  const list = []
  
  // X-Ray Flux
  if (props.xrayData?.flux?.length > 0) {
    const lastFlux = props.xrayData.flux[props.xrayData.flux.length - 1]
    let index = 0
    if (lastFlux >= 1e-4) index = 4
    else if (lastFlux >= 1e-5) index = 3
    else if (lastFlux >= 1e-6) index = 2
    else if (lastFlux >= 1e-7) index = 1
    
    const baseMessage = messages.xrayFlux[index]
    const fluxVal = lastFlux.toExponential(1).toUpperCase()
    list.push(baseMessage.replace('flare observed', `flare observed (${fluxVal} W/M²)`))
  } else {
    list.push("X-RAY FLUX: DATA STREAM INITIALIZING... STANDBY FOR TELEMETRY.")
  }

  // Solar Wind
  if (props.solarWindData?.speed?.length > 0) {
    const lastSpeed = props.solarWindData.speed[props.solarWindData.speed.length - 1]
    let index = 0
    if (lastSpeed >= 800) index = 4
    else if (lastSpeed >= 600) index = 3
    else if (lastSpeed >= 500) index = 2
    else if (lastSpeed >= 400) index = 1
    
    const baseMessage = messages.solarWind[index]
    list.push(baseMessage.replace('detected', `detected (${Math.round(lastSpeed)} KM/S)`))
  } else {
    list.push("SOLAR WIND: ANALYZING PARTICLE VELOCITY... SENSORS ONLINE.")
  }

  // Proton Flux
  if (props.protonData?.p10?.length > 0) {
    const lastP10 = props.protonData.p10[props.protonData.p10.length - 1]
    let index = 0
    if (lastP10 >= 10000) index = 4
    else if (lastP10 >= 1000) index = 3
    else if (lastP10 >= 100) index = 2
    else if (lastP10 >= 10) index = 1
    
    const baseMessage = messages.protonFlux[index]
    list.push(baseMessage.replace('detected', `detected (${lastP10.toFixed(1)} PFU)`))
  } else {
    list.push("PROTON FLUX: MONITORING RADIATION LEVELS... BACKGROUND NOMINAL.")
  }

  // Kp Index
  if (props.kpData?.observedData?.length > 0) {
    const lastKp = props.kpData.observedData[props.kpData.observedData.length - 1]
    let index = 0
    if (lastKp >= 8) index = 4
    else if (lastKp >= 7) index = 3
    else if (lastKp >= 6) index = 2
    else if (lastKp >= 5) index = 1
    
    const baseMessage = messages.kpIndex[index]
    list.push(baseMessage.replace(').', `) CURRENT KP: ${lastKp}.`))
  } else {
    list.push("KP INDEX: CALCULATING GEOMAGNETIC DISTURBANCE... SCANNING.")
  }

  return list
})

const currentIndex = ref(0)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    if (activeMessages.value.length > 0) {
      currentIndex.value = (currentIndex.value + 1) % activeMessages.value.length
    }
  }, 10000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="ticker-panel flex items-center gap-4 h-16 px-6 bg-[#141313] border border-[#1C1C1E] rounded-sm">
    <div class="flex items-center gap-3 border-r border-[#353434] pr-6">
      <div class="w-2 h-2 bg-[#4ae183] rounded-full animate-pulse shadow-[0_0_8px_#4ae183]"></div>
      <h1 class="text-[#4ae183] font-bold uppercase tracking-[0.2em] text-base whitespace-nowrap font-mono">
        Space Weather
      </h1>
    </div>

    <div class="flex-1 overflow-hidden px-4">
      <transition name="fade" mode="out-in">
        <p :key="currentIndex" class="text-[#c8c6ca] font-mono text-xs md:text-sm uppercase tracking-wider">
          <span class="text-[#4ae183] mr-2">>>></span>
          {{ activeMessages[currentIndex] }}
        </p>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
