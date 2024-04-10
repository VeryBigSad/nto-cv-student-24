import logging

from aiogram import F, Bot, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
import httpx
from core.utils.texts import _
from core.keyboards.inline import get_diagram_keyboard

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(lambda m: m.photo, F.chat.type == "private")
async def photo_handler(message: types.Message, bot: Bot, state: FSMContext):
    await message.react([types.ReactionTypeEmoji(emoji="❤️")])
    await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    file_id = message.photo[-1].file_id
    result = await bot.download(file_id)

    city = (await state.get_data())["city"]
    # send request with aiohttp to localhost:8000/api/v1/classify-text
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:80/api/v1/classify-image?city={city}",
            files={"image": ("file.jpg", result, "image/jpeg")},
        )
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
