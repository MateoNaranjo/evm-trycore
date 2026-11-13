from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.schemas.common import ErrorResponse
from app.services.exceptions import ResourceNotFoundError

NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse,
        "description": "El recurso solicitado no existe.",
    }
}


async def handle_resource_not_found(_: Request, error: ResourceNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(detail=str(error)).model_dump(),
    )


def register_error_handlers(application: FastAPI) -> None:
    application.add_exception_handler(ResourceNotFoundError, handle_resource_not_found)
