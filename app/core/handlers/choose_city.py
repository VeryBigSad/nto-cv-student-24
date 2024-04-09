import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import choose_action
from core.schemas.v1.enums import CityEnum
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="Choose city router")


@router.callback_query(lambda c: c.data and c.data.startswith("city:"))
async def choose_city_handler(query: types.CallbackQuery, state: FSMContext):
    city = query.data.split(":")[1]
    await query.answer()
    await query.message.edit_text(
        _("SEE_LANDMARKS_IN_CITY", city=CityEnum.get_city_name_by_enum(CityEnum(city))),
        reply_markup=choose_action()
    )
    await state.update_data(city=city)
