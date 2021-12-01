import app.configuration as configuration
from aiogram import types


class WishInfo:
    def __init__(self, data):
        self.data = data
        self.is_deleted = False

    async def send_to_async(self, user_id, **kwargs):
        raise NotImplementedError()

    def delete(self):
        self.is_deleted = True

    def __hash__(self):
        return hash(self.data)


class TextWishInfo(WishInfo):
    async def send_to_async(self, chat_id, **kwargs):
        string_format = kwargs.pop('format', 'Текстовая хотелка: {}')
        await configuration.bot.send_message(chat_id, string_format.format(self.data), **kwargs)

    def __str__(self):
        return str(self.data)


class PhotoWishInfo(WishInfo):
    async def send_to_async(self, chat_id, **kwargs):
        kwargs.pop('format', None)
        kwargs['caption'] = 'Фотография подарка'
        await configuration.bot.send_photo(chat_id, self.data, **kwargs)

    def __str__(self):
        return 'Фото'


class LinkWishInfo(WishInfo):
    async def send_to_async(self, chat_id, **kwargs):
        string_format = kwargs.pop('format', 'Ссылка на смысл жизни: {}')
        kwargs['parse_mode'] = types.ParseMode.HTML
        await configuration.bot.send_message(chat_id, string_format.format(self.data), **kwargs)

    def __str__(self):
        return str(self.data)
