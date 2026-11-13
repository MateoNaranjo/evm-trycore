from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.persistence.models import ActivityRecord, ProjectRecord


class ProjectRepository:
    """Acceso a datos del agregado Proyecto (un proyecto y sus actividades)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_projects(self) -> list[ProjectRecord]:
        statement = (
            select(ProjectRecord)
            .options(selectinload(ProjectRecord.activities))
            .order_by(ProjectRecord.id)
        )
        return list(self._session.scalars(statement))

    def find_project(self, project_id: int) -> ProjectRecord | None:
        return self._session.get(
            ProjectRecord, project_id, options=[selectinload(ProjectRecord.activities)]
        )

    def find_activity(self, project_id: int, activity_id: int) -> ActivityRecord | None:
        statement = select(ActivityRecord).where(
            ActivityRecord.id == activity_id, ActivityRecord.project_id == project_id
        )
        return self._session.scalars(statement).first()

    def save(self, record: ProjectRecord | ActivityRecord) -> None:
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

    def delete(self, record: ProjectRecord | ActivityRecord) -> None:
        self._session.delete(record)
        self._session.commit()
