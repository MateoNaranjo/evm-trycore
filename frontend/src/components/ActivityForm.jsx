import { useState } from 'react'

import { MAX_PERCENTAGE, MIN_PERCENTAGE } from '../constants/evm'

const DECIMAL_STEP = '0.01'
const MIN_COST = 0

const NUMERIC_FIELDS = [
  { name: 'budget_at_completion', label: 'Presupuesto (BAC)', min: DECIMAL_STEP },
  {
    name: 'planned_percentage',
    label: '% planificado a la fecha',
    min: MIN_PERCENTAGE,
    max: MAX_PERCENTAGE,
  },
  { name: 'actual_percentage', label: '% real completado', min: MIN_PERCENTAGE, max: MAX_PERCENTAGE },
  { name: 'actual_cost', label: 'Costo real (AC)', min: MIN_COST },
]

const EMPTY_ACTIVITY = {
  name: '',
  budget_at_completion: '',
  planned_percentage: '',
  actual_percentage: '',
  actual_cost: '',
}

function toFormValues(activity) {
  if (!activity) {
    return EMPTY_ACTIVITY
  }
  return Object.fromEntries(
    Object.keys(EMPTY_ACTIVITY).map((field) => [field, String(activity[field])]),
  )
}

function toPayload(values) {
  const numericValues = NUMERIC_FIELDS.map(({ name }) => [name, Number(values[name])])
  return { name: values.name.trim(), ...Object.fromEntries(numericValues) }
}

function ActivityForm({ activity, onSubmit, onCancel }) {
  const [values, setValues] = useState(() => toFormValues(activity))
  const isEditing = Boolean(activity)

  function updateField(event) {
    const { name, value } = event.target
    setValues((previous) => ({ ...previous, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const wasSaved = await onSubmit(toPayload(values))
    if (wasSaved && !isEditing) {
      setValues(EMPTY_ACTIVITY)
    }
  }

  return (
    <form className="panel activity-form" onSubmit={handleSubmit}>
      <h2>{isEditing ? `Editar actividad: ${activity.name}` : 'Nueva actividad'}</h2>
      <div className="activity-form__fields">
        <label>
          Nombre
          <input name="name" value={values.name} onChange={updateField} required />
        </label>
        {NUMERIC_FIELDS.map(({ name, label, min, max }) => (
          <label key={name}>
            {label}
            <input
              name={name}
              type="number"
              step={DECIMAL_STEP}
              min={min}
              max={max}
              value={values[name]}
              onChange={updateField}
              required
            />
          </label>
        ))}
      </div>
      <div className="activity-form__actions">
        <button type="submit" className="button">
          {isEditing ? 'Guardar cambios' : 'Agregar actividad'}
        </button>
        {isEditing && (
          <button type="button" className="button button--secondary" onClick={onCancel}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}

export default ActivityForm
