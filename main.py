import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from env_data import BotToken
from bot.dp import dp
from bot.buttons.reply import main_menu

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Salom! Kundalik botga xush kelibsiz.", reply_markup=main_menu)

from bot.handlers import *

async def main() -> None:
    bot = Bot(
        token=BotToken.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())