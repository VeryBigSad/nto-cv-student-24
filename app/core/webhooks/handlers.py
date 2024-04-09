import logging
from fastapi import APIRouter, HTTPException, Header, Depends
from aiogram import Bot
from core.webhooks.models import TestResultModel
from core.wlui.context import WLUIContextVar
from configs.settings import env_parameters


def authorize_user(auth_token: str = Header(None)):
    if auth_token != env_parameters.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


@router.post("/video_lesson_result")
async def test_handler(body: TestResultModel):
    return {"kek": True}
