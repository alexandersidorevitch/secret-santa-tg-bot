import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv
from loguru import logger
from app.participant_io import ParticipantIO

load_dotenv()

token = os.getenv('BOT_TOKEN')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

logger.add('logging/file.log', format='{time} {level} {message}', rotation='1 MB', compression='zip',
           level='WARNING')

participant_io = ParticipantIO()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/view_my_wishes", description="Вывести мои пожелания"),
        BotCommand(command="/delete_wish", description="Удалить пожелание"),
    ]
    await bot.set_my_commands(commands)
