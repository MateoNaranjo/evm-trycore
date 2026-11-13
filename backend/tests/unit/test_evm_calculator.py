from decimal import Decimal

import pytest

from app.domain.evm import (
    ActivityProgress,
    CostStatus,
    ScheduleStatus,
    calculate_activity_metrics,
    calculate_project_metrics,
)


def build_activity(budget, planned, actual, cost):
    return ActivityProgress(
        budget_at_completion=Decimal(budget),
        planned_percentage=Decimal(planned),
        actual_percentage=Decimal(actual),
        actual_cost=Decimal(cost),
    )


# Actividad A: gasta más de lo que avanza y va detrás del plan.
OVERSPENT_AND_LATE = build_activity("10000", "50", "40", "6000")
# Actividad B: gasta menos de lo que avanza y va adelantada.
EFFICIENT_AND_AHEAD = build_activity("20000", "30", "35", "5000")


class TestActivityMetrics:
    def test_overspent_and_late_activity_matches_hand_calculation(self):
        metrics = calculate_activity_metrics(OVERSPENT_AND_LATE)

        assert metrics.planned_value == Decimal("5000.00")
        assert metrics.earned_value == Decimal("4000.00")
        assert metrics.actual_cost == Decimal("6000.00")
        assert metrics.cost_variance == Decimal("-2000.00")
        assert metrics.schedule_variance == Decimal("-1000.00")
        assert metrics.cost_performance_index == Decimal("0.6667")
        assert metrics.schedule_performance_index == Decimal("0.8000")
        assert metrics.estimate_at_completion == Decimal("15000.00")
        assert metrics.variance_at_completion == Decimal("-5000.00")
        assert metrics.cost_status is CostStatus.OVER_BUDGET
        assert metrics.schedule_status is ScheduleStatus.BEHIND_SCHEDULE

    def test_efficient_and_ahead_activity_matches_hand_calculation(self):
        metrics = calculate_activity_metrics(EFFICIENT_AND_AHEAD)

        assert metrics.planned_value == Decimal("6000.00")
        assert metrics.earned_value == Decimal("7000.00")
        assert metrics.cost_variance == Decimal("2000.00")
        assert metrics.schedule_variance == Decimal("1000.00")
        assert metrics.cost_performance_index == Decimal("1.4000")
        assert metrics.schedule_performance_index == Decimal("1.1667")
        assert metrics.estimate_at_completion == Decimal("14285.71")
        assert metrics.variance_at_completion == Decimal("5714.29")
        assert metrics.cost_status is CostStatus.UNDER_BUDGET
        assert metrics.schedule_status is ScheduleStatus.AHEAD_OF_SCHEDULE

    def test_activity_exactly_on_plan_is_on_budget_and_on_schedule(self):
        metrics = calculate_activity_metrics(build_activity("1000", "50", "50", "500"))

        assert metrics.cost_performance_index == Decimal("1.0000")
        assert metrics.schedule_performance_index == Decimal("1.0000")
        assert metrics.variance_at_completion == Decimal("0.00")
        assert metrics.cost_status is CostStatus.ON_BUDGET
        assert metrics.schedule_status is ScheduleStatus.ON_SCHEDULE

    def test_zero_actual_cost_with_progress_leaves_cost_indices_undefined(self):
        metrics = calculate_activity_metrics(build_activity("1000", "50", "20", "0"))

        assert metrics.earned_value == Decimal("200.00")
        assert metrics.cost_variance == Decimal("200.00")
        assert metrics.cost_performance_index is None
        assert metrics.estimate_at_completion is None
        assert metrics.variance_at_completion is None
        assert metrics.cost_status is CostStatus.NOT_AVAILABLE
        assert metrics.schedule_performance_index == Decimal("0.4000")

    def test_activity_not_started_has_no_indices(self):
        metrics = calculate_activity_metrics(build_activity("1000", "0", "0", "0"))

        assert metrics.planned_value == Decimal("0.00")
        assert metrics.earned_value == Decimal("0.00")
        assert metrics.cost_variance == Decimal("0.00")
        assert metrics.schedule_variance == Decimal("0.00")
        assert metrics.cost_performance_index is None
        assert metrics.schedule_performance_index is None
        assert metrics.cost_status is CostStatus.NOT_AVAILABLE
        assert metrics.schedule_status is ScheduleStatus.NOT_AVAILABLE

    def test_zero_actual_progress_with_spending_is_over_budget_without_estimate(self):
        metrics = calculate_activity_metrics(build_activity("1000", "30", "0", "250"))

        assert metrics.earned_value == Decimal("0.00")
        assert metrics.cost_variance == Decimal("-250.00")
        assert metrics.cost_performance_index == Decimal("0.0000")
        assert metrics.cost_status is CostStatus.OVER_BUDGET
        assert metrics.schedule_performance_index == Decimal("0.0000")
        assert metrics.schedule_status is ScheduleStatus.BEHIND_SCHEDULE
        assert metrics.estimate_at_completion is None
        assert metrics.variance_at_completion is None

    def test_zero_planned_progress_leaves_schedule_index_undefined(self):
        metrics = calculate_activity_metrics(build_activity("1000", "0", "10", "100"))

        assert metrics.planned_value == Decimal("0.00")
        assert metrics.schedule_variance == Decimal("100.00")
        assert metrics.schedule_performance_index is None
        assert metrics.schedule_status is ScheduleStatus.NOT_AVAILABLE
        assert metrics.cost_performance_index == Decimal("1.0000")

    def test_completed_activity_earns_its_full_budget(self):
        metrics = calculate_activity_metrics(build_activity("1000", "100", "100", "1200"))

        assert metrics.earned_value == Decimal("1000.00")
        assert metrics.estimate_at_completion == Decimal("1200.00")
        assert metrics.variance_at_completion == Decimal("-200.00")

    def test_estimate_at_completion_uses_unrounded_cost_index(self):
        metrics = calculate_activity_metrics(build_activity("300", "10", "10", "90"))

        assert metrics.cost_performance_index == Decimal("0.3333")
        # Con el CPI redondeado (0.3333) daría 900.09; el valor correcto es 900.00.
        assert metrics.estimate_at_completion == Decimal("900.00")

    def test_estimate_at_completion_equals_actual_cost_plus_remaining_work_at_current_efficiency(
        self,
    ):
        budget, earned, cost = Decimal("10000"), Decimal("4000"), Decimal("6000")
        exact_cost_index = earned / cost
        alternative_formula = cost + (budget - earned) / exact_cost_index

        metrics = calculate_activity_metrics(OVERSPENT_AND_LATE)

        assert metrics.estimate_at_completion == alternative_formula.quantize(Decimal("0.01"))


