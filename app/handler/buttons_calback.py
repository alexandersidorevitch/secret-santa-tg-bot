import app.configuration as configuration
from aiogram import types
from app.factory import ParticipantFactory


async def delete_wish_button(call: types.CallbackQuery):
    *_, wish_index_to_delete, wishes_len = call.data.split('_')
    wish_index_to_delete = int(wish_index_to_delete)
    participant = ParticipantFactory.get_participant(call.from_user, call.message.chat.id)
    if len(participant.wishes) < int(wishes_len):
        await call.message.answer('Я не могу его удалить, т.к. данный подарок мог быть удаленен.\n'
                                  r'Введите /delete_wish, чтобы удалить подарок')
    else:
        wish_to_delete = participant.wishes[wish_index_to_delete]
        participant.wishes[wish_index_to_delete].delete()
        configuration.participant_io.save(participant)
        await call.message.answer('Убрал из вашего списка это пожелание')
        await wish_to_delete.send_to_async(call.message.chat.id)