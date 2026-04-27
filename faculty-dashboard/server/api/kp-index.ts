import type { KpForecastItem } from '../types'

export default defineEventHandler(async () => {
  const res = await $fetch<KpForecastItem[]>('https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json')

  const observed = res.filter(item => item.observed !== 'predicted')

  const labels = observed.map(item => item.time_tag)
  const data = observed.map(item => Number(item.kp))

  return { labels, data }
})
