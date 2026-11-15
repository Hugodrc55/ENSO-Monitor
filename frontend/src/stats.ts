import type { Observation } from './api'
import { monthIndex } from './format'

/**
 * Seuil NOAA, en °C : période chaude (El Niño) si ONI ≥ +0,5, froide (La Niña)
 * si ONI ≤ −0,5. Un épisode exige au moins 5 saisons consécutives au-delà.
 * Source et choix de ≥ plutôt que > : docs/DONNEES_NOAA.md, section 2.
 */
export const NOAA_THRESHOLD = 0.5

export const isWarm = (value: number): boolean => value >= NOAA_THRESHOLD
export const isCold = (value: number): boolean => value <= -NOAA_THRESHOLD

export type PeriodSummary = {
  count: number
  first: Observation
  last: Observation
  highest: Observation
  lowest: Observation
}

/**
 * Résumé d'observations triées par date ; null si la liste est vide.
 * En cas d'égalité, la saison la plus ancienne est retenue comme extrême.
 */
export function summarize(observations: readonly Observation[]): PeriodSummary | null {
  const first = observations[0]
  const last = observations.at(-1)
  if (first === undefined || last === undefined) return null

  let highest = first
  let lowest = first
  for (const observation of observations) {
    if (observation.oni > highest.oni) highest = observation
    if (observation.oni < lowest.oni) lowest = observation
  }
  return { count: observations.length, first, last, highest, lowest }
}

/**
 * Longueur de la plus longue suite de saisons consécutives qui vérifient la
 * condition. Un mois manquant entre deux saisons interrompt la suite.
 */
export function longestRun(
  observations: readonly Observation[],
  condition: (value: number) => boolean,
): number {
  let longest = 0
  let current = 0
  let previousMonth: number | null = null

  for (const observation of observations) {
    const month = monthIndex(observation.reference_month)
    const consecutive = previousMonth !== null && month === previousMonth + 1
    current = condition(observation.oni) ? (consecutive ? current + 1 : 1) : 0
    longest = Math.max(longest, current)
    previousMonth = month
  }
  return longest
}
