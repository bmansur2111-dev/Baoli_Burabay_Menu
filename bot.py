import json
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

# Вставьте сюда ваш НОВЫЙ сгенерированный токен от BotFather
BOT_TOKEN = "8818978434:AAH5mg_5CdPHGxNcSkxeR7X16-Qqu7_OfnQ"

# Загружаем меню из JSON-файла
with open("menu.json", "r", encoding="utf-8") as file:
    menu_data = json.load(file)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Генерация клавиатуры со списком категорий меню
def get_categories_keyboard():
    buttons = []
    categories = list(menu_data["categories"].keys())
    
    # Расставляем кнопки по 2 в ряд
    for i in range(0, len(categories), 2):
        row = [InlineKeyboardButton(text=categories[i], callback_data=f"cat_{i}")]
        if i + 1 < len(categories):
            row.append(InlineKeyboardButton(text=categories[i + 1], callback_data=f"cat_{i+1}"))
        buttons.append(row)
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Хэндлер на команду /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        f"👋 **Добро пожаловать в {menu_data['restaurant']}!**\n\n"
        f"Выберите интересующую вас категорию из меню ниже:"
    )
    await message.answer(text, reply_markup=get_categories_keyboard(), parse_mode="Markdown")

# Хэндлер на нажатие по категории
@dp.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):
    cat_index = int(callback.data.split("_")[1])
    cat_name = list(menu_data["categories"].keys())[cat_index]
    items = menu_data["categories"][cat_name]

    text = f"🍽 **{cat_name}**\n\n"
    for item in items:
        text += f"• **{item['name']}** — {item['price']} ₸\n"
    
    text += f"\n_Обслуживание: {menu_data['service_charge']}_"

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к категориям", callback_data="main_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=back_keyboard, parse_mode="Markdown")
    await callback.answer()

# Хэндлер для возврата в главное меню
@dp.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    text = (
        f"👋 **Добро пожаловать в {menu_data['restaurant']}!**\n\n"
        f"Выберите интересующую вас категорию из меню ниже:"
    )
    await callback.message.edit_text(text, reply_markup=get_categories_keyboard(), parse_mode="Markdown")
    await callback.answer()

# Запуск бота
async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
