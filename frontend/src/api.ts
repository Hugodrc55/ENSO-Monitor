// Contrat de GET /api/v1/observations (backend/app/observations.py).

export type Period = {
  /** Début inclus, au format AAAA-MM-JJ. */
  start: string
  /** Fin incluse, au format AAAA-MM-JJ. */
  end: string
}

export type Observation = {
  /** 1er jour du mois central de la saison, au format AAAA-MM-JJ. */
  reference_month: string
  /** Code NOAA de la saison glissante de trois mois, par exemple NDJ. */
  season: string
  /** Année NOAA de la saison : celle du mois central. */
  year: number
  /** Anomalie ONI en °C, deux décimales. */
  oni: number
}

export type SeriesInfo = {
  code: string
  name: string
  version: string
  unit: string
  source: string
}

export type ObservationsResponse = {
  series: SeriesInfo
  start: string
  end: string
  observations: Observation[]
}

/** Erreur à afficher telle quelle : le message est rédigé pour l'utilisateur. */
export class ApiError extends Error {
  readonly status: number | null

  constructor(message: string, status: number | null = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function fetchObservations(
  period: Period,
  signal: AbortSignal,
): Promise<ObservationsResponse> {
  const query = new URLSearchParams({ start: period.start, end: period.end })
  const response = await fetch(`/api/v1/observations?${query.toString()}`, { signal })

  // Une erreur peut arriver sans corps JSON (proxy, serveur arrêté).
  const body: unknown = await response.json().catch(() => null)

  if (!response.ok) {
    throw new ApiError(describeHttpError(response.status, body), response.status)
  }

  const data = parseObservationsResponse(body)
  if (data === null) {
    throw new ApiError('La réponse de l’API n’a pas le format attendu.')
  }
  return data
}

function describeHttpError(status: number, body: unknown): string {
  if (status === 503) {
    return 'L’API répond, mais la base de données est indisponible.'
  }
  // FastAPI renvoie `detail` : une phrase pour nos erreurs, une liste pour celles de Pydantic.
  if (isRecord(body) && typeof body.detail === 'string') {
    return body.detail
  }
  if (status >= 500) {
    return `L’API est injoignable ou en erreur (code HTTP ${status}).`
  }
  return `L’API a refusé la demande (code HTTP ${status}).`
}

// TypeScript ne vérifie pas le JSON reçu sur le réseau : on le contrôle ici.

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function isIsoDate(value: unknown): value is string {
  return typeof value === 'string' && ISO_DATE.test(value)
}

function parseSeries(value: unknown): SeriesInfo | null {
  if (!isRecord(value)) return null
  const { code, name, version, unit, source } = value
  if (
    typeof code !== 'string' ||
    typeof name !== 'string' ||
    typeof version !== 'string' ||
    typeof unit !== 'string' ||
    typeof source !== 'string'
  ) {
    return null
  }
  return { code, name, version, unit, source }
}

function parseObservation(value: unknown): Observation | null {
  if (!isRecord(value)) return null
  const { reference_month, season, year, oni } = value
  if (
    !isIsoDate(reference_month) ||
    typeof season !== 'string' ||
    typeof year !== 'number' ||
    typeof oni !== 'number' ||
    !Number.isFinite(oni)
  ) {
    return null
  }
  return { reference_month, season, year, oni }
}

function parseObservationsResponse(value: unknown): ObservationsResponse | null {
  if (!isRecord(value) || !Array.isArray(value.observations)) return null
  const series = parseSeries(value.series)
  const { start, end } = value
  if (series === null || !isIsoDate(start) || !isIsoDate(end)) return null

  const observations: Observation[] = []
  for (const item of value.observations) {
    const observation = parseObservation(item)
    if (observation === null) return null
    observations.push(observation)
  }
  return { series, start, end, observations }
}
