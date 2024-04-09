import logging

from aiogram import F, Router, types
from aiogram.enums import ChatAction
from core.keyboards.inline import get_diagram_keyboard

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(F.chat.type == "private")
async def text_handler(message: types.Message):
    await message.react([types.ReactionTypeEmoji(emoji="❤️")])
    await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    await message.answer(
        "Возможно, это <b>фотография достопримечательности</b>",
        reply_markup=get_diagram_keyboard()
    )
