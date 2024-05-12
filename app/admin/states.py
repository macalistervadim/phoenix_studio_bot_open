import aiogram.fsm.state


class CreateItem(aiogram.fsm.state.StatesGroup):
    title = aiogram.fsm.state.State()
    description = aiogram.fsm.state.State()
    image = aiogram.fsm.state.State()
    price = aiogram.fsm.state.State()
    deadline = aiogram.fsm.state.State()
