from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Text

from source.core.config import ADMINS
from source.core.messanger import respond, respond_with_photo
from source.database import sql_db
from source.localization import ru
from source.keyboards import keyboard_admin


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def get_access_handler(message: Message) -> None:
    """
    Checks user is group's admin and returns global ID var with his id
    :param message: Aiogram message object
    :return: global ID with users id and access to admin menu if he is admin
    """
    if message.from_user.id in ADMINS:
        await respond(message, ru.MSG_ADMIN_CHECKED, keyboard_admin.button_case_admin)
        await message.delete()


async def start_cm(message: Message, state=None) -> None:
    """
    Asks image of product
    :param message: Aiogram message object
    :param state: Aiogram FSMContext
    :return: Sent ask of photo
    """
    if message.from_user.id in ADMINS:
        await FSMAdmin.photo.set()
        await message.reply(ru.MSG_LOAD_PHOTO)


async def cancel_handler(message: Message, state=FSMContext) -> None:
    """
    Cancels active FSM if user change his mind and sends confirm message
    :param message: Aiogram message object
    :param state: Aiogram FSMContext
    :return: Canceled FSM and sent confirm message
    """
    if message.from_user.id in ADMINS:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply(ru.MSG_INPUT_CANCELED)


async def load_photo(message: Message, state: FSMContext) -> None:
    """
    Sets up photo and asks name of product
    :param message: Aiogram message object
    :param state: Aiogram FSMContext
    :return: Set up image and sent ask of name
    """
    if message.from_user.id in ADMINS:
        if message.content_type != "photo":
            await message.answer(ru.ERR_NOT_IMG)
            return
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply(ru.MSG_INPUT_NAME)


async def input_name(message: Message, state: FSMContext) -> None:
    """
    Sets up photo and asks description of product
    :param message: Aiogram message object
    :param state: Aiogram FSMContext
    :return: Set up name and sent ask of description
    """
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply(ru.MSG_INPUT_DESC)


async def input_description(message: Message, state: FSMContext) -> None:
    """
    Sets up description and asks price of product
    :param message: Aiogram message object
    :param state: Aiogram FSMContext
    :return: Set up description and sent ask of price
    """
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        await message.reply(ru.MSG_INPUT_PRICE)


async def input_price(message: Message, state: FSMContext) -> None:
    """
    Sets up price
    :param message: Aiogram message object
    :param state: Aiogram FSMContext
    :return: Set up price
    """
    if message.from_user.id in ADMINS:
        try:
            async with state.proxy() as data:
                data["price"] = float(message.text)
        except (TypeError, ValueError):
            await message.reply(ru.ERR_NOT_NUM)
            return
        await sql_db.sql_add(state)
        await state.finish()


async def delete_dish(message: Message) -> None:
    """
    Query deletion dish from menu database
    :param message: Aiogram message object
    :return: Query deletion dish from menu
    """
    if message.from_user.id in ADMINS:
        for dish in sql_db.get_menu():
            button = ru.QRY_DELETE.format(dish[1])
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton(button, callback_data=f"del {dish[1]}"))
            await respond_with_photo(message, dish[0], ru.MSG_DISH.format(dish[1], dish[2], dish[3]), markup)
        await message.delete()


async def run_deletion_dish(query: CallbackQuery) -> None:
    """
    Delete dish from menu database
    :param query: Aiogram query object
    :return: Deleted dish from menu
    """
    dish = query.data.replace("del ", "")
    sql_db.del_dish(dish)
    await query.answer(text=ru.MSG_DELETED.format(dish), show_alert=True)


def reg_admin_handlers(dp: Dispatcher) -> None:
    """
    Register admin handlers in the dispatcher of the bot
    :param dp: Dispatcher of the bot
    :return: Registered handlers
    """
    dp.register_message_handler(get_access_handler, Text(equals=ru.CMD_ADMIN, ignore_case=True))
    dp.register_message_handler(start_cm, Text(equals=ru.CMD_LOAD, ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=ru.CMD_CANCEL)
    dp.register_message_handler(cancel_handler, Text(equals=ru.CMD_CANCEL, ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo)
    dp.register_message_handler(input_name, state=FSMAdmin.name)
    dp.register_message_handler(input_description, state=FSMAdmin.description)
    dp.register_message_handler(input_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_dish, Text(equals=ru.CMD_DELETE, ignore_case=True))
    dp.register_callback_query_handler(run_deletion_dish, lambda q: q.data and q.data.startswith("del "))
