"""JWT token storage and management."""

import json
import logging
from datetime import UTC, datetime, timedelta
from typing import TypedDict

from src.infrastructure.logger import get_logger
from src.infrastructure.redis import RedisPool

logger = get_logger(__name__)


class TokenData(TypedDict):
    """Token data structure."""

    access_token: str
    refresh_token: str
    expires_at: int
    user_id: str


class TokenStorage:
    """Store and manage JWT tokens in Redis."""

    def __init__(self, ttl_days: int = 30):
        """
        Initialize token storage.

        Args:
            ttl_days: Token time-to-live in days
        """
        self.ttl_seconds = ttl_days * 24 * 60 * 60
        self.redis = RedisPool.get_client()
        logger.info(f"TokenStorage initialized with TTL: {ttl_days} days")

    def _get_key(self, telegram_id: int) -> str:
        """Get Redis key for a user."""
        return f"support_bot:tokens:{telegram_id}"

    async def save(self, telegram_id: int, tokens: TokenData) -> None:
        """
        Save tokens to Redis.

        Args:
            telegram_id: User's Telegram ID
            tokens: Token data to store
        """
        key = self._get_key(telegram_id)
        await self.redis.setex(key, self.ttl_seconds, json.dumps(tokens))
        logger.debug(f"Tokens saved for user {telegram_id}")

    async def get(self, telegram_id: int) -> TokenData | None:
        """
        Get tokens from Redis.

        Args:
            telegram_id: User's Telegram ID

        Returns:
            Token data or None if not found
        """
        key = self._get_key(telegram_id)
        data = await self.redis.get(key)

        if data is None:
            return None

        return json.loads(data)

    async def delete(self, telegram_id: int) -> None:
        """
        Delete tokens from Redis.

        Args:
            telegram_id: User's Telegram ID
        """
        key = self._get_key(telegram_id)
        await self.redis.delete(key)
        logger.info(f"Tokens deleted for user {telegram_id}")

    async def is_authenticated(self, telegram_id: int) -> bool:
        """
        Check if user is authenticated.

        Args:
            telegram_id: User's Telegram ID

        Returns:
            True if user has valid tokens
        """
        tokens = await self.get(telegram_id)
        return tokens is not None

    async def needs_refresh(self, telegram_id: int, buffer_minutes: int = 5) -> bool:
        """
        Check if tokens need refresh.

        Args:
            telegram_id: User's Telegram ID
            buffer_minutes: Minutes before expiry to refresh

        Returns:
            True if tokens need refresh
        """
        tokens = await self.get(telegram_id)
        if tokens is None:
            return False

        now = datetime.now(UTC).timestamp()
        expires_at = tokens["expires_at"]
        buffer_seconds = buffer_minutes * 60

        return (expires_at - now) < buffer_seconds

    async def is_token_expired(self, telegram_id: int) -> bool:
        """
        Check if token is expired.

        Args:
            telegram_id: User's Telegram ID

        Returns:
            True if token is expired
        """
        tokens = await self.get(telegram_id)
        if tokens is None:
            return True

        now = datetime.now(UTC).timestamp()
        return now > tokens["expires_at"]
