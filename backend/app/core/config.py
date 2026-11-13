from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_title: str = "EVM Tracker API"
    app_description: str = (
        "API para gestionar proyectos y actividades y calcular sus indicadores "
        "de Valor Ganado (Earned Value Management)."
    )
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/evm_db"
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
