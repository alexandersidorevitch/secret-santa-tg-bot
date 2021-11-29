from aiogram.dispatcher.filters.state import State, StatesGroup


class TextWishState(StatesGroup):
    wait_for_wish = State()


class LinkWishState(StatesGroup):
    wait_for_wish = State()


class PhotoWishState(StatesGroup):
    wait_for_wish = State()
