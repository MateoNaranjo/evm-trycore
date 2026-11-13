from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])

HEALTHY_STATUS = "ok"


class HealthResponse(BaseModel):
    status: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Verificar que el API está activo",
    description="Retorna `ok` si el servicio está en ejecución.",
)
def check_health() -> HealthResponse:
    return HealthResponse(status=HEALTHY_STATUS)
