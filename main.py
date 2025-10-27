import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ==================== Настройки ====================
TOKEN = 8416618652:AAFAh8IqxhTEMJ_2kAlOPYHCc-dSo8W6EBw
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==================== Контент ====================
JOKES = [
    "Почему программисты любят кофе? ☕ Потому что они не любят баги!",
    "Сарказм – моё любимое оружие 😏",
    "Шутка дня: Если что-то работает, не трогай. Если не работает – всё равно не трогай!",
]

FACTS = [
    "В космосе никто не слышит твой сарказм 😎",
    "Бананы – ягоды, а клубника – нет",
    "Слоны не могут прыгать",
]

RIDDLES = [
    {"q": "Что всегда впереди, но никогда не приходит?", "a": "завтра"},
    {"q": "Что можно поймать, но нельзя бросить?", "a": "холод"},
    {"q": "У какого слова 5 букв, но оно означает цифру?", "a": "десять"},
]

SARCASM = [
    "О, как неожиданно 🙄",
    "Ну конечно, потому что я же всё могу 😏",
    "Да, твоя логика меня поражает 🤨",
]

# ==================== Игры ====================
async def roll_dice(message: types.Message):
    await message.answer(f"Бросаем кубик 🎲: Выпало {random.randint(1,6)}")

async def guess_number_start(message: types.Message):
    number = random.randint(1,10)
    chat_guesses[message.chat.id] = number
    await message.answer("Я загадал число от 1 до 10. Попробуй угадать! Напиши /try <число>")

async def guess_number_try(message: types.Message, user_try: str):
    if not user_try.isdigit():
        await message.answer("Введи число 😏")
        return
    user_try = int(user_try)
    correct = chat_guesses.get(message.chat.id)
    if correct is None:
        await message.answer("Сначала напиши /guess 😏")
    elif user_try == correct:
        await message.answer("Угадал! 🎉 Ты настоящий мастер сарказма!")
        del chat_guesses[message.chat.id]
    else:
        await message.answer(f"Неправильно 😒 Я загадал {correct}. Попробуй ещё раз /guess")

# ==================== Хранилище ====================
chat_riddles = {}  # chat_id: correct_answer
chat_guesses = {}  # chat_id: number_to_guess

# ==================== Меню ====================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Шутки", callback_data="menu_joke"),
        InlineKeyboardButton("Факты", callback_data="menu_fact"),
        InlineKeyboardButton("Загадки", callback_data="menu_riddle"),
        InlineKeyboardButton("Игры 🎲", callback_data="menu_games"),
        InlineKeyboardButton("Сарказм", callback_data="menu_sarcasm")
    )
    return kb

# ==================== Обработчики ====================
@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой саркастичный бот 😏\nВыбери категорию:", reply_markup=main_menu())

@dp.callback_query()
async def menu_handler(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    data = callback.data

    if data == "menu_joke":
        await bot.send_message(chat_id, random.choice(JOKES))
    elif data == "menu_fact":
        await bot.send_message(chat_id, random.choice(FACTS))
    elif data == "menu_riddle":
        riddle = random.choice(RIDDLES)
        chat_riddles[chat_id] = riddle["a"]
        await bot.send_message(chat_id, f"Загадка: {riddle['q']}\nНапиши /answer <твой ответ>")
    elif data == "menu_games":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("Бросить кубик", callback_data="game_dice"),
            InlineKeyboardButton("Угадай число", callback_data="game_guess")
        )
        await bot.send_message(chat_id, "Выбери игру:", reply_markup=kb)
    elif data == "menu_sarcasm":
        await bot.send_message(chat_id, random.choice(SARCASM))
    elif data == "game_dice":
        await roll_dice(callback.message)
    elif data == "game_guess":
        await guess_number_start(callback.message)

@dp.message()
async def all_messages(message: types.Message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text.startswith("/answer"):
        answer = text.replace("/answer","").strip()
        correct = chat_riddles.get(chat_id)
        if correct is None:
            await message.answer("Сначала попроси загадку командой /start 😏")
        elif answer.lower() == correct.lower():
            await message.answer("Верно! 🎉 Ты гений сарказма!")
            del chat_riddles[chat_id]
        else:
            await message.answer(f"Нет 😒 Правильный ответ: {correct}")

    elif text.startswith("/try"):
        user_try = text.replace("/try","").strip()
        await guess_number_try(message, user_try)

# ==================== Запуск ====================
if __name__ == "__main__":
    import asyncio
    from aiogram import F
    asyncio.run(dp.start_polling(bot))