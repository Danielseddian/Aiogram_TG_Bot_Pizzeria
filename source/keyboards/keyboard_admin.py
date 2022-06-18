from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from source.localization import ru

button_load = KeyboardButton(ru.CMD_LOAD)
button_delete = KeyboardButton(ru.CMD_DELETE)

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete)
