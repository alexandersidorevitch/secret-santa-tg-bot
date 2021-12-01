import app.settings as settings
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.participant_io import ParticipantIO
from loguru import logger

bot = Bot(token=settings.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

logger.add('logging/file.log', format='{time} | {level} | {message}', rotation='1 MB', compression='zip',
           level='INFO')

participant_io = ParticipantIO()
