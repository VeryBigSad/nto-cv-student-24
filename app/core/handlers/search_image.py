import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router(name="Search image router")


@router.callback_query(lambda c: c.data and c.data == "search_image")
async def search_text_handler(message: types.Message, state: FSMContext):
    await message.answer("(поиск по картинке)")
