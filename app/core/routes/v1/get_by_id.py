import logging
from typing import Any

import httpx
from aiogram import Bot
from configs.settings import env_parameters
from core.wlui.context import WLUIContextVar
from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


# {'Name':Name, 'Kind':Kind, 'City':City, 'OSM':OSM, 'WikiData':WikiData, 'Rate':Rate, 'Lon':Lon, 'Lat':Lat}
class Response(BaseModel):
    Name: Any
    Kind: Any
    OSM: Any
    WikiData: Any
    Rate: Any
    Lon: float
    Lat: float


@router.get("/get-by-id/{xid}", response_model=Response, status_code=status.HTTP_200_OK)
async def classify_image_route(xid: str) -> dict:
    """Загрузка изображений для последующей классификации"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{env_parameters.API_URL}/xid",
            json={"xid": xid},
            headers={
                "x-node-id": env_parameters.X_NODE_ID,
                "Authorization": f"Bearer {env_parameters.IAM_TOKEN}",
                "x-folder-id": env_parameters.X_FOLDER_ID
            },
        )
        return resp.json()
    

