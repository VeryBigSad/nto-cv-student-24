from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.utils.i18n import gettext


# i18n function
def _(text: str, **kwargs) -> str:
    return gettext(text).format(**kwargs)


def get_localization_with_lang(text: str, lang: str | None = None, **kwargs) -> str:
    return gettext(text, locale=lang).format(**kwargs)


# create individual commands menu for users, depends on user status
async def set_user_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(command="about", description=_("ABOUT_COMMAND")),
        BotCommand(command="faq", description=_("HELP_COMMAND")),
        BotCommand(command="invite", description=_("INVITE_COMMAND")),
        BotCommand(command="cancel", description=_("CANCEL_COMMAND")),
        BotCommand(command="start", description=_("START_COMMAND")),
    ]

    await bot.set_my_commands(commands=commands, scope=scope)


async def set_admin_commands(bot: Bot, scope: BotCommandScopeChat):
    commands = [
        BotCommand(command="about", description=_("ABOUT_COMMAND")),
        BotCommand(command="faq", description=_("HELP_COMMAND")),
        BotCommand(command="invite", description=_("INVITE_COMMAND")),
        BotCommand(command="cancel", description=_("CANCEL_COMMAND")),
        BotCommand(command="start", description=_("START_COMMAND")),
    ]

    await bot.set_my_commands(commands=commands, scope=scope)
