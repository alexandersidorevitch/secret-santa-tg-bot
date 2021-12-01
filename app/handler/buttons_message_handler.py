import app.configuration as configuration
import app.text_markup as text
from aiogram import types
from aiogram.dispatcher import FSMContext
from app.factory import ParticipantFactory
from app.states import LinkWishState, PhotoWishState, TextWishState
from app.entities.wish_info import LinkWishInfo, PhotoWishInfo, TextWishInfo


class CancelButton:
    @staticmethod
    async def cancel_to_add(message: types.Message, state: FSMContext):
        configuration.logger.info(f'{message.from_user.username} pressed cancel button')
        await state.finish()
        await message.answer(text.Buttons.Cancel.ANSWER)


class TextWishButton:
    @staticmethod
    async def set_message_waiting(message: types.Message):
        configuration.logger.info(f'{message.from_user.username} waiting for add text wish')
        await TextWishState.wait_for_wish.set()
        await message.answer(text.Buttons.Text.ANSWER)

    @staticmethod
    async def add_wish(message: types.Message, state: FSMContext):
        configuration.logger.info(f'{message.from_user.username} adding text wish')
        participant = ParticipantFactory.get_participant(message.from_user, message.chat.id)
        participant.add_wish(
            TextWishInfo(message.text)
        )
        configuration.participant_io.save(participant)
        await state.finish()
        await message.answer('Хорош!!')

    @staticmethod
    async def errors_handler(message: types.Message, state: FSMContext):
        configuration.logger.info(f'{message.from_user.username} try to add {message.content_type} to text wish')
        await message.answer(text.Buttons.Text.ANSWER_FOR_WRONG_CONTENT_TYPE)


class LinkWishButton:
    @staticmethod
    async def set_message_waiting(message: types.Message):
        await LinkWishState.wait_for_wish.set()
        await message.answer(text.Buttons.Link.ANSWER)

    @staticmethod
    async def add_wish(message: types.Message, state: FSMContext):
        participant = ParticipantFactory.get_participant(message.from_user, message.chat.id)
        participant.add_wish(
            LinkWishInfo(message.text)
        )
        configuration.participant_io.save(participant)
        await state.finish()
        await message.answer('Хорош!!')

    @staticmethod
    async def errors_handler(message: types.Message, state: FSMContext):
        await message.answer(text.Buttons.Link.ANSWER_FOR_WRONG_CONTENT_TYPE)


class PhotoWishButton:
    @staticmethod
    async def set_message_waiting(message: types.Message):
        await PhotoWishState.wait_for_wish.set()
        await message.answer(text.Buttons.Photo.ANSWER)

    @staticmethod
    async def add_wish(message: types.Message, state: FSMContext):
        participant = ParticipantFactory.get_participant(message.from_user, message.chat.id)
        participant.add_wish(
            PhotoWishInfo(message.photo[-1].file_id)
        )
        configuration.participant_io.save(participant)
        await state.finish()
        await message.answer('Хорош!!')

    @staticmethod
    async def errors_handler(message: types.Message, state: FSMContext):
        await message.answer(text.Buttons.Photo.ANSWER_FOR_WRONG_CONTENT_TYPE)
