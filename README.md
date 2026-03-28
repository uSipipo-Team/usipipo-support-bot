# uSipipo Support Bot

[![Production](https://img.shields.io/badge/status-production-success.svg)](https://github.com/uSipipo-Team/usipipo-support-bot)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/uSipipo-Team/usipipo-support-bot/releases)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Bot de Telegram dedicado para gestión de tickets de soporte técnico del ecosistema uSipipo

## 📋 Descripción

uSipipo Support Bot es un bot de Telegram especializado en la gestión de tickets de soporte técnico. Proporciona a los usuarios una interfaz sencilla para crear, rastrear y comunicarse sobre sus tickets de soporte, de manera independiente al bot principal de características (`@usipipobot`).

## 🎯 Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Iniciar bot y mostrar bienvenida | `/start` |
| `/help` | Mostrar ayuda | `/help` |
| `/tickets` | Listar todos mis tickets | `/tickets` |
| `/nuevoticket` | Crear nuevo ticket de soporte | `/nuevoticket` |

## 🚀 Características

- ✅ **Gestión de Tickets** - Crear, ver y cerrar tickets
- ✅ **Categorías** - Técnico, Pagos, Servicios, General
- ✅ **Mensajería** - Enviar y recibir mensajes en tickets
- ✅ **Autenticación Invisible** - JWT con auto-refresh
- ✅ **Notificaciones** - Alertas en tiempo real
- ✅ **Historial** - Complete message history per ticket

## 📦 Instalación

### Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/uSipipo-Team/usipipo-support-bot.git
cd usipipo-support-bot

# Instalar dependencias con uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --dev

# Configurar entorno
cp example.env .env
# Editar .env con tus credenciales

# Ejecutar tests
uv run pytest

# Ejecutar bot
uv run python -m src
```

### Docker

```bash
# Build
docker build -t usipipo-support-bot .

# Ejecutar
docker run --env-file .env usipipo-support-bot
```

### Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f support-bot
```

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` con:

```bash
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_support
BOT_USERNAME=uSipipoSupport_Bot

# Backend API
BACKEND_URL=https://api.usipipo.com
API_PREFIX=/api/v1

# Redis
REDIS_URL=redis://localhost:6379/1

# Logging
LOG_LEVEL=INFO
```

### Obtener Bot Token

1. Hablar con [@BotFather](https://t.me/BotFather)
2. Enviar `/newbot`
3. Seguir instrucciones
4. Copiar token

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Telegram      │
│ @uSipipoSupport_Bot │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Support Bot    │
│  (Python 3.13)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Backend v0.10  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL+Redis│
└─────────────────┘
```

Ver [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) para más detalles.

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/bot/test_tickets_handlers.py
```

## 📊 Cobertura de Tests

| Tipo | Cantidad | Cobertura |
|------|----------|-----------|
| Unit Tests | ~50 | 90%+ |
| Integration Tests | ~10 | Critical paths |
| E2E Tests | ~5 | Happy paths |
| **Total** | **~65** | **90%+** |

## 🚀 Deployment en Producción

### systemd Service

```bash
# Copiar service file
sudo cp usipipo-support-bot.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio
sudo systemctl enable usipipo-support-bot

# Iniciar servicio
sudo systemctl start usipipo-support-bot

# Ver estado
sudo systemctl status usipipo-support-bot
```

Ver [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) para guía completa.

## 📖 Documentación

La documentación completa está centralizada en el repositorio principal:

- [Architecture](https://github.com/uSipipo-Team/usipipo-docs/tree/main/support-bot/ARCHITECTURE.md) - Arquitectura del sistema
- [Deployment](https://github.com/uSipipo-Team/usipipo-docs/tree/main/support-bot/DEPLOYMENT.md) - Guía de despliegue
- [User Guide](https://github.com/uSipipo-Team/usipipo-docs/tree/main/support-bot/USER-GUIDE.md) - Guía de usuario
- [Design Document](https://github.com/uSipipo-Team/usipipo-docs/tree/main/plans/support-bot/2026-03-28-support-bot-design.md) - Diseño técnico
- [Implementation Plan](https://github.com/uSipipo-Team/usipipo-docs/tree/main/plans/support-bot/implementation-plan.md) - Plan de implementación
- [CHANGELOG](CHANGELOG.md) - Historial de cambios
- [CONTRIBUTING](CONTRIBUTING.md) - Guía de contribución

## 🔗 Enlaces Relacionados

- **Design Document:** [plans/support-bot/2026-03-28-support-bot-design.md](https://github.com/uSipipo-Team/usipipo-docs/tree/main/plans/support-bot/)
- **Main Bot:** [usipipo-telegram-bot](https://github.com/uSipipo-Team/usipipo-telegram-bot)
- **Backend:** [usipipo-backend](https://github.com/uSipipo-Team/usipipo-backend)
- **Ecosystem:** [usipipo-docs](https://github.com/uSipipo-Team/usipipo-docs)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

## 👥 Equipo

Desarrollado por el equipo de uSipipo.

**Contacto:** usipipo@gmail.com

---

**Hecho con ❤️ para el ecosistema uSipipo**
