from app.entities.wish_info import WishInfo


class Participant:
    def __init__(self, name, username, chat_id):
        self.chat_id = chat_id
        self.username = username
        self.name = name
        self._wishes = []
        self.receiver = None

    @property
    def unique(self):
        return self.username

    @property
    def wishes(self):
        return list(filter(lambda wish: not wish.is_deleted, self._wishes))

    def add_wish(self, wish: WishInfo):
        self._wishes.append(wish)

    def add_wishes(self, *wishes: WishInfo):
        for wish in wishes:
            self.add_wish(wish)
