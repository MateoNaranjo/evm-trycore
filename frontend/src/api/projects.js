import { request } from './client'

export function listProjects() {
  return request('/projects')
}

export function getProject(projectId) {
  return request(`/projects/${projectId}`)
}

export function createProject(project) {
  return request('/projects', { method: 'POST', body: project })
}

export function deleteProject(projectId) {
  return request(`/projects/${projectId}`, { method: 'DELETE' })
}
