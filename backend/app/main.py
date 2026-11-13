from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import activities, health, projects
from app.api.error_handlers import register_error_handlers
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/swagger-ui",
        openapi_url="/api-docs",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    for router in (health.router, projects.router, activities.router):
        application.include_router(router, prefix=settings.api_prefix)
    register_error_handlers(application)
    return application


app = create_app()
