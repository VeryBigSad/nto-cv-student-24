import logging

from aiogram import F, Router, types
from aiogram.enums import ChatAction
from core.keyboards.inline import get_diagram_keyboard

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(lambda m: m.photo, F.chat.type == "private")
async def photo_handler(message: types.Message):
    # heart emoji
    await message.react([types.ReactionTypeEmoji(emoji="❤️")])
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.answer(
        "Возможно, это <b>описание фото</b>",
        reply_markup=get_diagram_keyboard(),
    )
