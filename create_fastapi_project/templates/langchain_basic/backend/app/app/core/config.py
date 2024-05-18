import os
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    MODE: ModeEnum = ModeEnum.development
    PROJECT_NAME: str = "app"    
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    OPENAI_API_KEY: str
    UNSPLASH_API_KEY: str
    SERP_API_KEY: str

    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=os.path.expanduser("~/.env")
    )


settings = Settings()
