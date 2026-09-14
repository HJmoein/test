"""
Weather handler - handles plain city name messages.
"""

import logging
import html
from aiogram import Router, F
from aiogram.types import Message

from app.services.city_mapper import normalize_city
from app.services.weather_api import weather_service, CityNotFoundError, InvalidApiKeyError, WeatherServiceUnavailableError
from app.utils.formatter import format_weather
from app.database.database import upsert_user, update_last_city

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def weather_handler(message: Message) -> None:
    """Handle city name as plain text."""
    if not message.text or not message.from_user:
        return

    city_raw = message.text.strip()

    # Ignore empty or very long inputs
    if not city_raw:
        await message.answer("❌ لطفاً نام شهر را وارد کنید.")
        return

    if len(city_raw) > 100:
        await message.answer("❌ نام شهر بیش از حد طولانی است.")
        return

    # Ignore if looks like command or callback leftover
    if city_raw.startswith("/"):
        return

    # Normalize Persian to English for API
    city_for_api = normalize_city(city_raw)

    # Save user and show typing? Just proceed
    try:
        await upsert_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_city=city_raw,
        )
    except Exception as e:
        logger.error(f"Failed to upsert user in weather_handler: {e}")

    # Fetch weather
    try:
        data = await weather_service.get_current_weather(city_for_api)
        text = format_weather(data)
        await message.answer(text)

        # Update last_city with original input (preserve Persian)
        try:
            await update_last_city(message.from_user.id, city_raw)
        except Exception as e:
            logger.error(f"Failed to update last_city: {e}")

    except CityNotFoundError:
        await message.answer("❌ <b>شهر موردنظر پیدا نشد. لطفاً نام شهر را بررسی کنید.</b>")
    except InvalidApiKeyError:
        logger.error(f"Invalid API key error for city {city_for_api}")
        await message.answer("❌ <b>خطا در اتصال به سرویس هواشناسی. لطفاً بعداً دوباره تلاش کنید.</b>")
    except WeatherServiceUnavailableError as e:
        logger.error(f"Weather service unavailable for {city_for_api}: {e}")
        await message.answer("⚠️ <b>سرویس هواشناسی موقتاً در دسترس نیست. لطفاً چند لحظه بعد دوباره امتحان کنید.</b>")
    except Exception as e:
        logger.exception(f"Unexpected error in weather_handler for {city_for_api}: {e}")
        # Never expose traceback to user
        await message.answer("⚠️ <b>خطای غیرمنتظره‌ای رخ داد. لطفاً دوباره تلاش کنید.</b>")
