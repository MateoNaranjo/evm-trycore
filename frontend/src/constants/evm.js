export const MIN_PERCENTAGE = 0
export const MAX_PERCENTAGE = 100

export const TONE = {
  GOOD: 'good',
  BAD: 'bad',
  NEUTRAL: 'neutral',
}

export const NOT_AVAILABLE_STATUS = 'NOT_AVAILABLE'

export const STATUS_DETAILS = {
  UNDER_BUDGET: { label: 'Bajo presupuesto', tone: TONE.GOOD },
  ON_BUDGET: { label: 'En presupuesto', tone: TONE.GOOD },
  OVER_BUDGET: { label: 'Sobre presupuesto', tone: TONE.BAD },
  AHEAD_OF_SCHEDULE: { label: 'Adelantado', tone: TONE.GOOD },
  ON_SCHEDULE: { label: 'A tiempo', tone: TONE.GOOD },
  BEHIND_SCHEDULE: { label: 'Atrasado', tone: TONE.BAD },
  [NOT_AVAILABLE_STATUS]: { label: 'Sin datos', tone: TONE.NEUTRAL },
}

export const PROJECT_KPIS = [
  { key: 'budget_at_completion', label: 'BAC', hint: 'Presupuesto total' },
  { key: 'planned_value', label: 'PV', hint: 'Valor planificado' },
  { key: 'earned_value', label: 'EV', hint: 'Valor ganado' },
  { key: 'actual_cost', label: 'AC', hint: 'Costo real' },
  { key: 'cost_variance', label: 'CV', hint: 'Variación de costo (EV − AC)' },
  { key: 'schedule_variance', label: 'SV', hint: 'Variación de cronograma (EV − PV)' },
  { key: 'estimate_at_completion', label: 'EAC', hint: 'Costo estimado al terminar' },
  { key: 'variance_at_completion', label: 'VAC', hint: 'Desviación esperada al terminar' },
]
