import { PROJECT_KPIS } from '../constants/evm'
import {
  describeCostIndex,
  describeScheduleIndex,
  summarizeProjectHealth,
} from '../utils/evmInterpretation'
import { formatMoney } from '../utils/format'
import StatusIndicator from './StatusIndicator'

function ProjectSummary({ metrics }) {
  const health = summarizeProjectHealth(metrics)

  return (
    <section className="panel">
      <h2>Indicadores del proyecto</h2>
      <p className={`health health--${health.tone}`}>{health.message}</p>

      <div className="indicators">
        <StatusIndicator
          title="CPI · Desempeño de costo"
          index={metrics.cost_performance_index}
          status={metrics.cost_status}
          description={describeCostIndex(metrics.cost_performance_index)}
        />
        <StatusIndicator
          title="SPI · Desempeño de cronograma"
          index={metrics.schedule_performance_index}
          status={metrics.schedule_status}
          description={describeScheduleIndex(metrics.schedule_performance_index)}
        />
      </div>

      <dl className="kpis">
        {PROJECT_KPIS.map(({ key, label, hint }) => (
          <div key={key} className="kpi" title={hint}>
            <dt>
              {label} <span className="kpi__hint">{hint}</span>
            </dt>
            <dd className={metrics[key] < 0 ? 'negative' : undefined}>
              {formatMoney(metrics[key])}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}

export default ProjectSummary
