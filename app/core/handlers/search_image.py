import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from core.schemas.v1.enums import CityEnum
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="Search image router")


@router.callback_query(lambda c: c.data and c.data == "search_image")
async def search_text_handler(query: types.CallbackQuery, state: FSMContext):
    city = (await state.get_data()).get("city")
    await query.message.answer(_("SEND_PHOTO_PLEASE", city=CityEnum.get_city_name_by_enum(CityEnum(city))))
    await query.answer()