import type { Observation } from './api'

const SHORT_MONTHS = [
  'janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin',
  'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.',
]
const LONG_MONTHS = [
  'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
  'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre',
]

/**
 * Rang d'un mois, compté depuis l'an 0 : « 2015-12-01 » donne 2015 × 12 + 11.
 * Calculé sur le texte AAAA-MM-JJ, sans objet Date, donc sans effet de fuseau horaire.
 */
export function monthIndex(isoDate: string): number {
  return Number(isoDate.slice(0, 4)) * 12 + Number(isoDate.slice(5, 7)) - 1
}

/** « déc. 2015 » pour le rang d'un mois. */
export function formatMonth(index: number): string {
  const year = Math.floor(index / 12)
  return `${SHORT_MONTHS[index - year * 12] ?? ''} ${year}`
}

/** « 1er mai 1997 » pour « 1997-05-01 ». */
export function formatDate(isoDate: string): string {
  const day = Number(isoDate.slice(8, 10))
  const month = LONG_MONTHS[Number(isoDate.slice(5, 7)) - 1] ?? ''
  return `${day === 1 ? '1er' : day} ${month} ${isoDate.slice(0, 4)}`
}

/** « mai 1997 » pour « 1997-05-01 ». */
export function formatMonthLong(isoDate: string): string {
  return `${LONG_MONTHS[Number(isoDate.slice(5, 7)) - 1] ?? ''} ${isoDate.slice(0, 4)}`
}

/** Code NOAA et année : « NDJ 2015 ». */
export function seasonLabel(observation: Observation): string {
  return `${observation.season} ${observation.year}`
}

/** Les trois mois moyennés autour du mois central : NDJ 2015 → « nov. 2015 – janv. 2016 ». */
export function seasonMonths(observation: Observation): string {
  const central = monthIndex(observation.reference_month)
  return `${formatMonth(central - 1)} – ${formatMonth(central + 1)}`
}

/** Nombre signé à la française : +2,59 ; −1,85 ; 0,00. Le signe moins est U+2212. */
export function formatSigned(value: number, decimals = 2): string {
  const sign = value > 0 ? '+' : value < 0 ? '−' : ''
  return `${sign}${Math.abs(value).toFixed(decimals).replace('.', ',')}`
}

/** Espace insécable : la valeur et son unité restent sur la même ligne. */
export const NBSP = String.fromCharCode(0xa0)

/** Valeur ONI avec son unité : « +2,59 °C ». */
export function formatOni(value: number, unit: string): string {
  return `${formatSigned(value)}${NBSP}${unit}`
}

/** « 1 saison », « 12 saisons ». */
export function plural(count: number, word: string): string {
  return `${count} ${word}${count > 1 ? 's' : ''}`
}
