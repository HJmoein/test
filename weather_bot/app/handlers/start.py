"""
Start and help handlers.
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.keyboards.main import get_main_keyboard
from app.database.database import upsert_user

logger = logging.getLogger(__name__)
router = Router()


WELCOME_TEXT = (
    "<b>👋 سلام! به ربات هواشناسی خوش آمدید</b>\n\n"
    "🌍 نام هر شهری را به فارسی یا انگلیسی بفرستید تا آب‌وهوای لحظه‌ای آن را ببینید.\n"
    "مثال: <code>تهران</code> یا <code>Tehran</code>\n\n"
    "⚖️ برای مقایسه دو شهر:\n"
    "<code>/compare تهران مشهد</code>\n\n"
    "از دکمه‌های زیر استفاده کنید:"
)

HELP_TEXT = (
    "<b>❓ راهنمای ربات هواشناسی</b>\n\n"
    "🔹 <b>دریافت آب‌وهوا:</b>\n"
    "کافیست نام شهر را ارسال کنید.\n"
    "مثال: <code>اصفهان</code> یا <code>London</code>\n\n"
    "🔹 <b>مقایسه دو شهر:</b>\n"
    "<code>/compare تهران مشهد</code>\n"
    "<code>/compare Tehran London</code>\n"
    "برای شهرهای دو کلمه‌ای از کاما استفاده کنید:\n"
    "<code>/compare New York, London</code>\n\n"
    "🔹 <b>دستورات:</b>\n"
    "/start - شروع مجدد\n"
    "/help - همین راهنما\n"
    "/compare - مقایسه دو شهر"
)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """Handle /start command."""
    try:
        user = message.from_user
        if user:
            await upsert_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
            )
    except Exception as e:
        logger.error(f"Failed to upsert user on /start: {e}")

    await message.answer(WELCOME_TEXT, reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handle /help command."""
    await message.answer(HELP_TEXT, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "action_start")
async def callback_start(callback: CallbackQuery) -> None:
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=get_main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "action_help")
async def callback_help(callback: CallbackQuery) -> None:
    await callback.message.edit_text(HELP_TEXT, reply_markup=get_main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "action_weather")
async def callback_weather(callback: CallbackQuery) -> None:
    text = (
        "<b>🌤 دریافت آب‌وهوا</b>\n\n"
        "لطفاً نام شهر را به فارسی یا انگلیسی ارسال کنید.\n"
        "مثال: <code>تهران</code> یا <code>Paris</code>"
    )
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "action_compare")
async def callback_compare(callback: CallbackQuery) -> None:
    text = (
        "<b>⚖️ مقایسه دو شهر</b>\n\n"
        "فرمت صحیح:\n"
        "<code>/compare شهر اول شهر دوم</code>\n\n"
        "مثال:\n"
        "<code>/compare تهران مشهد</code>\n"
        "<code>/compare Tehran London</code>\n\n"
        "برای شهرهای دو کلمه‌ای:\n"
        "<code>/compare New York, London</code>"
    )
    await callback.message.answer(text)
    await callback.answer()
