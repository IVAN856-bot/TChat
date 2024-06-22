import time
from aiogram import F
from Directory.database.data import DataBase
from aiogram import Router

from aiogram.types import Message, FSInputFile
import logging


router = Router(name=__name__)
logging.basicConfig(level=logging.INFO)

quote_buffer = {}
DB = DataBase()
images = "Directory/images/"


@router.message(F.text.lower().in_(["обнять"]))
async def rp2_1(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)
    name = DB.get_data(user_id, "name")

    reply = message.reply_to_message
    if not reply:
        return await message.reply("Пиши команду в ответ на сообщение")
    else:
        reply_user_id = reply.from_user.id
        DB.reg_user(reply_user_id)
        reply_name = DB.get_data(reply_user_id, "name")

    sec = time.time()
    premium1_check = DB.get_data(user_id, "premium1")

    if premium1_check == 0 or int(sec) - int(premium1_check) >= 2592000:
        money = 2
        balance1 = DB.get_data(user_id, "balance1")
        balance2 = DB.get_data(user_id, "balance2")

        if balance1 < money:
            profile1 = f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>"
            return await message.answer(f"<blockquote>Необходимо: 🧶2</blockquote>\n"
                                        f"{profile1}: 🧶{balance1} 🧵{balance2}")

        DB.edit_data_set(user_id, "balance1", balance1 - money)
        profile1 = f"<a href='tg://user?id={user_id}'>{name}</a>"
        profile2 = f"<a href='tg://user?id={reply_user_id}'>{reply_name}</a>"
        balance1 = DB.get_data(user_id, "balance1")
        balance2 = DB.get_data(user_id, "balance2")
        text1 = (f"<blockquote>{profile1}: 🧶{balance1} 🧵{balance2}</blockquote>\n"
                 f"{profile1} обнял(а) {profile2}")
        await message.answer(text=text1)
        return

    last_time_farm = sec - premium1_check
    remaining_days = int(max(0, 30 - last_time_farm / 86400)) + 1
    profile1 = f"<a href='tg://user?id={user_id}'>{name}</a>"
    profile2 = f"<a href='tg://user?id={reply_user_id}'>{reply_name}</a>"
    photo_prem1 = FSInputFile(images+"1.jpg")
    text = (f"<blockquote>{profile1} Осталось дней: 🗓{remaining_days}/30</blockquote>\n"
            f"{profile1} крепко обнял(а) {profile2}\n")
    await message.answer_photo(photo=photo_prem1, caption=text, show_caption_above_media=True)


@router.message(F.text.lower().in_(["обнять"]))
async def rp2_1(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)
    name = DB.get_data(user_id, "name")

    reply = message.reply_to_message
    if not reply:
        return await message.reply("Пиши команду в ответ на сообщение")
    else:
        reply_user_id = reply.from_user.id
        DB.reg_user(reply_user_id)
        reply_name = DB.get_data(reply_user_id, "name")

    sec = time.time()
    premium1_check = DB.get_data(user_id, "premium1")

    if premium1_check == 0 or int(sec) - int(premium1_check) >= 2592000:
        money = 2
        balance1 = DB.get_data(user_id, "balance1")
        balance2 = DB.get_data(user_id, "balance2")

        if balance1 < money:
            profile1 = f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>"
            return await message.answer(f"<blockquote>Необходимо: 🧶2</blockquote>\n"
                                        f"{profile1}: 🧶{balance1} 🧵{balance2}")

        DB.edit_data_set(user_id, "balance1", balance1 - money)
        profile1 = f"<a href='tg://user?id={user_id}'>{name}</a>"
        profile2 = f"<a href='tg://user?id={reply_user_id}'>{reply_name}</a>"
        balance1 = DB.get_data(user_id, "balance1")
        balance2 = DB.get_data(user_id, "balance2")
        text1 = (f"<blockquote>{profile1}: 🧶{balance1} 🧵{balance2}</blockquote>\n"
                 f"{profile1} обнял(а) {profile2}")
        await message.answer(text=text1)
        return

    last_time_farm = sec - premium1_check
    remaining_days = int(max(0, 30 - last_time_farm / 86400)) + 1
    profile1 = f"<a href='tg://user?id={user_id}'>{name}</a>"
    profile2 = f"<a href='tg://user?id={reply_user_id}'>{reply_name}</a>"
    photo_prem1 = FSInputFile(images+"1.jpg")
    text = (f"<blockquote>{profile1} Осталось дней: 🗓{remaining_days}/30</blockquote>\n"
            f"{profile1} крепко обнял(а) {profile2}\n")
    await message.answer_photo(photo=photo_prem1, caption=text, show_caption_above_media=True)
