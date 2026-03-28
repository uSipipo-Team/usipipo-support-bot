"""Tests for Token Storage."""

import json
import time
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from src.infrastructure.token_storage import TokenStorage


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    redis_mock = MagicMock()
    redis_mock.setex = AsyncMock()
    redis_mock.get = AsyncMock()
    redis_mock.delete = AsyncMock()
    return redis_mock


@pytest.fixture
def token_storage(mock_redis):
    """Create TokenStorage with mock Redis."""
    storage = TokenStorage.__new__(TokenStorage)
    storage.ttl_seconds = 30 * 24 * 60 * 60  # 30 days
    storage.redis = mock_redis
    return storage


class TestTokenStorageSave:
    """Test TokenStorage save method."""

    @pytest.mark.asyncio
    async def test_save(self, token_storage, mock_redis):
        """Test saving tokens."""
        telegram_id = 123456789
        tokens = {
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": 9999999999,
            "user_id": "uuid-123"
        }
        
        await token_storage.save(telegram_id, tokens)
        
        # Verify Redis setex was called
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args
        assert call_args[0][0] == f"support_bot:tokens:{telegram_id}"
        assert call_args[0][1] == token_storage.ttl_seconds
        # Verify data is JSON
        data = json.loads(call_args[0][2])
        assert data["access_token"] == "test_access"


class TestTokenStorageGet:
    """Test TokenStorage get method."""

    @pytest.mark.asyncio
    async def test_get_success(self, token_storage, mock_redis):
        """Test getting tokens."""
        telegram_id = 123456789
        tokens_json = json.dumps({
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": 9999999999,
            "user_id": "uuid-123"
        })
        
        mock_redis.get = AsyncMock(return_value=tokens_json)
        
        result = await token_storage.get(telegram_id)
        
        assert result is not None
        assert result["access_token"] == "test_access"
        mock_redis.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_not_found(self, token_storage, mock_redis):
        """Test getting non-existent tokens."""
        telegram_id = 123456789
        
        mock_redis.get = AsyncMock(return_value=None)
        
        result = await token_storage.get(telegram_id)
        
        assert result is None
        mock_redis.get.assert_called_once()


class TestTokenStorageDelete:
    """Test TokenStorage delete method."""

    @pytest.mark.asyncio
    async def test_delete(self, token_storage, mock_redis):
        """Test deleting tokens."""
        telegram_id = 123456789
        
        await token_storage.delete(telegram_id)
        
        mock_redis.delete.assert_called_once()
        call_args = mock_redis.delete.call_args
        assert call_args[0][0] == f"support_bot:tokens:{telegram_id}"


class TestTokenStorageIsAuthenticated:
    """Test TokenStorage is_authenticated method."""

    @pytest.mark.asyncio
    async def test_is_authenticated_true(self, token_storage, mock_redis):
        """Test is_authenticated when tokens exist."""
        telegram_id = 123456789
        tokens_json = json.dumps({
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": 9999999999,
            "user_id": "uuid-123"
        })
        
        mock_redis.get = AsyncMock(return_value=tokens_json)
        
        result = await token_storage.is_authenticated(telegram_id)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_is_authenticated_false(self, token_storage, mock_redis):
        """Test is_authenticated when tokens don't exist."""
        telegram_id = 123456789
        
        mock_redis.get = AsyncMock(return_value=None)
        
        result = await token_storage.is_authenticated(telegram_id)
        
        assert result is False


class TestTokenStorageNeedsRefresh:
    """Test TokenStorage needs_refresh method."""

    @pytest.mark.asyncio
    async def test_needs_refresh_true(self, token_storage, mock_redis):
        """Test needs_refresh when token is about to expire."""
        telegram_id = 123456789
        # Token expires in 2 minutes (less than 5 minute buffer)
        expires_at = int(time.time()) + 120
        
        tokens_json = json.dumps({
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": expires_at,
            "user_id": "uuid-123"
        })
        
        mock_redis.get = AsyncMock(return_value=tokens_json)
        
        result = await token_storage.needs_refresh(telegram_id)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_needs_refresh_false(self, token_storage, mock_redis):
        """Test needs_refresh when token is still valid."""
        telegram_id = 123456789
        # Token expires in 1 hour (more than 5 minute buffer)
        expires_at = int(time.time()) + 3600
        
        tokens_json = json.dumps({
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": expires_at,
            "user_id": "uuid-123"
        })
        
        mock_redis.get = AsyncMock(return_value=tokens_json)
        
        result = await token_storage.needs_refresh(telegram_id)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_needs_refresh_no_tokens(self, token_storage, mock_redis):
        """Test needs_refresh when no tokens exist."""
        telegram_id = 123456789
        
        mock_redis.get = AsyncMock(return_value=None)
        
        result = await token_storage.needs_refresh(telegram_id)
        
        assert result is False


class TestTokenStorageIsTokenExpired:
    """Test TokenStorage is_token_expired method."""

    @pytest.mark.asyncio
    async def test_is_token_expired_true(self, token_storage, mock_redis):
        """Test is_token_expired when token is expired."""
        telegram_id = 123456789
        # Token expired 1 hour ago
        expires_at = int(time.time()) - 3600
        
        tokens_json = json.dumps({
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": expires_at,
            "user_id": "uuid-123"
        })
        
        mock_redis.get = AsyncMock(return_value=tokens_json)
        
        result = await token_storage.is_token_expired(telegram_id)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_is_token_expired_false(self, token_storage, mock_redis):
        """Test is_token_expired when token is still valid."""
        telegram_id = 123456789
        # Token expires in 1 hour
        expires_at = int(time.time()) + 3600
        
        tokens_json = json.dumps({
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "expires_at": expires_at,
            "user_id": "uuid-123"
        })
        
        mock_redis.get = AsyncMock(return_value=tokens_json)
        
        result = await token_storage.is_token_expired(telegram_id)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_is_token_expired_no_tokens(self, token_storage, mock_redis):
        """Test is_token_expired when no tokens exist."""
        telegram_id = 123456789
        
        mock_redis.get = AsyncMock(return_value=None)
        
        result = await token_storage.is_token_expired(telegram_id)
        
        assert result is True
