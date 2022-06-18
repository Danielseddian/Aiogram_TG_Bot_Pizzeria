from aiogram import types, Dispatcher


async def echo_send(message: types.Message):
    lower_text = message.text.lower()
    if lower_text in ("привет", "привет!"):
        await message.reply("И тебе привет!")


def reg_other_handlers(dp: Dispatcher) -> None:
    """
    Register other's handlers in the dispatcher of the bot
    :param dp: Dispatcher of the bot
    :return: Registered handlers
    """
    dp.register_message_handler(echo_send)
