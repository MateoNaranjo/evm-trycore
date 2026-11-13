from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.persistence.project_repository import ProjectRepository
from app.services.activity_service import ActivityService
from app.services.project_service import ProjectService

DbSession = Annotated[Session, Depends(get_db_session)]


def get_project_service(session: DbSession) -> ProjectService:
    return ProjectService(ProjectRepository(session))


def get_activity_service(session: DbSession) -> ActivityService:
    return ActivityService(ProjectRepository(session))


ProjectServiceDependency = Annotated[ProjectService, Depends(get_project_service)]
ActivityServiceDependency = Annotated[ActivityService, Depends(get_activity_service)]
