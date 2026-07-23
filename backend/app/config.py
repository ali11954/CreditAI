from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "CreditAI Enterprise Platform"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/creditai",
        env="DATABASE_URL"
    )
    DATABASE_URL_SYNC: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/creditai",
        env="DATABASE_URL_SYNC"
    )
    
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    SUPABASE_URL: Optional[str] = Field(default=None, env="SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = Field(default=None, env="SUPABASE_KEY")
    
    SAP_URL: Optional[str] = Field(default=None, env="SAP_URL")
    SAP_CLIENT: Optional[str] = Field(default=None, env="SAP_CLIENT")
    SAP_USERNAME: Optional[str] = Field(default=None, env="SAP_USERNAME")
    SAP_PASSWORD: Optional[str] = Field(default=None, env="SAP_PASSWORD")
    
    AI_API_KEY: Optional[str] = Field(default=None, env="AI_API_KEY")
    AI_MODEL: str = Field(default="gpt-4", env="AI_MODEL")
    AI_TEMPERATURE: float = Field(default=0.7, env="AI_TEMPERATURE")
    
    CORS_ORIGINS: list = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    SMS_API_KEY: Optional[str] = Field(default=None, env="SMS_API_KEY")
    SMS_API_URL: Optional[str] = Field(default=None, env="SMS_API_URL")
    
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_UPLOAD_SIZE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
