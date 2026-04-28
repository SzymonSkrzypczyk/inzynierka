import { createDataCache } from '../utils/cache'
import type { ProtonFluxItem } from '../types'

const cache = createDataCache<{ labels: string[]; p10: number[]; p100: number[] }>()

export default defineEventHandler(async () => {
  return cache.get(async () => {
    const res = await $fetch<ProtonFluxItem[]>(
      'https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json'
    )

    const byTime = new Map<string, { p10?: number; p100?: number }>()

    for (const item of res) {
      const tag = item.time_tag
      if (!byTime.has(tag)) {
        byTime.set(tag, {})
      }

      const entry = byTime.get(tag)!

      if (item.energy === '>=10 MeV') {
        entry.p10 = Number(item.flux)
      }

      if (item.energy === '>=100 MeV') {
        entry.p100 = Number(item.flux)
      }
    }

    const merged: { label: string; p10: number; p100: number }[] = []

    for (const [label, values] of byTime) {
      if (values.p10 !== undefined && values.p100 !== undefined) {
        merged.push({
          label,
          p10: values.p10,
          p100: values.p100
        })
      }
    }

    merged.sort((a, b) => new Date(a.label).getTime() - new Date(b.label).getTime())

    return {
      labels: merged.map(m => m.label),
      p10: merged.map(m => m.p10),
      p100: merged.map(m => m.p100)
    }
  })
})