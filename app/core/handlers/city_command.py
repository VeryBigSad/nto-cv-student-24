import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from core.keyboards.inline import choose_city
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="City command router")


@router.message(Command(commands=["city"]), F.chat.type == "private")
async def city_command(message: types.Message):
    await message.answer(text=_("CITY_COMMAND"), reply_markup=choose_city())
