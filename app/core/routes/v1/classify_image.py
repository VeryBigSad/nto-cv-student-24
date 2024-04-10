import logging

import httpx
from aiogram import Bot
from configs.settings import env_parameters
from core.schemas.v1.enums import CityEnum
from core.schemas.v1.schemas import ClassifyImage
from core.wlui.context import WLUIContextVar
from fastapi import APIRouter, UploadFile, status

router = APIRouter()
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


@router.post("/classify-image", response_model=ClassifyImage.Response, status_code=status.HTTP_200_OK)
async def classify_image_route(image: UploadFile, city: CityEnum):
    """Загрузка изображений для последующей классификации"""
    city_letter = city.get_letter()
    async with httpx.AsyncClient() as client:
        async with client.post(
            f"{env_parameters.API_URL}/text?city={city_letter}",
            files={"file": (image.filename, image.file, image.content_type)},
        ) as response:
            response_json = response.json()
    pass
    

