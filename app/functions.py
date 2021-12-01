from random import randint, shuffle

import app.configuration as configuration
from aiogram import types
from app.factory import ParticipantFactory


async def start_mailing_async(message: types.Message):
    shuffled_participants = get_shuffle_participants()
    participants_length = len(shuffled_participants)
    if participants_length:
        shift = randint(1, participants_length - 1)
        await message.answer('ok')
        for i, participant in enumerate(shuffled_participants):
            participant.receiver = shuffled_participants[(i + shift) % participants_length]
            await configuration.bot.send_message(participant.chat_id, f'Вы дарите @{participant.receiver.username},')
            for wish in participant.receiver.wishes:
                await wish.send_to_async(participant.chat_id)
    else:
        await message.answer('Все пусто!')


def get_shuffle_participants():
    shuffled_participants = list(configuration.participant_io.participants.values())
    shuffle(shuffled_participants)
    return shuffled_participants


async def view_participant_wishes(message: types.Message):
    participant = ParticipantFactory.get_participant(message.from_user, message.chat.id)
    if participant.wishes:
        for wish in participant.wishes:
            await wish.send_to_async(participant.chat_id, format='Вы хотели бы {}')
    else:
        await message.answer('У вас не желашек((')
