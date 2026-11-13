from app.persistence.models import ActivityRecord
from app.persistence.project_repository import ProjectRepository
from app.schemas.activity import ActivityRequest, ActivityResponse
from app.services.evm_report import build_activity_response
from app.services.exceptions import ResourceNotFoundError


class ActivityService:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def add_activity(self, project_id: int, request: ActivityRequest) -> ActivityResponse:
        if self._repository.find_project(project_id) is None:
            raise ResourceNotFoundError.for_project(project_id)
        activity = ActivityRecord(project_id=project_id, **request.model_dump())
        self._repository.save(activity)
        return build_activity_response(activity)

    def update_activity(
        self, project_id: int, activity_id: int, request: ActivityRequest
    ) -> ActivityResponse:
        activity = self._get_existing_activity(project_id, activity_id)
        for field_name, value in request.model_dump().items():
            setattr(activity, field_name, value)
        self._repository.save(activity)
        return build_activity_response(activity)

    def delete_activity(self, project_id: int, activity_id: int) -> None:
        self._repository.delete(self._get_existing_activity(project_id, activity_id))

    def _get_existing_activity(self, project_id: int, activity_id: int) -> ActivityRecord:
        activity = self._repository.find_activity(project_id, activity_id)
        if activity is None:
            raise ResourceNotFoundError.for_activity(project_id, activity_id)
        return activity
