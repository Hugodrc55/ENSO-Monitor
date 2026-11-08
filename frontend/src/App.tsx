import { useEffect, useState } from 'react'
import { fetchHealth } from './api'

type ConnectionState =
  | { status: 'loading' }
  | { status: 'success' }
  | { status: 'error' }

export default function App() {
  const [connection, setConnection] = useState<ConnectionState>({ status: 'loading' })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    // Une requête qui ne répond pas ne doit pas laisser l'écran en attente.
    const timeout = window.setTimeout(() => controller.abort(), 5000)
    let active = true

    fetchHealth(controller.signal)
      .then(() => {
        if (active) setConnection({ status: 'success' })
      })
      .catch(() => {
        if (active) setConnection({ status: 'error' })
      })
      .finally(() => window.clearTimeout(timeout))

    // Ignore une ancienne réponse après démontage ou nouvelle tentative.
    return () => {
      active = false
      window.clearTimeout(timeout)
      controller.abort()
    }
  }, [attempt])

  function retry() {
    setConnection({ status: 'loading' })
    setAttempt((previous) => previous + 1)
  }

  return (
    <>
      <header className="site-header">
        <a className="brand" href="/" aria-label="ENSO Monitor — accueil">
          <span className="brand-mark" aria-hidden="true">≈</span>
          ENSO Monitor
        </a>
        <span className="project-label">HETIC · WEB3</span>
      </header>

      <main>
        <p className="eyebrow">El Niño & La Niña</p>
        <h1>Un regard sur les variations du Pacifique.</h1>
        <p className="introduction">
          ENSO Monitor est un projet d’exploration des données climatiques de la NOAA.
          L’application se construit progressivement : cette première version vérifie
          la connexion au service.
        </p>

        <section className="connection-card" aria-labelledby="connection-title">
          <div className="card-heading">
            <h2 id="connection-title">État du service</h2>
            <span className="step-label">Première étape</span>
          </div>

          <div className="connection-message" role="status" aria-live="polite" aria-atomic="true">
            <span className={`status-dot ${connection.status}`} aria-hidden="true" />
            <div>
              <p className="status-title">
                {connection.status === 'loading' && 'Connexion en cours…'}
                {connection.status === 'success' && 'Service accessible'}
                {connection.status === 'error' && 'Service indisponible'}
              </p>
              <p className="status-description">
                {connection.status === 'loading' && 'Nous vérifions la réponse du service.'}
                {connection.status === 'success' && 'La communication avec l’application fonctionne.'}
                {connection.status === 'error' && 'La connexion a échoué. Vous pouvez réessayer.'}
              </p>
            </div>
          </div>

          <button type="button" onClick={retry} disabled={connection.status === 'loading'}>
            {connection.status === 'loading' ? 'Vérification…' : 'Vérifier à nouveau'}
          </button>
        </section>

        <p className="data-note">
          Aucune observation climatique n’est encore affichée.
          La série retenue pour la suite est l’indice NOAA ONI, version ERSSTv6.
        </p>
      </main>

      <footer>Projet individuel · Développement progressif et données sourcées</footer>
    </>
  )
}
