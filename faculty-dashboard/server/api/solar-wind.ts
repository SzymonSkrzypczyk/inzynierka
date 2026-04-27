import { createDataCache } from '../utils/cache'
import type { AceSwepamItem } from '../types'

const cache = createDataCache<{ labels: string[], speed: number[] }>()

export default defineEventHandler(async () => {
  return cache.get(async () => {
    const swepam = await $fetch<AceSwepamItem[]>('https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json')

    const items = swepam
      .map(item => ({
        label: item.time_tag,
        speed: Number(item.speed)
      }))
      .sort((a, b) => new Date(a.label).getTime() - new Date(b.label).getTime())

    return {
      labels: items.map(m => m.label),
      speed: items.map(m => m.speed)
    }
  })
})
