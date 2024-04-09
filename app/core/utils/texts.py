from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from configs.settings import env_parameters

if env_parameters.PROD_MODE:
    from core.wi18n import gettext_async
else:
    from aiogram.utils.i18n import gettext

available_roles = ['admin', 'clamper', 'member']


# i18n function
async def _(text: str, **kwargs):
    if env_parameters.PROD_MODE:
        translation = await gettext_async(text)
        return translation.format(**kwargs)
    else:
        return gettext(text).format(**kwargs)


# create individual commands menu for users, depends on user status
async def set_user_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(
            command='about',
            description=await _('ABOUT_COMMAND')
        ),
        BotCommand(
            command='faq',
            description=await _('HELP_COMMAND')
        ),
        BotCommand(
            command='invite',
            description=await _('INVITE_COMMAND')
        ),
        BotCommand(
            command='cancel',
            description=await _('CANCEL_COMMAND')
        ),
        BotCommand(
            command='start',
            description=await _('START_COMMAND')
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=scope)


async def set_admin_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(
            command='about',
            description=await _('ABOUT_COMMAND')
        ),
        BotCommand(
            command='faq',
            description=await _('HELP_COMMAND')
        ),
        BotCommand(
            command='invite',
            description=await _('INVITE_COMMAND')
        ),
        BotCommand(
            command='cancel',
            description=await _('CANCEL_COMMAND')
        ),
        BotCommand(
            command='start',
            description=await _('START_COMMAND')
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=scope)
