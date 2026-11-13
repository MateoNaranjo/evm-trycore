import { useCallback } from 'react'

import { getProject, listProjects } from '../api/projects'
import { useResource } from './useResource'

export function useProjects() {
  return useResource(listProjects)
}

export function useProjectDetail(projectId) {
  const load = useCallback(
    () => (projectId === null ? Promise.resolve(null) : getProject(projectId)),
    [projectId],
  )
  return useResource(load)
}
