"""JWT authentication middleware."""

import logging
from typing import Any

from telegram import Update
from telegram.ext import BaseMiddleware, Dispatcher

from src.infrastructure.api_client import APIClient
from src.infrastructure.logger import get_logger
from src.infrastructure.token_storage import TokenStorage

logger = get_logger(__name__)


class AuthMiddleware(BaseMiddleware):
    """Middleware for JWT authentication."""

    def __init__(self, api_client: APIClient, token_storage: TokenStorage):
        """
        Initialize auth middleware.

        Args:
            api_client: API client for token refresh
            token_storage: Token storage instance
        """
        super().__init__()
        self.api = api_client
        self.tokens = token_storage
        logger.info("AuthMiddleware initialized")

    async def __call__(
        self,
        handler: Any,
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        """
        Process update through middleware.

        Args:
            handler: Next handler in chain
            event: Telegram update
            data: Handler data

        Returns:
            Handler result
        """
        # Skip if no user (e.g., callback queries without message)
        if not isinstance(event, Update) or event.effective_user is None:
            return await handler(event, data)

        telegram_id = event.effective_user.id

        # Check authentication
        if not await self.tokens.is_authenticated(telegram_id):
            logger.warning(f"Unauthenticated access attempt by user {telegram_id}")
            if event.effective_message:
                await event.effective_message.reply_text(
                    "❌ Por favor, iniciá sesión primero con /start",
                )
            return None

        # Check if token needs refresh
        if await self.tokens.needs_refresh(telegram_id):
            logger.info(f"Refreshing token for user {telegram_id}")
            await self._refresh_token(telegram_id)

        return await handler(event, data)

    async def _refresh_token(self, telegram_id: int) -> None:
        """
        Refresh user's JWT token.

        Args:
            telegram_id: User's Telegram ID
        """
        try:
            tokens = await self.tokens.get(telegram_id)
            if tokens is None:
                return

            # Call refresh endpoint
            response = await self.api.post(
                "/auth/refresh",
                json={"refresh_token": tokens["refresh_token"]},
            )

            # Save new tokens
            await self.tokens.save(
                telegram_id,
                {
                    "access_token": response["access_token"],
                    "refresh_token": response["refresh_token"],
                    "expires_at": response["expires_in"],
                    "user_id": response["user_id"],
                },
            )

            logger.info(f"Token refreshed for user {telegram_id}")

        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
