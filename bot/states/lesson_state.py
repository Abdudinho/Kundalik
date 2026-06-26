from aiogram.fsm.state import State, StatesGroup

class LessonState(StatesGroup):
    day = State()
    subject = State()
    edit_day = State()
    edit_subject = State()
    delete_day = State()