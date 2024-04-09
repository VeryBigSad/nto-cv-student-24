from aiogram.fsm.state import State, StatesGroup


class RegistrationStateGroup(StatesGroup):
    get_fio = State()
    get_email = State()
    is_this_your_email = State()
    get_verification_code = State()
    get_phone = State()
    get_city = State()
    get_status = State()
    save_data = State()
