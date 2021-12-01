from typing import Any, Callable, Union

import app.settings as settings
from aiogram import types

is_admin: Callable[[types.Message], Union[bool, Any]] = lambda \
        message: message.from_user.username == settings.ADMIN_USERNAME
