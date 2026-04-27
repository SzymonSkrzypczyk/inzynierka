export default defineEventHandler(async () => {
  const [swepam, mag] = await Promise.all([
    $fetch('https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json'),
    $fetch('https://services.swpc.noaa.gov/json/ace/mag/ace_mag_1h.json')
  ]) as [any[], any[]]

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
