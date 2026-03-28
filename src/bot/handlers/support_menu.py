"""Handlers for Support Bot main menu."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from src.bot.keyboards.support import SupportKeyboard
from src.bot.keyboards.messages_tickets import TicketsMessages
from src.bot.keyboards.auth import AuthMessages

logger = logging.getLogger(__name__)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main support menu."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    message = (
        "👋 *¡Hola! Bienvenido al Soporte Técnico de uSipipo* ✨\n\n"
        "Soy tu asistente virtual y estoy aquí para ayudarte.\n\n"
        "*¿Qué necesitas hoy?*"
    )

    await query.edit_message_text(
        text=message,
        reply_markup=SupportKeyboard.main_menu(),
        parse_mode="Markdown",
    )


async def show_tickets_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show tickets menu (redirect to /tickets)."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    message = (
        "🎫 *Gestión de Tickets*\n\n"
        "Aquí puedes ver y gestionar tus tickets de soporte.\n\n"
        "Usa el comando /tickets para ver tus tickets existentes."
    )

    await query.edit_message_text(
        text=message,
        reply_markup=SupportKeyboard.back_to_main(),
        parse_mode="Markdown",
    )


async def show_new_ticket_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show new ticket menu (redirect to /nuevoticket)."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    message = (
        "📝 *Crear Nuevo Ticket*\n\n"
        "Para crear un nuevo ticket de soporte, usa el comando /nuevoticket.\n\n"
        "🔹 *Categorías disponibles:*\n"
        "• 🖥️ Técnico - Problemas con VPN, conexión\n"
        "• 💳 Pagos - Problemas con pagos, facturación\n"
        "• 📦 Servicios - Planes, paquetes de datos\n"
        "• ❓ General - Otras consultas"
    )

    await query.edit_message_text(
        text=message,
        reply_markup=SupportKeyboard.back_to_main(),
        parse_mode="Markdown",
    )


async def show_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help/FAQ menu."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    message = (
        "❓ *Ayuda y Preguntas Frecuentes*\n\n"
        "🔹 *Problemas Comunes:*\n\n"
        "1️⃣ *La VPN no conecta*\n"
        "• Verifica tu conexión a internet\n"
        "• Revisa que tu clave no haya expirado\n"
        "• Intenta reconectar\n\n"
        "2️⃣ *La conexión es lenta*\n"
        "• Prueba en speedtest.net o check-host.net\n"
        "• Verifica si hay problemas del servicio\n"
        "• Intenta cambiar de servidor\n\n"
        "3️⃣ *Problemas de pago*\n"
        "• Verifica tu método de pago\n"
        "• Contacta soporte si el problema persiste\n\n"
        "🔹 *¿No encuentras tu respuesta?*\n"
        "Crea un ticket y nuestro equipo te ayudará."
    )

    await query.edit_message_text(
        text=message,
        reply_markup=SupportKeyboard.quick_help(),
        parse_mode="Markdown",
    )


async def show_status_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show service status."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    message = (
        "📊 *Estado del Servicio*\n\n"
        "✅ *Todos los sistemas operativos*\n\n"
        "• Bot: OK\n"
        "• Backend: OK\n"
        "• Servidores VPN: OK\n"
        "• Sistema de Tickets: OK\n\n"
        "🔹 *¿Problemas?*\n"
        "Si estás experimentando problemas, crea un ticket."
    )

    await query.edit_message_text(
        text=message,
        reply_markup=SupportKeyboard.back_to_main(),
        parse_mode="Markdown",
    )


async def show_agent_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show agent contact menu."""
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    message = (
        "💬 *Hablar con un Agente*\n\n"
        "Para hablar con un agente de soporte:\n\n"
        "1️⃣ *Crea un ticket* - Es el método más rápido\n"
        "2️⃣ *Describe tu problema* - Sé lo más detallado posible\n"
        "3️⃣ *Espera respuesta* - Te responderemos lo antes posible\n\n"
        "🔹 *Tiempo de respuesta promedio:*\n"
        "• Horario laboral: 1-2 horas\n"
        "• Fuera de horario: 24 horas\n\n"
        "Usa /nuevoticket para crear un ticket."
    )

    await query.edit_message_text(
        text=message,
        reply_markup=SupportKeyboard.back_to_main(),
        parse_mode="Markdown",
    )


def get_support_menu_handlers():
    """Return all support menu callback handlers."""
    from telegram.ext import CallbackQueryHandler

    return [
        CallbackQueryHandler(show_main_menu, pattern="^support_main_menu$"),
        CallbackQueryHandler(show_tickets_menu, pattern="^support_tickets$"),
        CallbackQueryHandler(show_new_ticket_menu, pattern="^support_new_ticket$"),
        CallbackQueryHandler(show_help_menu, pattern="^support_help$"),
        CallbackQueryHandler(show_status_menu, pattern="^support_status$"),
        CallbackQueryHandler(show_agent_menu, pattern="^support_agent$"),
    ]
