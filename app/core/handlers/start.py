import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from core.db.models import User

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(Command(commands=["start"]), F.chat.type == "private")
async def start_command(
    message: types.Message, bot: Bot, state: FSMContext, command: CommandObject
):
    await User.update_or_create(
        id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "language_code": message.from_user.language_code,
            "is_premium": False,
        },
    )
    await message.answer(text="yo hello")
