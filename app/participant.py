from app.wish_info import WishInfo


class Participant:
    def __init__(self, name, user_id, user_name):
        self.id = user_id
        self.user_name = user_name
        self.name = name
        self.wishes = []
        self.receiver = None

    def add_wish(self, wish: WishInfo):
        self.wishes.append(wish)

    def add_wishes(self, *wishes: WishInfo):
        for wish in wishes:
            self.add_wish(wish)
