import logging

import aiohttp
from aiogram import Bot
from configs.settings import env_parameters
from core.schemas.v1.enums import CityEnum
from core.schemas.v1.schemas import ClassifyText, CoordinateModel
from core.wlui.context import WLUIContextVar
from fastapi import APIRouter, status

router = APIRouter()
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


@router.post(
    "/classify-text",
    response_model=list[ClassifyText.Response],
    status_code=status.HTTP_200_OK,
)
async def classify_text_route(body: ClassifyText.Request, city: CityEnum):
    """Загрузка текста для классификации"""
    text = body.text
    city_letter = city.get_letter()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{env_parameters.API_URL}/text",
            json={"text": text, "city": city_letter},
        ) as response:
            response_json = await response.json()
    results = [{
        "xid": res.get("xid"),
        "name": res.get("name"),
        "category": res.get("category"),
        "city": city.value,
        "coordinates": CoordinateModel(latitude=res.get("coord")[1], longitude=res.get("coord")[0]),
        "probability": res.get("probs"),
        "image_bytes": res.get("images"),
    } for res in response_json]
    return results
