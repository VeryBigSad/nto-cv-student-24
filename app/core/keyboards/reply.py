from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from core.utils.texts import _


async def get_contact() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=await _("SHARE_CONTACT_BUTTON"), request_contact=True)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


async def is_this_your_email_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=await _("YES_MY_EMAIL_BUTTON"))
    kb.button(text=await _("NOT_MY_EMAIL_BUTTON"))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
