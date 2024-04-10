import asyncio
import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from core.utils.texts import _
from core.keyboards.inline import choose_action, choose_city
from core.schemas.v1.enums import CityEnum

logger = logging.getLogger(__name__)
router = Router(name="results router")


@router.callback_query(lambda c: c.data and c.data == "more_info")
async def search_text_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("Диаграмма распределения вероятности")
    await query.message.answer("Топ Н результатов по вероятности: названия, категория")
    await query.message.answer(
        "Диаграмма с топ Н результатов по вероятности: названия, категория"
    )
    await asyncio.sleep(1)
    city = (await state.get_data()).get("city")
    if city is None:
        await query.message.answer(text=_("START_COMMAND"), reply_markup=choose_city())
        return
    city_pretty = CityEnum.get_city_name_by_enum(CityEnum(city))
    await query.message.answer(
        _("SEE_LANDMARKS_IN_CITY", city=city_pretty), reply_markup=choose_action()
    )
