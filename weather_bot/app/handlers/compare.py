"""
Compare handler - /compare city1 city2 with concurrent fetching via asyncio.gather
"""

import asyncio
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.city_mapper import normalize_city
from app.services.weather_api import weather_service, CityNotFoundError, InvalidApiKeyError, WeatherServiceUnavailableError
from app.utils.formatter import format_compare

logger = logging.getLogger(__name__)
router = Router()


COMPARE_USAGE = (
    "❌ <b>فرمت صحیح:</b>\n"
    "<code>/compare شهر اول شهر دوم</code>\n\n"
    "مثال:\n"
    "<code>/compare تهران مشهد</code>\n"
    "<code>/compare Tehran London</code>\n\n"
    "برای شهرهای دو کلمه‌ای:\n"
    "<code>/compare New York, London</code>"
)


def parse_compare_args(text: str) -> tuple[str | None, str | None, str | None]:
    """
    Parse /compare arguments.
    Returns (city1_raw, city2_raw, error)
    Supports:
      /compare تهران مشهد
      /compare Tehran London
      /compare New York, London
      /compare تهران، مشهد (with Persian comma)
    """
    # Remove command prefix
    if text.startswith("/compare"):
        raw = text[len("/compare"):].strip()
    else:
        raw = text.strip()

    if not raw:
        return None, None, "empty"

    # Normalize different comma types
    raw = raw.replace("،", ",")

    # If comma present, split by comma (for multi-word cities)
    if "," in raw:
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if len(parts) != 2:
            return None, None, "invalid_comma"
        city1, city2 = parts[0], parts[1]
        if not city1 or not city2:
            return None, None, "missing"
        if len(city1) > 100 or len(city2) > 100:
            return None, None, "too_long"
        return city1, city2, None

    # No comma: split by whitespace
    parts = raw.split()
    if len(parts) < 2:
        return None, None, "missing"
    if len(parts) == 2:
        return parts[0], parts[1], None

    # More than 2 words without comma - ambiguous, show usage
    return None, None, "invalid_space"


@router.message(Command("compare"))
async def compare_handler(message: Message) -> None:
    """Handle /compare command with concurrent requests."""
    if not message.text:
        await message.answer(COMPARE_USAGE)
        return

    city1_raw, city2_raw, error = parse_compare_args(message.text)

    if error:
        if error == "missing":
            await message.answer(
                "❌ <b>لطفاً نام دو شهر را وارد کنید.</b>\n\n" + COMPARE_USAGE
            )
        elif error in ("invalid_comma", "invalid_space"):
            await message.answer(COMPARE_USAGE)
        elif error == "empty":
            await message.answer(COMPARE_USAGE)
        elif error == "too_long":
            await message.answer("❌ نام شهر بیش از حد طولانی است.")
        else:
            await message.answer(COMPARE_USAGE)
        return

    assert city1_raw is not None and city2_raw is not None

    city1_api = normalize_city(city1_raw)
    city2_api = normalize_city(city2_raw)

    # Inform user we are fetching (optional, not required but nice)
    # Do not block, just proceed to fetch concurrently

    try:
        # MUST use asyncio.gather concurrently
        data1, data2 = await asyncio.gather(
            weather_service.get_current_weather(city1_api),
            weather_service.get_current_weather(city2_api),
        )

        text = format_compare(data1, data2)
        await message.answer(text)

    except CityNotFoundError as e:
        logger.warning(f"City not found in compare: {city1_api}, {city2_api} error={e}")
        await message.answer("❌ <b>شهر موردنظر پیدا نشد. لطفاً نام شهر را بررسی کنید.</b>")
    except InvalidApiKeyError:
        logger.error("Invalid API key in compare")
        await message.answer("❌ <b>خطا در اتصال به سرویس هواشناسی. لطفاً بعداً دوباره تلاش کنید.</b>")
    except WeatherServiceUnavailableError as e:
        logger.error(f"Weather service unavailable in compare: {e}")
        await message.answer("⚠️ <b>سرویس هواشناسی موقتاً در دسترس نیست. لطفاً چند لحظه بعد دوباره امتحان کنید.</b>")
    except Exception as e:
        logger.exception(f"Unexpected error in compare_handler: {e}")
        await message.answer("⚠️ <b>خطای غیرمنتظره‌ای رخ داد. لطفاً دوباره تلاش کنید.</b>")
