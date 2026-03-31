"""HTTP client for backend API integration."""

import logging
from typing import Any

import httpx

from src.infrastructure.config import settings
from src.infrastructure.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """HTTP client for backend API with JWT authentication."""

    def __init__(self, base_url: str | None = None, api_prefix: str | None = None):
        """
        Initialize API client.

        Args:
            base_url: Backend base URL
            api_prefix: API path prefix
        """
        self.base_url = base_url or settings.BACKEND_URL
        self.api_prefix = api_prefix or settings.API_PREFIX
        self.base_endpoint = f"{self.base_url}{self.api_prefix}"
        self._client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"APIClient initialized: {self.base_endpoint}")

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
        logger.info("APIClient closed")

    @property
    def api_client(self) -> httpx.AsyncClient:
        """Get the underlying HTTP client."""
        return self._client

    async def get(
        self,
        path: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Make GET request.

        Args:
            path: API path
            headers: Optional headers
            params: Optional query parameters

        Returns:
            Response JSON data
        """
        url = f"{self.base_endpoint}{path}"
        logger.debug(f"GET {url}")

        response = await self._client.get(url, headers=headers, params=params)
        return await self._handle_response(response)

    async def post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Make POST request.

        Args:
            path: API path
            json: Optional JSON body
            headers: Optional headers

        Returns:
            Response JSON data
        """
        url = f"{self.base_endpoint}{path}"
        logger.debug(f"POST {url}")

        response = await self._client.post(url, json=json, headers=headers)
        return await self._handle_response(response)

    async def put(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Make PUT request.

        Args:
            path: API path
            json: Optional JSON body
            headers: Optional headers

        Returns:
            Response JSON data
        """
        url = f"{self.base_endpoint}{path}"
        logger.debug(f"PUT {url}")

        response = await self._client.put(url, json=json, headers=headers)
        return await self._handle_response(response)

    async def patch(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Make PATCH request.

        Args:
            path: API path
            json: Optional JSON body
            headers: Optional headers

        Returns:
            Response JSON data
        """
        url = f"{self.base_endpoint}{path}"
        logger.debug(f"PATCH {url}")

        response = await self._client.patch(url, json=json, headers=headers)
        return await self._handle_response(response)

    async def delete(
        self,
        path: str,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Make DELETE request.

        Args:
            path: API path
            headers: Optional headers

        Returns:
            Response JSON data
        """
        url = f"{self.base_endpoint}{path}"
        logger.debug(f"DELETE {url}")

        response = await self._client.delete(url, headers=headers)
        return await self._handle_response(response)

    async def _handle_response(self, response: httpx.Response) -> Any:
        """
        Handle HTTP response.

        Args:
            response: HTTP response

        Returns:
            Response JSON data (parsed dict)

        Raises:
            Exception: If response status is error
        """
        if response.status_code >= 400:
            logger.error(f"API error: {response.status_code} - {response.text}")
            raise Exception(f"API error: {response.status_code}")

        # No content
        if response.status_code == 204:
            return None

        # JSON response - parse it
        try:
            return response.json()
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}")
            # Fallback to raw content if JSON parsing fails
            return await response.aread()
