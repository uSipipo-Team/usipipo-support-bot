"""Tests for Tickets Handlers."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.bot.handlers.tickets import TicketsHandler, get_tickets_handlers, get_tickets_callback_handlers
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
def mock_update():
    """Mock Telegram update."""
    update = MagicMock()
    update.effective_user = MagicMock()
    update.effective_user.id = 123456789
    update.effective_user.first_name = "Test"
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    update.callback_query.data = "ticket_view:uuid-123"
    return update


@pytest.fixture
def mock_context():
    """Mock Telegram context."""
    context = MagicMock()
    context.user_data = {}
    context.chat_data = {}
    context.bot_data = {}
    return context


@pytest.fixture
def mock_ticket_data():
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
def mock_tickets_list(mock_ticket_data):
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


class TestTicketsHandlerInitialization:
    """Test TicketsHandler initialization."""

    def test_init(self, mock_api_client, mock_token_storage):
        """Test handler initialization."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        assert handler.api.api_client == mock_api_client.api_client
        assert handler.tokens == mock_token_storage


class TestListTickets:
    """Test list_tickets handler."""

    @pytest.mark.asyncio
    async def test_list_tickets_success(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage,
        mock_tickets_list
    ):
        """Test successful ticket listing."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_api_client.api_client.get.return_value = mock_tickets_list
        
        await handler.list_tickets(mock_update, mock_context)
        
        mock_api_client.api_client.get.assert_called_once()
        mock_update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_tickets_empty(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test listing with no tickets."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_api_client.api_client.get.return_value = []
        
        await handler.list_tickets(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_tickets_not_authenticated(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test listing when not authenticated."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_token_storage.is_authenticated.return_value = False
        
        await handler.list_tickets(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_tickets_error(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test listing with API error."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_api_client.api_client.get.side_effect = Exception("API Error")
        
        await handler.list_tickets(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once()


class TestCreateTicket:
    """Test create_ticket handler."""

    @pytest.mark.asyncio
    async def test_create_ticket_success(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test successful ticket creation initiation."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        
        await handler.create_ticket(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_ticket_not_authenticated(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test creation when not authenticated."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_token_storage.is_authenticated.return_value = False
        
        await handler.create_ticket(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once()


class TestSelectCategoryCallback:
    """Test select_category_callback handler."""

    @pytest.mark.asyncio
    async def test_select_category_technical(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage,
        mock_ticket_data
    ):
        """Test selecting technical category."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_update.callback_query.data = "ticket_cat:technical"
        mock_api_client.api_client.post.return_value = mock_ticket_data
        
        await handler.select_category_callback(mock_update, mock_context)
        
        mock_api_client.api_client.post.assert_called_once()
        call_args = mock_api_client.api_client.post.call_args
        assert call_args[1]["json"]["category"] == "technical"

    @pytest.mark.asyncio
    async def test_select_category_invalid(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test selecting invalid category."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_update.callback_query.data = "ticket_cat:invalid"
        
        await handler.select_category_callback(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_called_once()


class TestViewTicketCallback:
    """Test view_ticket_callback handler."""

    @pytest.mark.asyncio
    async def test_view_ticket_success(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage,
        mock_ticket_data
    ):
        """Test viewing ticket details."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_update.callback_query.data = "ticket_view:uuid-123"
        mock_api_client.api_client.get.return_value = mock_ticket_data
        
        await handler.view_ticket_callback(mock_update, mock_context)
        
        mock_api_client.api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_view_ticket_not_authenticated(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test viewing when not authenticated."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_token_storage.is_authenticated.return_value = False
        
        await handler.view_ticket_callback(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_called_once()


class TestCloseTicketCallback:
    """Test close_ticket_callback handler."""

    @pytest.mark.asyncio
    async def test_close_ticket_success(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage,
        mock_ticket_data
    ):
        """Test closing ticket."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_update.callback_query.data = "ticket_close:uuid-123"
        mock_api_client.api_client.post.return_value = mock_ticket_data

        await handler.close_ticket_callback(mock_update, mock_context)

        mock_api_client.api_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_ticket_error(
        self,
        mock_update,
        mock_context,
        mock_api_client,
        mock_token_storage
    ):
        """Test closing with error."""
        handler = TicketsHandler(mock_api_client, mock_token_storage)
        mock_update.callback_query.data = "ticket_close:uuid-123"
        mock_api_client.api_client.post.side_effect = Exception("API Error")

        await handler.close_ticket_callback(mock_update, mock_context)

        mock_update.callback_query.edit_message_text.assert_called_once()


class TestGetTicketsHandlers:
    """Test get_tickets_handlers function."""

    def test_get_tickets_handlers(self, mock_api_client, mock_token_storage):
        """Test handler registration."""
        handlers = get_tickets_handlers(mock_api_client, mock_token_storage)

        assert len(handlers) == 3
        # commands is a frozenset
        assert "nuevoticket" in handlers[0].commands
        assert "tickets" in handlers[1].commands
        assert "cancelar" in handlers[2].commands


class TestGetTicketsCallbackHandlers:
    """Test get_tickets_callback_handlers function."""

    def test_get_tickets_callback_handlers(self, mock_api_client, mock_token_storage):
        """Test callback handler registration."""
        handlers = get_tickets_callback_handlers(mock_api_client, mock_token_storage)

        assert len(handlers) == 5
