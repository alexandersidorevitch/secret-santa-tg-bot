import json

from aiogram import Bot


class Present:
    def __init__(self):
        self.data = ''

    def get_product(self):
        raise NotImplementedError()

    def get_serialized_obj(self):
        return json.dumps({
            'data': self.data,
            'class_name': self.__class__.__name__,
        })

    def send(self, bot: Bot):
        raise NotImplementedError()
