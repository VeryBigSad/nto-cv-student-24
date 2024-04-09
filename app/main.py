import core.middlewares
from aiogram import Bot, Dispatcher
from configs.settings import env_parameters
from core.handlers import help, language, search_image, search_text, start
from core.routes import core_router
from core.setup import local_register
from core.wlui.context import WLUIContextVar
from core.wlui.middleware import WnLoggingUserIdMiddleware
from fastapi import FastAPI

wnl_middleware = WnLoggingUserIdMiddleware(WLUIContextVar())
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")

dp = Dispatcher()
core.middlewares.i18n.setup(dp)

dp.update.middleware.register(wnl_middleware)

dp.include_router(start.router)
dp.include_router(help.router)
dp.include_router(language.router)
dp.include_router(search_image.router)
dp.include_router(search_text.router)

app = FastAPI()
app.include_router(core_router)

local_register.register_main_bot(
    dp, app, bot, allowed_updates=dp.resolve_used_update_types()
)
