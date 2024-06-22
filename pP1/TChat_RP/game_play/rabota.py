import time
import logging
from random import randint
from aiogram import F
from aiogram import Router
from aiogram.types import Message

from Directory.database.data import DataBase

router = Router()
logging.basicConfig(level=logging.INFO)

quote_buffer = {}
DB = DataBase()


@router.message(F.text.lower() == "шахта")
async def work(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    DB.reg_user(user_id)

    sec = time.time()
    last_time_farm = DB.get_data(user_id, "last_time_farm")
    if last_time_farm == 0 or int(sec) - int(last_time_farm) >= 14400:
        DB.edit_data_set(user_id, "last_time_farm", sec)

        win = randint(10, 99)
        owner_id = DB.get_data(user_id, "owner_id")
        if owner_id == 0:
            new_balance1 = DB.get_data(user_id, "balance1") + win
            DB.edit_data_set(user_id, "balance1", new_balance1)

            await message.reply(f"Вы успешно получили: 🧶{win}!")
        else:
            new_balance1 = DB.get_data(user_id, "balance1") + win - 5
            DB.edit_data_set(user_id, "balance1", new_balance1)

            new_owner_balance1 = DB.get_data(owner_id, "balance1") + 5
            DB.edit_data_set(owner_id, "balance1", new_owner_balance1)

            await message.reply(f"Вы успешно получили: 🧶{win},\nВаш владелец получил 5 от вашей зп")
    else:
        secs = 14400 + int(last_time_farm) - int(sec)
        hours = secs // 3600
        minutes = (secs % 3600) // 60
        await message.reply(f"Следующая попытка через {hours} час(а) и {minutes} мин. ⏱️")


@router.message(F.text.lower() == "предсказание")  # 🥠
async def bonus(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    DB.reg_user(user_id)

    sec = time.time()
    cookie = DB.get_data(user_id, "cookie")
    if cookie == 0 or int(sec) - int(cookie) >= 7200:  # Если 2 часа прошло, пользователь снова может предсказать
        DB.edit_data_set(user_id, "cookie", sec)  # Обновляем время прошлого использования, не прерывая работу функции

    else:
        remaining_sec = int(sec) - int(cookie)  # Оставшейся время в секундах
        remaining_sec = 7200 - remaining_sec  # remaining_sec - время, которое уже прошло
        hours = remaining_sec // 3600  # получаем количество полных часов
        minutes = (remaining_sec % 3600) // 60  # получаем оставшиеся минуты

        await message.reply(f"Следующая попытка через {hours} час(а) и {minutes} мин. ⏱️")

