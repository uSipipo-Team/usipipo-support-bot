# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-03-28

### Added
- **AuthHandler** - Autenticación invisible para usuarios de Telegram
- **Comando /me** - Mostrar perfil de usuario autenticado
- **Comando /unlink** - Revocar acceso del bot
- **Mensajes de autenticación** - Mensajes mejorados para usuarios no autenticados
- **Auto-registro automático** - Integración con endpoint `/auth/telegram/auto-register` del backend

### Changed
- **/start ahora autentica** - El comando `/start` registra y autentica automáticamente al usuario
- **Mensajes de error mejorados** - Ahora incluyen prompt "Usa /start para autenticarte"
- **Soporte para usuarios existentes** - Usuarios de `@usipipobot` acceden automáticamente al support bot

### Technical Details
- **Files Created:** 2 files (`src/bot/handlers/auth.py`, `src/bot/keyboards/auth.py`)
- **Files Modified:** 3 files (`src/main.py`, `src/bot/handlers/tickets.py`, `src/bot/keyboards/messages_tickets.py`)
- **Lines Added:** ~250 lines
- **Tests:** Pendientes de implementación

### Backend Integration
- POST /api/v1/auth/telegram/auto-register - Auto-registro de usuarios
- POST /api/v1/auth/refresh - Auto-refresh de tokens JWT
- GET /users/me - Obtener perfil de usuario

## [0.1.0] - 2026-03-28

### Added
- Initial release of uSipipo Support Bot
- Ticket management system (`/tickets`, `/nuevoticket`)
- Category selection (Technical, Billing, Services, General)
- Ticket message history
- Invisible authentication with JWT
- Redis token storage with auto-refresh
- Comprehensive test suite (90%+ coverage)
- CI/CD pipeline (Ruff, Mypy, Pytest, Bandit)
- Docker support
- systemd service configuration
- Professional documentation

### Technical Details
- Python 3.13
- python-telegram-bot v21.0+
- Hexagonal architecture
- Backend integration: usipipo-backend v0.10.0+

[Unreleased]: https://github.com/uSipipo-Team/usipipo-support-bot/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/uSipipo-Team/usipipo-support-bot/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/uSipipo-Team/usipipo-support-bot/releases/tag/v0.1.0
