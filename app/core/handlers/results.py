import asyncio
import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from core.utils.texts import _
from core.keyboards.inline import choose_action, choose_city
from core.schemas.v1.enums import CityEnum
import plotly.graph_objects as go
from PIL import Image
import io

logger = logging.getLogger(__name__)
router = Router(name="results router")


@router.callback_query(lambda c: c.data and c.data == "more_info")
async def search_text_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.edit_reply_markup(reply_markup=None)
    results = (await state.get_data())["results"]
    names = [result["name"] for result in results]
    probs = [result["probability"] for result in results]
    colors = ['#33a0ff', '#33aaff', '#33b4ff', '#33beff', '#33c8ff', '#33d2ff', '#33dcff', '#33e6ff', '#33f0ff', '#33faff'][::-1]
    colors = colors[:len(names)]
    # Create a bar chart
    fig = go.Figure(data=[go.Bar(y=names[::-1], x=probs[::-1], marker_color=colors, orientation='h')])

    # Add titles and labels
    fig.update_layout(title='',
                    xaxis_title='Вероятность',
                    yaxis_title='Название')
    img_bytes = fig.to_image(format="png")
    img = io.BytesIO(img_bytes)
    await query.message.answer_photo(
        photo=img,
        caption="Диаграмма распределения вероятности"
    )

    await asyncio.sleep(2.5)
    city = (await state.get_data()).get("city")
    if city is None:
        await query.message.answer(text=_("START_COMMAND"), reply_markup=choose_city())
        return
    city_pretty = CityEnum.get_city_name_by_enum(CityEnum(city))
    await query.message.answer(
        _("SEE_LANDMARKS_IN_CITY", city=city_pretty), reply_markup=choose_action()
    )
