import type { Observation } from '../api'
import { formatSigned, plural, seasonLabel, seasonMonths } from '../format'

type Props = {
  observations: readonly Observation[]
  unit: string
}

/** Les valeurs de la courbe sous forme de tableau, lisible au clavier et par un lecteur d'écran. */
export function ObservationsTable({ observations, unit }: Props) {
  return (
    <details className="values">
      <summary>Tableau des valeurs ({plural(observations.length, 'saison')})</summary>
      {/* Zone défilante : focusable pour pouvoir la faire défiler au clavier. */}
      <div className="table-scroll" tabIndex={0} role="region" aria-label="Valeurs ONI de la période">
        <table>
          <caption>Anomalie ONI par saison glissante de trois mois, en {unit}</caption>
          <thead>
            <tr>
              <th scope="col">Saison</th>
              <th scope="col">Mois moyennés</th>
              <th scope="col" className="number">ONI ({unit})</th>
            </tr>
          </thead>
          <tbody>
            {observations.map((observation) => (
              <tr key={observation.reference_month}>
                <th scope="row">{seasonLabel(observation)}</th>
                <td>{seasonMonths(observation)}</td>
                <td className="number">{formatSigned(observation.oni)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  )
}
