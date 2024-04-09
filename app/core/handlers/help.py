import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router(name="Help router")


@router.message(Command(commands=["start"]), F.chat.type == "private")
async def help_command(
    message: types.Message, bot: Bot, state: FSMContext, command: CommandObject
):
    await message.answer(text="Help message")
