from aiogram.utils import executor

from core.create import dp
from handlers import client, other, admin
from localization import ru
from database import sql_db


async def on_startup(_):
    print(ru.MSG_BOT_CONNECTED)
    sql_db.sql_start()

admin.reg_admin_handlers(dp)
client.reg_client_handlers(dp)
other.reg_other_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
