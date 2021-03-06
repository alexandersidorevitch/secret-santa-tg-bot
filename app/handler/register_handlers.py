import app.text_markup as text
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentTypes
from aiogram.utils.exceptions import BotBlocked
from app.handler.buttons_calback import delete_wish_button
from app.handler.buttons_message_handler import CancelButton, LinkWishButton, PhotoWishButton, TextWishButton
from app.handler.command import celebrate, delete_wish_command, start_bot_command, view_wishes_command, \
    view_participants, incomprehensible_message
from app.states import LinkWishState, PhotoWishState, TextWishState
from app.filters import is_admin
from app.handler.bot_exceptions import error_bot_blocked


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_bot_command, commands=['start'])
    dp.register_message_handler(view_wishes_command, commands=['view_my_wishes'])
    dp.register_message_handler(celebrate, is_admin, commands=['celebrate'])
    dp.register_message_handler(delete_wish_command, commands=['delete_wish'])
    dp.register_message_handler(view_participants, is_admin, commands=['see_participants'])


def register_buttons_callbacks(dp: Dispatcher):
    # Register button for delete wishes from participant wish list
    dp.register_callback_query_handler(delete_wish_button, Text(startswith="delete_button_"))


def register_buttons_handlers(dp: Dispatcher):
    # Register button for canceling all states
    dp.register_message_handler(CancelButton.cancel_to_add,
                                text=text.Buttons.Cancel.CAPTION,
                                state='*')

    # Register waiting function for wishes
    dp.register_message_handler(TextWishButton.set_message_waiting,
                                text=text.Buttons.Text.CAPTION,
                                state='*')
    url_regexp = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    dp.register_message_handler(LinkWishButton.set_message_waiting,
                                text=text.Buttons.Link.CAPTION,
                                state='*')
    dp.register_message_handler(PhotoWishButton.set_message_waiting,
                                text=text.Buttons.Photo.CAPTION,
                                state='*')

    # Register function for add wishes
    dp.register_message_handler(TextWishButton.add_wish,
                                state=TextWishState.wait_for_wish,
                                content_types=ContentTypes.TEXT)
    dp.register_message_handler(LinkWishButton.add_wish,
                                state=LinkWishState.wait_for_wish,
                                regexp=url_regexp,
                                content_types=ContentTypes.TEXT)
    dp.register_message_handler(PhotoWishButton.add_wish,
                                state=PhotoWishState.wait_for_wish,
                                content_types=ContentTypes.PHOTO,
                                )

    # Register error handler
    dp.register_message_handler(TextWishButton.errors_handler,
                                state=TextWishState.wait_for_wish,
                                content_types=ContentTypes.ANY)
    dp.register_message_handler(LinkWishButton.errors_handler,
                                state=LinkWishState.wait_for_wish,
                                content_types=ContentTypes.ANY)

    dp.register_message_handler(PhotoWishButton.errors_handler,
                                state=PhotoWishState.wait_for_wish,
                                content_types=ContentTypes.ANY)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(incomprehensible_message,
                                content_types=ContentTypes.ANY)


def register_error_handler(dp: Dispatcher):
    dp.errors_handler(error_bot_blocked, BotBlocked)


def register_all_handlers(dp: Dispatcher):
    register_commands(dp)
    register_buttons_callbacks(dp)
    register_buttons_handlers(dp)
    register_message_handler(dp)
    register_error_handler(dp)
