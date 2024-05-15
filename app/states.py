import aiogram.fsm.state


class CreateOrder(aiogram.fsm.state.StatesGroup):
    description_order = aiogram.fsm.state.State()
