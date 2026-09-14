"""
Telegram inline keyboards - Persian UI.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard with 3 buttons."""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🌤 هواشناسی", callback_data="action_weather"))
    builder.add(InlineKeyboardButton(text="⚖️ مقایسه دو شهر", callback_data="action_compare"))
    builder.add(InlineKeyboardButton(text="❓ راهنما", callback_data="action_help"))
    builder.adjust(2, 1)
    return builder.as_markup()


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Back to main menu."""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🏠 بازگشت به منو", callback_data="action_start"))
    return builder.as_markup()
