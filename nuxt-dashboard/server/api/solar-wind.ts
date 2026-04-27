export default defineEventHandler(() => {
  const speed = []
  const bz = []
  const labels = []
  const now = new Date()

  for (let i = 100; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 15 * 60 * 1000)
    labels.push(time.toISOString())
    speed.push(400 + Math.random() * 200 + (i > 70 ? 200 : 0))
    bz.push(Math.sin(i / 5) * 5 + (Math.random() - 0.5) * 2)
  }

  return {
    labels,
    speed,
    bz
  }
})
