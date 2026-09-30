
import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💅 Послуги"),
            KeyboardButton(text="💰 Ціни"),
        ],
        [
            KeyboardButton(text="📅 Записатися"),
            KeyboardButton(text="📍 Адреса"),
        ],
        [
            KeyboardButton(text="📞 Контакти"),
        ],
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "💅 Вітаю! Я бот майстра манікюру!\n\n"
        "Оберіть потрібний розділ:",
        reply_markup=main_menu
    )


@dp.message(lambda message: message.text == "💅 Послуги")
async def services(message: Message):
    await message.answer(
        "💅 Наші послуги:\n\n"
        "• Манікюр\n"
        "• Покриття гель-лаком\n"
        "• Нарощування нігтів\n"
        "• Дизайн нігтів\n"
        "• Педикюр"
    )


@dp.message(lambda message: message.text == "💰 Ціни")
async def prices(message: Message):
    await message.answer(
        "💰 Ціни:\n\n"
        "• Манікюр — уточнюйте\n"
        "• Гель-лак — уточнюйте\n"
        "• Нарощування — уточнюйте\n"
        "• Дизайн — від 20 грн\n"
        "• Педикюр — уточнюйте"
    )


@dp.message(lambda message: message.text == "📍 Адреса")
async def address(message: Message):
    await message.answer(
        "📍 Адреса:\n"
        "Хмельницький\n\n"
        "Точну адресу повідомимо під час запису."
    )


@dp.message(lambda message: message.text == "📞 Контакти")
async def contacts(message: Message):
    await message.answer(
        "📞 Контакти:\n\n"
        "Для запису натисніть «📅 Записатися»."
    )


@dp.message(lambda message: message.text == "📅 Записатися")
async def booking(message: Message):
    await message.answer(
        "📅 Для запису напишіть одним повідомленням:\n\n"
        "💅 Послуга:\n"
        "📅 Дата:\n"
        "⏰ Час:\n"
        "👤 Ім'я:\n\n"
        "Наприклад:\n"
        "Гель-лак\n"
        "5 жовтня\n"
        "15:00\n"
        "Анна"
    )


@dp.message()
async def receive_booking(message: Message):
    if not message.text:
        return

    if message.text.startswith("/"):
        return

    if message.text in [
        "💅 Послуги",
        "💰 Ціни",
        "📅 Записатися",
        "📍 Адреса",
        "📞 Контакти"
    ]:
        return

    client_name = message.from_user.full_name
    username = message.from_user.username

    username_text = f"@{username}" if username else "немає"

    booking_text = (
        "🔔 НОВИЙ ЗАПИС!\n\n"
        f"👤 Клієнт: {client_name}\n"
        f"📱 Telegram: {username_text}\n\n"
        "📝 Повідомлення клієнта:\n"
        f"{message.text}"
    )

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=booking_text
    )

    await message.answer(
        "✅ Дякуємо! Вашу заявку отримано.\n\n"
        "Майстер зв'яжеться з вами для підтвердження запису."
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


async def main():
    await start_web_server()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
