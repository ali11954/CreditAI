from typing import Optional, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "CreditAI Enterprise Platform"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    ENVIRONMENT: str = Field(
        default="production",
        validation_alias="ENVIRONMENT"
    )

    DEBUG: bool = Field(
        default=False,
        validation_alias="DEBUG"
    )


    # =========================
    # Database
    # =========================

    DATABASE_URL: str = Field(
        default=(
            "postgresql+asyncpg://"
            "postgres:postgres@localhost:5432/creditai"
        ),
        validation_alias="DATABASE_URL"
    )


    DATABASE_URL_SYNC: str = Field(
        default=(
            "postgresql://"
            "postgres:postgres@localhost:5432/creditai"
        ),
        validation_alias="DATABASE_URL_SYNC"
    )


    @property
    def async_database_url(self) -> str:
        url = self.DATABASE_URL

        # Switch to psycopg for Supabase pgbouncer compatibility
        url = url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
        url = url.replace("postgresql://", "postgresql+psycopg://")

        # Fix ssl param for psycopg (psycopg uses sslmode, not ssl)
        import re
        url = re.sub(r'[?&]ssl=true', '', url)
        url = re.sub(r'[?&]ssl=require', '', url)
        url = re.sub(r'[?&]sslmode=disable', '', url)
        if 'sslmode=' not in url:
            sep = '&' if '?' in url else '?'
            url = f"{url}{sep}sslmode=require"

        return url



    # =========================
    # Redis
    # =========================

    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL"
    )


    # =========================
    # Security
    # =========================

    SECRET_KEY: str = Field(
        default="change-this-secret-key",
        validation_alias="SECRET_KEY"
    )

    ALGORITHM: str = "HS256"


    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )


    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        validation_alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )



    # =========================
    # Supabase
    # =========================

    SUPABASE_URL: Optional[str] = Field(
        default=None,
        validation_alias="SUPABASE_URL"
    )

    SUPABASE_KEY: Optional[str] = Field(
        default=None,
        validation_alias="SUPABASE_KEY"
    )



    # =========================
    # SAP Integration
    # =========================

    SAP_URL: Optional[str] = Field(
        default=None,
        validation_alias="SAP_URL"
    )

    SAP_CLIENT: Optional[str] = Field(
        default=None,
        validation_alias="SAP_CLIENT"
    )

    SAP_USERNAME: Optional[str] = Field(
        default=None,
        validation_alias="SAP_USERNAME"
    )

    SAP_PASSWORD: Optional[str] = Field(
        default=None,
        validation_alias="SAP_PASSWORD"
    )



    # =========================
    # AI
    # =========================

    AI_API_KEY: Optional[str] = Field(
        default=None,
        validation_alias="AI_API_KEY"
    )


    AI_MODEL: str = Field(
        default="gpt-4",
        validation_alias="AI_MODEL"
    )


    AI_TEMPERATURE: float = Field(
        default=0.7,
        validation_alias="AI_TEMPERATURE"
    )



    # =========================
    # CORS
    # =========================

    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "https://creditai-frontend.onrender.com",
        ],
        validation_alias="CORS_ORIGINS"
    )



    # =========================
    # Email
    # =========================

    SMTP_HOST: Optional[str] = Field(
        default=None,
        validation_alias="SMTP_HOST"
    )

    SMTP_PORT: int = Field(
        default=587,
        validation_alias="SMTP_PORT"
    )

    SMTP_USER: Optional[str] = Field(
        default=None,
        validation_alias="SMTP_USER"
    )

    SMTP_PASSWORD: Optional[str] = Field(
        default=None,
        validation_alias="SMTP_PASSWORD"
    )



    # =========================
    # SMS
    # =========================

    SMS_API_KEY: Optional[str] = Field(
        default=None,
        validation_alias="SMS_API_KEY"
    )


    SMS_API_URL: Optional[str] = Field(
        default=None,
        validation_alias="SMS_API_URL"
    )



    # =========================
    # Uploads
    # =========================

    UPLOAD_DIR: str = Field(
        default="uploads",
        validation_alias="UPLOAD_DIR"
    )


    MAX_UPLOAD_SIZE: int = Field(
        default=10 * 1024 * 1024,
        validation_alias="MAX_UPLOAD_SIZE"
    )



    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )



settings = Settings()