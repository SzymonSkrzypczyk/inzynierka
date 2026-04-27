import { createDataCache } from '../utils/cache'
import type { XrayFluxItem } from '../types'

const cache = createDataCache<{ labels: string[], flux: number[] }>()

export default defineEventHandler(async () => {
  return cache.get(async () => {
    const res = await $fetch<XrayFluxItem[]>('https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json')

    // Sample every 10th data point (every 10 minutes)
    const sampledData = res.filter((_, index) => index % 10 === 0)
    
    const labels = sampledData.map(item => item.time_tag)
    const flux = sampledData.map(item => Number(item.flux))

    return { labels, flux }
  })
})
