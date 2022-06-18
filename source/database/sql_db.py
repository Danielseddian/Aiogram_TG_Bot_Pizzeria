import sqlite3 as sq
from aiogram.types import Message

from source.core.messanger import respond_with_photo
from source.localization import ru


def sql_start():
    """
    Create menu database if not exists and create global variables: database and cursor
    :return: created menu database
    """
    global base, cur
    base = sq.connect("pizza_bot.db")
    cur = base.cursor()
    if base:
        print(ru.MSG_DB_CONNECTED)
    base.execute(
        "CREATE TABLE if NOT EXISTS     menu("
        "   dish_id         INTEGER     PRIMARY KEY     AUTOINCREMENT,"
        "   img             TEXT        NOT NULL,"
        "   name            TEXT        NOT NULL        UNIQUE,"
        "   description     TEXT,"
        "   price           FLOAT       NOT NULL"
        ")"
    )
    base.commit()


async def sql_add(state) -> None:
    """
    Add dish into menu database
    :param state: Bot state with data about dish
    :return: Added dish
    """
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu(img, name, description, price) VALUES (?,?,?,?)", tuple(data.values()))
        base.commit()


def get_menu() -> list:
    """
    Query menu from menu database
    :return: Pizza's menu
    """
    return cur.execute(f"SELECT img, name, description, price FROM menu").fetchall()


def del_dish(name) -> None:
    """
    Delete dish from menu database
    :return: Deleted dish
    """
    cur.execute("DELETE FROM menu WHERE name == ?", (name,))
    base.commit()
