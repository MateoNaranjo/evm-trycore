from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from app.domain.evm.constants import MAX_PERCENTAGE, MIN_PERCENTAGE, ZERO


class CostStatus(StrEnum):
    UNDER_BUDGET = "UNDER_BUDGET"
    ON_BUDGET = "ON_BUDGET"
    OVER_BUDGET = "OVER_BUDGET"
    NOT_AVAILABLE = "NOT_AVAILABLE"


class ScheduleStatus(StrEnum):
    AHEAD_OF_SCHEDULE = "AHEAD_OF_SCHEDULE"
    ON_SCHEDULE = "ON_SCHEDULE"
    BEHIND_SCHEDULE = "BEHIND_SCHEDULE"
    NOT_AVAILABLE = "NOT_AVAILABLE"


@dataclass(frozen=True)
class ActivityProgress:
    """Datos de avance de una actividad a la fecha de corte. Porcentajes en escala 0–100."""

    budget_at_completion: Decimal
    planned_percentage: Decimal
    actual_percentage: Decimal
    actual_cost: Decimal

    def __post_init__(self) -> None:
        if self.budget_at_completion <= ZERO:
            raise ValueError("El presupuesto (BAC) debe ser mayor que cero.")
        if self.actual_cost < ZERO:
            raise ValueError("El costo real (AC) no puede ser negativo.")
        _ensure_valid_percentage(self.planned_percentage, "planificado")
        _ensure_valid_percentage(self.actual_percentage, "real")


def _ensure_valid_percentage(percentage: Decimal, label: str) -> None:
    if not MIN_PERCENTAGE <= percentage <= MAX_PERCENTAGE:
        raise ValueError(
            f"El porcentaje de avance {label} debe estar entre "
            f"{MIN_PERCENTAGE} y {MAX_PERCENTAGE}."
        )


@dataclass(frozen=True)
class EvmMetrics:
    """Indicadores de Valor Ganado. Los índices son None cuando no se pueden calcular."""

    budget_at_completion: Decimal
    planned_value: Decimal
    earned_value: Decimal
    actual_cost: Decimal
    cost_variance: Decimal
    schedule_variance: Decimal
    cost_performance_index: Decimal | None
    schedule_performance_index: Decimal | None
    estimate_at_completion: Decimal | None
    variance_at_completion: Decimal | None
    cost_status: CostStatus
    schedule_status: ScheduleStatus
