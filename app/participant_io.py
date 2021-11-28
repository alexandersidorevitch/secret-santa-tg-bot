import pickle

from app.participant import Participant


class ParticipantIO:
    def __init__(self, filename='participants.pickle'):
        self.filename = filename
        self.__participants = dict()

    def save(self, participant):
        self.__participants[participant.id] = self.participants.get(participant.id, participant)
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
