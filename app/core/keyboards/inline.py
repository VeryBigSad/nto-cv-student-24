from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.texts import _
from configs.settings import env_parameters


async def get_cities_kb(separated_cities_list: list) -> list:
    if not separated_cities_list:
        return []

    keyboard_pages = []  # for 'book menu'

    # fetch data for button text and callback_data
    for i, chunk in enumerate(separated_cities_list):
        kb = InlineKeyboardBuilder()

        if len(chunk) == env_parameters.NUMBER_OF_CITIES_PER_PAGE:  # chunk - channels per page
            end_len = env_parameters.NUMBER_OF_CITIES_PER_PAGE
        else:
            end_len = len(chunk)

        for city in range(0, end_len):
            kb.button(text=chunk[city]['city_name'], callback_data=chunk[city]['city_id'])  # values from fsm_functions
            kb.adjust(1)

        if len(separated_cities_list) > 1:
            kb.row(InlineKeyboardButton(text=await _('BACK'), callback_data='back'),
                   InlineKeyboardButton(text=await _('FORWARD'), callback_data='forward'))

        keyboard_pages.append(kb.as_markup(resize_keyboard=True))

    return keyboard_pages


async def continue_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=await _('CONTINUE_BUTTON'), callback_data='continue')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def ref_link_kb(link) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=await _('REF_LINK_BUTTON'), url=link)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def pick_status_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=await _('MEMBER_BUTTON'), callback_data='member')
    kb.button(text=await _('CLAMPER_BUTTON'), callback_data='clamper')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def get_verification_code_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=await _('RESEND_EMAIL'), callback_data='resend_email')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def start_webapp(button_text: str, url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=button_text, web_app=WebAppInfo(url=url))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
