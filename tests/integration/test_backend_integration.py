"""Integration tests for Support Bot with Backend API."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.bot.handlers.tickets import TicketsHandler
from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage


@pytest.fixture
def mock_api_client():
    """Mock API client."""
    client = MagicMock(spec=APIClient)
    client.base_url = "https://test.api.usipipo.com"
    client.api_prefix = "/api/v1"
    client.base_endpoint = "https://test.api.usipipo.com/api/v1"
    client.api_client = MagicMock()
    client.api_client.get = AsyncMock()
    client.api_client.post = AsyncMock()
    client.api_client.patch = AsyncMock()
    return client


@pytest.fixture
def mock_token_storage():
    """Mock token storage."""
    storage = MagicMock(spec=TokenStorage)
    storage.is_authenticated = AsyncMock(return_value=True)
    storage.get = AsyncMock(return_value={
        "access_token": "test_token",
        "refresh_token": "test_refresh",
        "expires_at": 9999999999,
        "user_id": "uuid-123"
    })
    storage.save = AsyncMock()
    storage.needs_refresh = AsyncMock(return_value=False)
    return storage


class TestBackendIntegration:
    """Test backend API integration."""

    @pytest.mark.asyncio
    async def test_list_tickets_integration(
        self,
        mock_api_client,
        mock_token_storage
    ):
        """Test listing tickets from backend."""
        # Mock backend response
        mock_tickets = [
            {
                "id": "uuid-123",
                "ticket_number": "#TKT-12345",
                "subject": "Test ticket",
                "status": "OPEN",
                "created_at": "2026-03-28T10:00:00Z"
            }
        ]
        mock_api_client.api_client.get.return_value = mock_tickets
        
        # Create handler
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        
        # Mock update and context
        update = MagicMock()
        update.effective_user = MagicMock()
        update.effective_user.id = 123456789
        update.message = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        
        # Call handler
        await handler.list_tickets(update, context)
        
        # Verify API was called with correct endpoint and auth
        mock_api_client.api_client.get.assert_called_once()
        call_args = mock_api_client.api_client.get.call_args
        assert call_args[0][0] == "/tickets"
        assert "Authorization" in call_args[1]["headers"]
        assert call_args[1]["headers"]["Authorization"].startswith("Bearer ")

    @pytest.mark.asyncio
    async def test_create_ticket_integration(
        self,
        mock_api_client,
        mock_token_storage
    ):
        """Test creating ticket via backend."""
        # Mock backend response
        mock_ticket = {
            "id": "uuid-123",
            "ticket_number": "#TKT-12345",
            "category": "technical",
            "subject": "Test ticket",
            "status": "OPEN",
            "created_at": "2026-03-28T10:00:00Z"
        }
        mock_api_client.api_client.post.return_value = mock_ticket
        
        # Create handler
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        
        # Mock update and context
        update = MagicMock()
        update.effective_user = MagicMock()
        update.effective_user.id = 123456789
        update.callback_query = MagicMock()
        update.callback_query.data = "ticket_cat:technical"
        update.callback_query.answer = AsyncMock()
        update.callback_query.edit_message_text = AsyncMock()
        context = MagicMock()
        context.user_data = {}
        
        # Call handler
        await handler.select_category_callback(update, context)
        
        # Verify API was called with correct endpoint and data
        mock_api_client.api_client.post.assert_called_once()
        call_args = mock_api_client.api_client.post.call_args
        assert call_args[1]["json"]["category"] == "technical"
        assert "Authorization" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_close_ticket_integration(
        self,
        mock_api_client,
        mock_token_storage
    ):
        """Test closing ticket via backend."""
        # Mock backend response
        mock_ticket = {
            "id": "uuid-123",
            "ticket_number": "#TKT-12345",
            "status": "CLOSED"
        }
        mock_api_client.api_client.patch.return_value = mock_ticket
        
        # Create handler
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        
        # Mock update and context
        update = MagicMock()
        update.effective_user = MagicMock()
        update.effective_user.id = 123456789
        update.callback_query = MagicMock()
        update.callback_query.data = "ticket_close:uuid-123"
        update.callback_query.answer = AsyncMock()
        update.callback_query.edit_message_text = AsyncMock()
        context = MagicMock()
        
        # Call handler
        await handler.close_ticket_callback(update, context)
        
        # Verify API was called with correct endpoint
        mock_api_client.api_client.patch.assert_called_once()
        call_args = mock_api_client.api_client.patch.call_args
        assert "/tickets/uuid-123/close" in call_args[0][0]
        assert "Authorization" in call_args[1]["headers"]


class TestAuthenticationFlow:
    """Test authentication flow."""

    @pytest.mark.asyncio
    async def test_unauthenticated_user_blocked(
        self,
        mock_api_client,
        mock_token_storage
    ):
        """Test that unauthenticated users are blocked."""
        # Mock unauthenticated user
        mock_token_storage.is_authenticated.return_value = False
        
        # Create handler
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        
        # Mock update
        update = MagicMock()
        update.effective_user = MagicMock()
        update.effective_user.id = 123456789
        update.message = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        
        # Call handler
        await handler.list_tickets(update, context)
        
        # Verify NOT_AUTHORIZED message was sent
        update.message.reply_text.assert_called_once()
        call_args = update.message.reply_text.call_args
        assert "❌" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_authenticated_user_allowed(
        self,
        mock_api_client,
        mock_token_storage
    ):
        """Test that authenticated users can access."""
        # Mock authenticated user
        mock_token_storage.is_authenticated.return_value = True
        # Mock empty response
        mock_api_client.api_client.get.return_value = []
        
        # Create handler
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        
        # Mock update
        update = MagicMock()
        update.effective_user = MagicMock()
        update.effective_user.id = 123456789
        update.message = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        
        # Call handler
        await handler.list_tickets(update, context)
        
        # Verify API was called (user was allowed through)
        mock_api_client.api_client.get.assert_called_once()
