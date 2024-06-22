from aiogram.types import Message
from Directory.database.data import DataBase
from aiogram import Router
from aiogram.filters import Command, CommandObject
import logging

router = Router(name=__name__)
logging.basicConfig(level=logging.INFO)

quote_buffer = {}
DB = DataBase()


@router.message(Command(commands=["nick", "nickname"]))
async def nickname_cmd(message: Message, command: CommandObject):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    args = command.args
    if not args:
        return await message.reply("Пиши команду правильно: /nick ИМЯ")
    else:
        nick = str(args)
        if len(nick) > 12:
            return await message.reply("Этот ник слишком большой! Используй ник менее 12 символов")
        else:
            DB.edit_data_set(user_id, "name", nick)
            await message.reply(f"Вы успешно поставили ник: <b>{nick}</b>")


@router.message(Command('avatar'))
async def edit_avatar_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    print("АААА")
    if not message.photo:
        return await message.reply("Отправьте фото с комментарием /avatar!")

    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id

    DB.edit_data_set(user_id, "avatar_id", photo_id)

    await message.reply("Изменения внесены!")


@router.message(Command('info'))
async def edit_info_cmd(message: Message, command: CommandObject):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    args = command.args
    if not args:
        return await message.reply(f"Введите команду в формате:"
                                   f"\n/info [ваше описание]")

    if len(str(args)) > 140:
        return await message.reply("Максимальное количество символов описания: 140")
    else:
        DB.edit_data_set(user_id, "user_info", args)

    await message.reply("Изменения внесены!")
