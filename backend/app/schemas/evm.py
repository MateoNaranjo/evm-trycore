from pydantic import BaseModel, ConfigDict, Field

from app.domain.evm import CostStatus, ScheduleStatus
from app.schemas.common import JsonDecimal


class EvmMetricsResponse(BaseModel):
    """Indicadores de Valor Ganado. Los índices son null cuando no se pueden calcular."""

    model_config = ConfigDict(from_attributes=True)

    budget_at_completion: JsonDecimal = Field(description="BAC: presupuesto total planificado.")
    planned_value: JsonDecimal = Field(description="PV = % planificado × BAC.")
    earned_value: JsonDecimal = Field(description="EV = % completado × BAC.")
    actual_cost: JsonDecimal = Field(description="AC: costo real incurrido.")
    cost_variance: JsonDecimal = Field(description="CV = EV − AC. Negativo: sobrecosto.")
    schedule_variance: JsonDecimal = Field(description="SV = EV − PV. Negativo: atraso.")
    cost_performance_index: JsonDecimal | None = Field(
        description="CPI = EV / AC. null si AC es cero."
    )
    schedule_performance_index: JsonDecimal | None = Field(
        description="SPI = EV / PV. null si PV es cero."
    )
    estimate_at_completion: JsonDecimal | None = Field(
        description="EAC = BAC / CPI. null si CPI es cero o no está definido."
    )
    variance_at_completion: JsonDecimal | None = Field(
        description="VAC = BAC − EAC. null si EAC no está definido."
    )
    cost_status: CostStatus = Field(description="Interpretación del CPI.")
    schedule_status: ScheduleStatus = Field(description="Interpretación del SPI.")
