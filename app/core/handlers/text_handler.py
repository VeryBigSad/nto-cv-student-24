import logging

import aiohttp
from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import get_diagram_keyboard
from core.utils.texts import _

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(F.chat.type == "private")
async def text_handler(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.react([types.ReactionTypeEmoji(emoji="❤️")])
    text = message.text
    city = (await state.get_data())["city"]
    # send request with aiohttp to localhost:8000/api/v1/classify-text
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://localhost:80/api/v1/classify-text?city={city}",
            json={"text": text},
        ) as response:
            response_json = await response.json()
    await state.update_data(results=response_json)
    texts = ""
    for i in response_json:
        texts += _(
            "TEXT_HANDLER_RESULT",
            category=i["category"],
            name=i["name"],
            coordinates=f"{i['coordinates']['longitude']}, {i['coordinates']['latitude']}",
            probability=round(i["probability"], 3),
        ) + "\n\n"
    await message.answer_media_group(
        media=[
            types.InputMediaPhoto(media=f"https://storage.yandexcloud.net/misis-progrev-gradientov/{i['xid']}.jpg") for i in response_json
        ],
    )
    await message.answer(
        texts,
        reply_markup=get_diagram_keyboard(),
    )
