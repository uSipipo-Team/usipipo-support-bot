"""Global error handler for Telegram bot."""

import logging

from telegram import Update
from telegram.error import BadRequest, Forbidden, NetworkError, TelegramError
from telegram.ext import ContextTypes

from src.infrastructure.logger import get_logger

logger = get_logger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors in the Telegram bot.

    Args:
        update: The update that caused the error
        context: The context object containing error information
    """
    # Log the error
    logger.error(
        "Exception while handling an update:",
        exc_info=context.error,
        extra={
            "update_type": type(update).__name__,
            "chat_id": context.chat_id if hasattr(context, "chat_id") else None,
        },
    )

    # Check if we can reply to the user
    if isinstance(update, Update) and update.effective_message:
        # Handle specific error types
        if isinstance(context.error, Forbidden):
            # The bot was blocked by the user
            logger.warning(f"Bot was blocked by user {context.user_id}")
            return

        if isinstance(context.error, BadRequest):
            # Bad request (e.g., message to edit not found)
            logger.warning(f"Bad request: {context.error.message}")
            return

        if isinstance(context.error, NetworkError):
            # Network error
            logger.warning(f"Network error: {context.error}")
            await update.effective_message.reply_text(
                "⚠️ Error de conexión. Por favor intentá de nuevo en unos segundos.",
            )
            return

        # Generic error message
        await update.effective_message.reply_text(
            "❌ Ocurrió un error inesperado. Por favor intentá de nuevo.\n\n"
            "Si el problema persiste, contactá a soporte.",
        )
