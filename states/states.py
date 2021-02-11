from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    txt = State()


class Review(StatesGroup):
    offer = State()
    complain = State()
