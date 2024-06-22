from aiogram.types import Message
from Directory.database.data import DataBase
from aiogram import Router
from aiogram.filters import Command, CommandObject
import logging
from Directory.config import admin_id


router = Router(name=__name__)
logging.basicConfig(level=logging.INFO)

quote_buffer = {}
DB = DataBase()


@router.message(Command('edit'))  # /edit bal1 + 100
async def bal_1(message: Message, command: CommandObject):
    user_id = message.from_user.id

    if user_id not in admin_id:  # Проверка на админа
        return

    if not command.args:
        await message.reply("Вводите команду правильно!")
        return
    data = command.args.split()

    if data[0] == 'bal1' and len(data) == 3:  # /edit1(2) bal [+/-/=] [кол-во валюты]
        reply = message.reply_to_message
        if not reply:
            return await message.reply("Команда должна быть ответом на сообщение")
        else:
            reply_user_id = reply.from_user.id
            DB.reg_user(reply_user_id)
        try:
            money = int(data[2])
            user2 = reply.from_user.first_name
            profile2_link = f"tg://user?id={reply.from_user.id}"
            profile2 = f"<a href='{profile2_link}'>{user2}</a>"
        except ValueError:
            await message.reply(
                "Вы ввели команду не правильно! Правильный ввод команды: /edit1(2) bal [+/-/=] [кол-во валюты]")
            return

        balance1 = DB.get_data(user_id, "balance1")
        match data[1]:
            case "+":
                DB.edit_data_set(reply_user_id, "balance1", balance1 + money)
                await message.reply(f"Сумма 🧶{money} успешно добавлена к балансу пользователя {profile2}.")
            case "-":
                DB.edit_data_set(reply_user_id, "balance1", balance1 - money)
                await message.reply(f"Сумма 🧶{money} выписана из баланса пользователя {profile2}.")
            case "=":
                DB.edit_data_set(reply_user_id, "balance1", money)
                await message.reply(f"Баланс пользователя {profile2} установлен на сумму 🧶{money}.")
            case _:
                return await message.reply(
                    "Вы ввели команду не правильно! Правильный ввод команды: /edit1(2) bal [+/-/=] [кол-во валюты]")
    elif data[0] == 'bal2' and len(data) == 3:  # /edit1(2) bal [+/-/=] [кол-во валюты]
        reply = message.reply_to_message
        if not reply:
            return await message.reply("Команда должна быть ответом на сообщение")
        else:
            reply_user_id = reply.from_user.id
            DB.reg_user(reply_user_id)
        try:
            money = int(data[2])
            user2 = reply.from_user.first_name
            profile2_link = f"tg://user?id={reply.from_user.id}"
            profile2 = f"<a href='{profile2_link}'>{user2}</a>"
        except ValueError:
            await message.reply(
                "Вы ввели команду не правильно! Правильный ввод команды: /edit1(2) bal [+/-/=] [кол-во валюты]")
            return

        balance2 = DB.get_data(reply_user_id, "balance2")
        match data[1]:
            case "+":
                DB.edit_data_set(reply_user_id, "balance2", balance2+money)
                await message.reply(f"Сумма 🧵{money} успешно добавлена к балансу пользователя {profile2}.")
            case "-":
                DB.edit_data_set(reply_user_id, "balance2", balance2-money)
                await message.reply(f"Сумма 🧵{money} выписана из баланса пользователя с ID: {profile2}.")
            case "=":
                DB.edit_data_set(reply_user_id, "balance2", money)
                await message.reply(f"Баланс пользователя {profile2} установлен на сумму 🧵{money}.")
            case _:
                return await message.reply(
                    "Вы ввели команду не правильно! Правильный ввод команды: /edit1(2) bal [+/-/=] [кол-во валюты]")


@router.message(Command('photo_id'))
async def handle_photo(message: Message):
    if message.photo:
        photo_id = message.photo[-1].file_id  # Получаем id последней (самой большой) версии фото
        await message.reply(f"<blockquote>ID вашей фотографии:</blockquote> "
                            f"{photo_id}")
    else:
        await message.reply("Пожалуйста, отправьте фотографию.")
