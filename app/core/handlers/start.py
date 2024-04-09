import logging

from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject
from core.db.models import User
from core.keyboards.inline import choose_action, choose_language
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(Command(commands=["start"]), F.chat.type == "private")
async def start_command(message: types.Message, command: CommandObject):
    user, is_created = await User.update_or_create(
        id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "language_code": message.from_user.language_code,
            "is_premium": False,
        },
    )
    if is_created:
        await message.answer(
            text=_("START_COMMAND_FIRST_TIME"), reply_markup=choose_language()
        )
        user.deeplink = command.args
        await user.save()
    else:
        await message.answer(text=_("START_COMMAND"), reply_markup=choose_action())
