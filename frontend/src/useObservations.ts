import { useCallback, useEffect, useState } from 'react'
import { ApiError, fetchObservations, type ObservationsResponse, type Period } from './api'

// Au-delà, on abandonne. L'API répond 503 après 5 s si la base est injoignable :
// ce délai doit être plus long pour afficher ce message précis.
const TIMEOUT_MS = 10_000

export type ObservationsState =
  | { status: 'loading' }
  | { status: 'success'; data: ObservationsResponse }
  | { status: 'error'; message: string }

type Settled = Exclude<ObservationsState, { status: 'loading' }>

/**
 * Charge les observations d'une période et les recharge dès que la période change.
 *
 * Chaque requête est identifiée par une clé (période + tentative). Tant que la
 * réponse de la clé courante n'est pas arrivée, l'état est « loading ». Une
 * réponse arrivée trop tard, pour une ancienne période, est ignorée.
 */
export function useObservations({ start, end }: Period): {
  state: ObservationsState
  retry: () => void
} {
  const [attempt, setAttempt] = useState(0)
  const [settled, setSettled] = useState<{ key: string; state: Settled } | null>(null)
  const key = `${start}/${end}/${attempt}`

  useEffect(() => {
    const controller = new AbortController()
    let active = true
    let timedOut = false
    const timeout = window.setTimeout(() => {
      timedOut = true
      controller.abort()
    }, TIMEOUT_MS)

    fetchObservations({ start, end }, controller.signal)
      .then((data) => {
        if (active) setSettled({ key, state: { status: 'success', data } })
      })
      .catch((error: unknown) => {
        if (active) setSettled({ key, state: { status: 'error', message: describe(error, timedOut) } })
      })
      .finally(() => window.clearTimeout(timeout))

    // Nouvelle période ou démontage : la requête en cours est annulée et ignorée.
    return () => {
      active = false
      window.clearTimeout(timeout)
      controller.abort()
    }
  }, [key, start, end])

  const retry = useCallback(() => setAttempt((previous) => previous + 1), [])
  const state: ObservationsState = settled?.key === key ? settled.state : { status: 'loading' }
  return { state, retry }
}

function describe(error: unknown, timedOut: boolean): string {
  if (timedOut) return `L’API n’a pas répondu en ${TIMEOUT_MS / 1000} secondes.`
  if (error instanceof ApiError) return error.message
  // fetch rejette sans réponse HTTP : serveur arrêté, réseau coupé.
  return 'Impossible de joindre l’API. Vérifiez qu’elle est lancée, puis réessayez.'
}
