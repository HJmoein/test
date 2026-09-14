"""
Application startup and router registration for aiogram 3.x
"""

import asyncio
import logging
import sys
from pathlib import Path

# Allow running as `python app/main.py` from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app import config
from app.database.database import init_db
from app.services.weather_api import weather_service
from app.handlers import start as start_handler
from app.handlers import compare as compare_handler
from app.handlers import weather as weather_handler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def on_startup() -> None:
    """Initialize database and HTTP session."""
    # Validate env - also catch placeholder value
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or ":" not in config.BOT_TOKEN:
        logger.error("BOT_TOKEN is missing or invalid! Set it in .env file.")
        raise RuntimeError("BOT_TOKEN is not set or invalid. Check your .env file. Get token from @BotFather")

    if not config.WEATHER_API_KEY:
        logger.error("WEATHER_API_KEY is missing! Set it in .env file.")
        raise RuntimeError("WEATHER_API_KEY is not set. Check your .env file.")

    await init_db()
    await weather_service.create_session()
    logger.info("Startup complete")


async def on_shutdown(bot: Bot) -> None:
    """Cleanly close HTTP session and bot session."""
    logger.info("Shutting down...")
    try:
        await weather_service.close()
    except Exception as e:
        logger.error(f"Error closing weather service: {e}")

    try:
        await bot.session.close()
    except Exception as e:
        logger.error(f"Error closing bot session: {e}")
    logger.info("Shutdown complete")


async def main() -> None:
    """Main entry point."""
    await on_startup()

    bot: Bot | None = None
    try:
        bot = Bot(
            token=config.BOT_TOKEN,  # type: ignore[arg-type]
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        dp = Dispatcher()

        # Router registration order matters:
        # 1. start (handles /start, /help, callbacks)
        # 2. compare (handles /compare)
        # 3. weather (catch-all city names) - must be last
        dp.include_router(start_handler.router)
        dp.include_router(compare_handler.router)
        dp.include_router(weather_handler.router)

        logger.info("Bot is starting polling...")
        await dp.start_polling(bot)
    finally:
        if bot is not None:
            await on_shutdown(bot)
        else:
            # Bot never created, still close weather service
            try:
                await weather_service.close()
            except Exception as e:
                logger.error(f"Error closing weather service: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except RuntimeError as e:
        logger.error(f"Failed to start: {e}")
        sys.exit(1)
