from aiogram import Router, F
from aiogram.types import Message

from Directory.database.data import DataBase
from Directory.config import bot_id

router = Router()
DB = DataBase()


@router.message(F.text.lower() == "купить", F.reply_to_message)
async def buy_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)
    owner_id = DB.get_data(user_id, "owner_id")

    if message.chat.type == 'private':
        return await message.reply("Ну и кого ты тут возьмёшь в рабство? Пиши команду в группе!")

    if not message.reply_to_message:
        return await message.reply("Вводи команду в ответ на сообщение человека, которого хочешь взять в рабство")
    else:
        reply = message.reply_to_message
        reply_id = int(reply.from_user.id)

        if int(reply_id) == user_id:
            return await message.reply("И как ты представляешь себе это?")
        elif int(reply_id) == owner_id:
            return await message.reply("Нельзя купить своего хозяина!")
        elif int(reply_id) == bot_id:
            return await message.reply("Бота не трожь!")

        DB.reg_user(reply_id)
        reply_cost = DB.get_data(reply_id, "cost")
        reply_owner_id = DB.get_data(reply_id, "owner_id")

    slaves = DB.get_data(user_id, "slaves")
    if str(reply_id) in slaves:
        return await message.reply("Этот раб уже принадлежит тебе!")
    elif len(slaves) >= 3:
        return await message.reply("Нельзя покупать больше 3-х рабов!")

    balance1 = DB.get_data(user_id, "balance1")
    if balance1 < reply_cost:
        return await message.reply(f"У вас недостаточно денег, чтобы купить раба!\nЦена этого раба: {reply_cost}")
    else:
        slaves.append(reply_id)
        DB.edit_data_set(user_id, "slaves", slaves)
        DB.edit_data_set(reply_id, "cost", reply_cost + 10)

        if reply_owner_id == 0:
            DB.edit_data_set(reply_id, "owner_id", user_id)
            DB.edit_data_set(user_id, "balance1", balance1 - reply_cost)
        else:
            reply_owner_slaves = DB.get_data(reply_owner_id, "slaves")
            if str(reply_id) in reply_owner_slaves:
                reply_owner_slaves.remove(str(reply_id))
            DB.edit_data_set(reply_owner_id, "slaves", reply_owner_slaves)

            DB.edit_data_set(reply_id, "owner_id", user_id)

    await message.reply(f"Вы успешно купили раба!")


@router.message(F.text.lower().startswith("выпустить"), F.reply_to_message)
async def emancipate_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    reply = message.reply_to_message
    slave_id = reply.from_user.id
    DB.reg_user(slave_id)

    slaves = DB.get_data(user_id, "slaves")
    if str(slave_id) not in slaves:
        return await message.reply("Этот раб не принадлежит тебе!")

    slaves.remove(str(slave_id))
    DB.edit_data_set(user_id, "slaves", slaves)
    DB.edit_data_set(slave_id, "owner_id", 0)
    DB.edit_data_set(slave_id, "cost", 50)
    await message.answer("Вы освободили раба!")


@router.message(F.text.lower() == "цена")
async def sale_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    reply = message.reply_to_message
    if not reply:
        return await message.reply("Вводи команду в ответ на сообщение потенциального раба!")
    else:
        reply_id = reply.from_user.id
        DB.reg_user(reply_id)

        reply_cost = DB.get_data(reply_id, "cost")

    await message.reply(f"Цена этого потенциального раба: {reply_cost}")


@router.message(F.text.lower().startswith("купить"), ~F.reply_to_message)
async def buy_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)
    owner_id = DB.get_data(user_id, "owner_id")

    arg = message.text.split()
    if len(arg) == 1 or len(arg) > 2:
        return await message.reply("Пиши команду правильно:\nкупить id")
    else:
        reply_id = int(arg[1])
        reply_exists = DB.user_exists(reply_id)
        if not reply_exists:
            return await message.reply("Пользователь не зарегистрирован в боте")

        if int(reply_id) == user_id:
            return await message.reply("И как ты представляешь себе это?")
        elif int(reply_id) == owner_id:
            return await message.reply("Нельзя купить своего хозяина!")
        elif int(reply_id) == bot_id:
            return await message.reply("Бота не трожь!")

        reply_cost = DB.get_data(reply_id, "cost")
        reply_owner_id = DB.get_data(reply_id, "owner_id")

    slaves = DB.get_data(user_id, "slaves")
    if str(reply_id) in slaves:
        return await message.reply("Этот раб уже принадлежит тебе!")
    elif len(slaves) >= 3:
        return await message.reply("Нельзя покупать больше 3-х рабов!")

    balance1 = DB.get_data(user_id, "balance1")
    if balance1 < reply_cost:
        return await message.reply(f"У вас недостаточно денег, чтобы купить раба!\nЦена этого раба: {reply_cost}")
    else:
        slaves.append(reply_id)
        DB.edit_data_set(user_id, "slaves", slaves)
        DB.edit_data_set(reply_id, "cost", reply_cost + 10)

        if reply_owner_id == 0:
            DB.edit_data_set(reply_id, "owner_id", user_id)
            DB.edit_data_set(user_id, "balance1", balance1 - reply_cost)
        else:
            reply_owner_slaves = DB.get_data(reply_owner_id, "slaves")
            if str(reply_id) in reply_owner_slaves:
                reply_owner_slaves.remove(str(reply_id))
            DB.edit_data_set(reply_owner_id, "slaves", reply_owner_slaves)

            DB.edit_data_set(reply_id, "owner_id", user_id)

    await message.reply(f"Вы успешно купили раба!")


@router.message(F.text.lower().startswith("выпустить"), ~F.reply_to_message)
async def emancipate_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    arg = message.text.split()
    if len(arg) == 1 or len(arg) > 2:
        return await message.reply("Пиши команду правильно:\nвыпустить id")
    else:
        slave_id = int(arg[1])

    slaves = DB.get_data(user_id, "slaves")
    if str(slave_id) not in slaves:
        return await message.reply("Этот раб не принадлежит тебе!")

    slaves.remove(str(slave_id))
    DB.edit_data_set(user_id, "slaves", slaves)
    DB.edit_data_set(slave_id, "owner_id", 0)
    DB.edit_data_set(slave_id, "cost", 50)
    await message.answer("Вы освободили раба!")
