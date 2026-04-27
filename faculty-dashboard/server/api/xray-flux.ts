export default defineEventHandler(async () => {
  const res = await $fetch('https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json') as any[]

  const labels = res.map(item => item.time_tag)
  const flux = res.map(item => Number(item.flux))

  return { labels, flux }
})
