from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.schemas.v1.enums import CityEnum
from core.utils.texts import _, get_localization_with_lang


def choose_language() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_("ENGLISH_LANG_BUTTON"), callback_data="en_lang_button")
    kb.button(text=_("RUSSIAN_LANG_BUTTON"), callback_data="ru_lang_button")
    kb.button(text=_("CHINESE_LANG_BUTTON"), callback_data="ch_lang_button")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_diagram_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_("GET_MORE_INFO_BUTTON"), callback_data="more_info")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def choose_city(user_language: str | None = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    cities = [city.value for city in CityEnum]
    for city in cities:
        kb.button(
            text=get_localization_with_lang(f"CITY_NAMED_{city.upper()}_BUTTON", user_language),
            callback_data=f"city:{city.lower()}"
        )
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
