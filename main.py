import os
import asyncio
from datetime import datetime, timedelta

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart


TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()


# =========================================================
# ГОЛОВНЕ МЕНЮ
# =========================================================

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


# =========================================================
# ПОСЛУГИ
# =========================================================

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧼 Чистка"),
            KeyboardButton(text="💅 Манікюр з укріпленням"),
        ],
        [
            KeyboardButton(text="💅 Нарощення 1–2"),
            KeyboardButton(text="💅 Нарощення 3–4"),
        ],
        [
            KeyboardButton(text="🔧 Корекція нарощених"),
            KeyboardButton(text="✨ Реставрація"),
        ],
        [
            KeyboardButton(text="🦶 Гігієнічний педикюр"),
        ],
        [
            KeyboardButton(text="🦶 Педикюр 1"),
            KeyboardButton(text="🦶 Педикюр 2"),
        ],
        [
            KeyboardButton(text="🦶 Педикюр 3"),
        ],
        [
            KeyboardButton(text="✨ Френч"),
        ],
    ],
    resize_keyboard=True
)


# =========================================================
# ЦІНИ
# =========================================================

prices_text = """
💰 ЦІНИ

💅 МАНІКЮР

• Чистка — 250 грн
  Зняття матеріалу,
  чистка кутикули,
  опил форми

• Манікюр з укріпленням — 550 грн


💅 НАРОЩЕННЯ

• Нарощення 1–2 — 600 грн

• Нарощення 3–4 — 700 грн

• Корекція нарощених — від 550 грн

• Реставрація та підняття
  клюючих нігтиків — 650 грн

• Френч — 100 грн


🦶 ПЕДИКЮР

• Гігієнічний педикюр — 500 грн
  Чистка пальчиків та п'ят,
  без покриття

• Педикюр 1 — 550 грн
  Покриття гель-лаком
  без чистки пальчиків і п'ят

• Педикюр 2 — 600 грн
  Покриття гель-лаком
  + чистка пальчиків

• Педикюр 3 — 650 грн
  Покриття гель-лаком
  + чистка пальчиків і п'ят
"""


# =========================================================
# ДАНІ ЗАПИСУ
# =========================================================

user_data = {}

# Тут зберігаються зайняті слоти:
# ("2026-10-05", "16:00")
booked_slots = set()


booking_services = [
    "🧼 Чистка",
    "💅 Манікюр з укріпленням",
    "💅 Нарощення 1–2",
    "💅 Нарощення 3–4",
    "🔧 Корекція нарощених",
    "✨ Реставрація",
    "🦶 Гігієнічний педикюр",
    "🦶 Педикюр 1",
    "🦶 Педикюр 2",
    "🦶 Педикюр 3",
    "✨ Френч",
]


# =========================================================
# START
# =========================================================

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "💅 Вітаю! Я бот майстра манікюру!\n\n"
        "Оберіть потрібний розділ:",
        reply_markup=main_menu
    )


# =========================================================
# ПОСЛУГИ
# =========================================================

@dp.message(lambda message: message.text == "💅 Послуги")
async def services(message: Message):
    await message.answer(
        "💅 НАШІ ПОСЛУГИ\n\n"
        "🧼 Чистка\n"
        "💅 Манікюр з укріпленням\n"
        "💅 Нарощення 1–2\n"
        "💅 Нарощення 3–4\n"
        "🔧 Корекція нарощених\n"
        "✨ Реставрація\n"
        "🦶 Гігієнічний педикюр\n"
        "🦶 Педикюр 1\n"
        "🦶 Педикюр 2\n"
        "🦶 Педикюр 3\n"
        "✨ Френч"
    )


# =========================================================
# ЦІНИ
# =========================================================

@dp.message(lambda message: message.text == "💰 Ціни")
async def prices(message: Message):
    await message.answer(prices_text)


# =========================================================
# АДРЕСА
# =========================================================

@dp.message(lambda message: message.text == "📍 Адреса")
async def address(message: Message):
    await message.answer(
        "📍 АДРЕСА\n\n"
        "Хмельницький\n\n"
        "Точну адресу повідомимо під час запису."
    )


# =========================================================
# КОНТАКТИ
# =========================================================

@dp.message(lambda message: message.text == "📞 Контакти")
async def contacts(message: Message):
    await message.answer(
        "📞 КОНТАКТИ\n\n"
        "Для запису натисніть «📅 Записатися»."
    )


# =========================================================
# ПОЧАТОК ЗАПИСУ
# =========================================================

@dp.message(lambda message: message.text == "📅 Записатися")
async def booking(message: Message):

    user_data[message.from_user.id] = {}

    await message.answer(
        "📅 ПОЧНЕМО ЗАПИС!\n\n"
        "Оберіть потрібну послугу:",
        reply_markup=services_menu
    )


# =========================================================
# ВИБІР ПОСЛУГИ
# =========================================================

@dp.message(lambda message: message.text in booking_services)
async def choose_service(message: Message):

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    user_data[user_id]["service"] = message.text

    await message.answer(
        f"✅ Обрана послуга:\n{message.text}\n\n"
        "👤 Напишіть ваше ім'я:"
    )


