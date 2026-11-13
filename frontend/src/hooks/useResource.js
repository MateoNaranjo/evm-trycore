import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Carga un recurso asíncrono y expone `reload` para volver a pedirlo.
 * Si llegan respuestas fuera de orden, solo se conserva la de la última petición.
 */
export function useResource(load) {
  const [state, setState] = useState({ data: null, error: null, isLoading: true })
  const latestRequestId = useRef(0)

  const reload = useCallback(async () => {
    latestRequestId.current += 1
    const requestId = latestRequestId.current
    setState((previous) => ({ ...previous, isLoading: true }))
    try {
      const data = await load()
      if (requestId === latestRequestId.current) {
        setState({ data, error: null, isLoading: false })
      }
    } catch (error) {
      if (requestId === latestRequestId.current) {
        setState({ data: null, error: error.message, isLoading: false })
      }
    }
  }, [load])

  useEffect(() => {
    reload()
  }, [reload])

  return { ...state, reload }
}
