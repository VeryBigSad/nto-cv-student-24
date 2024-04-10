import logging

import httpx
from aiogram import Bot
from pydantic import BaseModel
from configs.settings import env_parameters
from core.schemas.v1.schemas import ClassifyImage
from core.wlui.context import WLUIContextVar
from fastapi import APIRouter, status

router = APIRouter()
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


class Thingy(BaseModel):
    xid: str

# {'Name':Name, 'Kind':Kind, 'City':City, 'OSM':OSM, 'WikiData':WikiData, 'Rate':Rate, 'Lon':Lon, 'Lat':Lat}
class Response(BaseModel):
    Name: str
    Kind: str
    OSM: str
    WikiData: str
    Rate: str
    Lon: str
    Lat: str


@router.get("/get-by-id", response_model=Response, status_code=status.HTTP_200_OK)
async def classify_image_route(body: Thingy) -> dict:
    """Загрузка изображений для последующей классификации"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{env_parameters.API_URL}/xid",
            json={"xid": body.xid},
        )
        return resp.json()
    

