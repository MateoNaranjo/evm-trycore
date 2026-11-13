from pydantic import BaseModel, ConfigDict, Field

from app.persistence.models import NAME_MAX_LENGTH
from app.schemas.activity import ActivityResponse
from app.schemas.evm import EvmMetricsResponse


class ProjectRequest(BaseModel):
    """Datos de un proyecto. Se usa para crear y para reemplazar."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH, examples=["Portal de clientes"])
    description: str | None = Field(default=None, examples=["Migración del portal a la nube"])


class ProjectSummaryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    activity_count: int
    metrics: EvmMetricsResponse = Field(description="Indicadores consolidados del proyecto.")


class ProjectDetailResponse(BaseModel):
    id: int
    name: str
    description: str | None
    activities: list[ActivityResponse]
    metrics: EvmMetricsResponse = Field(description="Indicadores consolidados del proyecto.")
