import app.text_design as text
from aiogram import types
from aiogram.types import InlineKeyboardButton
from app.factory import ParticipantFactory
from app.functions import start_mailing_async, view_participant_wishes
from app.keyboards import START_REPLY_KEYBOARD, get_inline_keyboard


async def start_bot_command(message: types.Message):
    await message.answer(text.Commands.Start.WELCOME_TEXT.format(message.from_user.full_name),
                         reply_markup=START_REPLY_KEYBOARD)


async def view_wishes_command(message: types.Message):
    await view_participant_wishes(message)


async def celebrate(message: types.Message):
    await start_mailing_async(message)


async def delete_wish_command(message: types.Message):
    participant = ParticipantFactory.get_participant(message.from_user, message.chat.id)
    if participant.wishes:
        buttons = [
            InlineKeyboardButton(f'{i + 1}. {wish}', callback_data=f'delete_button_{i}_{len(participant.wishes)}')
            for i, wish in enumerate(participant.wishes)
        ]
        keyboard = get_inline_keyboard(buttons, row_width=2)
        await message.answer(text.Commands.DeleteWish.WELCOME_TEXT, reply_markup=keyboard)
    else:
        await message.answer(text.Commands.DeleteWish.EMPTY_WISH_LIST)
