"""Redis connection pool management."""

import logging
from typing import ClassVar

import redis.asyncio as redis

from src.infrastructure.logger import get_logger

logger = get_logger(__name__)


class RedisPool:
    """Redis connection pool singleton."""

    _instance: ClassVar["RedisPool | None"] = None
    _pool: ClassVar[redis.ConnectionPool | None] = None

    def __init__(self):
        """Private constructor."""
        if RedisPool._instance is not None:
            raise RuntimeError("Use RedisPool.get_instance() instead")

    @classmethod
    async def get_instance(cls, redis_url: str) -> "RedisPool":
        """
        Get or create the Redis pool singleton.

        Args:
            redis_url: Redis connection URL

        Returns:
            RedisPool instance
        """
        if cls._instance is None:
            cls._instance = cls()
            cls._pool = redis.ConnectionPool.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=50,
            )
            logger.info(f"Redis pool created: {redis_url}")

        return cls._instance

    @classmethod
    def get_client(cls) -> redis.Redis:
        """
        Get a Redis client from the pool.

        Returns:
            Redis client instance
        """
        if cls._pool is None:
            raise RuntimeError("RedisPool not initialized. Call get_instance() first.")

        return redis.Redis(connection_pool=cls._pool)

    @classmethod
    async def close(cls) -> None:
        """Close the Redis pool."""
        if cls._pool is not None:
            await cls._pool.disconnect()
            cls._pool = None
            cls._instance = None
            logger.info("Redis pool closed")

    @classmethod
    async def health_check(cls) -> bool:
        """
        Check Redis connection health.

        Returns:
            True if Redis is reachable, False otherwise
        """
        try:
            client = cls.get_client()
            await client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
