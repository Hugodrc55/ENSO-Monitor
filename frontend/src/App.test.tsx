import { cleanup, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { Observation } from './api'
import App from './App'

// Parcours de l'interface avec une API simulée. Les valeurs ci-dessous sont
// FICTIVES, choisies pour le test : ce ne sont pas des observations NOAA.

const SEASONS = ['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ']

function season(referenceMonth: string, oni: number): Observation {
  return {
    reference_month: referenceMonth,
    season: SEASONS[Number(referenceMonth.slice(5, 7)) - 1] ?? '',
    year: Number(referenceMonth.slice(0, 4)),
    oni,
  }
}

const FICTIVE_OBSERVATIONS: Observation[] = [
  season('1988-05-01', -0.2),
  season('1988-06-01', -0.6),
  season('1988-07-01', -0.9),
  season('1988-08-01', -1.4),
  season('1988-09-01', -1.1),
  season('1988-10-01', -0.7),
  season('1997-05-01', 0.4),
  season('1997-06-01', 0.8),
  season('1997-07-01', 1.3),
  season('1997-08-01', 1.9),
  season('1997-09-01', 1.6),
  season('1997-10-01', 1.2),
  season('2015-07-01', 0.31),
  season('2015-12-01', 1.11),
  season('2016-02-01', 0.77),
]

const FICTIVE_SERIES = {
  code: 'ONI_ERSSTv6',
  name: 'Oceanic Niño Index (ONI)',
  version: 'version de test',
  unit: '°C',
  source: 'Source fictive pour les tests',
}

/** Réponse de GET /api/v1/observations : observations dont la date est dans [start, end]. */
function fakeResponse(url: string): Response {
  const params = new URL(url, 'http://localhost').searchParams
  const start = params.get('start') ?? ''
  const end = params.get('end') ?? ''
  const observations = FICTIVE_OBSERVATIONS.filter(
    (observation) => observation.reference_month >= start && observation.reference_month <= end,
  )
  return new Response(JSON.stringify({ series: FICTIVE_SERIES, start, end, observations }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}

function stubApi(options: { failFirst?: boolean } = {}) {
  let online = !options.failFirst
  const fetchMock = vi.fn((input: RequestInfo | URL) =>
    online
      ? Promise.resolve(fakeResponse(String(input)))
      : Promise.reject(new TypeError('Failed to fetch')),
  )
  vi.stubGlobal('fetch', fetchMock)
  return { fetchMock, goOnline: () => (online = true) }
}

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

/** Texte ramené à des espaces simples, espaces insécables comprises. */
const clean = (value: string | null | undefined) => (value ?? '').replace(/\s+/g, ' ').trim()
const text = (element: Element | null) => clean(element?.textContent)

function explorer() {
  return screen.getByRole('region', { name: 'Anomalie ONI par saison' })
}

/** Valeur affichée dans le résumé, sous l'intitulé donné. */
function summaryValue(term: string): string {
  return text(within(explorer()).getByText(term, { selector: 'dt' }).nextElementSibling)
}

async function choosePeriod(start: string, end: string) {
  const user = userEvent.setup()
  const section = explorer()
  await user.clear(within(section).getByLabelText('Début'))
  await user.type(within(section).getByLabelText('Début'), start)
  await user.clear(within(section).getByLabelText('Fin'))
  await user.type(within(section).getByLabelText('Fin'), end)
  await user.click(within(section).getByRole('button', { name: 'Afficher' }))
  return user
}

describe('Courbe ONI filtrable', () => {
  it('recharge les observations et met à jour les valeurs affichées quand la période change', async () => {
    const { fetchMock } = stubApi()
    render(<App />)

    expect(text(within(explorer()).getByRole('status'))).toBe('Chargement des observations…')

    // Période initiale : toute la série, donc les 15 saisons fictives.
    await within(explorer()).findByText('Anomalie la plus élevée')
    expect(summaryValue('Saisons')).toBe('15')
    expect(summaryValue('Première saison')).toBe('AMJ 1988')
    expect(summaryValue('Anomalie la plus élevée')).toBe('+1,90 °C (JAS 1997)')
    expect(summaryValue('Anomalie la plus basse')).toBe('−1,40 °C (JAS 1988)')

    const user = await choosePeriod('2015-07-01', '2016-03-01')

    // Nouvelle requête avec la période saisie…
    expect(fetchMock).toHaveBeenLastCalledWith(
      '/api/v1/observations?start=2015-07-01&end=2016-03-01',
      expect.anything(),
    )
    // … et nouvelles valeurs à l'écran : résumé, courbe et tableau.
    await within(explorer()).findByText('Du 1er juillet 2015 au 1er mars 2016 : 3 saisons.')
    expect(summaryValue('Saisons')).toBe('3')
    expect(summaryValue('Première saison')).toBe('JJA 2015')
    expect(summaryValue('Dernière saison')).toBe('JFM 2016')
    expect(summaryValue('Anomalie la plus élevée')).toBe('+1,11 °C (NDJ 2015)')
    expect(summaryValue('Anomalie la plus basse')).toBe('+0,31 °C (JJA 2015)')
    expect(within(explorer()).queryByText(/1997/)).toBeNull()

    const chart = within(explorer()).getByRole('slider', { name: 'Saison sélectionnée sur la courbe' })
    expect(clean(chart.getAttribute('aria-valuetext'))).toBe('JFM 2016 (janv. 2016 – mars 2016) : +0,77 °C')
    // Au clavier, Début place le curseur sur la première saison de la nouvelle période.
    chart.focus()
    await user.keyboard('{Home}')
    expect(clean(chart.getAttribute('aria-valuetext'))).toBe('JJA 2015 (juin 2015 – août 2015) : +0,31 °C')

    await user.click(within(explorer()).getByText('Tableau des valeurs (3 saisons)'))
    const rows = within(explorer())
      .getAllByRole('row')
      .slice(1) // ligne d'en-tête
      .map((row) => Array.from(row.children).map(text).join(' | '))
    expect(rows).toEqual([
      'JJA 2015 | juin 2015 – août 2015 | +0,31',
      'NDJ 2015 | nov. 2015 – janv. 2016 | +1,11',
      'JFM 2016 | janv. 2016 – mars 2016 | +0,77',
    ])
  })

  it('refuse des dates inversées sans appeler l’API', async () => {
    const { fetchMock } = stubApi()
    render(<App />)
    await within(explorer()).findByText('Anomalie la plus élevée')
    const callsBefore = fetchMock.mock.calls.length

    await choosePeriod('2016-01-01', '2015-01-01')

    expect(text(within(explorer()).getByRole('alert'))).toBe(
      'La date de début (1er janvier 2016) est postérieure à la date de fin (1er janvier 2015).',
    )
    expect(fetchMock.mock.calls.length).toBe(callsBefore)
    expect(summaryValue('Saisons')).toBe('15')
  })

  it('signale une période sans observation', async () => {
    stubApi()
    render(<App />)
    await within(explorer()).findByText('Anomalie la plus élevée')

    await choosePeriod('1940-01-01', '1949-12-31')

    await within(explorer()).findByText(
      'Aucune saison ONI du 1er janvier 1940 au 31 décembre 1949. La série commence avec la saison DJF 1950.',
    )
    expect(within(explorer()).queryByText('Saisons', { selector: 'dt' })).toBeNull()
    expect(within(explorer()).queryByRole('slider')).toBeNull()
  })

  it('affiche une erreur réseau, puis les valeurs après « Réessayer »', async () => {
    const { goOnline } = stubApi({ failFirst: true })
    const user = userEvent.setup()
    render(<App />)

    await within(explorer()).findByText(
      'Impossible de joindre l’API. Vérifiez qu’elle est lancée, puis réessayez.',
    )
    goOnline()
    await user.click(within(explorer()).getByRole('button', { name: 'Réessayer' }))

    await within(explorer()).findByText('Anomalie la plus élevée')
    expect(summaryValue('Saisons')).toBe('15')
  })
})

describe('Comparaison de deux épisodes', () => {
  it('calcule les valeurs de chaque fenêtre à partir de la réponse de l’API', async () => {
    const { fetchMock } = stubApi()
    render(<App />)

    const section = screen.getByRole('region', { name: 'Deux épisodes comparés' })
    const table = await within(section).findByRole('table')
    const cells = (label: RegExp) =>
      within(within(table).getByRole('row', { name: label })).getAllByRole('cell').map(text)

    expect(fetchMock).toHaveBeenCalledWith('/api/v1/observations?start=1997-05-01&end=1998-04-01', expect.anything())
    expect(fetchMock).toHaveBeenCalledWith('/api/v1/observations?start=1988-05-01&end=1989-04-01', expect.anything())
    expect(cells(/^Saisons disponibles/)).toEqual(['6 (AMJ 1997 à SON 1997)', '6 (AMJ 1988 à SON 1988)'])
    expect(cells(/^Anomalie la plus élevée/)).toEqual(['+1,90 °C (JAS 1997)', '−0,20 °C (AMJ 1988)'])
    expect(cells(/^Anomalie la plus basse/)).toEqual(['+0,40 °C (AMJ 1997)', '−1,40 °C (JAS 1988)'])
    expect(cells(/^Plus longue suite/)).toEqual([
      '5 saisons d’affilée (≥ +0,5 °C)',
      '5 saisons d’affilée (≤ −0,5 °C)',
    ])
    expect(within(section).getByText(/L’ONI culmine à \+1,90/)).toBeTruthy()
  })
})
