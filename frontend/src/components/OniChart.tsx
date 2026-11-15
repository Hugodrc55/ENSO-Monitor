import {
  useEffect,
  useRef,
  useState,
  type KeyboardEvent,
  type PointerEvent,
  type RefObject,
} from 'react'
import type { Observation } from '../api'
import { formatMonth, formatOni, formatSigned, monthIndex, seasonLabel, seasonMonths } from '../format'
import { NOAA_THRESHOLD } from '../stats'

type Props = {
  observations: readonly Observation[]
  unit: string
}

const MARGIN = { top: 28, right: 20, bottom: 44, left: 48 }
// Pas possibles entre deux graduations horizontales, en mois.
const MONTH_STEPS = [1, 3, 6, 12, 24, 60, 120, 240]
const MIN_TICK_SPACING = 72 // px

/**
 * Courbe de l'anomalie ONI, dessinée en SVG.
 *
 * Un point = une saison glissante de trois mois, placée à son mois central.
 * La saison sélectionnée se choisit à la souris, au doigt ou au clavier
 * (comportement d'un curseur ARIA, role="slider").
 */
export function OniChart({ observations, unit }: Props) {
  const surfaceRef = useRef<HTMLDivElement>(null)
  const width = useElementWidth(surfaceRef, 720)
  const height = width < 480 ? 240 : 300
  // Par défaut, la saison la plus récente de la période.
  const [selected, setSelected] = useState(observations.length - 1)

  const left = MARGIN.left
  const right = width - MARGIN.right
  const top = MARGIN.top
  const bottom = height - MARGIN.bottom

  // Axe horizontal : rang du mois central de chaque saison.
  const months = observations.map((observation) => monthIndex(observation.reference_month))
  const firstMonth = months[0] ?? 0
  const lastMonth = months.at(-1) ?? firstMonth
  const span = lastMonth - firstMonth
  const x = (month: number) =>
    span === 0 ? (left + right) / 2 : left + ((month - firstMonth) / span) * (right - left)

  // Axe vertical : toujours au moins de −1 à +1 °C, pour que 0 et les seuils restent visibles.
  const values = observations.map((observation) => observation.oni)
  const yMin = Math.floor(Math.min(-1, ...values) * 2) / 2
  const yMax = Math.ceil(Math.max(1, ...values) * 2) / 2
  const y = (value: number) => bottom - ((value - yMin) / (yMax - yMin)) * (bottom - top)

  const yStep = yMax - yMin > 3 ? 1 : 0.5
  const yTicks = integersBetween(Math.ceil(yMin / yStep), Math.floor(yMax / yStep)).map(
    (k) => k * yStep,
  )

  const monthStep =
    MONTH_STEPS.find((step) => ((right - left) * step) / Math.max(span, 1) >= MIN_TICK_SPACING) ??
    240
  const xTicks: number[] = []
  for (let month = Math.ceil(firstMonth / monthStep) * monthStep; month <= lastMonth; month += monthStep) {
    xTicks.push(month)
  }
  const xLabel = (month: number) =>
    monthStep >= 12 ? String(Math.floor(month / 12)) : formatMonth(month)

  const points = observations.map((observation, i) => ({
    month: months[i] ?? firstMonth,
    value: observation.oni,
  }))
  const line = points
    .map((point, i) => `${i === 0 ? 'M' : 'L'}${x(point.month).toFixed(1)},${y(point.value).toFixed(1)}`)
    .join('')
  const areas = signedAreas(points, x, y)

  const current = observations[selected]
  const valueText = current
    ? `${seasonLabel(current)} (${seasonMonths(current)}) : ${formatOni(current.oni, unit)}`
    : ''

  function selectAt(clientX: number, svg: SVGSVGElement) {
    const rect = svg.getBoundingClientRect()
    if (rect.width === 0) return
    const px = ((clientX - rect.left) * width) / rect.width
    const month = firstMonth + ((px - left) / (right - left)) * span
    setSelected(nearestIndex(months, month))
  }

  function onPointer(event: PointerEvent<SVGSVGElement>) {
    selectAt(event.clientX, event.currentTarget)
  }

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const last = observations.length - 1
    const moves: Record<string, number> = {
      ArrowLeft: selected - 1,
      ArrowDown: selected - 1,
      ArrowRight: selected + 1,
      ArrowUp: selected + 1,
      PageDown: selected - 12,
      PageUp: selected + 12,
      Home: 0,
      End: last,
    }
    const next = moves[event.key]
    if (next === undefined) return
    event.preventDefault()
    setSelected(Math.min(Math.max(next, 0), last))
  }

  return (
    <div className="chart">
      <p className="chart-readout" aria-hidden="true">
        {valueText}
      </p>
      <div
        ref={surfaceRef}
        className="chart-surface"
        role="slider"
        tabIndex={0}
        aria-label="Saison sélectionnée sur la courbe"
        aria-valuemin={0}
        aria-valuemax={observations.length - 1}
        aria-valuenow={selected}
        aria-valuetext={valueText}
        onKeyDown={onKeyDown}
      >
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          aria-hidden="true"
          focusable="false"
          onPointerDown={onPointer}
          onPointerMove={onPointer}
        >
          {/* Graduations et grille verticales */}
          {yTicks.map((tick) => (
            <g key={`y${tick}`}>
              <line className="grid" x1={left} x2={right} y1={y(tick)} y2={y(tick)} />
              <text className="tick" x={left - 8} y={y(tick)} dy="0.32em" textAnchor="end">
                {tick === 0 ? '0' : formatSigned(tick, 1)}
              </text>
            </g>
          ))}
          <text className="axis-title" x={left - 40} y={14}>
            Anomalie ONI ({unit})
          </text>

          {/* Graduations horizontales */}
          {xTicks.map((tick) => (
            <g key={`x${tick}`}>
              <line className="tick-mark" x1={x(tick)} x2={x(tick)} y1={bottom} y2={bottom + 5} />
              <text className="tick" x={x(tick)} y={bottom + 18} textAnchor="middle">
                {xLabel(tick)}
              </text>
            </g>
          ))}
          <text className="axis-title" x={(left + right) / 2} y={height - 6} textAnchor="middle">
            Mois central de la saison
          </text>

          {/* Surfaces au-dessus et au-dessous de 0, puis zéro et seuils NOAA */}
          <path className="area-warm" d={areas.warm} />
          <path className="area-cool" d={areas.cool} />
          <line className="zero" x1={left} x2={right} y1={y(0)} y2={y(0)} />
          <line className="threshold-warm" x1={left} x2={right} y1={y(NOAA_THRESHOLD)} y2={y(NOAA_THRESHOLD)} />
          <line className="threshold-cool" x1={left} x2={right} y1={y(-NOAA_THRESHOLD)} y2={y(-NOAA_THRESHOLD)} />

          <path className="series" d={line} />
          {/* Avec peu de saisons, chaque point est visible. */}
          {points.length <= 60 &&
            points.map((point) => (
              <circle key={point.month} className="point" cx={x(point.month)} cy={y(point.value)} r={2.5} />
            ))}

          {current && (
            <g className="cursor">
              <line x1={x(months[selected] ?? firstMonth)} x2={x(months[selected] ?? firstMonth)} y1={top} y2={bottom} />
              <circle cx={x(months[selected] ?? firstMonth)} cy={y(current.oni)} r={4.5} />
            </g>
          )}
        </svg>
      </div>
      <p className="chart-help">
        Survolez ou touchez la courbe. Au clavier, placez-y le focus : flèches pour changer de
        saison, Pg↑ et Pg↓ pour un an, Début et Fin pour les extrémités.
      </p>
    </div>
  )
}

