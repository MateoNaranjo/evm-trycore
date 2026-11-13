import { request } from './client'

function activitiesPath(projectId) {
  return `/projects/${projectId}/activities`
}

export function createActivity(projectId, activity) {
  return request(activitiesPath(projectId), { method: 'POST', body: activity })
}

export function updateActivity(projectId, activityId, activity) {
  return request(`${activitiesPath(projectId)}/${activityId}`, { method: 'PUT', body: activity })
}

export function deleteActivity(projectId, activityId) {
  return request(`${activitiesPath(projectId)}/${activityId}`, { method: 'DELETE' })
}
