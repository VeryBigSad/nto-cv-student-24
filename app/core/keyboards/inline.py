from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.texts import _


def choose_language() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_("ENGLISH_LANG_BUTTON"), callback_data="en_lang_button")
    kb.button(text=_("RUSSIAN_LANG_BUTTON"), callback_data="ru_lang_button")
    kb.button(text=_("CHINESE_LANG_BUTTON"), callback_data="ch_lang_button")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def choose_action() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_("SEND_PICTURE_BUTTON"), callback_data="search_image")
    kb.button(text=_("SEND_TEXT_BUTTON"), callback_data="search_text")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def start_webapp(button_text: str, url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=button_text, web_app=WebAppInfo(url=url))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
