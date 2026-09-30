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

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💅 Манікюр"),
            KeyboardButton(text="💅 Гель-лак"),
        ],
        [
            KeyboardButton(text="💅 Нарощування"),
            KeyboardButton(text="🎨 Дизайн"),
        ],
        [
            KeyboardButton(text="🦶 Педикюр"),
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


# Початок запису
@dp.message(lambda message: message.text == "📅 Записатися")
async def booking(message: Message):
    await message.answer(
        "📅 Почнемо запис!\n\n"
        "Оберіть потрібну послугу:",
        reply_markup=services_menu
    )


# Вибір послуги
@dp.message(lambda message: message.text in [
    "💅 Манікюр",
    "💅 Гель-лак",
    "💅 Нарощування",
    "🎨 Дизайн",
    "🦶 Педикюр"
])
async def choose_service(message: Message):
    service = message.text

    await message.answer(
        f"✅ Обрана послуга: {service}\n\n"
        "Тепер напишіть ваше ім'я:"
    )

    # Зберігаємо послугу
    await state_save(message.from_user.id, "service", service)


# Тимчасове сховище записів
user_data = {}


async def state_save(user_id, key, value):
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id][key] = value


# Отримання імені
@dp.message()
async def booking_steps(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    # Ім'я
    if "service" in data and "name" not in data:
        data["name"] = message.text

        await message.answer(
            "📅 Добре!\n\n"
            "Тепер напишіть бажану дату.\n\n"
            "Наприклад: 5 жовтня"
        )
        return

    # Дата
    if "name" in data and "date" not in data:
        data["date"] = message.text

        await message.answer(
            "⏰ Тепер напишіть бажаний час.\n\n"
            "Наприклад: 15:00"
        )
        return

    # Час
    if "date" in data and "time" not in data:
        data["time"] = message.text

        await message.answer(
            "📋 Перевірте ваш запис:\n\n"
            f"💅 Послуга: {data['service']}\n"
            f"👤 Ім'я: {data['name']}\n"
            f"📅 Дата: {data['date']}\n"
            f"⏰ Час: {data['time']}\n\n"
            "Якщо все правильно, напишіть: ТАК"
        )
        return

    # Підтвердження
    if "time" in data and message.text.lower() in ["так", "да", "yes"]:
        username = message.from_user.username
        username_text = f"@{username}" if username else "немає"

        booking_text = (
            "🔔 НОВИЙ ЗАПИС!\n\n"
            f"👤 Ім'я: {data['name']}\n"
            f"📱 Telegram: {username_text}\n"
            f"💅 Послуга: {data['service']}\n"
            f"📅 Дата: {data['date']}\n"
            f"⏰ Час: {data['time']}"
        )

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=booking_text
        )

        await message.answer(
            "✅ Запис прийнято!\n\n"
            "Дякуємо за заявку. Майстер зв'яжеться з вами для підтвердження."
        )

        del user_data[user_id]
        return


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
