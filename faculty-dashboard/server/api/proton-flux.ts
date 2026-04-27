export default defineEventHandler(() => {
  const p10 = []
  const p100 = []
  const labels = []
  const now = new Date()

  for (let i = 100; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 15 * 60 * 1000)
    labels.push(time.toISOString())
    p10.push(0.1 + Math.pow(10, (i/100) * 3) * (0.5 + Math.random() * 0.5))
    p100.push(0.01 + Math.pow(10, (i/100) * 2) * (0.5 + Math.random() * 0.5))
  }

  return {
    labels,
    p10,
    p100
  }
})
