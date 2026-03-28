"""Structured logging configuration."""

import logging
import sys
from typing import Any

from src.infrastructure.config import settings


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields
        if hasattr(record, "telegram_id"):
            log_data["telegram_id"] = record.telegram_id
        if hasattr(record, "ticket_id"):
            log_data["ticket_id"] = record.ticket_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Simple string representation (not actual JSON for readability)
        parts = [f'{k}="{v}"' if isinstance(v, str) else f"{k}={v}" for k, v in log_data.items()]
        return " ".join(parts)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    logger_instance = logging.getLogger(name)

    # Only configure if not already configured
    if not logger_instance.handlers:
        logger_instance.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

        # Use JSON formatter for production, simple for development
        if settings.LOG_FILE:
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )

        logger_instance.addHandler(console_handler)

        # File handler if configured
        if settings.LOG_FILE:
            try:
                file_handler = logging.FileHandler(settings.LOG_FILE)
                file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
                file_handler.setFormatter(JSONFormatter())
                logger_instance.addHandler(file_handler)
            except Exception as e:
                logger_instance.warning(f"Failed to create log file: {e}")

        # Prevent propagation to root logger
        logger_instance.propagate = False

    return logger_instance
