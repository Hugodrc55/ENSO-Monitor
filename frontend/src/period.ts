import type { Period } from './api'

/**
 * Toute la série, jusqu'à aujourd'hui (date locale). La première saison, DJF 1950,
 * a pour mois central janvier 1950.
 */
export function fullSeriesPeriod(): Period {
  const today = new Date()
  const pad = (n: number) => String(n).padStart(2, '0')
  return {
    start: '1950-01-01',
    end: `${today.getFullYear()}-${pad(today.getMonth() + 1)}-${pad(today.getDate())}`,
  }
}
