import { describe, expect, it } from 'vitest'
import { anomalyColor } from './palette'

describe('anomalyColor', () => {
  it('donne le fond de page pour une anomalie nulle', () => {
    expect(anomalyColor(0)).toBe('rgb(238, 243, 244)')
  })

  it('donne le rouge plein à +2,5 °C et le bleu plein à −2,5 °C, et pas au-delà', () => {
    expect(anomalyColor(2.5)).toBe('rgb(179, 50, 31)')
    expect(anomalyColor(3.2)).toBe('rgb(179, 50, 31)')
    expect(anomalyColor(-2.5)).toBe('rgb(31, 95, 158)')
  })

  it('fonce la teinte en proportion de l’écart', () => {
    // À mi-chemin (1,25 °C), chaque canal est à mi-chemin entre le fond et le rouge.
    expect(anomalyColor(1.25)).toBe('rgb(209, 147, 138)')
  })
})
