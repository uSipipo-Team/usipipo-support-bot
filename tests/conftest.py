"""Pytest fixtures and configuration for uSipipo Support Bot tests."""

import asyncio
import os
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

# Set test environment before importing app modules
os.environ["BOT_TOKEN"] = "test_bot_token"
os.environ["BACKEND_URL"] = "https://test.api.usipipo.com"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"

from src.infrastructure.api_client import APIClient
from src.infrastructure.config import Settings, get_settings
from src.infrastructure.token_storage import TokenStorage


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_telegram_user() -> MagicMock:
    """Mock Telegram user."""
    user = MagicMock()
    user.id = 123456789
    user.first_name = "Test"
    user.last_name = "User"
    user.username = "testuser"
    return user


@pytest.fixture
def mock_telegram_message() -> MagicMock:
    """Mock Telegram message."""
    message = MagicMock()
    message.message_id = 1
    message.text = "/start"
    return message


@pytest.fixture
def mock_telegram_update(mock_telegram_user, mock_telegram_message) -> MagicMock:
    """Mock Telegram update."""
    update = MagicMock()
    update.update_id = 1
    update.effective_user = mock_telegram_user
    update.effective_message = mock_telegram_message
    update.message = mock_telegram_message
    return update


@pytest.fixture
def mock_callback_query() -> MagicMock:
    """Mock Telegram callback query."""
    query = MagicMock()
    query.id = "query_123"
    query.data = "ticket_view:uuid-123"
    query.message = MagicMock()
    return query


@pytest.fixture
def mock_context() -> MagicMock:
    """Mock Telegram context."""
    context = MagicMock()
    context.user_data = {}
    context.chat_data = {}
    context.bot_data = {}
    return context


@pytest.fixture
def mock_settings() -> Settings:
    """Mock settings for testing."""
    settings = MagicMock(spec=Settings)
    settings.BOT_TOKEN = "test_bot_token"
    settings.BOT_USERNAME = "uSipipoSupport_Bot"
    settings.BACKEND_URL = "https://test.api.usipipo.com"
    settings.API_PREFIX = "/api/v1"
    settings.backend_base_url = "https://test.api.usipipo.com/api/v1"
    settings.REDIS_URL = "redis://localhost:6379/0"
    settings.LOG_LEVEL = "DEBUG"
    return settings


@pytest.fixture
def mock_api_client() -> APIClient:
    """Mock API client for testing."""
    client = MagicMock(spec=APIClient)
    client.base_url = "https://test.api.usipipo.com"
    client.api_prefix = "/api/v1"
    client.base_endpoint = "https://test.api.usipipo.com/api/v1"
    client.api_client = AsyncMock()
    return client


@pytest_asyncio.fixture
async def mock_token_storage() -> TokenStorage:
    """Mock token storage for testing."""
    storage = MagicMock(spec=TokenStorage)
    storage.is_authenticated = AsyncMock(return_value=True)
    storage.get = AsyncMock(return_value={
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_at": 9999999999,
        "user_id": "uuid-123"
    })
    storage.save = AsyncMock()
    storage.delete = AsyncMock()
    storage.needs_refresh = AsyncMock(return_value=False)
    storage.is_token_expired = AsyncMock(return_value=False)
    return storage


@pytest.fixture
def mock_ticket_data() -> dict[str, Any]:
    """Mock ticket data."""
    return {
        "id": "uuid-123",
        "ticket_number": "#TKT-12345",
        "category": "technical",
        "subject": "VPN connection issue",
        "status": "OPEN",
        "created_at": "2026-03-28T10:00:00Z",
        "user_id": "uuid-user-123",
    }


@pytest.fixture
def mock_tickets_list(mock_ticket_data) -> list[dict[str, Any]]:
    """Mock list of tickets."""
    return [
        mock_ticket_data,
        {
            "id": "uuid-124",
            "ticket_number": "#TKT-12346",
            "category": "billing",
            "subject": "Payment issue",
            "status": "RESPONDED",
            "created_at": "2026-03-27T10:00:00Z",
            "user_id": "uuid-user-123",
        }
    ]


@pytest.fixture
def mock_api_response_success() -> dict[str, Any]:
    """Mock successful API response."""
    return {
        "success": True,
        "message": "Operation successful"
    }


@pytest.fixture
def mock_api_response_error() -> dict[str, Any]:
    """Mock error API response."""
    return {
        "success": False,
        "error": "Operation failed"
    }
