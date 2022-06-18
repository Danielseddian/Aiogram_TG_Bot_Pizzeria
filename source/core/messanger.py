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
        return await bot.send_message(message.from_user.id, text, reply_markup=markup)
    except aiogram_exceptions.CantInitiateConversation:
        await message.reply(ru.ERR_NOT_REG)
    except aiogram_exceptions.BotBlocked:
        await message.reply(ru.ERR_BLOCKED)


async def respond_with_photo(message: Message, photo_id: str, text: str, markup: markups = None) -> Union[Bot, None]:
    """
    Sends private message to the message's author or warn about subscribing
    :param message: Aiogram message object
    :param photo_id: Photo id for sending
    :param text: Text of message for sending
    :param markup: Keyboard markup for running keyboards
    :return: Sent message to the message's author
    """
    try:
        return await bot.send_photo(message.from_user.id, photo_id, text, reply_markup=markup)
    except aiogram_exceptions.CantInitiateConversation:
        await message.reply(ru.ERR_NOT_REG)
    except aiogram_exceptions.BotBlocked:
        await message.reply(ru.ERR_BLOCKED)
