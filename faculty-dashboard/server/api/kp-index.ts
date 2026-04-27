import { createDataCache } from '../utils/cache'
import type { KpForecastItem } from '../types'

const cache = createDataCache<{ labels: string[], data: number[] }>()

export default defineEventHandler(async () => {
  return cache.get(async () => {
    const res = await $fetch<KpForecastItem[]>('https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json')

    const observed = res.filter(item => item.observed !== 'predicted')

    const labels = observed.map(item => item.time_tag)
    const data = observed.map(item => Number(item.kp))

    return { labels, data }
  })
})
