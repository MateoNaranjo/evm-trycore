from fastapi import APIRouter, status

from app.api.dependencies import ProjectServiceDependency
from app.api.error_handlers import NOT_FOUND_RESPONSE
from app.schemas.project import ProjectDetailResponse, ProjectRequest, ProjectSummaryResponse

router = APIRouter(prefix="/projects", tags=["Proyectos"])


@router.get(
    "",
    summary="Listar proyectos",
    description="Retorna todos los proyectos con sus indicadores EVM consolidados.",
)
def list_projects(service: ProjectServiceDependency) -> list[ProjectSummaryResponse]:
    return service.list_projects()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Crear proyecto",
    description="Crea un proyecto sin actividades.",
)
def create_project(
    request: ProjectRequest, service: ProjectServiceDependency
) -> ProjectDetailResponse:
    return service.create_project(request)


@router.get(
    "/{project_id}",
    responses=NOT_FOUND_RESPONSE,
    summary="Consultar proyecto",
    description=(
        "Retorna el proyecto con sus actividades, los indicadores EVM de cada actividad "
        "y los indicadores consolidados del proyecto."
    ),
)
def get_project(project_id: int, service: ProjectServiceDependency) -> ProjectDetailResponse:
    return service.get_project(project_id)


@router.put(
    "/{project_id}",
    responses=NOT_FOUND_RESPONSE,
    summary="Editar proyecto",
    description="Reemplaza el nombre y la descripción del proyecto.",
)
def update_project(
    project_id: int, request: ProjectRequest, service: ProjectServiceDependency
) -> ProjectDetailResponse:
    return service.update_project(project_id, request)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NOT_FOUND_RESPONSE,
    summary="Eliminar proyecto",
    description="Elimina el proyecto y todas sus actividades.",
)
def delete_project(project_id: int, service: ProjectServiceDependency) -> None:
    service.delete_project(project_id)