/** Largeur réelle de l'élément, suivie au redimensionnement. */
function useElementWidth(ref: RefObject<HTMLElement | null>, fallback: number): number {
  const [width, setWidth] = useState(fallback)
  useEffect(() => {
    const element = ref.current
    // Absent du DOM simulé des tests : on garde la largeur par défaut.
    if (element === null || typeof ResizeObserver === 'undefined') return
    const observer = new ResizeObserver((entries) => {
      const measured = entries[0]?.contentRect.width ?? 0
      if (measured > 0) setWidth(Math.round(measured))
    })
    observer.observe(element)
    return () => observer.disconnect()
  }, [ref])
  return width
}

function integersBetween(from: number, to: number): number[] {
  const result: number[] = []
  for (let k = from; k <= to; k += 1) result.push(k)
  return result
}

function nearestIndex(months: readonly number[], month: number): number {
  let best = 0
  months.forEach((candidate, i) => {
    if (Math.abs(candidate - month) < Math.abs((months[best] ?? candidate) - month)) best = i
  })
  return best
}

type Point = { month: number; value: number }

/**
 * Contours des surfaces chaude (au-dessus de 0) et froide (au-dessous).
 * Quand la courbe traverse 0 entre deux saisons, le point de passage est
 * interpolé, pour que chaque surface s'arrête exactement sur l'axe.
 */
function signedAreas(
  points: readonly Point[],
  x: (month: number) => number,
  y: (value: number) => number,
): { warm: string; cool: string } {
  const withCrossings: Point[] = []
  points.forEach((point, i) => {
    const previous = points[i - 1]
    if (previous && previous.value * point.value < 0) {
      const t = previous.value / (previous.value - point.value)
      withCrossings.push({ month: previous.month + t * (point.month - previous.month), value: 0 })
    }
    withCrossings.push(point)
  })

  const first = withCrossings[0]
  const last = withCrossings.at(-1)
  if (!first || !last) return { warm: '', cool: '' }

  const outline = (clamp: (value: number) => number) =>
    `M${x(first.month)},${y(0)}` +
    withCrossings.map((point) => `L${x(point.month).toFixed(1)},${y(clamp(point.value)).toFixed(1)}`).join('') +
    `L${x(last.month)},${y(0)}Z`

  return {
    warm: outline((value) => Math.max(value, 0)),
    cool: outline((value) => Math.min(value, 0)),
  }
}
