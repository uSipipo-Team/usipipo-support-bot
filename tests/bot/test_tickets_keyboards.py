"""Tests for Ticket Keyboards."""

from src.bot.keyboards.tickets import TicketsKeyboard


class TestTicketsKeyboardTicketsList:
    """Test tickets_list keyboard."""

    def test_tickets_list_with_tickets(self, mock_tickets_list):
        """Test keyboard with tickets."""
        keyboard = TicketsKeyboard.tickets_list(mock_tickets_list)
        
        # Verify keyboard structure
        assert len(keyboard.inline_keyboard) == 3  # 2 tickets + 1 back button
        
        # Verify first ticket button
        first_button = keyboard.inline_keyboard[0][0]
        assert "🟢" in first_button.text  # OPEN status
        assert "#TKT-12345" in first_button.text
        assert first_button.callback_data == "ticket_view:uuid-123"
        
        # Verify second ticket button
        second_button = keyboard.inline_keyboard[1][0]
        assert "🟡" in second_button.text  # RESPONDED status
        assert "#TKT-12346" in second_button.text
        
        # Verify back button
        back_button = keyboard.inline_keyboard[2][0]
        assert back_button.text == "🔄 Actualizar"
        assert back_button.callback_data == "tickets_back"

    def test_tickets_list_empty(self):
        """Test keyboard with empty list."""
        keyboard = TicketsKeyboard.tickets_list([])
        
        # Only back button
        assert len(keyboard.inline_keyboard) == 1
        assert keyboard.inline_keyboard[0][0].callback_data == "tickets_back"

    def test_tickets_list_limits_to_10(self):
        """Test keyboard limits to 10 tickets."""
        tickets = [
            {"id": f"uuid-{i}", "ticket_number": f"#TKT-{i}", "status": "OPEN"}
            for i in range(15)
        ]
        
        keyboard = TicketsKeyboard.tickets_list(tickets)
        
        # Should only show 10 tickets + 1 back button
        assert len(keyboard.inline_keyboard) == 11


class TestTicketsKeyboardTicketDetail:
    """Test ticket_detail keyboard."""

    def test_ticket_detail(self):
        """Test ticket detail keyboard."""
        keyboard = TicketsKeyboard.ticket_detail("uuid-123")
        
        # Verify keyboard structure (4 rows)
        assert len(keyboard.inline_keyboard) == 4
        
        # Verify buttons
        messages_btn = keyboard.inline_keyboard[0][0]
        assert messages_btn.text == "💬 Ver Mensajes"
        assert messages_btn.callback_data == "ticket_messages:uuid-123"
        
        send_btn = keyboard.inline_keyboard[1][0]
        assert send_btn.text == "📩 Enviar Mensaje"
        assert send_btn.callback_data == "ticket_send:uuid-123"
        
        close_btn = keyboard.inline_keyboard[2][0]
        assert close_btn.text == "✅ Cerrar Ticket"
        assert close_btn.callback_data == "ticket_close:uuid-123"
        
        back_btn = keyboard.inline_keyboard[3][0]
        assert back_btn.text == "🔙 Volver"
        assert back_btn.callback_data == "tickets_back"


class TestTicketsKeyboardCategories:
    """Test categories keyboard."""

    def test_categories(self):
        """Test category selection keyboard."""
        keyboard = TicketsKeyboard.categories()
        
        # Verify keyboard structure (4 categories)
        assert len(keyboard.inline_keyboard) == 4
        
        # Verify categories
        tech_btn = keyboard.inline_keyboard[0][0]
        assert tech_btn.text == "🖥️ Técnico"
        assert tech_btn.callback_data == "ticket_cat:technical"
        
        billing_btn = keyboard.inline_keyboard[1][0]
        assert billing_btn.text == "💳 Pagos"
        assert billing_btn.callback_data == "ticket_cat:billing"
        
        services_btn = keyboard.inline_keyboard[2][0]
        assert services_btn.text == "📦 Servicios"
        assert services_btn.callback_data == "ticket_cat:services"
        
        general_btn = keyboard.inline_keyboard[3][0]
        assert general_btn.text == "❓ General"
        assert general_btn.callback_data == "ticket_cat:general"


class TestTicketsKeyboardTicketActions:
    """Test ticket_actions keyboard."""

    def test_ticket_actions(self):
        """Test ticket actions keyboard."""
        keyboard = TicketsKeyboard.ticket_actions("uuid-123")
        
        # Verify keyboard structure (3 rows)
        assert len(keyboard.inline_keyboard) == 3
        
        # Verify buttons
        send_btn = keyboard.inline_keyboard[0][0]
        assert send_btn.text == "📩 Enviar Mensaje"
        assert send_btn.callback_data == "ticket_send:uuid-123"
        
        close_btn = keyboard.inline_keyboard[1][0]
        assert close_btn.text == "✅ Cerrar Ticket"
        assert close_btn.callback_data == "ticket_close:uuid-123"
        
        back_btn = keyboard.inline_keyboard[2][0]
        assert back_btn.text == "🔙 Volver"
        assert back_btn.callback_data == "tickets_back"


class TestTicketsKeyboardBackToTickets:
    """Test back_to_tickets keyboard."""

    def test_back_to_tickets(self):
        """Test back to tickets keyboard."""
        keyboard = TicketsKeyboard.back_to_tickets()
        
        # Verify keyboard structure (1 row)
        assert len(keyboard.inline_keyboard) == 1
        
        # Verify button
        back_btn = keyboard.inline_keyboard[0][0]
        assert back_btn.text == "🔙 Volver a Tickets"
        assert back_btn.callback_data == "tickets_back"
