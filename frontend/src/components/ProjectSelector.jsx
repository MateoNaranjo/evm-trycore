import { useState } from 'react'

const EMPTY_PROJECT = { name: '', description: '' }

function ProjectSelector({ projects, selectedProjectId, onSelect, onCreate, onDelete }) {
  const [newProject, setNewProject] = useState(EMPTY_PROJECT)

  function updateField(event) {
    const { name, value } = event.target
    setNewProject((previous) => ({ ...previous, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const wasCreated = await onCreate({
      name: newProject.name,
      description: newProject.description || null,
    })
    if (wasCreated) {
      setNewProject(EMPTY_PROJECT)
    }
  }

  return (
    <section className="panel project-selector">
      <div className="project-selector__current">
        <label htmlFor="project">Proyecto</label>
        <select
          id="project"
          value={selectedProjectId ?? ''}
          onChange={(event) => onSelect(Number(event.target.value))}
          disabled={projects.length === 0}
        >
          {projects.length === 0 && <option value="">No hay proyectos</option>}
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name} ({project.activity_count} actividades)
            </option>
          ))}
        </select>
        <button
          type="button"
          className="button button--danger"
          onClick={onDelete}
          disabled={selectedProjectId === null}
        >
          Eliminar proyecto
        </button>
      </div>

      <form className="project-selector__form" onSubmit={handleSubmit}>
        <input
          name="name"
          placeholder="Nombre del nuevo proyecto"
          value={newProject.name}
          onChange={updateField}
          required
        />
        <input
          name="description"
          placeholder="Descripción (opcional)"
          value={newProject.description}
          onChange={updateField}
        />
        <button type="submit" className="button">
          Crear proyecto
        </button>
      </form>
    </section>
  )
}

export default ProjectSelector
