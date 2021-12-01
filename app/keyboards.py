from aiogram import types
import app.text_markup as text


def get_inline_keyboard(buttons, **kwargs):
    kwargs['resize_keyboard'] = True
    keyboard = types.InlineKeyboardMarkup(**kwargs)
    keyboard.add(*buttons)
    return keyboard


def get_reply_keyboard(buttons, **kwargs):
    kwargs['resize_keyboard'] = True
    keyboard = types.ReplyKeyboardMarkup(**kwargs)
    keyboard.add(*buttons)
    return keyboard


START_REPLY_KEYBOARD = get_reply_keyboard([
    text.Buttons.Text.CAPTION,
    text.Buttons.Link.CAPTION,
    text.Buttons.Photo.CAPTION,
    text.Buttons.Cancel.CAPTION,
], row_width=1)
