from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Haftalik darslar")],
        [KeyboardButton(text="➕ Dars qo'shish")],
        [KeyboardButton(text="✏️ Darsni o'zgartirish")],
        [KeyboardButton(text="❌ Darsni o'chirish")]
    ],
    resize_keyboard=True
)