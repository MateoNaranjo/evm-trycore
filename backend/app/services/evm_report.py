"""Construye las respuestas del API combinando los datos persistidos con los indicadores EVM."""

from app.domain.evm import (
    ActivityProgress,
    EvmMetrics,
    calculate_activity_metrics,
    calculate_project_metrics,
)
from app.persistence.models import ActivityRecord, ProjectRecord
from app.schemas.activity import ActivityResponse
from app.schemas.evm import EvmMetricsResponse
from app.schemas.project import ProjectDetailResponse, ProjectSummaryResponse


def build_activity_response(activity: ActivityRecord) -> ActivityResponse:
    return ActivityResponse(
        id=activity.id,
        project_id=activity.project_id,
        name=activity.name,
        budget_at_completion=activity.budget_at_completion,
        planned_percentage=activity.planned_percentage,
        actual_percentage=activity.actual_percentage,
        actual_cost=activity.actual_cost,
        metrics=_to_metrics_response(calculate_activity_metrics(_to_progress(activity))),
    )


def build_project_summary(project: ProjectRecord) -> ProjectSummaryResponse:
    return ProjectSummaryResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        activity_count=len(project.activities),
        metrics=_project_metrics(project),
    )


def build_project_detail(project: ProjectRecord) -> ProjectDetailResponse:
    return ProjectDetailResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        activities=[build_activity_response(activity) for activity in project.activities],
        metrics=_project_metrics(project),
    )


def _project_metrics(project: ProjectRecord) -> EvmMetricsResponse:
    progress = [_to_progress(activity) for activity in project.activities]
    return _to_metrics_response(calculate_project_metrics(progress))


def _to_progress(activity: ActivityRecord) -> ActivityProgress:
    return ActivityProgress(
        budget_at_completion=activity.budget_at_completion,
        planned_percentage=activity.planned_percentage,
        actual_percentage=activity.actual_percentage,
        actual_cost=activity.actual_cost,
    )


def _to_metrics_response(metrics: EvmMetrics) -> EvmMetricsResponse:
    return EvmMetricsResponse.model_validate(metrics)
