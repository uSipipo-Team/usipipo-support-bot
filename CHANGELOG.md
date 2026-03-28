# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/uSipipo-Team/usipipo-support-bot/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/uSipipo-Team/usipipo-support-bot/releases/tag/v0.1.0
