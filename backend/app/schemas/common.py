from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer

# Pydantic serializa Decimal como string por defecto; el API expone números JSON.
JsonDecimal = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]


class ErrorResponse(BaseModel):
    detail: str = Field(description="Descripción del error.", examples=["Proyecto 7 no existe."])
