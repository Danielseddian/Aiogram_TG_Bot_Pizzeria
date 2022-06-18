from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.dispatcher.filters import Text

from source.core.messanger import respond, respond_with_photo
from source.database import sql_db
from source.keyboards.keyboard_client import keyboard_client
from source.localization import ru


async def start(message: Message) -> None:
    """
    Sends a reply with a wish of bon appetit to the "start" request
    :param message: Aiogram message object
    :return: Sent message with a wish of bon appetit
    """
    await respond(message, ru.MSG_WELCOME, keyboard_client)
    await message.delete()


async def get_working_hours(message: Message) -> None:
    """
    Sends a reply with working hours
    :param message: Aiogram message object
    :return: Sent message with working hours
    """
    await respond(message, ru.MSG_HOURS)
    await message.delete()


async def get_location(message: Message) -> None:
    """
    Sends a reply with the location of the restaurant
    :param message: Aiogram message object
    :return: Sent message with the location
    """
    await respond(message, ru.MSG_LOC)
    await message.delete()


async def close_keyboard(message: Message) -> None:
    """
    Hide keyboard
    :param message: Aiogram message object
    :return: Closed keyboard
    """
    await respond(message, ru.MSG_KB_HIDED, ReplyKeyboardRemove())
    await message.delete()


async def get_pizza_menu(message: Message) -> None:
    """
    Show pizza's menu
    :param message: Aiogram message object
    :return: Pizza's menu
    """
    for dish in sql_db.get_menu():
        await respond_with_photo(message, dish[0], ru.MSG_DISH.format(dish[1], dish[2], dish[3]))
    await message.delete()


def reg_client_handlers(dp: Dispatcher) -> None:
    """
    Register client's handlers in the dispatcher of the bot
    :param dp: Dispatcher of the bot
    :return: Registered handlers
    """
    dp.register_message_handler(start, commands=["start", "начало"])
    dp.register_message_handler(start, Text(equals=ru.CMD_START, ignore_case=True))
    dp.register_message_handler(get_pizza_menu, Text(equals=ru.CMD_MENU, ignore_case=True))
    dp.register_message_handler(get_working_hours, Text(equals=ru.CMD_GET_HOURS, ignore_case=True))
    dp.register_message_handler(get_location, Text(equals=ru.CMD_GET_LOC, ignore_case=True))
    dp.register_message_handler(close_keyboard, Text(equals=ru.CMD_HIDE_KB, ignore_case=True))
