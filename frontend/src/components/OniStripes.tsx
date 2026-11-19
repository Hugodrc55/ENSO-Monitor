import { useState } from 'react'
import { monthIndex, seasonLabel } from '../format'
import { anomalyColor } from '../palette'
import { fullSeriesPeriod } from '../period'
import { useObservations } from '../useObservations'

/**
 * Bande d'en-tête : un trait vertical par saison de la série, coloré selon
 * l'anomalie ONI. C'est une vue d'ensemble ; les valeurs exactes se lisent dans
 * la courbe et dans son tableau. Tant que les données ne sont pas là, ou en cas
 * d'erreur, une bande vide garde la place : la section suivante affiche l'erreur.
 */
export function OniStripes() {
  const [period] = useState(fullSeriesPeriod)
  const { state } = useObservations(period)
  const observations = state.status === 'success' ? state.data.observations : []
  const first = observations[0]
  const last = observations.at(-1)

  if (first === undefined || last === undefined) {
    return <div className="stripes stripes-pending" aria-hidden="true" />
  }

  // Une unité de largeur par mois : un mois manquant laisserait un vide visible.
  const origin = monthIndex(first.reference_month)
  const width = monthIndex(last.reference_month) - origin + 1

  return (
    <figure className="stripes">
      <svg viewBox={`0 0 ${width} 1`} preserveAspectRatio="none" aria-hidden="true" focusable="false">
        {observations.map((observation) => (
          <rect
            key={observation.reference_month}
            x={monthIndex(observation.reference_month) - origin}
            y={0}
            width={1.05}
            height={1}
            fill={anomalyColor(observation.oni)}
          />
        ))}
      </svg>
      <figcaption>
        <span className="stripes-end">{seasonLabel(first)}</span>
        <span className="stripes-legend">
          Une bande par saison : <span className="key key-cool" aria-hidden="true" />
          bleu si l’anomalie est négative, <span className="key key-warm" aria-hidden="true" />
          rouge si elle est positive. Plus la teinte est foncée, plus l’écart est grand.
        </span>
        <span className="stripes-end">{seasonLabel(last)}</span>
      </figcaption>
    </figure>
  )
}
