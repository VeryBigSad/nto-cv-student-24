import logging
from fastapi import APIRouter
from aiogram import Bot
from core.schemas.v1.schemas import ClassifyText
from core.schemas.v1.enums import CityEnum
from core.wlui.context import WLUIContextVar
from configs.settings import env_parameters
from fastapi import status
import aiohttp

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
            f"{env_parameters.API_URL}/text?city={city_letter}",
            json={"text": text},
        ) as response:
            response = await response.json()
    results = [{
        "xid": "test_xid",
        "name": res.get("name"),
        "category": "test_category",
        "city": city,
        "probs": res.get("probs"),
        "coordinates": res.get("coord"),
    } for res in response]
    return results
