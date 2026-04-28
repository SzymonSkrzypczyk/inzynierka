interface TimeSeriesData {
  labels: string[]
  [key: string]: any[]
}

export function createDataCache<T extends TimeSeriesData>() {
  let cache: T | null = null
  let lastFetch = 0
  const TTL = 5 * 60 * 1000

  function merge(existing: T, fresh: T): T {
    const existingLabels = new Set(existing.labels)
    const newIndices = fresh.labels
      .map((label, idx) => ({ label, idx }))
      .filter(({ label }) => !existingLabels.has(label))
      .map(({ idx }) => idx)

    const result: any = { labels: [...existing.labels] }
    for (const key of Object.keys(fresh)) {
      if (key === 'labels') continue
      if (Array.isArray((fresh as any)[key])) {
        result[key] = [
          ...(existing as any)[key],
          ...newIndices.map(i => (fresh as any)[key][i])
        ]
      }
    }
    return result as T
  }

  return {
    async get(fetcher: () => Promise<T>): Promise<T> {
      const now = Date.now()
      if (cache && now - lastFetch < TTL) {
        return cache
      }

      try {
        const fresh = await fetcher()
        cache = cache ? merge(cache, fresh) : fresh
        lastFetch = now
        return cache
      } catch (error) {
        if (cache) {
          console.warn('Fetch failed, returning stale cache:', error)
          return cache
        }
        throw error
      }
    }
  }
}
