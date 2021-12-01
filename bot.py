import asyncio

import app.configuration as configuration
from app.handler.register_handlers import register_all_handlers


async def main():
    await configuration.set_commands(configuration.bot)
    register_all_handlers(configuration.dp)
    await configuration.dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
