import os
from logging import WARNING

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)

logger.add('logging/file_{time}.log', format='{time} {level} {message}', rotation='1 MB', compression='zip',
           level=WARNING)
