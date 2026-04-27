import { createDataCache } from '../utils/cache'
import type { KpForecastItem } from '../types'

const cache = createDataCache<any>()

export default defineEventHandler(async () => {
  return cache.get(async () => {
    const res = await $fetch<KpForecastItem[]>('https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json')

    const observed = res.filter(item => item.observed !== 'predicted').sort((a, b) => new Date(a.time_tag).getTime() - new Date(b.time_tag).getTime())
    const predicted = res.filter(item => item.observed === 'predicted').sort((a, b) => new Date(a.time_tag).getTime() - new Date(b.time_tag).getTime())

    return {
      observedLabels: observed.map(item => item.time_tag),
      observedData: observed.map(item => Number(item.kp)),
      predictedLabels: predicted.map(item => item.time_tag),
      predictedData: predicted.map(item => Number(item.kp))
    }
  })
})
