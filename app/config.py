from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 현재 서비스가 구동 중인 인프라 위치
    # 예: "AWS-Region-A" | "OnPremise-Standby" | "AWS-Region-B"
    jithub_location: str = "AWS-Region-A"

    # 온프레미스 PostgreSQL 연결 정보
    database_url: str = "postgresql://postgres:postgres@localhost:5432/jithub"

    class Config:
        env_prefix = "JITHUB_"
        env_file = ".env"


settings = Settings()
