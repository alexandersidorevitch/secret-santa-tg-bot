import asyncio
from random import randint, shuffle

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import app.configuration as configuration
from app.factory import ParticipantFactory
from app.wish_info import *

is_admin = lambda message: message.from_user.username == configuration.ADMIN_USERNAME


class TextWishState(StatesGroup):
    wait_for_wish = State()


class LinkWishState(StatesGroup):
    wait_for_wish = State()


class PhotoWishState(StatesGroup):
    wait_for_wish = State()


@configuration.dp.message_handler(commands=['start'])
async def start_bot_command(message: types.Message):
    buttons = [
        InlineKeyboardButton(text='Добавить пожелание', callback_data='add_wish'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer('[Приведственный текст]', reply_markup=keyboard)


@configuration.dp.message_handler(commands=['view_my_wishes'])
async def view_wishes_command(message: types.Message):
    await view_participant_wishes(message)


@configuration.dp.message_handler(is_admin, commands=['celebrate'])
async def celebrate(message: types.Message):
    shuffled_participants = get_shuffle_participants()
    participants_length = len(shuffled_participants)
    shift = randint(0, participants_length - 1)

    await message.answer('HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
    for i, participant in enumerate(shuffled_participants):
        participant.receiver = shuffled_participants[(i + shift) % participants_length]
        for wish in participant.receiver.wishes:
            await wish.send_to_async(participant.id)


def get_shuffle_participants():
    shuffled_participants = tuple(configuration.participant_io.participants.values())
    shuffle(shuffled_participants)
    return shuffled_participants


async def view_participant_wishes(message):
    participant = ParticipantFactory.get_participant(message.from_user)
    if participant.wishes:
        for wish in participant.wishes:
            await wish.send_to_async(message, format='Вы хотели бы {}')
    else:
        await message.answer('У вас не желашек((')


@configuration.dp.callback_query_handler(text='add_wish')
async def add_present(call: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(text='Добавить текстовое описание', callback_data='add_text_wish_button'),
        InlineKeyboardButton(text='Добавить фото подарка', callback_data='add_photo_wish_button'),
        InlineKeyboardButton(text='Добавить ссылку на подарок', callback_data='add_link_wish_button')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await call.message.answer('Выберите что хотите добавить', reply_markup=keyboard)


@configuration.dp.callback_query_handler(text='add_text_wish_button', state='*')
async def add_text_wish_button(call: types.CallbackQuery):
    await TextWishState.wait_for_wish.set()
    await call.message.answer('Введите текст')


@configuration.dp.message_handler(state=TextWishState.wait_for_wish, content_types=ContentTypes.TEXT)
async def add_text_wish(message: types.Message, state: FSMContext):
    participant = ParticipantFactory.get_participant(message.from_user)
    participant.add_wish(
        TextWishInfo(message.text)
    )
    configuration.participant_io.save(participant)
    await state.finish()
    await message.answer('Хорош!!')

ContentTypes.
@configuration.dp.message_handler(state=TextWishState.wait_for_wish, content_types=ContentTypes.ANY)
async def add_text_wish(message: types.Message, state: FSMContext):
    await message.answer('Введите текст((')


@configuration.dp.callback_query_handler(text='add_link_wish_button', state='*')
async def add_link_wish_button(call: types.CallbackQuery):
    await LinkWishState.wait_for_wish.set()
    await call.message.answer('Введите ссылку')


@configuration.dp.message_handler(state=LinkWishState.wait_for_wish, content_types=ContentTypes.TEXT)
async def add_link_wish(message: types.Message, state: FSMContext):
    if message.text.strip():
        participant = ParticipantFactory.get_participant(message.from_user)
        participant.add_wish(
            LinkWishInfo(message.text)
        )
        configuration.participant_io.save(participant)
        await state.finish()
        await message.answer('Хорош!!')
    else:
        await message.answer('Введите ссылку((')


@configuration.dp.message_handler(state=LinkWishState.wait_for_wish, content_types=ContentTypes.ANY)
async def incorrect_content_type_link_wish(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ссылку((')


@configuration.dp.callback_query_handler(text='add_photo_wish_button', state='*')
async def add_photo_wish_button(call: types.CallbackQuery):
    await PhotoWishState.wait_for_wish.set()
    await call.message.answer('Введите фото')


@configuration.dp.message_handler(state=PhotoWishState.wait_for_wish, content_types=ContentTypes.PHOTO)
async def add_photo_wish(message: types.Message, state: FSMContext):
    participant = ParticipantFactory.get_participant(message.from_user)
    participant.add_wish(
        PhotoWishInfo(message.photo[-1].file_id)
    )
    configuration.participant_io.save(participant)
    await state.finish()
    await message.answer('Хорош!!')


@configuration.dp.message_handler(state=PhotoWishState.wait_for_wish, content_types=ContentTypes.ANY)
async def incorrect_content_type_photo_wish(message: types.Message, state: FSMContext):
    await message.answer('Отправьте фото((')


async def main():
    await configuration.set_commands(configuration.bot)
    await configuration.dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
