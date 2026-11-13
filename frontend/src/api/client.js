const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'
const HTTP_NO_CONTENT = 204
const CONNECTION_ERROR_MESSAGE = 'No se pudo conectar con el API. ¿Está corriendo el backend?'
const GENERIC_ERROR_MESSAGE = 'Ocurrió un error inesperado.'

const FIELD_LABELS = {
  name: 'Nombre',
  description: 'Descripción',
  budget_at_completion: 'Presupuesto (BAC)',
  planned_percentage: '% planificado',
  actual_percentage: '% real',
  actual_cost: 'Costo real (AC)',
}

export async function request(path, { method = 'GET', body } = {}) {
  const options = { method }
  if (body !== undefined) {
    options.headers = { 'Content-Type': 'application/json' }
    options.body = JSON.stringify(body)
  }

  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options)
  } catch {
    throw new Error(CONNECTION_ERROR_MESSAGE)
  }

  if (!response.ok) {
    throw new Error(await readErrorMessage(response))
  }
  return response.status === HTTP_NO_CONTENT ? null : response.json()
}

async function readErrorMessage(response) {
  try {
    const payload = await response.json()
    return describeErrorDetail(payload.detail)
  } catch {
    return GENERIC_ERROR_MESSAGE
  }
}

function describeErrorDetail(detail) {
  if (!Array.isArray(detail)) {
    return detail ?? GENERIC_ERROR_MESSAGE
  }
  return detail
    .map((error) => {
      const fieldName = error.loc.at(-1)
      return `${FIELD_LABELS[fieldName] ?? fieldName}: ${error.msg}`
    })
    .join(' · ')
}
