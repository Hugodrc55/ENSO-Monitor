import { useId, useState, type FormEvent } from 'react'
import type { Period } from '../api'
import { formatDate } from '../format'

type Props = {
  initial: Period
  onApply: (period: Period) => void
}

/**
 * Formulaire de période. La période n'est transmise qu'à la validation du
 * formulaire, et seulement si elle est cohérente : pas de requête à chaque
 * chiffre saisi, ni pour des dates inversées.
 */
export function PeriodFilter({ initial, onApply }: Props) {
  const [start, setStart] = useState(initial.start)
  const [end, setEnd] = useState(initial.end)
  const [error, setError] = useState<string | null>(null)
  const id = useId()

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const problem = validatePeriod(start, end)
    setError(problem)
    if (problem === null) onApply({ start, end })
  }

  const describedBy = error === null ? `${id}-hint` : `${id}-hint ${id}-error`

  return (
    // noValidate : les messages d'erreur sont ceux de l'application, en français.
    <form className="period-filter" onSubmit={submit} noValidate aria-label="Période affichée">
      <div className="field">
        <label htmlFor={`${id}-start`}>Début</label>
        <input
          id={`${id}-start`}
          type="date"
          value={start}
          onChange={(event) => setStart(event.target.value)}
          aria-invalid={error !== null}
          aria-describedby={describedBy}
        />
      </div>
      <div className="field">
        <label htmlFor={`${id}-end`}>Fin</label>
        <input
          id={`${id}-end`}
          type="date"
          value={end}
          onChange={(event) => setEnd(event.target.value)}
          aria-invalid={error !== null}
          aria-describedby={describedBy}
        />
      </div>
      <button type="submit">Afficher</button>

      <p id={`${id}-hint`} className="field-hint">
        Bornes incluses. Une saison est retenue si son mois central commence dans la période.
      </p>
      {error !== null && (
        <p id={`${id}-error`} className="field-error" role="alert">
          {error}
        </p>
      )}
    </form>
  )
}

/** Message d'erreur, ou null si la période peut être envoyée à l'API. */
export function validatePeriod(start: string, end: string): string | null {
  // Un champ date incomplet ou invalide a pour valeur la chaîne vide.
  if (start === '' || end === '') {
    return 'Indiquez une date de début et une date de fin complètes.'
  }
  // Le format AAAA-MM-JJ se compare correctement comme du texte.
  if (start > end) {
    return `La date de début (${formatDate(start)}) est postérieure à la date de fin (${formatDate(end)}).`
  }
  return null
}
