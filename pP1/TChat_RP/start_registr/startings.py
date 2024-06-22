from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from Directory.database.data import DataBase
from Directory.keyboard.inline import shop
from aiogram import Router, F
import logging

router = Router(name=__name__)
logging.basicConfig(level=logging.INFO)

quote_buffer = {}
DB = DataBase()  # Создание экземпляра класса DataBase


@router.message(CommandStart())
async def start_cmd(message: Message):
    user_id = message.from_user.id
    DB.reg_user(user_id)

    user_first_name = message.from_user.first_name
    user_link = f"tg://user?id={user_id}"

    await message.reply(f"<b><a href='{user_link}'>{user_first_name}</a></b> зарегистрирован!")


@router.message(F.text.lower().startswith("помощь"))
@router.message(Command('help'))
async def help_cmd(message: Message):
    if message.chat.type != "private":
        return await message.reply("Воспользуйтесь командой в чате с ботом.")

    arg = message.text.split()
    if len(arg) == 1:
        await message.answer(f"Приветствую вас в разделе помощи!\n"
                             f"\nЧтобы ознакомится со всеми рп-командами используйте команду: <code>/help rp</code>\n"
                             f"\nБот умеет работать с вашими данными, если напишите в чат команду “Профиль”, "
                             f"вы сможете следить за вашим игровым счетом, так же доступно редактирование"
                             f" вашего профиля.\n"
                             f"\nЧтобы немного заработать напишите команду “Фарм”.\n"
                             f"\nВы можете ознакомится с магазином: <code>/shop</code>")
    elif len(arg) == 2 and arg[1] in ["rp", "рп"]:
        await message.answer("Все рп-команды за 🧶2:"
                             "\nОбнять, поцеловать, ударить, укусить, хвалить, "
                             "кормить, погладить, позвать, схватить, признаться.\n"
                             "\nВсе рп-команды за 🧶5:"
                             "\nМинет, куни, трахнуть, попа, ахегао, "
                             "грудь, член, раздеть, прижать, шлепнуть.\n"
                             "\nПодписка аниме с крутым дизайном поддерживает все выше команды."
                             " Чтобы использовать крутой дизайн рп-команд вам необходимо писать в начале команды '@'.\n"
                             "\nПример: '@Обнять'.")


@router.message(Command('shop'))
async def shop_cmd(message: Message):
    if message.chat.type != "private":
        await message.reply("Воспользуйтесь командой в чате с ботом.")

    else:
        await message.answer(
            text="На данный момент нет автоматических команд для покупки товаров, однако вы можете "
                 "уточнить какие товары имеются можно по этому официальному аккаунту @shop_TChat",
            reply_markup=shop())
