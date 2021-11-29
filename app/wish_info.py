from aiogram import types
from aiogram.types import InputMediaPhoto
import app.configuration as configuration
from aiogram.utils.markdown import hide_link


class WishInfo:
    def __init__(self, data):
        self.data = data

    async def send_to_async(self, user_id, **kwargs):
        raise NotImplementedError()


class TextWishInfo(WishInfo):
    async def send_to_async(self, user_id, **kwargs):
        string_format = kwargs.pop('format', '{}')
        await configuration.bot.send_message(user_id, string_format.format(self.data), **kwargs)

    def __str__(self):
        return str(self.data)


class PhotoWishInfo(WishInfo):
    async def send_to_async(self, user_id, **kwargs):
        kwargs.pop('format', None)
        await configuration.bot.send_photo(user_id, self.data, **kwargs)

    def __str__(self):
        return 'Фото'


class LinkWishInfo(WishInfo):
    async def send_to_async(self, user_id, **kwargs):
        kwargs.pop('format', None)
        kwargs['parse_mode'] = types.ParseMode.HTML
        await configuration.bot.send_message(user_id, f'{self.data} Хеллоу', **kwargs)

    def __str__(self):
        return str(self.data)
