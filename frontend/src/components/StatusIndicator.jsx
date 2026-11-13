import { getStatusDetails } from '../utils/evmInterpretation'
import { formatIndex } from '../utils/format'
import StatusBadge from './StatusBadge'

function StatusIndicator({ title, index, status, description }) {
  const { tone } = getStatusDetails(status)
  return (
    <article className={`indicator indicator--${tone}`}>
      <header className="indicator__header">
        <h3>{title}</h3>
        <StatusBadge status={status} />
      </header>
      <p className="indicator__value">{formatIndex(index)}</p>
      <p className="indicator__description">{description}</p>
    </article>
  )
}

export default StatusIndicator
