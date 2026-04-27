export default defineEventHandler(() => {
  const data = []
  const labels = []
  const now = new Date()

  for (let i = 24; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 3 * 60 * 60 * 1000) // every 3 hours
    labels.push(time.toISOString())
    data.push(Math.random() * 5) // Kp 0-5 for most
  }

  // Add some spikes
  data[10] = 7.33
  data[11] = 8.66
  data[18] = 6.00

  return {
    labels,
    data
  }
})
