"""uSipipo Support Bot - Main entry point."""

import asyncio
import logging
from typing import Any

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from src.bot.handlers.auth import AuthHandler
from src.bot.handlers.tickets import get_tickets_callback_handlers, get_tickets_handlers
from src.infrastructure.api_client import APIClient
from src.infrastructure.config import settings
from src.infrastructure.error_handler import error_handler
from src.infrastructure.logger import get_logger
from src.infrastructure.redis import RedisPool
from src.infrastructure.token_storage import TokenStorage

logger = get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /start")

    if update.message:
        await update.message.reply_text(
            f"👋 Hola {user.first_name if user else 'Usuario'}!\n\n"
            "Bienvenido al **uSipipo Support Bot**.\n\n"
            "Este bot te ayuda a gestionar tus tickets de soporte técnico.\n\n"
            "📋 *Comandos disponibles:*\n"
            "/tickets - Ver tus tickets\n"
            "/nuevoticket - Crear nuevo ticket\n"
            "/help - Mostrar ayuda\n\n"
            "Para comenzar, usá /nuevoticket para crear un ticket.",
            parse_mode="Markdown",
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /help")

    if update.message:
        await update.message.reply_text(
            "📖 *Ayuda - uSipipo Support Bot*\n\n"
            "Este bot te permite:\n\n"
            "• 🎫 Crear tickets de soporte\n"
            "• 📝 Ver el estado de tus tickets\n"
            "• 💬 Enviar mensajes a tus tickets\n"
            "• ✅ Cerrar tickets resueltos\n\n"
            "*Comandos:*\n"
            "/start - Iniciar el bot\n"
            "/tickets - Ver tus tickets\n"
            "/nuevoticket - Crear nuevo ticket\n"
            "/help - Mostrar esta ayuda\n\n"
            "*Categorías disponibles:*\n"
            "🖥️ Técnico - Problemas con VPN, conexión\n"
            "💳 Pagos - Problemas con pagos, facturación\n"
            "📦 Servicios - Planes, paquetes de datos\n"
            "❓ General - Otras consultas",
            parse_mode="Markdown",
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /status")

    if update.message:
        await update.message.reply_text(
            "✅ **Todos los sistemas operativos**\n\n"
            "Bot: OK\n"
            "Backend: OK\n"
            "Redis: OK",
            parse_mode="Markdown",
        )


# Global instances (initialized in create_application)
_api_client: APIClient | None = None
_token_storage: TokenStorage | None = None
_auth_handler: AuthHandler | None = None


async def _init_dependencies() -> None:
    """Initialize global dependencies."""
    global _api_client, _token_storage, _auth_handler

    # Initialize Redis pool
    await RedisPool.get_instance(settings.REDIS_URL)
    logger.info("Redis pool initialized")

    # Initialize API client
    _api_client = APIClient(
        base_url=settings.BACKEND_URL,
        api_prefix=settings.API_PREFIX,
    )
    logger.info(f"API client initialized: {settings.backend_base_url}")

    # Initialize token storage
    _token_storage = TokenStorage()
    logger.info("Token storage initialized")

    # Initialize auth handler
    _auth_handler = AuthHandler(_api_client, _token_storage)
    logger.info("AuthHandler initialized")


def _get_api_client() -> APIClient:
    """Get initialized API client."""
    if _api_client is None:
        raise RuntimeError("APIClient not initialized. Call _init_dependencies first.")
    return _api_client


def _get_token_storage() -> TokenStorage:
    """Get initialized token storage."""
    if _token_storage is None:
        raise RuntimeError("TokenStorage not initialized. Call _init_dependencies first.")
    return _token_storage


def _get_auth_handler() -> AuthHandler:
    """Get initialized auth handler."""
    if _auth_handler is None:
        raise RuntimeError("AuthHandler not initialized. Call _init_dependencies first.")
    return _auth_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    auth_handler = _get_auth_handler()
    await auth_handler.start_handler(update, context)


async def me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /me command - show user profile."""
    auth_handler = _get_auth_handler()
    await auth_handler.me_handler(update, context)


async def unlink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /unlink command - revoke bot access."""
    auth_handler = _get_auth_handler()
    await auth_handler.unlink_handler(update, context)


def create_application(token: str) -> Application:
    """Create and configure the Telegram application."""
    logger.info("Initializing Support Bot application...")

    # Initialize dependencies (Redis, API client, token storage)
    asyncio.run(_init_dependencies())

    app = Application.builder().token(token).build()

    # Get initialized dependencies
    api_client = _get_api_client()
    token_storage = _get_token_storage()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("unlink", unlink))

    # Register ticket command handlers
    for handler in get_tickets_handlers(api_client, token_storage):
        app.add_handler(handler)

    # Register ticket callback handlers
    for handler in get_tickets_callback_handlers(api_client, token_storage):
        app.add_handler(handler)

    # Register support menu handlers
    from src.bot.handlers.support_menu import get_support_menu_handlers
    for handler in get_support_menu_handlers():
        app.add_handler(handler)

    # Register error handler
    app.add_error_handler(error_handler)  # type: ignore[arg-type]

    logger.info("Support Bot handlers registered successfully")
    return app


def main() -> None:
    """Run the bot."""
    logger.info("Starting uSipipo Support Bot...")

    # Create application
    app = create_application(settings.BOT_TOKEN)

    # Run bot
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
