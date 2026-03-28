"""Tests for Infrastructure Components."""

import pytest

from src.infrastructure.config import Settings, get_settings


class TestSettings:
    """Test Settings class."""

    def test_settings_default_values(self):
        """Test default settings values."""
        settings = Settings(
            BOT_TOKEN="test_token",
            BOT_USERNAME="test_bot",
            BACKEND_URL="https://test.api.com",
            REDIS_URL="redis://localhost:6379/0",  # Match test environment
        )
        
        assert settings.API_PREFIX == "/api/v1"
        assert settings.REDIS_URL == "redis://localhost:6379/0"
        assert settings.LOG_LEVEL == "INFO"
        assert settings.LOG_FILE is None

    def test_settings_backend_base_url(self):
        """Test backend_base_url property."""
        settings = Settings(
            BOT_TOKEN="test_token",
            BACKEND_URL="https://test.api.com",
            API_PREFIX="/api/v1",
        )
        
        assert settings.backend_base_url == "https://test.api.com/api/v1"

    def test_settings_custom_values(self):
        """Test custom settings values."""
        settings = Settings(
            BOT_TOKEN="test_token",
            BOT_USERNAME="CustomBot",
            BACKEND_URL="https://custom.api.com",
            API_PREFIX="/api/v2",
            REDIS_URL="redis://custom:6379/2",
            LOG_LEVEL="DEBUG",
            LOG_FILE="/var/log/test.log",
        )
        
        assert settings.BOT_USERNAME == "CustomBot"
        assert settings.API_PREFIX == "/api/v2"
        assert settings.REDIS_URL == "redis://custom:6379/2"
        assert settings.LOG_LEVEL == "DEBUG"
        assert settings.LOG_FILE == "/var/log/test.log"

    def test_settings_backend_base_url_custom_prefix(self):
        """Test backend_base_url with custom prefix."""
        settings = Settings(
            BOT_TOKEN="test_token",
            BACKEND_URL="https://custom.api.com",
            API_PREFIX="/api/v2",
        )
        
        assert settings.backend_base_url == "https://custom.api.com/api/v2"


class TestGetSettings:
    """Test get_settings function."""

    def test_get_settings_returns_settings(self):
        """Test get_settings returns Settings instance."""
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_get_settings_cached(self):
        """Test get_settings returns cached instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
