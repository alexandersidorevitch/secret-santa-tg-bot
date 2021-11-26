from aiogram import types
from aiogram.utils import executor

import configuration


@configuration.dp.message_handler(commands=['start'])
async def start_bot_command(message: types.Message):
    await message.answer('[Приведственный текст]')


if __name__ == '__main__':
    executor.start_polling(configuration.dp)
