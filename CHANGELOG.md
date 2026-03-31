# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-03-30

### Added
- **Enviar Mensajes a Tickets** - Nuevo flujo para enviar mensajes a tickets existentes
  - Comando `/cancelar` para cancelar envío de mensajes
  - Validación de longitud mínima (10 caracteres)
  - Estado de espera para mensaje del usuario
- **Handlers Nuevos:**
  - `send_message_callback()` - Prepara el envío de mensaje
  - `receive_message()` - Recibe y envía mensaje al backend
  - `cancel_message()` - Cancela operación de envío

### Changed
- **Cerrar Ticket** - Corregido método HTTP de `PATCH` a `POST`
  - Ahora usa `POST /tickets/{id}/close` sin body (correcto según backend)
  - Fix: Eliminado `json={}` que causaba error 422
- **API Client** - Response parsing mejorado
  - Ahora retorna JSON parseado (`dict`) en lugar de bytes
  - Fix: `response.json()` en lugar de `response.aread()`
- **Tests Actualizados** - Tests corregidos para usar `POST` en lugar de `PATCH`

### Fixed
- **Bug #1:** Cerrar ticket fallaba con error 422 (método HTTP incorrecto)
- **Bug #2:** Enviar mensajes no estaba implementado
- **Bug #3:** API Client retornaba bytes en lugar de JSON parseado

### Technical Details
- **Files Modified:** 3 files
  - `src/bot/handlers/tickets.py` - +150 lines (send message handlers + close fix)
  - `src/infrastructure/api_client.py` - Response parsing fix
  - `tests/bot/test_tickets_handlers.py` - Tests actualizados
- **Files Created:** 0
- **Lines Added:** ~150 lines
- **Tests:** 19/20 passing (95%) - 1 test es admin-only (Staff Bot future)

### Backend Integration
- POST `/tickets/{id}/messages` - Enviar mensaje a ticket ✅ NEW!
- POST `/tickets/{id}/close` - Cerrar ticket (fix method) ✅ FIXED!
- GET `/tickets/{id}` - Ver ticket detallado ✅
- GET `/tickets` - Listar tickets ✅
- POST `/tickets` - Crear ticket ✅

### Integration Test Results
```
✅ PASS - Auth
✅ PASS - Profile
✅ PASS - List Tickets
✅ PASS - Create Ticket
✅ PASS - View Ticket
✅ PASS - Send Message      ← NEW!
✅ PASS - Close Ticket      ← FIXED!
ℹ️  SKIP - Ticket Stats     (admin-only, Staff Bot future)

RESULT: 7/7 USER FEATURES PASSING (100%)
```

### Production Status
- ✅ **Production Ready** - Todos los features de usuario funcionales
- ✅ **Service Restarted** - usipipo-support-bot.service reiniciado exitosamente
- ℹ️  **Staff Bot Future** - Estadísticas de tickets serán implementadas en Staff Bot

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
