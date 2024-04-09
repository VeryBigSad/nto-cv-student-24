import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="Help router")


@router.message(Command(commands=["help"]), F.chat.type == "private")
async def help_command(
    message: types.Message, bot: Bot, state: FSMContext, command: CommandObject
):
    await message.answer(text=_("HELP_COMMAND"))
