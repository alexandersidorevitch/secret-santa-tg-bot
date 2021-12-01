from aiogram import types
from aiogram.utils.exceptions import BotBlocked

import app.configuration as configuration


async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    configuration.logger.exception(f'Bot has blocked  by @{update.message.from_user.username}, Error: {exception}')

    return True
