from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jithub_location: str = "LOCAL-DEV"
    database_url: str = "postgresql://postgres:postgres@auth-db:5432/auth_db"
    secret_key: str = "jithub-secret-key-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 43200

    class Config:
        env_prefix = "JITHUB_"


settings = Settings()
