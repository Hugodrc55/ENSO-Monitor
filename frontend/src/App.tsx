import { EpisodeComparison } from './components/EpisodeComparison'
import { OniExplorer } from './components/OniExplorer'

export default function App() {
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
        <h1>Les anomalies de température du Pacifique depuis 1950.</h1>
        <p className="introduction">
          L’indice ONI de la NOAA mesure l’écart de température de surface de la mer dans la
          région Niño 3.4, au centre du Pacifique équatorial. Au-dessus de +0,5 °C, la NOAA parle
          de conditions El Niño ; au-dessous de −0,5 °C, de conditions La Niña.
        </p>

        <OniExplorer />
        <EpisodeComparison />
      </main>

      <footer>
        Projet individuel HETIC WEB3 · Données NOAA CPC, ONI ERSSTv6 · Observations passées,
        aucune prévision
      </footer>
    </>
  )
}
