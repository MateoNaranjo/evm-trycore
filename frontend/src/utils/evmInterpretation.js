import { NOT_AVAILABLE_STATUS, STATUS_DETAILS, TONE } from '../constants/evm'
import { formatMoney, formatRatioAsPercentage } from './format'

export function getStatusDetails(status) {
  return STATUS_DETAILS[status] ?? STATUS_DETAILS[NOT_AVAILABLE_STATUS]
}

export function describeCostIndex(costPerformanceIndex) {
  if (costPerformanceIndex === null) {
    return 'Aún no hay costo real registrado para comparar.'
  }
  return `Por cada $1 gastado se han generado ${formatMoney(costPerformanceIndex)} de valor.`
}

export function describeScheduleIndex(schedulePerformanceIndex) {
  if (schedulePerformanceIndex === null) {
    return 'No hay avance planificado a la fecha de corte.'
  }
  return `Se avanza al ${formatRatioAsPercentage(schedulePerformanceIndex)} del ritmo planificado.`
}

export function summarizeProjectHealth(metrics) {
  const statuses = [metrics.cost_status, metrics.schedule_status].map(getStatusDetails)
  const knownStatuses = statuses.filter((status) => status.tone !== TONE.NEUTRAL)

  if (knownStatuses.length === 0) {
    return { tone: TONE.NEUTRAL, message: 'Registra actividades con avance y costo para ver el análisis.' }
  }

  const statusText = knownStatuses.map((status) => status.label.toLowerCase()).join(' y ')
  if (knownStatuses.some((status) => status.tone === TONE.BAD)) {
    return { tone: TONE.BAD, message: `Atención: el proyecto está ${statusText}.` }
  }
  return { tone: TONE.GOOD, message: `El proyecto va bien: ${statusText}.` }
}
