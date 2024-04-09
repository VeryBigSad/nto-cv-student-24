import core.middlewares
from aiogram import Bot, Dispatcher
from configs.settings import env_parameters
from core.handlers import welcome
from core.setup import local_register
from core.webhooks import app
from core.wlui.middleware import WnLoggingUserIdMiddleware
from core.wlui.context import WLUIContextVar


wnl_middleware = WnLoggingUserIdMiddleware(WLUIContextVar())
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode='HTML')

dp = Dispatcher()
core.middlewares.i18n.setup(dp)

dp.update.middleware.register(wnl_middleware)

dp.include_router(welcome.router)

local_register.register_main_bot(dp, app, bot, allowed_updates=dp.resolve_used_update_types())
