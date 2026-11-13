"""Cálculo de indicadores de Valor Ganado (EVM).

Los valores se calculan con precisión completa y solo se redondean al construir el
resultado. Así, por ejemplo, EAC = BAC / CPI usa el CPI exacto y no el redondeado.
"""

from collections.abc import Iterable
from decimal import Decimal

from app.domain.evm.constants import (
    INDEX_PRECISION,
    MONEY_PRECISION,
    ON_TARGET_INDEX,
    PERCENTAGE_BASE,
    ROUNDING_MODE,
    ZERO,
)
from app.domain.evm.models import ActivityProgress, CostStatus, EvmMetrics, ScheduleStatus


def calculate_activity_metrics(activity: ActivityProgress) -> EvmMetrics:
    return _build_metrics(
        budget_at_completion=activity.budget_at_completion,
        planned_value=_planned_value(activity),
        earned_value=_earned_value(activity),
        actual_cost=activity.actual_cost,
    )


def calculate_project_metrics(activities: Iterable[ActivityProgress]) -> EvmMetrics:
    """Consolida sumando BAC, PV, EV y AC antes de calcular los índices.

    Promediar los CPI/SPI de cada actividad daría el mismo peso a una actividad
    pequeña que a una grande; sumar los valores pondera por presupuesto.
    """
    activity_list = list(activities)
    return _build_metrics(
        budget_at_completion=sum((a.budget_at_completion for a in activity_list), ZERO),
        planned_value=sum((_planned_value(a) for a in activity_list), ZERO),
        earned_value=sum((_earned_value(a) for a in activity_list), ZERO),
        actual_cost=sum((a.actual_cost for a in activity_list), ZERO),
    )


def _planned_value(activity: ActivityProgress) -> Decimal:
    return activity.planned_percentage / PERCENTAGE_BASE * activity.budget_at_completion


def _earned_value(activity: ActivityProgress) -> Decimal:
    return activity.actual_percentage / PERCENTAGE_BASE * activity.budget_at_completion


def _build_metrics(
    budget_at_completion: Decimal,
    planned_value: Decimal,
    earned_value: Decimal,
    actual_cost: Decimal,
) -> EvmMetrics:
    cost_performance_index = _divide_or_none(earned_value, actual_cost)
    schedule_performance_index = _divide_or_none(earned_value, planned_value)
    estimate_at_completion = _divide_or_none(budget_at_completion, cost_performance_index)
    variance_at_completion = (
        None if estimate_at_completion is None else budget_at_completion - estimate_at_completion
    )
    rounded_cost_index = _round_index(cost_performance_index)
    rounded_schedule_index = _round_index(schedule_performance_index)

    return EvmMetrics(
        budget_at_completion=_round_money(budget_at_completion),
        planned_value=_round_money(planned_value),
        earned_value=_round_money(earned_value),
        actual_cost=_round_money(actual_cost),
        cost_variance=_round_money(earned_value - actual_cost),
        schedule_variance=_round_money(earned_value - planned_value),
        cost_performance_index=rounded_cost_index,
        schedule_performance_index=rounded_schedule_index,
        estimate_at_completion=_round_optional_money(estimate_at_completion),
        variance_at_completion=_round_optional_money(variance_at_completion),
        cost_status=_classify_cost(rounded_cost_index),
        schedule_status=_classify_schedule(rounded_schedule_index),
    )


def _divide_or_none(numerator: Decimal, denominator: Decimal | None) -> Decimal | None:
    """Retorna None cuando el denominador es cero o no está definido (indicador no calculable)."""
    if denominator is None or denominator == ZERO:
        return None
    return numerator / denominator


def _classify_cost(index: Decimal | None) -> CostStatus:
    if index is None:
        return CostStatus.NOT_AVAILABLE
    if index > ON_TARGET_INDEX:
        return CostStatus.UNDER_BUDGET
    if index < ON_TARGET_INDEX:
        return CostStatus.OVER_BUDGET
    return CostStatus.ON_BUDGET


def _classify_schedule(index: Decimal | None) -> ScheduleStatus:
    if index is None:
        return ScheduleStatus.NOT_AVAILABLE
    if index > ON_TARGET_INDEX:
        return ScheduleStatus.AHEAD_OF_SCHEDULE
    if index < ON_TARGET_INDEX:
        return ScheduleStatus.BEHIND_SCHEDULE
    return ScheduleStatus.ON_SCHEDULE


def _round_money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_PRECISION, rounding=ROUNDING_MODE)


def _round_optional_money(value: Decimal | None) -> Decimal | None:
    return None if value is None else _round_money(value)


def _round_index(value: Decimal | None) -> Decimal | None:
    return None if value is None else value.quantize(INDEX_PRECISION, rounding=ROUNDING_MODE)
