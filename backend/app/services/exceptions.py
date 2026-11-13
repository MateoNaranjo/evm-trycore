PROJECT_NOT_FOUND_MESSAGE = "Proyecto {project_id} no existe."
ACTIVITY_NOT_FOUND_MESSAGE = "Actividad {activity_id} no existe en el proyecto {project_id}."


class ResourceNotFoundError(Exception):
    """Se lanza cuando el recurso solicitado no existe."""

    @classmethod
    def for_project(cls, project_id: int) -> "ResourceNotFoundError":
        return cls(PROJECT_NOT_FOUND_MESSAGE.format(project_id=project_id))

    @classmethod
    def for_activity(cls, project_id: int, activity_id: int) -> "ResourceNotFoundError":
        return cls(
            ACTIVITY_NOT_FOUND_MESSAGE.format(project_id=project_id, activity_id=activity_id)
        )
