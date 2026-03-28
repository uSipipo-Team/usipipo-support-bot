"""Mensajes de autenticación para el uSipipo Support Bot."""


class AuthMessages:
    """Mensajes para autenticación invisible en Support Bot."""

    # /start command
    WELCOME_NEW_USER = (
        "✅ ¡Bienvenido a uSipipo Support!\n\n"
        "Tu cuenta ha sido creada y estás autenticado.\n\n"
        "Usa el menú principal para navegar."
    )

    WELCOME_RETURNING_USER = (
        "👋 *¡Hola! Bienvenido al Soporte Técnico de uSipipo* ✨\n\n"
        "Soy tu asistente virtual y estoy aquí para ayudarte.\n\n"
        "*¿Qué necesitas hoy?*\n\n"
        "🎫 *Gestión de Tickets*\n"
        "• Ver tus tickets existentes\n"
        "• Crear nuevo ticket\n"
        "• Consultar estado\n\n"
        "❓ *Ayuda y Recursos*\n"
        "• Preguntas frecuentes\n"
        "• Estado del servicio\n"
        "• Hablar con agente\n\n"
        "🔹 *Si vienes de @usipipobot*, podemos ayudarte con:\n"
        "• Problemas de conexión VPN\n"
        "• Facturación y pagos\n"
        "• Configuración de claves\n"
        "• Otros problemas técnicos"
    )

    # Deep link specific messages
    WELCOME_FROM_MAIN_BOT = (
        "👋 *¡Hola! Veo que vienes de @usipipobot* ✨\n\n"
        "Entiendo que necesitas ayuda con algo.\n\n"
        "Para brindarte la mejor atención, por favor:\n\n"
        "1️⃣ *Revisa tus tickets existentes* - Puede que ya tengas uno en proceso\n"
        "2️⃣ *Crea un nuevo ticket* - Si es un problema nuevo\n"
        "3️⃣ *Consulta el estado del servicio* - Para ver si hay problemas generales\n\n"
        "🔹 *Nuestro equipo te responderá lo antes posible*"
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
