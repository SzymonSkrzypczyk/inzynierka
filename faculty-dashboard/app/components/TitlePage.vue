<template>
  <div class="panel flex flex-col items-center justify-center relative overflow-hidden h-full border-none bg-[#0A0A0B]">
    <!-- Background subtle effect -->
    <div class="absolute inset-0 bg-grid opacity-20"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-[#0A0A0B]/50 to-[#0A0A0B]"></div>

    <!-- Main Title -->
    <div class="relative z-10 flex flex-col items-center">
      <div class="w-24 h-1 bg-[#4ae183] mb-8 animate-pulse shadow-[0_0_15px_#4ae183]"></div>
      <h1 class="text-[#4ae183] text-8xl md:text-9xl font-bold uppercase tracking-[0.3em] font-mono text-center">
        Space<br>Weather
      </h1>
      <div class="w-24 h-1 bg-[#4ae183] mt-8 animate-pulse shadow-[0_0_15px_#4ae183]"></div>
      <p class="text-[#c8c6ca] mt-12 font-mono tracking-[0.5em] uppercase text-xl animate-fade-in">Mission Control System</p>
    </div>

    <!-- Bottom Right Credit -->
    <div class="absolute bottom-12 right-12 z-10 flex flex-col items-end animate-fade-in-delayed">
      <span class="text-[#7e7d7f] font-mono text-xs uppercase tracking-widest">System Architect</span>
      <span class="text-[#e5e2e1] font-mono text-lg uppercase tracking-wider font-bold">created by: Szymon Skrzypczyk</span>
      <a href="https://www.linkedin.com/in/szymon-skrzypczyk" class="text-[#4ae183] font-mono text-xs underline mt-1 opacity-70 hover:opacity-100 transition-opacity">
        www.linkedin.com/in/szymon-skrzypczyk
      </a>
    </div>

    <!-- Decorative elements -->
    <div class="absolute top-12 right-12 text-[#353434] font-mono text-xs flex flex-col items-end opacity-50">
      <span>REF: SWPC-MC-2024</span>
      <span>STATUS: OPERATIONAL</span>
    </div>
  </div>
</template>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(to right, #1C1C1E 1px, transparent 1px),
    linear-gradient(to bottom, #1C1C1E 1px, transparent 1px);
  background-size: 60px 60px;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in-delayed {
  0% { opacity: 0; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}

.animate-fade-in {
  animation: fade-in 1.5s ease-out forwards;
}

.animate-fade-in-delayed {
  animation: fade-in-delayed 3s ease-out forwards;
}
</style>
