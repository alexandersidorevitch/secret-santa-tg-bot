from aiogram import types
from app.participant import Participant

import app.configuration as configuration


class ParticipantFactory:
    @staticmethod
    def get_participant(user_info) -> Participant:
        user_id = user_info.id
        if user_id not in configuration.participant_io.participants:
            configuration.participant_io.save(
                Participant(user_info.full_name, user_id, user_info.username)
            )
        return configuration.participant_io.participants[user_id]
