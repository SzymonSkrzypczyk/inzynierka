<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'

const props = defineProps({
  kpData: Object,
  solarWindData: Object,
  xrayData: Object,
  protonData: Object,
  activeMode: {
    type: String,
    default: 'all' // 'kpIndex', 'solarWind', 'xrayFlux', 'protonFlux', 'all'
  }
})

const messages = {
  xrayFlux: [
    "X-RAY FLUX: Class A flare observed. Impact: Very low background levels, negligible effects on ionosphere or communications.",
    "X-RAY FLUX: Class B flare observed. Impact: Moderate background radiation, minimal disruption to radio communications.",
    "X-RAY FLUX: Class C flare observed. Impact: R1-Minor radio blackout on sunlit side, brief degradation of HF radio communications.",
    "X-RAY FLUX: Class M flare observed. Impact: R2-Moderate radio blackout, affecting high-frequency radio communications on sunlit side.",
    "X-RAY FLUX: Class X flare observed. Impact: R3-Strong radio blackout, widespread HF communication blackout and GPS degradation."
  ],
  xrayFluxInfo: [
    "X-RAY FLUX: Solar flares release intense bursts of electromagnetic radiation. Classes A, B, C, M, and X denote increasing intensity.",
    "X-RAY FLUX: Extreme bursts can ionize the upper atmosphere, causing radio blackouts and affecting satellite communications.",
    "X-RAY FLUX: Monitoring X-ray flux is critical for predicting D-region ionospheric disturbances that impact HF radio.",
    "X-RAY FLUX: Solar flare intensity is measured in Watts per square meter (W/m²) in the 1-8 Angstrom wavelength band."
  ],
  
  solarWind: [
    "SOLAR WIND: Slow speed (300-400 km/s) detected. Impact: Nominal magnetospheric conditions, minimal geomagnetic activity.",
    "SOLAR WIND: Moderate speed (400-500 km/s) detected. Impact: Slight compression of magnetosphere, minor enhancements to auroral activity.",
    "SOLAR WIND: High speed (500-600 km/s) detected. Impact: Moderate magnetospheric compression, increased auroral activity at high latitudes.",
    "SOLAR WIND: Very high speed (600-800 km/s) detected. Impact: Significant magnetospheric compression, potential satellite drag effects and G1 geomagnetic storms.",
    "SOLAR WIND: Extreme speed (>800 km/s) detected. Impact: Severe magnetospheric disturbance, prolonged satellite drag and G2+ geomagnetic storms."
  ],
  solarWindInfo: [
    "SOLAR WIND: A stream of charged particles released from the upper atmosphere of the Sun, called the corona.",
    "SOLAR WIND: Interplanetary magnetic field (IMF) orientation, especially the Bz component, determines the energy transfer to Earth.",
    "SOLAR WIND: High-speed streams often originate from coronal holes, causing recurring geomagnetic activity.",
    "SOLAR WIND: Solar wind density and temperature also play key roles in how the Sun interacts with Earth's magnetosphere."
  ],
  
  protonFlux: [
    "PROTON FLUX: <10 pfu detected. Impact: Background radiation levels, no significant effects on spacecraft or aviation.",
    "PROTON FLUX: 10-100 pfu (S1-Minor). Impact: Minor radiation storm, slight risk to astronauts, possible single event upsets in satellites.",
    "PROTON FLUX: 100-1000 pfu (S2-Moderate). Impact: Moderate radiation storm, increased radiation risk for high-altitude flights over poles.",
    "PROTON FLUX: 1000-10,000 pfu (S3-Strong). Impact: Strong radiation storm, significant risk to astronauts and satellite electronics.",
    "PROTON FLUX: >10,000 pfu (S4-Severe). Impact: Severe radiation storm, mission-threatening radiation levels for space operations."
  ],
  protonFluxInfo: [
    "PROTON FLUX: High-energy protons from solar events can penetrate spacecraft and pose radiation risks to astronauts.",
    "PROTON FLUX: Solar Proton Events (SPEs) are often associated with large solar flares and coronal mass ejections.",
    "PROTON FLUX: Elevated proton levels can cause Single Event Upsets (SEU) in sensitive satellite electronics.",
    "PROTON FLUX: During radiation storms, commercial flights may be rerouted away from polar regions to reduce exposure."
  ],
  
  kpIndex: [
    "KP INDEX: Kp=3 (Unsettled). Impact: Weak auroras at high latitudes, minor fluctuations in power systems.",
    "KP INDEX: Kp=5 (Storm). Impact: G1-Minor geomagnetic storm, auroras visible in northern US/Canada, intermittent HF radio communication issues.",
    "KP INDEX: Kp=6 (Strong Storm). Impact: G2-Moderate geomagnetic storm, power grid voltage corrections needed, satellite navigation degradation.",
    "KP INDEX: Kp=7 (Severe Storm). Impact: G3-Strong geomagnetic storm, widespread voltage control issues, low-frequency radio navigation problems.",
    "KP INDEX: Kp=8 (Extreme Storm). Impact: G4-Severe geomagnetic storm, pipeline corrosion risks, widespread HF radio blackouts."
  ],
  kpIndexInfo: [
    "KP INDEX: Measures geomagnetic activity. A global indicator of auroral activity and potential power grid impacts.",
    "KP INDEX: Values range from 0 to 9. Higher values indicate more intense geomagnetic storms triggered by solar activity.",
    "KP INDEX: The index is derived from the maximum fluctuations of horizontal magnetic components at stations worldwide.",
    "KP INDEX: G-scale (G1 to G5) is directly linked to Kp values to communicate the severity of geomagnetic storms."
  ]
};

