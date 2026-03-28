"""Mensajes de autenticación para el uSipipo Support Bot."""


class AuthMessages:
    """Mensajes para autenticación invisible en Support Bot."""

    # /start command
    WELCOME_NEW_USER = (
        "✅ ¡Bienvenido a uSipipo Support!\n\n"
        "Tu cuenta ha sido creada y estás autenticado.\n\n"
        "Usa /help para ver los comandos disponibles de soporte."
    )

    WELCOME_RETURNING_USER = (
        "👋 ¡Bienvenido de nuevo a Soporte!\n\n"
        "Tu cuenta está vinculada con @usipipobot.\n\n"
        "Usa /help para ver los comandos disponibles."
    )

    # Auth errors
    AUTH_ERROR = (
        "❌ Error de autenticación.\n\n"
        "Intenta de nuevo en unos minutos."
    )

    # /unlink command
    UNLINK_NOT_AUTHENTICATED = "ℹ️ No tenías sesión iniciada."

    UNLINK_SUCCESS = (
        "✅ Tu cuenta ha sido desvinculada del bot de soporte.\n\n"
        "Tu cuenta principal en @usipipobot no se ve afectada."
    )

    # /me command
    ME_AUTHENTICATED = (
        "👤 <b>Tu Perfil - Soporte</b>\n\n"
        "ID: {user_id}\n"
        "Telegram: @{username}\n\n"
        "Tu cuenta está vinculada con @usipipobot."
    )

    ME_NOT_AUTHENTICATED = (
        "🔒 No autenticado\n\n"
        "Usa /start para iniciar sesión."
    )

    ME_ERROR = (
        "❌ Error al obtener perfil.\n\n"
        "Intenta de nuevo."
    )

    # Auth prompt for protected commands
    NOT_AUTHENTICATED_START_FIRST = (
        "⚠️ No estás autenticado\n\n"
        "Por favor iniciá el bot con /start para acceder a los comandos de soporte."
    )
