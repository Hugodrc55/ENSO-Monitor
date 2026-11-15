import type { Observation, Period } from '../api'
import { NBSP, formatMonthLong, formatOni, formatSigned, plural, seasonLabel } from '../format'
import { NOAA_THRESHOLD, isCold, isWarm, longestRun, summarize, type PeriodSummary } from '../stats'
import { useObservations } from '../useObservations'

type Episode = {
  title: string
  period: Period
  /** Condition de dépassement du seuil NOAA pour la phase de l'épisode. */
  beyond: (value: number) => boolean
  /** Seuil affiché, sans unité. */
  threshold: string
}

/*
 * Fenêtres de 12 saisons, de mai à avril : dates de référence des saisons AMJ à
 * MAM. Ce sont des fenêtres choisies pour ce projet, pas les dates officielles
 * de début et de fin des épisodes. Justification : docs/DECISIONS.md, D29.
 */
export const EL_NINO: Episode = {
  title: 'El Niño 1997-1998',
  period: { start: '1997-05-01', end: '1998-04-01' },
  beyond: isWarm,
  threshold: `≥ ${formatSigned(NOAA_THRESHOLD, 1)}`,
}
export const LA_NINA: Episode = {
  title: 'La Niña 1988-1989',
  period: { start: '1988-05-01', end: '1989-04-01' },
  beyond: isCold,
  threshold: `≤ ${formatSigned(-NOAA_THRESHOLD, 1)}`,
}

type Analysis = {
  summary: PeriodSummary | null
  /** Plus longue suite de saisons consécutives au-delà du seuil. */
  run: number
}

function analyse(episode: Episode, observations: readonly Observation[]): Analysis {
  return { summary: summarize(observations), run: longestRun(observations, episode.beyond) }
}

/** Deux épisodes historiques, chacun chargé depuis l'API ; les valeurs sont calculées ici. */
export function EpisodeComparison() {
  const warm = useObservations(EL_NINO.period)
  const cold = useObservations(LA_NINA.period)

  function retry() {
    warm.retry()
    cold.retry()
  }

  const loading = warm.state.status === 'loading' || cold.state.status === 'loading'
  const failed = [warm.state, cold.state].find((state) => state.status === 'error')

  let content
  if (failed?.status === 'error') {
    content = (
      <>
        <p className="load-status error" role="status">
          Comparaison indisponible : {failed.message}
        </p>
        <button type="button" onClick={retry}>
          Réessayer
        </button>
      </>
    )
  } else if (warm.state.status === 'success' && cold.state.status === 'success') {
    const unit = warm.state.data.series.unit
    content = (
      <ComparisonResult
        warm={analyse(EL_NINO, warm.state.data.observations)}
        cold={analyse(LA_NINA, cold.state.data.observations)}
        unit={unit}
      />
    )
  } else {
    content = (
      <p className="load-status loading" role="status">
        Chargement de la comparaison…
      </p>
    )
  }

  return (
    <section className="card" aria-labelledby="comparison-title" aria-busy={loading}>
      <h2 id="comparison-title">Deux épisodes comparés</h2>
      <p>
        <strong>Pourquoi ces périodes ?</strong> Ce sont deux épisodes marqués de la série, à neuf
        ans d’écart, l’un chaud et l’autre froid. Chaque fenêtre couvre douze saisons, de mai à
        avril, pour encadrer le pic de fin d’année. Ces fenêtres sont un choix de ce projet : ce ne
        sont pas les dates officielles de début et de fin des épisodes.
      </p>
      {content}
    </section>
  )
}

function ComparisonResult({ warm, cold, unit }: { warm: Analysis; cold: Analysis; unit: string }) {
  const columns: [Episode, Analysis][] = [
    [EL_NINO, warm],
    [LA_NINA, cold],
  ]
  const rows: { label: string; cell: (episode: Episode, analysis: Analysis) => string }[] = [
    {
      label: 'Fenêtre analysée (mois centraux)',
      cell: (episode) =>
        `${formatMonthLong(episode.period.start)} à ${formatMonthLong(episode.period.end)}`,
    },
    {
      label: 'Saisons disponibles',
      cell: (_, { summary }) =>
        summary === null
          ? 'Aucune'
          : `${summary.count} (${seasonLabel(summary.first)} à ${seasonLabel(summary.last)})`,
    },
    {
      label: 'Anomalie la plus élevée',
      cell: (_, { summary }) =>
        summary === null
          ? '—'
          : `${formatOni(summary.highest.oni, unit)} (${seasonLabel(summary.highest)})`,
    },
    {
      label: 'Anomalie la plus basse',
      cell: (_, { summary }) =>
        summary === null
          ? '—'
          : `${formatOni(summary.lowest.oni, unit)} (${seasonLabel(summary.lowest)})`,
    },
    {
      label: 'Plus longue suite au-delà du seuil NOAA',
      cell: (episode, { run }) => `${plural(run, 'saison')} d’affilée (${episode.threshold}${NBSP}${unit})`,
    },
  ]

  return (
    <>
      <div className="table-wrap">
        <table className="comparison">
          <caption>Valeurs calculées à partir des observations renvoyées par l’API</caption>
          <thead>
            <tr>
              <th scope="col">Indicateur</th>
              {columns.map(([episode]) => (
                <th scope="col" key={episode.title}>
                  {episode.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.label}>
                <th scope="row">{row.label}</th>
                {columns.map(([episode, analysis]) => (
                  <td key={episode.title}>{row.cell(episode, analysis)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3>Ce que l’on observe</h3>
      <p>{describe(warm, cold, unit)}</p>

      <h3>Limites de la comparaison</h3>
      <p>
        Chaque anomalie est calculée par rapport à une période de référence de 30 ans, mise à jour
        tous les 5 ans : à neuf ans d’écart, les deux épisodes n’ont pas la même référence, et
        leurs amplitudes ne se comparent qu’approximativement. Les saisons glissantes se
        chevauchent : douze valeurs ne sont pas douze mesures indépendantes. Enfin, l’ONI décrit
        seulement la température de surface d’une région du Pacifique, sans les pluies ni les
        impacts, et deux épisodes ne permettent aucune généralisation.
      </p>
    </>
  )
}

/** Phrases construites à partir des valeurs calculées : aucun chiffre n'est écrit en dur. */
function describe(warm: Analysis, cold: Analysis, unit: string): string {
  if (warm.summary === null || cold.summary === null) {
    return 'Une des deux fenêtres ne contient aucune saison : la comparaison n’est pas possible.'
  }
  const peak = warm.summary.highest
  const trough = cold.summary.lowest
  const stronger =
    Math.abs(peak.oni) > Math.abs(trough.oni)
      ? `l’écart le plus fort est celui de l’épisode chaud`
      : Math.abs(peak.oni) < Math.abs(trough.oni)
        ? `l’écart le plus fort est celui de l’épisode froid`
        : 'les deux écarts extrêmes sont égaux'

  return (
    `L’ONI culmine à ${formatOni(peak.oni, unit)} (${seasonLabel(peak)}) pendant ${EL_NINO.title} ` +
    `et descend jusqu’à ${formatOni(trough.oni, unit)} (${seasonLabel(trough)}) pendant ${LA_NINA.title}. ` +
    `Le seuil est franchi ${plural(warm.run, 'saison')} d’affilée pour le premier et ` +
    `${plural(cold.run, 'saison')} d’affilée pour le second ; la NOAA en exige au moins 5 ` +
    `pour parler d’épisode. En valeur absolue, ${stronger}.`
  )
}
