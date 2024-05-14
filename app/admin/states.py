import aiogram.fsm.state


class CreateItem(aiogram.fsm.state.StatesGroup):
    title = aiogram.fsm.state.State()
    description = aiogram.fsm.state.State()
    image = aiogram.fsm.state.State()
    price = aiogram.fsm.state.State()
    deadline = aiogram.fsm.state.State()


class EditItem(aiogram.fsm.state.StatesGroup):
    item = aiogram.fsm.state.State()
    choice = aiogram.fsm.state.State()
    editable_object = aiogram.fsm.state.State()
    edit_item = aiogram.fsm.state.State()


class DeleteItem(aiogram.fsm.state.StatesGroup):
    item = aiogram.fsm.state.State()
    choice = aiogram.fsm.state.State()


class CreatePcode(aiogram.fsm.state.StatesGroup):
    name = aiogram.fsm.state.State()
    discount = aiogram.fsm.state.State()
    activations = aiogram.fsm.state.State()


class DeletePocde(aiogram.fsm.state.StatesGroup):
    name = aiogram.fsm.state.State()
    choice = aiogram.fsm.state.State()