class TestProjectMetrics:
    def test_project_without_activities_returns_zero_totals_and_no_indices(self):
        metrics = calculate_project_metrics([])

        assert metrics.budget_at_completion == Decimal("0.00")
        assert metrics.planned_value == Decimal("0.00")
        assert metrics.earned_value == Decimal("0.00")
        assert metrics.actual_cost == Decimal("0.00")
        assert metrics.cost_performance_index is None
        assert metrics.schedule_performance_index is None
        assert metrics.estimate_at_completion is None
        assert metrics.variance_at_completion is None
        assert metrics.cost_status is CostStatus.NOT_AVAILABLE
        assert metrics.schedule_status is ScheduleStatus.NOT_AVAILABLE

    def test_project_with_single_activity_matches_that_activity(self):
        project_metrics = calculate_project_metrics([OVERSPENT_AND_LATE])

        assert project_metrics == calculate_activity_metrics(OVERSPENT_AND_LATE)

    def test_project_indices_are_weighted_by_budget_not_averaged(self):
        metrics = calculate_project_metrics([OVERSPENT_AND_LATE, EFFICIENT_AND_AHEAD])

        assert metrics.budget_at_completion == Decimal("30000.00")
        assert metrics.planned_value == Decimal("11000.00")
        assert metrics.earned_value == Decimal("11000.00")
        assert metrics.actual_cost == Decimal("11000.00")
        # El promedio simple de CPI sería (0.6667 + 1.4) / 2 = 1.0333, lo cual es incorrecto.
        assert metrics.cost_performance_index == Decimal("1.0000")
        assert metrics.schedule_performance_index == Decimal("1.0000")
        assert metrics.estimate_at_completion == Decimal("30000.00")
        assert metrics.variance_at_completion == Decimal("0.00")
        assert metrics.cost_status is CostStatus.ON_BUDGET
        assert metrics.schedule_status is ScheduleStatus.ON_SCHEDULE

    def test_project_without_actual_cost_has_no_cost_index(self):
        metrics = calculate_project_metrics(
            [build_activity("1000", "10", "5", "0"), build_activity("2000", "20", "0", "0")]
        )

        assert metrics.cost_performance_index is None
        assert metrics.cost_status is CostStatus.NOT_AVAILABLE


class TestActivityProgressValidation:
    @pytest.mark.parametrize(
        ("budget", "planned", "actual", "cost"),
        [
            ("0", "50", "50", "100"),
            ("-1", "50", "50", "100"),
            ("1000", "-1", "50", "100"),
            ("1000", "101", "50", "100"),
            ("1000", "50", "-1", "100"),
            ("1000", "50", "101", "100"),
            ("1000", "50", "50", "-1"),
        ],
        ids=[
            "zero_budget",
            "negative_budget",
            "negative_planned",
            "planned_over_100",
            "negative_actual",
            "actual_over_100",
            "negative_cost",
        ],
    )
    def test_invalid_activity_values_are_rejected(self, budget, planned, actual, cost):
        with pytest.raises(ValueError):
            build_activity(budget, planned, actual, cost)

    def test_boundary_percentages_are_accepted(self):
        activity = build_activity("1", "0", "100", "0")

        assert activity.actual_percentage == Decimal("100")
