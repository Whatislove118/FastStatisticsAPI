from pathlib import Path

import toml
from pydantic import AnyUrl, BaseSettings, validator

PROJECT_DIR = Path(__file__).parent.parent.parent
PYPROJECT_CONTENT = toml.load(f"{PROJECT_DIR}/pyproject.toml")["tool"]["poetry"]


class Settings(BaseSettings):
    POSTGRES_HOST: str = "192.168.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: str = ""

    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    @validator("SQLALCHEMY_DATABASE_URI")
    def _resolve_db_uri(cls, v: str, values: dict[str, str]):
        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            host=values.get("POSTGRES_HOST"),
            password=values.get("POSTGRES_PASSWORD"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings = Settings()
