import { EpisodeComparison } from './components/EpisodeComparison'
import { OniExplorer } from './components/OniExplorer'
import { OniStripes } from './components/OniStripes'

export default function App() {
  return (
    <>
      <header className="hero">
        <div className="hero-inner">
          <div className="topbar">
            <a className="brand" href="/" aria-label="ENSO Monitor — accueil">
              <span className="brand-mark" aria-hidden="true">≈</span>
              ENSO Monitor
            </a>
            <span className="project-label">Projet HETIC WEB3</span>
          </div>

          <h1>Les anomalies de température du Pacifique depuis 1950</h1>
          <p className="introduction">
            L’indice ONI de la NOAA mesure l’écart de température de surface de la mer dans la
            région Niño 3.4, au centre du Pacifique équatorial. Au-dessus de +0,5 °C, la NOAA parle
            de conditions El Niño ; au-dessous de −0,5 °C, de conditions La Niña.
          </p>
          <OniStripes />
        </div>
      </header>

      <main>
        <OniExplorer />
        <EpisodeComparison />
      </main>

      <footer>
        <p>
          Données : NOAA Climate Prediction Center, indice ONI version ERSSTv6. Observations
          passées uniquement, sans prévision.
        </p>
        <p>Projet individuel HETIC WEB3.</p>
      </footer>
    </>
  )
}
