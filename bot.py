from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

from handlers.create_agent_handler import create_agent_handlers
from handlers.get_agents_handler import get_agent_handler
from database.agents_database import get_agent_for_user

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging_middleware = LoggingMiddleware()
dp.middleware.setup(logging_middleware)


create_agent_handlers(dp, bot)
get_agent_handler(dp, bot)


from handlers.text_message_handler import text_message_handler
text_message_handler(bot, dp)



if __name__ == "__main__":
    executor.start_polling(dp)
