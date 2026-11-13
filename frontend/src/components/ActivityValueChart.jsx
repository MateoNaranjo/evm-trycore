import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import { formatCompactMoney, formatMoney } from '../utils/format'

const CHART_HEIGHT = 320

const SERIES = [
  { key: 'planned_value', name: 'PV · Planificado', color: '#94a3b8' },
  { key: 'earned_value', name: 'EV · Ganado', color: '#2563eb' },
  { key: 'actual_cost', name: 'AC · Costo real', color: '#f59e0b' },
]

function toChartData(activities) {
  return activities.map((activity) => ({
    name: activity.name,
    ...Object.fromEntries(SERIES.map(({ key }) => [key, activity.metrics[key]])),
  }))
}

function ActivityValueChart({ activities }) {
  if (activities.length === 0) {
    return null
  }

  return (
    <section className="panel">
      <h2>PV vs EV vs AC por actividad</h2>
      <p className="chart__guide">
        Si la barra naranja (AC) supera a la azul (EV), la actividad gasta más de lo que avanza. Si
        la azul (EV) es menor que la gris (PV), va atrasada.
      </p>
      <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
        <BarChart data={toChartData(activities)}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" />
          <YAxis tickFormatter={formatCompactMoney} />
          <Tooltip formatter={(value) => formatMoney(value)} />
          <Legend />
          {SERIES.map(({ key, name, color }) => (
            <Bar key={key} dataKey={key} name={name} fill={color} radius={[4, 4, 0, 0]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </section>
  )
}

export default ActivityValueChart
