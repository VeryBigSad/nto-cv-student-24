from aiogram.fsm.state import State, StatesGroup


class WelcomeStateGroup(StatesGroup):
    wait_continue_kb = State()
    video_tests = State()
