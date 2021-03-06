from random import randint, shuffle

import app.configuration as configuration
from aiogram import Bot, types
from aiogram.types import BotCommand
from aiogram.utils.exceptions import BotBlocked
from app.entities.participant import Participant
from app.factory import ParticipantFactory


async def start_mailing_async(message: types.Message):
    shuffled_participants = get_shuffle_participants()
    participants_length = len(shuffled_participants)
    if participants_length >= 2:
        shift = randint(1, participants_length - 1)
        await message.answer(r"Let's go")
        try:
            for i, participant in enumerate(shuffled_participants):
                participant.receiver = shuffled_participants[(i + shift) % participants_length]
                try:
                    await configuration.bot.send_message(participant.chat_id,
                                                         f'Вы дарите @{participant.receiver.username}')
                    for wish in participant.receiver.wishes:
                        await wish.send_to_async(participant.chat_id)
                except BotBlocked as e:
                    configuration.participant_io.delete(participant)
                    raise e
        except BotBlocked as e:
            shuffled_participants = get_shuffle_participants()
            for i, participant in enumerate(shuffled_participants):
                await configuration.bot.send_message(participant.chat_id, f'Произошла ошибка, кто-то от нас ушел(. '
                                                                          f'Повторяю еще раз')
            await start_mailing_async(message)
            raise e

    else:
        await message.answer(f'Не хватате человек для рассылки {participants_length=}')


def get_shuffle_participants():
    shuffled_participants = list(configuration.participant_io.participants.values())
    shuffle(shuffled_participants)
    return shuffled_participants


async def view_participant_wishes(message: types.Message):
    participant = ParticipantFactory.get_participant(message.from_user, message.chat.id)
    if participant.wishes:
        for wish in participant.wishes:
            await wish.send_to_async(participant.chat_id)
    else:
        await message.answer('У вас не желашек((')


def verify_inline_button_callback(participant: Participant, verify_hash: str):
    return str(hash(participant)) == verify_hash


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/view_my_wishes", description="Вывести мои пожелания"),
        BotCommand(command="/delete_wish", description="Удалить пожелание"),
    ]
    await bot.set_my_commands(commands)
