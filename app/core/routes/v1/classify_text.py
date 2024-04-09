import logging
from fastapi import APIRouter
from aiogram import Bot
from core.schemas.v1.schemas import ClassifyText
from core.schemas.v1.enums import CityEnum
from core.wlui.context import WLUIContextVar
from configs.settings import env_parameters
from fastapi import status

router = APIRouter()
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


@router.post(
    "/classify-text",
    response_model=ClassifyText.Response,
    status_code=status.HTTP_200_OK,
)
async def classify_text_route(body: ClassifyText.Request, city: CityEnum):
    """Загрузка текста для классификации"""
    return {"kek": True}
