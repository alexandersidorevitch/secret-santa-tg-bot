import app.configuration as configuration
from app.entities.participant import Participant


class ParticipantFactory:
    @staticmethod
    def get_participant(user_info, chat_id) -> Participant:
        username = user_info.username
        if username not in configuration.participant_io.participants:
            configuration.participant_io.save(
                Participant(user_info.full_name, username, chat_id)
            )
        return configuration.participant_io.participants[username]
