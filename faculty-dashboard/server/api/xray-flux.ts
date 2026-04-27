export default defineEventHandler(() => {
  const flux = []
  const labels = []
  const now = new Date()

  for (let i = 100; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 15 * 60 * 1000)
    labels.push(time.toISOString())
    let base = 1e-8
    if (i > 45 && i < 55) base = 1e-4 // X-flare
    if (i > 15 && i < 25) base = 5e-6 // C-flare
    flux.push(base + Math.random() * base)
  }

  return {
    labels,
    flux
  }
})
