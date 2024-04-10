import logging

import aiohttp
from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from core.utils.texts import _
from core.keyboards.inline import get_diagram_keyboard

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(F.chat.type == "private")
async def text_handler(message: types.Message, state: FSMContext):
    await message.react([types.ReactionTypeEmoji(emoji="❤️")])
    text = message.text
    city = (await state.get_data())["city"]
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    # send request with aiohttp to localhost:8000/api/v1/classify-text
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://localhost:8000/api/v1/classify-text?city={city}",
            json={"text": text},
        ) as response:
            response_json = await response.json()
    await state.update_data(results=response_json)
    for idx in range(len(response_json)):
        i = response_json[idx]
        if idx == len(response_json) - 1:
            await message.answer(
                _(
                    "TEXT_HANDLER_RESULT",
                    category=i["category"],
                    name=i["name"],
                    coordinates=f"{i['coordinates']['longitude']}, {i['coordinates']['latitude']}",
                    probability=round(i["probability"], 3),
                ),
                reply_markup=get_diagram_keyboard(i["xid"]),
            )
            continue
        await message.answer(
            f"Возможно, это <b>{i['category']}</b> - <i>{i['name']}</i> TODO: add pictures",
        )
