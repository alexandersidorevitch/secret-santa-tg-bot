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


class PhotoWishInfo(WishInfo):
    async def send_to_async(self, user_id, **kwargs):
        kwargs.pop('format', None)
        await configuration.bot.send_photo(user_id, self.data, **kwargs)


class LinkWishInfo(WishInfo):
    async def send_to_async(self, user_id, **kwargs):
        kwargs.pop('format', None)
        await configuration.bot.send_message(f'{hide_link(user_id)} Хеллоу', self.data, **kwargs)
