import { formatIndex, formatMoney, formatPercentage } from '../utils/format'
import { getStatusDetails } from '../utils/evmInterpretation'

const MONEY_METRIC_COLUMNS = [
  { key: 'planned_value', label: 'PV' },
  { key: 'earned_value', label: 'EV' },
  { key: 'cost_variance', label: 'CV' },
  { key: 'schedule_variance', label: 'SV' },
]

const INDEX_COLUMNS = [
  { key: 'cost_performance_index', statusKey: 'cost_status', label: 'CPI' },
  { key: 'schedule_performance_index', statusKey: 'schedule_status', label: 'SPI' },
]

const FORECAST_COLUMNS = [
  { key: 'estimate_at_completion', label: 'EAC' },
  { key: 'variance_at_completion', label: 'VAC' },
]

function MoneyCell({ value }) {
  return <td className={value < 0 ? 'number negative' : 'number'}>{formatMoney(value)}</td>
}

function IndexCell({ value, status }) {
  const { label, tone } = getStatusDetails(status)
  return (
    <td className={`number index index--${tone}`} title={label}>
      {formatIndex(value)}
    </td>
  )
}

function ActivityTable({ activities, editingActivityId, onEdit, onDelete }) {
  if (activities.length === 0) {
    return (
      <section className="panel">
        <h2>Actividades</h2>
        <p className="empty">Este proyecto aún no tiene actividades.</p>
      </section>
    )
  }

  return (
    <section className="panel">
      <h2>Actividades</h2>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Actividad</th>
              <th>BAC</th>
              <th>% plan</th>
              <th>% real</th>
              <th>AC</th>
              {[...MONEY_METRIC_COLUMNS, ...INDEX_COLUMNS, ...FORECAST_COLUMNS].map(
                ({ key, label }) => (
                  <th key={key}>{label}</th>
                ),
              )}
              <th aria-label="Acciones" />
            </tr>
          </thead>
          <tbody>
            {activities.map((activity) => (
              <tr
                key={activity.id}
                className={activity.id === editingActivityId ? 'row--editing' : undefined}
              >
                <td>{activity.name}</td>
                <MoneyCell value={activity.budget_at_completion} />
                <td className="number">{formatPercentage(activity.planned_percentage)}</td>
                <td className="number">{formatPercentage(activity.actual_percentage)}</td>
                <MoneyCell value={activity.actual_cost} />
                {MONEY_METRIC_COLUMNS.map(({ key }) => (
                  <MoneyCell key={key} value={activity.metrics[key]} />
                ))}
                {INDEX_COLUMNS.map(({ key, statusKey }) => (
                  <IndexCell
                    key={key}
                    value={activity.metrics[key]}
                    status={activity.metrics[statusKey]}
                  />
                ))}
                {FORECAST_COLUMNS.map(({ key }) => (
                  <MoneyCell key={key} value={activity.metrics[key]} />
                ))}
                <td className="actions">
                  <button type="button" className="button button--small" onClick={() => onEdit(activity)}>
                    Editar
                  </button>
                  <button
                    type="button"
                    className="button button--small button--danger"
                    onClick={() => onDelete(activity)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default ActivityTable
