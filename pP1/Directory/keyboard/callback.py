import time

from aiogram import Router, F
from aiogram.types import CallbackQuery

from Directory.database.data import DataBase
from Directory.keyboard.inline import buy_premium1_data

router = Router()
DB = DataBase()


@router.callback_query(F.data == buy_premium1_data)
async def callback_rp1(call: CallbackQuery):
    user_id = call.from_user.id
    DB.reg_user(user_id)

    premium1_check = DB.get_data(user_id, "premium1")
    sec_time = time.time()
    if premium1_check == 0 or int(sec_time) - int(premium1_check) >= 2592000:
        pass
    else:
        return await call.answer("У вас уже имеется подписка!!!")
    money = 200
    bal2 = DB.get_data(user_id, "balance2")  # Получение баланса для проверки наличия валюты
    if bal2 < money:  # Если денег нет, то мы возвращаем сообщение
        return await call.answer("Недостаточно средств")
    else:
        DB.edit_data_set(user_id, "balance2", bal2-money)
        DB.edit_data_set(user_id, "premium1", sec_time)
    await call.answer("Покупка успешна!")
    await call.message.reply(text=call.message.text)
