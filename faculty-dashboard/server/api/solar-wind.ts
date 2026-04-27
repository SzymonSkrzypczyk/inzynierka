import { createDataCache } from '../utils/cache'
import type { AceSwepamItem, AceMagItem } from '../types'

const cache = createDataCache<{ labels: string[], speed: number[], bz: number[] }>()

export default defineEventHandler(async () => {
  return cache.get(async () => {
    const [swepam, mag] = await Promise.all([
      $fetch<AceSwepamItem[]>('https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json'),
      $fetch<AceMagItem[]>('https://services.swpc.noaa.gov/json/ace/mag/ace_mag_1h.json')
    ])

    const speedMap = new Map<string, number>()
    for (const item of swepam) {
      speedMap.set(item.time_tag, Number(item.speed))
    }

    const merged: { label: string; speed: number; bz: number }[] = []
    for (const item of mag) {
      const tag = item.time_tag
      const speed = speedMap.get(tag)
      if (speed !== undefined) {
        merged.push({
          label: tag,
          speed,
          bz: Number(item.gsm_bz)
        })
      }
    }

    merged.sort((a, b) => new Date(a.label).getTime() - new Date(b.label).getTime())

    return {
      labels: merged.map(m => m.label),
      speed: merged.map(m => m.speed),
      bz: merged.map(m => m.bz)
    }
  })
})
