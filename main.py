import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "💅 Вітаю! Я бот майстра манікюру!\n\n"
        "Напиши мені, щоб дізнатися про послуги та записатися."
    )


async def health(request):
    return web.Response(text="OK")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 10000))

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Web server started on port {port}")


async def main():
    await start_web_server()

    print("Telegram bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
