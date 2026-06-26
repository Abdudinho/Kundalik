from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.buttons.reply import main_menu
from dispetcher import dp

week_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Dushanba", callback_data="monday")],
        [InlineKeyboardButton(text="Seshanba", callback_data="tuesday")],
        [InlineKeyboardButton(text="Chorshanba", callback_data="wednesday")],
        [InlineKeyboardButton(text="Payshanba", callback_data="thursday")],
        [InlineKeyboardButton(text="Juma", callback_data="friday")]
    ]
)

