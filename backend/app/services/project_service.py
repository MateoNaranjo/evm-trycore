from app.persistence.models import ProjectRecord
from app.persistence.project_repository import ProjectRepository
from app.schemas.project import ProjectDetailResponse, ProjectRequest, ProjectSummaryResponse
from app.services.evm_report import build_project_detail, build_project_summary
from app.services.exceptions import ResourceNotFoundError


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def list_projects(self) -> list[ProjectSummaryResponse]:
        return [build_project_summary(project) for project in self._repository.list_projects()]

    def get_project(self, project_id: int) -> ProjectDetailResponse:
        return build_project_detail(self._get_existing_project(project_id))

    def create_project(self, request: ProjectRequest) -> ProjectDetailResponse:
        project = ProjectRecord(name=request.name, description=request.description)
        self._repository.save(project)
        return build_project_detail(project)

    def update_project(self, project_id: int, request: ProjectRequest) -> ProjectDetailResponse:
        project = self._get_existing_project(project_id)
        project.name = request.name
        project.description = request.description
        self._repository.save(project)
        return build_project_detail(project)

    def delete_project(self, project_id: int) -> None:
        self._repository.delete(self._get_existing_project(project_id))

    def _get_existing_project(self, project_id: int) -> ProjectRecord:
        project = self._repository.find_project(project_id)
        if project is None:
            raise ResourceNotFoundError.for_project(project_id)
        return project
