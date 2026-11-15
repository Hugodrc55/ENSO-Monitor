import { describe, expect, it } from 'vitest'
import type { Observation } from './api'
import { validatePeriod } from './components/PeriodFilter'
import { NBSP, formatOni, seasonMonths } from './format'
import { isCold, isWarm, longestRun, summarize } from './stats'

// Valeurs FICTIVES, choisies pour le test : ce ne sont pas des observations NOAA.
const obs = (reference_month: string, season: string, year: number, oni: number): Observation => ({
  reference_month,
  season,
  year,
  oni,
})

describe('summarize', () => {
  it('renvoie null pour une période vide', () => {
    expect(summarize([])).toBeNull()
  })

  it('retient la saison la plus ancienne en cas d’égalité', () => {
    const a = obs('2000-01-01', 'DJF', 2000, 1.2)
    const b = obs('2000-02-01', 'JFM', 2000, 1.2)
    const c = obs('2000-03-01', 'FMA', 2000, -0.3)
    expect(summarize([a, b, c])).toEqual({ count: 3, first: a, last: c, highest: a, lowest: c })
  })
})

describe('longestRun', () => {
  it('compte les saisons consécutives au-delà du seuil, bornes comprises', () => {
    const values = [0.4, 0.5, 0.9, 0.5, 0.49, 0.7].map((oni, i) =>
      obs(`2000-0${i + 1}-01`, 'X', 2000, oni),
    )
    expect(longestRun(values, isWarm)).toBe(3)
    expect(longestRun(values, isCold)).toBe(0)
  })

  it('interrompt la suite quand un mois manque', () => {
    const values = [obs('2000-01-01', 'X', 2000, -1), obs('2000-03-01', 'X', 2000, -1)]
    expect(longestRun(values, isCold)).toBe(1)
  })
})

describe('formatage', () => {
  it('écrit le signe, la virgule et l’unité', () => {
    expect(formatOni(2.59, '°C')).toBe(`+2,59${NBSP}°C`)
    expect(formatOni(-1.4, '°C')).toBe(`−1,40${NBSP}°C`)
    expect(formatOni(0, '°C')).toBe(`0,00${NBSP}°C`)
  })

  it('donne les trois mois d’une saison à cheval sur deux années', () => {
    expect(seasonMonths(obs('2015-12-01', 'NDJ', 2015, 0))).toBe('nov. 2015 – janv. 2016')
    expect(seasonMonths(obs('2016-01-01', 'DJF', 2016, 0))).toBe('déc. 2015 – févr. 2016')
  })
})

describe('validatePeriod', () => {
  it('accepte une période d’un seul jour et refuse les dates inversées ou incomplètes', () => {
    expect(validatePeriod('2015-12-01', '2015-12-01')).toBeNull()
    expect(validatePeriod('2016-01-01', '2015-01-01')).toMatch(/postérieure/)
    expect(validatePeriod('', '2015-01-01')).toMatch(/complètes/)
  })
})
