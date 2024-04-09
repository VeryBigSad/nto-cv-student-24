import asyncio
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from core.db.models import User
from core.keyboards.inline import choose_action, choose_language
from core.middlewares import i18n
from core.redis import set_user_language_by_id
from core.utils.other import await_something
from core.utils.texts import _, get_localization_with_lang

logger = logging.getLogger(__name__)
router = Router(name="Language router")


@router.message(Command(commands=["language", "lang"]), F.chat.type == "private")
async def choose_language_command(message: Message, state: FSMContext):
    await message.answer(text=_("CHOOSE_LANGUAGE"), reply_markup=choose_language())


@router.callback_query(lambda c: c.data and c.data.endswith("_lang_button"))
async def choose_language_callback_handler(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    if query.data == "en_lang_button":
        user_language = "en"
    elif query.data == "ru_lang_button":
        user_language = "ru"
    elif query.data == "ch_lang_button":
        user_language = "ch"

    await asyncio.gather(
        User.filter(id=query.from_user.id).update(language=user_language),
        set_user_language_by_id(user_id, user_language),
        i18n.set_locale(state, user_language),
        await_something(query.answer()),
        await_something(query.message.delete()),
    )
    await query.message.answer(
        text=get_localization_with_lang("START_COMMAND", lang=user_language),
        reply_markup=choose_action(),
    )