const activeMessages = computed(() => {
  const list = []
  
  const categories = [
    {
      id: 'xrayFlux',
      data: props.xrayData?.flux,
      thresholds: [1e-7, 1e-6, 1e-5, 1e-4],
      placeholder: "X-RAY FLUX: DATA STREAM INITIALIZING... STANDBY FOR TELEMETRY.",
      formatter: (val) => val.toExponential(1).toUpperCase() + ' W/M²',
      replaceTarget: 'flare observed',
      replaceValue: (val) => `flare observed (${val})`
    },
    {
      id: 'solarWind',
      data: props.solarWindData?.speed,
      thresholds: [400, 500, 600, 800],
      placeholder: "SOLAR WIND: ANALYZING PARTICLE VELOCITY... SENSORS ONLINE.",
      formatter: (val) => Math.round(val) + ' KM/S',
      replaceTarget: 'detected',
      replaceValue: (val) => `detected (${val})`
    },
    {
      id: 'protonFlux',
      data: props.protonData?.p10,
      thresholds: [10, 100, 1000, 10000],
      placeholder: "PROTON FLUX: MONITORING RADIATION LEVELS... BACKGROUND NOMINAL.",
      formatter: (val) => val.toFixed(1) + ' PFU',
      replaceTarget: 'detected',
      replaceValue: (val) => `detected (${val})`
    },
    {
      id: 'kpIndex',
      data: props.kpData?.observedData,
      thresholds: [5, 6, 7, 8],
      placeholder: "KP INDEX: CALCULATING GEOMAGNETIC DISTURBANCE... SCANNING.",
      formatter: (val) => val,
      replaceTarget: ').',
      replaceValue: (val) => `) CURRENT KP: ${val}.`
    }
  ]

  categories.forEach(cat => {
    if (props.activeMode === 'all' || props.activeMode === cat.id) {
      if (cat.data?.length > 0) {
        const lastVal = cat.data[cat.data.length - 1]
        let index = 0
        cat.thresholds.forEach((t, i) => { if (lastVal >= t) index = i + 1 })

        const baseMessage = messages[cat.id][index]
        list.push(baseMessage.replace(cat.replaceTarget, cat.replaceValue(cat.formatter(lastVal))))
      } else {
        list.push(cat.placeholder)
      }
      list.push(...messages[cat.id + 'Info'])
    }
  })

  return list
})

const currentIndex = ref(0)
let timer = null

// Reset index when changing modes to show the first message for the new chart
watch(() => props.activeMode, () => {
  currentIndex.value = 0
})

onMounted(() => {
  timer = setInterval(() => {
    if (activeMessages.value.length > 0) {
      currentIndex.value = (currentIndex.value + 1) % activeMessages.value.length
    }
  }, 6000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="ticker-panel flex items-center gap-4 h-16 px-6 bg-[#141313] border border-[#1C1C1E] rounded-sm">
    <div class="flex items-center gap-3 border-r border-[#353434] pr-6">
      <div class="w-2.5 h-2.5 bg-[#4ae183] rounded-full animate-pulse shadow-[0_0_8px_#4ae183]"></div>
      <h1 class="text-[#4ae183] font-bold uppercase tracking-[0.2em] text-2xl whitespace-nowrap font-mono">
        Space Weather
      </h1>
    </div>

    <div class="flex-1 overflow-hidden px-4">
      <transition name="fade" mode="out-in">
        <p :key="currentIndex" class="text-[#c8c6ca] font-mono text-sm md:text-base uppercase tracking-wider">
          <span class="text-[#4ae183] mr-2 font-bold">>>></span>
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
