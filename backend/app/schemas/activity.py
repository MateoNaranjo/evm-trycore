from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.domain.evm.constants import MAX_PERCENTAGE, MIN_PERCENTAGE, ZERO
from app.persistence.models import (
    DECIMAL_PLACES,
    MONEY_TOTAL_DIGITS,
    NAME_MAX_LENGTH,
    PERCENTAGE_TOTAL_DIGITS,
)
from app.schemas.common import JsonDecimal
from app.schemas.evm import EvmMetricsResponse


class ActivityRequest(BaseModel):
    """Datos de una actividad a la fecha de corte. Se usa para crear y para reemplazar."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=1, max_length=NAME_MAX_LENGTH, examples=["Diseño de base de datos"]
    )
    budget_at_completion: Decimal = Field(
        gt=ZERO,
        max_digits=MONEY_TOTAL_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="BAC: presupuesto total planificado de la actividad.",
        examples=[10000],
    )
    planned_percentage: Decimal = Field(
        ge=MIN_PERCENTAGE,
        le=MAX_PERCENTAGE,
        max_digits=PERCENTAGE_TOTAL_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="Porcentaje de avance planificado a la fecha de corte (0–100).",
        examples=[50],
    )
    actual_percentage: Decimal = Field(
        ge=MIN_PERCENTAGE,
        le=MAX_PERCENTAGE,
        max_digits=PERCENTAGE_TOTAL_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="Porcentaje de avance real completado (0–100).",
        examples=[40],
    )
    actual_cost: Decimal = Field(
        ge=ZERO,
        max_digits=MONEY_TOTAL_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="AC: costo real incurrido hasta la fecha.",
        examples=[6000],
    )


class ActivityResponse(BaseModel):
    id: int
    project_id: int
    name: str
    budget_at_completion: JsonDecimal
    planned_percentage: JsonDecimal
    actual_percentage: JsonDecimal
    actual_cost: JsonDecimal
    metrics: EvmMetricsResponse
