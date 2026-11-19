// Couleurs des anomalies, partagées par la bande d'en-tête et la feuille de style.

type Rgb = readonly [number, number, number]

const NEUTRAL: Rgb = [238, 243, 244] // #eef3f4, fond de page
const WARM: Rgb = [179, 50, 31] // #b3321f, El Niño
const COOL: Rgb = [31, 95, 158] // #1f5f9e, La Niña

/** Écart, en °C, à partir duquel la couleur est pleine. */
export const SATURATION = 2.5

/**
 * Couleur d'une anomalie ONI : rouge si elle est positive, bleu si elle est
 * négative, d'autant plus foncée que l'écart à 0 est grand. Interpolation linéaire
 * entre le fond de page (0 °C) et la couleur pleine (±2,5 °C et au-delà).
 */
export function anomalyColor(value: number): string {
  const t = Math.min(Math.abs(value) / SATURATION, 1)
  const end = value >= 0 ? WARM : COOL
  const mix = (i: 0 | 1 | 2) => Math.round(NEUTRAL[i] + (end[i] - NEUTRAL[i]) * t)
  return `rgb(${mix(0)}, ${mix(1)}, ${mix(2)})`
}
