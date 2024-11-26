from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from message_text.text import *


def start_functions_keyboard(language: str):
    """Функция для создания клавиатуры."""
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=f"🤖 {button_texts[language]['ai_help']}",
        callback_data='ai_help'
    ))
    keyboard.add(InlineKeyboardButton(
        text=f"🌐 {button_texts[language]['select_language']}",
        callback_data='change_language'
    ))
    return keyboard.adjust(1, ).as_markup()


def language_selection_keyboard(language: str):
    """Функция для создания клавиатуры выбора языка."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language_en"),
        InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="set_language_kgz"),
        InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))

    return keyboard.adjust(3).as_markup()


def get_cancel_keyboard(language: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=cancel[language], callback_data="cancel_ai_help"))
    return keyboard.adjust(1).as_markup()


def get_cancel_ai_help_keyboard(language: str):
    keyboard = InlineKeyboardBuilder()
    start_button = InlineKeyboardButton(text=chat_messages[language]['start_over'], callback_data="start_help")
    keyboard.add(cancel_button, start_button)
    return keyboard.adjust(1).as_markup()
