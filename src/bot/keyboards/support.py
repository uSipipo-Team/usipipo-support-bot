"""Inline keyboards for Support Bot main menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class SupportKeyboard:
    """Main menu keyboards for Support Bot."""

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """
        Keyboard for support main menu.

        Returns:
            InlineKeyboardMarkup: Keyboard with support options
        """
        keyboard = [
            # Tickets
            [
                InlineKeyboardButton("🎫 Mis Tickets", callback_data="support_tickets"),
                InlineKeyboardButton("📝 Nuevo Ticket", callback_data="support_new_ticket"),
            ],
            # Help & Status
            [
                InlineKeyboardButton("❓ Ayuda / FAQ", callback_data="support_help"),
                InlineKeyboardButton("📊 Estado del Servicio", callback_data="support_status"),
            ],
            # Agent Support
            [
                InlineKeyboardButton("💬 Hablar con Agente", callback_data="support_agent"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def quick_help() -> InlineKeyboardMarkup:
        """
        Keyboard for quick help options.

        Returns:
            InlineKeyboardMarkup: Keyboard with quick help options
        """
        keyboard = [
            [
                InlineKeyboardButton("📊 Ver Estado del Servicio", callback_data="support_status"),
            ],
            [
                InlineKeyboardButton("📝 Crear Ticket", callback_data="support_new_ticket"),
            ],
            [
                InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="support_main_menu"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_main() -> InlineKeyboardMarkup:
        """
        Keyboard to go back to main menu.

        Returns:
            InlineKeyboardMarkup: Back button
        """
        keyboard = [
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="support_main_menu")],
        ]
        return InlineKeyboardMarkup(keyboard)
