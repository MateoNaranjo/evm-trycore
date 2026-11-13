import { getStatusDetails } from '../utils/evmInterpretation'

function StatusBadge({ status }) {
  const { label, tone } = getStatusDetails(status)
  return <span className={`badge badge--${tone}`}>{label}</span>
}

export default StatusBadge