# =========================================================
# КНОПКИ ДАТ
# =========================================================

def create_date_menu():

    today = datetime.now().date()

    keyboard = []

    for i in range(7):

        date = today + timedelta(days=i)

        date_text = date.strftime("%d.%m")

        if i == 0:
            button_text = f"📅 Сьогодні {date_text}"
        elif i == 1:
            button_text = f"📅 Завтра {date_text}"
        else:
            button_text = f"📅 {date_text}"

        keyboard.append([
            KeyboardButton(text=button_text)
        ])

    keyboard.append([
        KeyboardButton(text="🤝 Інша дата — узгодити")
    ])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# =========================================================
# КНОПКИ ЧАСУ
# =========================================================

def create_time_menu(date_key):

    times = [
        "10:00",
        "13:00",
        "16:00",
        "18:30"
    ]

    keyboard = []

    for time in times:

        slot = (date_key, time)

        if slot not in booked_slots:

            keyboard.append([
                KeyboardButton(text=f"🕐 {time}")
            ])

    keyboard.append([
        KeyboardButton(
            text="🤝 Інший час — узгодити з майстром"
        )
    ])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# =========================================================
# ОСНОВНИЙ ПРОЦЕС ЗАПИСУ
# =========================================================

@dp.message()
async def booking_steps(message: Message):

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    # -----------------------------------------------------
    # ІМ'Я
    # -----------------------------------------------------

    if "service" in data and "name" not in data:

        data["name"] = message.text

        await message.answer(
            "📅 Добре!\n\n"
            "Тепер оберіть дату:",
            reply_markup=create_date_menu()
        )

        return


    # -----------------------------------------------------
    # ДАТА
    # -----------------------------------------------------

    if "name" in data and "date" not in data:

        text = message.text

        if text.startswith("📅"):

            date_text = text.replace("📅", "").strip()

            if "Сьогодні" in date_text:
                date_part = date_text.replace(
                    "Сьогодні", ""
                ).strip()

            elif "Завтра" in date_text:
                date_part = date_text.replace(
                    "Завтра", ""
                ).strip()

            else:
                date_part = date_text

            current_year = datetime.now().year

            date_key = (
                f"{current_year}-"
                f"{date_part[3:5]}-"
                f"{date_part[0:2]}"
            )

            data["date"] = date_key
            data["date_display"] = date_part

            await message.answer(
                f"📅 Обрана дата: {date_part}\n\n"
                "⏰ Оберіть вільний час:",
                reply_markup=create_time_menu(date_key)
            )

            return

        if text == "🤝 Інша дата — узгодити":

            data["date"] = "Інша дата"
            data["date_display"] = "Інша дата"

            await finish_booking(
                message,
                user_id,
                "Потрібно узгодити"
            )

            return


    # -----------------------------------------------------
    # ЧАС
    # -----------------------------------------------------

    if "date" in data and "time" not in data:

        text = message.text

        if text.startswith("🕐"):

            time = text.replace("🕐", "").strip()

            date_key = data["date"]

            slot = (date_key, time)

            # Додаткова перевірка
            if slot in booked_slots:

                await message.answer(
                    "❌ На жаль, цей час уже зайнятий.\n\n"
                    "Оберіть інший час:",
                    reply_markup=create_time_menu(date_key)
                )

                return

            # Бронюємо слот
            booked_slots.add(slot)

            data["time"] = time

            await finish_booking(
                message,
                user_id,
                time
            )

            return

        if text == "🤝 Інший час — узгодити з майстром":

            data["time"] = "Потрібно узгодити"

            await finish_booking(
                message,
                user_id,
                "Потрібно узгодити"
            )

            return


# =========================================================
# ЗАВЕРШЕННЯ ЗАПИСУ
# =========================================================

async def finish_booking(message: Message, user_id: int, time: str):

    data = user_data[user_id]

    username = message.from_user.username

    username_text = (
        f"@{username}"
        if username
        else "немає"
    )

    booking_text = (
        "🔔 НОВИЙ ЗАПИС!\n\n"
        f"👤 Ім'я: {data['name']}\n"
        f"📱 Telegram: {username_text}\n"
        f"💅 Послуга: {data['service']}\n"
        f"📅 Дата: {data['date_display']}\n"
        f"⏰ Час: {time}"
    )

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=booking_text
    )

    await message.answer(
        "✅ ЗАЯВКУ ОТРИМАНО!\n\n"
        "Майстер зв'яжеться з вами "
        "для підтвердження запису.",
        reply_markup=main_menu
    )

    del user_data[user_id]


# =========================================================
# RENDER HEALTH SERVER
# =========================================================

async def health(request):
    return web.Response(text="OK")


async def start_web_server():

    app = web.Application()

    app.router.add_get("/", health)

    runner = web.AppRunner(app)

    await runner.setup()

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()


# =========================================================
# MAIN
# =========================================================

async def main():

    await start_web_server()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
