import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router(name="Search text router")


@router.callback_query(lambda c: c.data and c.data == "search_text")
async def search_text_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text="(поиск по тексту)")
