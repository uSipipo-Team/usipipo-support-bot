"""Configuration management via pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Bot Configuration
    BOT_TOKEN: str
    BOT_USERNAME: str = "uSipipoSupport_Bot"

    # Backend API
    BACKEND_URL: str = "https://api.usipipo.com"
    API_PREFIX: str = "/api/v1"

    @property
    def backend_base_url(self) -> str:
        """Get full backend base URL."""
        return f"{self.BACKEND_URL}{self.API_PREFIX}"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/1"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
