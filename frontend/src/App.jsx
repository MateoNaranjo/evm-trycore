import { useState } from 'react'

import { createActivity, deleteActivity, updateActivity } from './api/activities'
import { createProject, deleteProject } from './api/projects'
import ActivityForm from './components/ActivityForm'
import ActivityTable from './components/ActivityTable'
import ActivityValueChart from './components/ActivityValueChart'
import ProjectSelector from './components/ProjectSelector'
import ProjectSummary from './components/ProjectSummary'
import { useProjectDetail, useProjects } from './hooks/useProjects'

const NEW_ACTIVITY_FORM_KEY = 'new'

function App() {
  const projects = useProjects()
  const [chosenProjectId, setChosenProjectId] = useState(null)
  const selectedProjectId = chosenProjectId ?? projects.data?.[0]?.id ?? null
  const project = useProjectDetail(selectedProjectId)
  const [editingActivity, setEditingActivity] = useState(null)
  const [actionError, setActionError] = useState(null)

  async function runAction(action, { reloadProject = true } = {}) {
    setActionError(null)
    try {
      await action()
      await Promise.all([projects.reload(), reloadProject && project.reload()])
      return true
    } catch (error) {
      setActionError(error.message)
      return false
    }
  }

  function selectProject(projectId) {
    setChosenProjectId(projectId)
    setEditingActivity(null)
  }

  function handleCreateProject(newProject) {
    return runAction(
      async () => {
        const created = await createProject(newProject)
        selectProject(created.id)
      },
      { reloadProject: false },
    )
  }

  function handleDeleteProject() {
    if (!window.confirm(`¿Eliminar el proyecto "${project.data?.name}" y todas sus actividades?`)) {
      return
    }
    runAction(
      async () => {
        await deleteProject(selectedProjectId)
        selectProject(null)
      },
      { reloadProject: false },
    )
  }

  function handleSaveActivity(activity) {
    return runAction(async () => {
      if (editingActivity) {
        await updateActivity(selectedProjectId, editingActivity.id, activity)
      } else {
        await createActivity(selectedProjectId, activity)
      }
      setEditingActivity(null)
    })
  }

  function handleDeleteActivity(activity) {
    if (!window.confirm(`¿Eliminar la actividad "${activity.name}"?`)) {
      return
    }
    runAction(async () => {
      await deleteActivity(selectedProjectId, activity.id)
      if (editingActivity?.id === activity.id) {
        setEditingActivity(null)
      }
    })
  }

  const loadError = projects.error ?? project.error

  return (
    <main className="dashboard">
      <header className="dashboard__header">
        <h1>EVM Tracker</h1>
        <p>Análisis de Valor Ganado: ¿el proyecto va bien en costo y cronograma?</p>
      </header>

      {(actionError ?? loadError) && (
        <p className="alert" role="alert">
          {actionError ?? loadError}
        </p>
      )}

      <ProjectSelector
        projects={projects.data ?? []}
        selectedProjectId={selectedProjectId}
        onSelect={selectProject}
        onCreate={handleCreateProject}
        onDelete={handleDeleteProject}
      />

      {project.data && (
        <>
          <ProjectSummary metrics={project.data.metrics} />
          <ActivityValueChart activities={project.data.activities} />
          <ActivityForm
            key={editingActivity?.id ?? NEW_ACTIVITY_FORM_KEY}
            activity={editingActivity}
            onSubmit={handleSaveActivity}
            onCancel={() => setEditingActivity(null)}
          />
          <ActivityTable
            activities={project.data.activities}
            editingActivityId={editingActivity?.id}
            onEdit={setEditingActivity}
            onDelete={handleDeleteActivity}
          />
        </>
      )}
    </main>
  )
}

export default App
