from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils import exceptions as aiogram_exceptions
from typing import Union

from source.core.create import bot
from source.localization import ru

markups = Union[ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup]


async def respond(message: Message, text, markup: markups = None) -> Union[Bot, None]:
    """
    Sends private message to the message's author or warn about subscribing
    :param message: Aiogram message object
    :param text: Text of message for sending
    :param markup: Keyboard markup for running keyboard
    :return: Sent message to the message's author
    """
    try:
        user_id = message.from_user.id
        return await bot.send_message(user_id, text, reply_markup=markup)
    except aiogram_exceptions:
        await message.reply(ru.ERR_NOT_REG)


async def respond_with_photo(message: Message, photo_id: str, text: str, markup: markups = None) -> Union[Bot, None]:
    """
    Sends private message to the message's author or warn about subscribing
    :param message: Aiogram message object
    :param photo_id: Photo id for sending
    :param text: Text of message for sending
    :param markup: Keyboard markup for running keyboard
    :return: Sent message to the message's author
    """
    try:
        user_id = message.from_user.id
        return await bot.send_photo(user_id, photo_id, text, reply_markup=markup)
    except aiogram_exceptions:
        await message.reply(ru.ERR_NOT_REG)
