from fastapi import APIRouter, status

from app.api.dependencies import ActivityServiceDependency
from app.api.error_handlers import NOT_FOUND_RESPONSE
from app.schemas.activity import ActivityRequest, ActivityResponse

router = APIRouter(prefix="/projects/{project_id}/activities", tags=["Actividades"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=NOT_FOUND_RESPONSE,
    summary="Crear actividad",
    description="Agrega una actividad al proyecto y retorna sus indicadores EVM calculados.",
)
def create_activity(
    project_id: int, request: ActivityRequest, service: ActivityServiceDependency
) -> ActivityResponse:
    return service.add_activity(project_id, request)


@router.put(
    "/{activity_id}",
    responses=NOT_FOUND_RESPONSE,
    summary="Editar actividad",
    description="Reemplaza los datos de la actividad y retorna sus indicadores recalculados.",
)
def update_activity(
    project_id: int,
    activity_id: int,
    request: ActivityRequest,
    service: ActivityServiceDependency,
) -> ActivityResponse:
    return service.update_activity(project_id, activity_id, request)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NOT_FOUND_RESPONSE,
    summary="Eliminar actividad",
    description="Elimina la actividad del proyecto.",
)
def delete_activity(
    project_id: int, activity_id: int, service: ActivityServiceDependency
) -> None:
    service.delete_activity(project_id, activity_id)
