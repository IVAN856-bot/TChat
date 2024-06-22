from aiogram.types import Message
from Directory.database.data import DataBase
from aiogram import Router, F
import logging

router = Router(name=__name__)
logging.basicConfig(level=logging.INFO)

quote_buffer = {}
DB = DataBase()


@router.message(F.text.lower() == "профиль", ~F.reply_to_message)
async def profile_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    user1 = DB.get_data(user_id, "name")
    profile1 = f"<a href='t.me/{message.from_user.username}'>{user1}</a>"

    descript = DB.get_data(user_id, "user_info")
    avatar_id = DB.get_data(user_id, "avatar_id")
    m1 = DB.get_data(user_id, "balance1")
    m2 = DB.get_data(user_id, "balance2")

    owner_id = DB.get_data(user_id, "owner_id")
    if owner_id == 0:
        owner = "отсутствует"
    else:
        owner_name = DB.get_data(owner_id, "name")
        owner = f"<a href='tg://user?id={owner_id}'>{owner_name}</a>"

    slaves = DB.get_data(user_id, "slaves")
    slaves_text = "Рабы:\n"
    if slaves:
        i = 1
        for slave in slaves:
            slave_name = DB.get_data(slave, "name")
            slaves_text += f"   {i}. <a href='tg://user?id={slave}'>{slave_name}</a>"
            slaves_text += f"       <code>{slave}</code>\n"
            i += 1
    else:
        slaves_text += "    отсутствуют"

    await message.answer_photo(
        photo=avatar_id,
        caption=f'''
<blockquote><b>Профиль - {profile1} </b>
Баланс: 🧶{m1} 🧵{m2}</blockquote>
О себе: <blockquote><i>{descript}</i></blockquote>
Хозяин: {owner}
{slaves_text}

Сменить ник: /nick
Сменить фото: /avatar
Сменить описание: /info''')


@router.message(F.text.lower() == "профиль", F.reply_to_message)
async def profile_cmd(message: Message):
    await message.reply("Просмотр чужого профиля: в разработке...")
