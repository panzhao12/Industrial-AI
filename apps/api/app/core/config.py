from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Industrial AI Troubleshooting Copilot API"
    app_version: str = "0.1.0"
    database_url: str = (
        "postgresql+psycopg://industrial_ai:industrial_ai@localhost:5432/industrial_ai"
    )
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
