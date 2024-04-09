import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="Help router")


@router.message(Command(commands=["help"]), F.chat.type == "private")
async def help_command(message: types.Message):
    await message.answer(text=_("HELP_COMMAND"))
