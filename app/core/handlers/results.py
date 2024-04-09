import asyncio
import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import choose_action
from core.schemas.v1.enums import CityEnum

logger = logging.getLogger(__name__)
router = Router(name="results router")


@router.callback_query(lambda c: c.data and c.data == "more_info")
async def search_text_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("Диаграмма распределения вероятности")
    await query.message.answer("Топ Н результатов по вероятности: названия, категория")
    await query.message.answer("Диаграмма с топ Н результатов по вероятности: названия, категория")
    await asyncio.sleep(1)
    city = (await state.get_data())["city"]
    city_pretty = CityEnum.get_city_name_by_enum(CityEnum(city))
    await query.message.answer(
        f"yooo -> {city_pretty}", reply_markup=choose_action()
    )
