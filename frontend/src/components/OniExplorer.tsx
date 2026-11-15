import { useState } from 'react'
import type { ObservationsResponse, Period } from '../api'
import { NBSP, formatDate, formatOni, formatSigned, plural, seasonLabel } from '../format'
import { NOAA_THRESHOLD, summarize } from '../stats'
import { useObservations, type ObservationsState } from '../useObservations'
import { ObservationsTable } from './ObservationsTable'
import { OniChart } from './OniChart'
import { PeriodFilter } from './PeriodFilter'

export const NOAA_ONI_PAGE =
  'https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/index.php'

/** Toute la série par défaut : la première saison, DJF 1950, a pour mois central janvier 1950. */
function defaultPeriod(): Period {
  const today = new Date()
  const pad = (n: number) => String(n).padStart(2, '0')
  return {
    start: '1950-01-01',
    end: `${today.getFullYear()}-${pad(today.getMonth() + 1)}-${pad(today.getDate())}`,
  }
}

/** Courbe filtrable : le formulaire change la période, qui déclenche un nouvel appel à l'API. */
export function OniExplorer() {
  const [period, setPeriod] = useState<Period>(defaultPeriod)
  const { state, retry } = useObservations(period)

  return (
    <section className="card" aria-labelledby="explorer-title" aria-busy={state.status === 'loading'}>
      <h2 id="explorer-title">Anomalie ONI par saison</h2>
      <PeriodFilter initial={period} onApply={setPeriod} />

      <p className={`load-status ${state.status}`} role="status">
        {statusMessage(state)}
      </p>
      {state.status === 'error' && (
        <button type="button" onClick={retry}>
          Réessayer
        </button>
      )}
      {state.status === 'success' && <Result data={state.data} />}
    </section>
  )
}

function statusMessage(state: ObservationsState): string {
  if (state.status === 'loading') return 'Chargement des observations…'
  if (state.status === 'error') return state.message
  const { start, end, observations } = state.data
  if (observations.length === 0) {
    return `Aucune saison ONI du ${formatDate(start)} au ${formatDate(end)}. La série commence avec la saison DJF 1950.`
  }
  return `Du ${formatDate(start)} au ${formatDate(end)} : ${plural(observations.length, 'saison')}.`
}

function Result({ data }: { data: ObservationsResponse }) {
  const { series, observations } = data
  const summary = summarize(observations)
  const threshold = (value: number) => `${formatSigned(value, 1)}${NBSP}${series.unit}`

  return (
    <>
      {summary !== null && (
        <>
          <dl className="summary" aria-label="Résumé de la période">
            <div>
              <dt>Saisons</dt>
              <dd>{summary.count}</dd>
            </div>
            <div>
              <dt>Première saison</dt>
              <dd>{seasonLabel(summary.first)}</dd>
            </div>
            <div>
              <dt>Dernière saison</dt>
              <dd>{seasonLabel(summary.last)}</dd>
            </div>
            <div>
              <dt>Anomalie la plus élevée</dt>
              <dd>
                {formatOni(summary.highest.oni, series.unit)} ({seasonLabel(summary.highest)})
              </dd>
            </div>
            <div>
              <dt>Anomalie la plus basse</dt>
              <dd>
                {formatOni(summary.lowest.oni, series.unit)} ({seasonLabel(summary.lowest)})
              </dd>
            </div>
          </dl>

          <figure className="chart-figure">
            {/* Rien n'est affiché pendant un chargement : chaque période crée une nouvelle
                courbe, dont la sélection part de la dernière saison. */}
            <OniChart observations={observations} unit={series.unit} />
            <ul className="legend">
              <li>
                <span className="swatch swatch-series" aria-hidden="true" />
                Anomalie ONI : un point par saison glissante de trois mois, placé au mois central
                (pas une mesure quotidienne)
              </li>
              <li>
                <span className="swatch swatch-warm" aria-hidden="true" />
                Seuil El Niño : {threshold(NOAA_THRESHOLD)}
              </li>
              <li>
                <span className="swatch swatch-cool" aria-hidden="true" />
                Seuil La Niña : {threshold(-NOAA_THRESHOLD)}
              </li>
            </ul>
            <figcaption>
              Selon la NOAA, un épisode El Niño ou La Niña exige au moins 5 saisons consécutives
              au-delà du seuil.
            </figcaption>
          </figure>
        </>
      )}

      <p className="source">
        <strong>Source :</strong> {series.source}. Série {series.name}, version {series.version}.
        Valeurs en {series.unit} à deux décimales, telles que publiées par la NOAA.{' '}
        <a href={NOAA_ONI_PAGE}>Page ONI v6 de la NOAA</a>
      </p>

      {summary !== null && <ObservationsTable observations={observations} unit={series.unit} />}
    </>
  )
}
