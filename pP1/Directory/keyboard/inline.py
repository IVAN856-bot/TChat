from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


buy_premium1_data = "buy_premium1_data"
test = "test"


def shop() -> InlineKeyboardMarkup:
    buy_premium1_b = InlineKeyboardButton(
        text="Купить подписку:🧵200 (Месяц)",
        callback_data=buy_premium1_data)
    row_kb = [[buy_premium1_b]]

    markup = InlineKeyboardMarkup(inline_keyboard=row_kb)
    return markup
