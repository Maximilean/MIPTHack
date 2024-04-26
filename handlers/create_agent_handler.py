from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.agents_database import save_agent
from parser import get_from_arxiv
from model.gigachat_model import create_agent

class UserInput(StatesGroup):
    name = State()
    scientific_article = State()
    description = State()


def create_agent_handlers(dp, bot):
    @dp.message_handler(commands=["create_agent"])
    async def start(message: types.Message):
        await message.answer("Привет! Для начала придумайте имя для нового агента:")
        await UserInput.name.set()

    @dp.message_handler(state=UserInput.name)
    async def process_login(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["name"] = message.text

        await message.answer("Теперь введи название статьи или темы:")
        await UserInput.scientific_article.set()

    @dp.message_handler(state=UserInput.scientific_article)
    async def process_password(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["scientific_article"] = message.text

        await message.answer("Отлично! Теперь введи описание нового бота:")
        await UserInput.description.set()

    @dp.message_handler(state=UserInput.description)
    async def process_description(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["description"] = message.text
            save_agent(
                message.from_user.id,
                data["name"],
                data["scientific_article"],
                data["description"],
            )
        agent_name = data["name"]
        articles = get_from_arxiv(data["scientific_article"])
        create_agent(message.from_user.id, agent_name, articles)
        await message.answer(f"Создан агент с названием {data['name']}")
        text = "<b>Использованы статьи: </b> \n"
        for idx, art in enumerate(articles):
            text += f"{idx+1}) {art['title']} \n"
        await message.answer(text, parse_mode="HTML")
        await state.finish()
