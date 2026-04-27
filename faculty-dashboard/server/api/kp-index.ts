export default defineEventHandler(async () => {
  const res = await $fetch('https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json') as any[]

  const observed = res.filter(item => item.observed !== 'predicted')

  const labels = observed.map(item => item.time_tag)
  const data = observed.map(item => Number(item.kp))

  return { labels, data }
})
