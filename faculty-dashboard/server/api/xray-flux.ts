import type { XrayFluxItem } from '../types'

export default defineEventHandler(async () => {
  const res = await $fetch<XrayFluxItem[]>('https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json')

  const labels = res.map(item => item.time_tag)
  const flux = res.map(item => Number(item.flux))

  return { labels, flux }
})
