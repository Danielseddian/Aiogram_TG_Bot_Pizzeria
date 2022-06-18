from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from source.localization import ru

keyboard_working = KeyboardButton(ru.CMD_GET_HOURS)
keyboard_location = KeyboardButton(ru.CMD_GET_LOC)
keyboard_menu = KeyboardButton(ru.CMD_MENU)
keyboard_close = KeyboardButton(ru.CMD_HIDE_KB)
# keyboard_give_my_loc = KeyboardButton(ru.CMD_MY_LOC, request_location=True)
# keyboard_give_my_num = KeyboardButton(ru.CMD_MY_NUM, request_contact=True)

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.row(keyboard_working, keyboard_location).row(keyboard_menu, keyboard_close)
# keyboard_client.row(keyboard_give_my_loc, keyboard_give_my_num)
