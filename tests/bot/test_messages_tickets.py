"""Tests for Ticket Messages."""

from src.bot.keyboards.messages_tickets import TicketsMessages


class TestTicketsMessagesMenu:
    """Test menu messages."""

    def test_tickets_list_message(self):
        """Test TICKETS_LIST message template."""
        template = TicketsMessages.Menu.TICKETS_LIST
        assert "{tickets}" in template
        assert "/nuevoticket" in template

    def test_no_tickets_message(self):
        """Test NO_TICKETS message."""
        message = TicketsMessages.Menu.NO_TICKETS
        assert "📭" in message
        assert "/nuevoticket" in message

    def test_ticket_detail_message(self):
        """Test TICKET_DETAIL message template."""
        template = TicketsMessages.Menu.TICKET_DETAIL
        assert "{ticket_number}" in template
        assert "{status}" in template
        assert "{subject}" in template
        assert "{category}" in template
        assert "{created_at}" in template
        assert "{last_message}" in template

    def test_create_ticket_message(self):
        """Test CREATE_TICKET message."""
        message = TicketsMessages.Menu.CREATE_TICKET
        assert "🎫" in message
        assert "🖥️ Técnico" in message
        assert "💳 Pagos" in message
        assert "📦 Servicios" in message
        assert "❓ General" in message

    def test_ticket_created_message(self):
        """Test TICKET_CREATED message template."""
        template = TicketsMessages.Menu.TICKET_CREATED
        assert "✅" in template
        assert "{ticket_number}" in template
        assert "{subject}" in template
        assert "/tickets" in template

    def test_message_sent_message(self):
        """Test MESSAGE_SENT message."""
        message = TicketsMessages.Menu.MESSAGE_SENT
        assert "✅" in message
        assert "{ticket_number}" in message

    def test_ticket_closed_message(self):
        """Test TICKET_CLOSED message template."""
        template = TicketsMessages.Menu.TICKET_CLOSED
        assert "✅" in template
        assert "{ticket_number}" in template


class TestTicketsMessagesError:
    """Test error messages."""

    def test_not_found_message(self):
        """Test NOT_FOUND message."""
        message = TicketsMessages.Error.NOT_FOUND
        assert "❌" in message

    def test_not_authorized_message(self):
        """Test NOT_AUTHORIZED message."""
        message = TicketsMessages.Error.NOT_AUTHORIZED
        assert "❌" in message

    def test_invalid_category_message(self):
        """Test INVALID_CATEGORY message."""
        message = TicketsMessages.Error.INVALID_CATEGORY
        assert "❌" in message

    def test_subject_too_short_message(self):
        """Test SUBJECT_TOO_SHORT message."""
        message = TicketsMessages.Error.SUBJECT_TOO_SHORT
        assert "❌" in message
        assert "5" in message

    def test_message_too_short_message(self):
        """Test MESSAGE_TOO_SHORT message."""
        message = TicketsMessages.Error.MESSAGE_TOO_SHORT
        assert "❌" in message
        assert "10" in message

    def test_system_error_message(self):
        """Test SYSTEM_ERROR message."""
        message = TicketsMessages.Error.SYSTEM_ERROR
        assert "❌" in message
