"""
WeatherAPI service with reusable aiohttp session and proper error handling.
"""

import logging
import aiohttp

from app import config

logger = logging.getLogger(__name__)


class WeatherApiError(Exception):
    """Base WeatherAPI error."""


class CityNotFoundError(WeatherApiError):
    """City not found (400 / 1006)."""


class InvalidApiKeyError(WeatherApiError):
    """Invalid or missing API key (401/403 or 2008)."""


class WeatherServiceUnavailableError(WeatherApiError):
    """Service temporarily unavailable (network, 500, timeout)."""


class WeatherService:
    """Async WeatherAPI client with reusable ClientSession."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or config.WEATHER_API_KEY
        self.base_url = base_url or config.WEATHER_API_BASE_URL
        self.session: aiohttp.ClientSession | None = None

    async def create_session(self) -> None:
        """Create aiohttp session if not exists or closed."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=10, connect=5, sock_read=7)
            self.session = aiohttp.ClientSession(timeout=timeout)
            logger.info("WeatherAPI session created")

    async def close(self) -> None:
        """Close aiohttp session cleanly."""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("WeatherAPI session closed")

    async def get_current_weather(self, city: str) -> dict:
        """
        Fetch current weather for city.
        Raises: CityNotFoundError, InvalidApiKeyError, WeatherServiceUnavailableError
        """
        if not city or not city.strip():
            raise CityNotFoundError("Empty city name")

        if not self.api_key:
            raise InvalidApiKeyError("Missing API key")

        await self.create_session()
        assert self.session is not None

        params = {
            "key": self.api_key,
            "q": city.strip(),
            "aqi": "no",
        }

        try:
            async with self.session.get(self.base_url, params=params) as response:
                # Try to parse JSON regardless of status for error codes
                try:
                    data = await response.json()
                except Exception as e:
                    logger.error(f"Invalid JSON response for city {city}: {e}")
                    raise WeatherServiceUnavailableError("Invalid JSON response")

                if response.status == 200:
                    return data

                # Handle API errors
                error = data.get("error", {}) if isinstance(data, dict) else {}
                error_code = error.get("code")
                error_msg = error.get("message", "")

                logger.warning(f"WeatherAPI error {response.status} code={error_code} msg={error_msg} city={city}")

                # City not found: 1006
                if response.status == 400 and error_code == 1006:
                    raise CityNotFoundError(f"City not found: {city}")

                # API key errors: 1002, 2006-2008
                if response.status in (401, 403) or error_code in (1002, 2006, 2007, 2008):
                    raise InvalidApiKeyError(f"Invalid API key: {error_msg}")

                # Bad request also treat as city not found if not key error
                if response.status == 400:
                    raise CityNotFoundError(f"City not found: {city}")

                # Server errors
                if response.status >= 500:
                    raise WeatherServiceUnavailableError(f"Server error {response.status}")

                # Fallback
                raise WeatherServiceUnavailableError(f"API error {response.status}: {error_msg}")

        except CityNotFoundError:
            raise
        except InvalidApiKeyError:
            raise
        except WeatherServiceUnavailableError:
            raise
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching weather for {city}: {e}")
            raise WeatherServiceUnavailableError(f"Network error: {e}") from e
        except Exception as e:
            # If already our custom errors, re-raise, else wrap
            if isinstance(e, WeatherApiError):
                raise
            logger.exception(f"Unexpected error fetching weather for {city}: {e}")
            raise WeatherServiceUnavailableError(str(e)) from e


# Global singleton for reuse across handlers (session reuse)
weather_service = WeatherService()
