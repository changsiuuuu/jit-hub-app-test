from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jithub_location: str = "LOCAL-DEV"
    database_url: str = "postgresql://postgres:postgres@tourist-db:5432/tourist_db"
    auth_service_url: str = "http://auth-service:8001"

    class Config:
        env_prefix = "JITHUB_"


settings = Settings()
