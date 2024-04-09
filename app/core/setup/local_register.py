import asyncio
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from core import db


def register_main_bot(dp: Dispatcher, app: FastAPI, bot: Bot, **kwargs):
    @app.on_event("startup")
    async def start_local_bot():
        await db.init()
        asyncio.create_task(dp.start_polling(bot, **kwargs))

    @app.on_event("shutdown")
    async def stop_local_bot():
        await db.close()
        await dp.stop_polling()
