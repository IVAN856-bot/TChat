import asyncio
import pytz
from datetime import datetime
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

from Directory.database.data import DataBase

router = Router()
DB = DataBase()


@router.message(F.text.lower().in_(["топ", "рейтинг"]))
async def top_rank(message: Message):
    curs = DB.get_db("cursor")
    curs.execute("SELECT user_id, balance1, name FROM users ORDER BY balance1 DESC LIMIT 10")
    users = curs.fetchall()

    if users:
        response = "<b>Топ 10 пользователей по балансу:</b>\n"
        i = 1
        for user in users:
            bal = str(user[1])
            if not user[2]:
                name = f"Топ {i}"
            else:
                name = f"{i}. {user[2]}"
            response += f"<blockquote><b>{name}\nБаланс: {bal} 🧶</b></blockquote>\n"
            i += 1
    else:
        return

    await message.reply(response, parse_mode=ParseMode.HTML)


async def gift():
    curs = DB.get_db("cursor")
    conn = DB.get_db("conn")
    while True:
        curs.execute("SELECT user_id, balance1, name FROM users ORDER BY balance1 DESC LIMIT 3")
        users = curs.fetchall()
        while not users or users == []:
            await asyncio.sleep(1)
        top1_id = users[0][0]

        day = datetime.now(pytz.timezone('Europe/Moscow')).day
        if int(day) == 1:
            balance2 = DB.get_data(int(top1_id), "balance2")
            DB.edit_data_set(int(top1_id), "balance2", balance2+25)

        await asyncio.sleep(43200)
