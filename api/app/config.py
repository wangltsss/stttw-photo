from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://photos:photos@localhost:5432/photos_dev"
    secret_key: str = "dev-secret-change-in-production"
    environment: str = "development"
    azure_storage_connection_string: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
