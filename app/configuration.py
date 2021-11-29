from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from app.participant_io import ParticipantIO
from loguru import logger
import app.settings as settings

bot = Bot(token=settings.TOKEN)
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
