import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Токены
from Directory.config import token
from TChat_RP.game_play.reiting import gift
# TChat_RP

from TChat_RP import router as main_router
from Directory import router as call_router


bot = None


async def main():
    global bot
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(main_router, call_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start():
    await asyncio.gather(main(), gift())


if __name__ == '__main__':
    try:
        print('Бот запущен!')
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Бот остановлен!')
