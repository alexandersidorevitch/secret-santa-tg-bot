import pickle

from app.entities.participant import Participant


class ParticipantIO:
    def __init__(self, filename='participants_info.pickle'):
        self.filename = filename
        self.__participants = dict()

    def save(self, participant):
        self.__participants[participant.unique] = self.participants.get(participant.unique, participant)
        self.__write(self.participants)

    def __write(self, data):
        with open(self.filename, 'wb') as file:
            file.write(pickle.dumps(data))

    @property
    def participants(self):
        if not self.__participants:
            self.__participants = self.read()
        return self.__participants

    @participants.setter
    def participants(self, value: dict[str, Participant]):
        if isinstance(value, dict):
            self.__participants = value

    def delete(self, participant):
        del self.participants[participant.username]

    def read(self) -> dict[str, Participant]:
        data = {}
        try:
            data = self.__read()
        except (FileNotFoundError, EOFError):
            self.__write(data)
        return data

    def __read(self) -> dict[str, Participant]:
        with open(self.filename, 'rb') as file:
            return pickle.loads(file.read())
