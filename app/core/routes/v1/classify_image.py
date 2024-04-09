import logging
from fastapi import APIRouter, UploadFile
from aiogram import Bot
from core.schemas.v1.schemas import ClassifyImage
from core.schemas.v1.enums import CityEnum
from core.wlui.context import WLUIContextVar
from configs.settings import env_parameters


router = APIRouter()
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


@router.post(
    "/classify-image",
    response_model=ClassifyImage.Response
)
async def classify_image_route(image: UploadFile, city: CityEnum):
    """Загрузка изображений для последующей классификации"""
    pass
