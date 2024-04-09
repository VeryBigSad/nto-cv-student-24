import logging

from aiogram import F, Router, types

from core.keyboards.inline import get_diagram_keyboard

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(F.chat.type == "private")
async def text_handler(message: types.Message):
    await message.answer(
        "Возможно, это <b>фотография достопримечательности</b>",
        reply_markup=get_diagram_keyboard()
    )
