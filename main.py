import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject


from database_interactions import DatabaseExecutor
from config import MESSAGE_HOUR, MESSAGE_MINUTE
from secret_token import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

dbex = DatabaseExecutor()

@dp.message(CommandStart())
async def cmd_start(message: Message):

    dbex.create_connection()
    dbex.set_group_id_to_message(message.chat.id)
    dbex.close_connection()

    await message.answer(str(message.chat.id))


@dp.message(Command('show_today_message'))
async def show_today_message(message: Message):
    await send_today_message(message.from_user.id)

@dp.message(Command('create_tables'))
async def show_today_message(message: Message):
    dbex.create_connection()
    dbex.create_tables()
    dbex.close_connection()
    await send_today_message(message.from_user.id)

@dp.message(Command('change_message_content_by_date'))
async def show_today_message(message: Message, command: CommandObject):
    args_string = command.args

    if args_string and "|" in args_string:
        message_to_change_date, new_message_content = args_string[:args_string.index("|"):], args_string[args_string.index("|")+1::]
        
        dbex.create_connection()
        dbex.change_message_content_by_date(message_to_change_date, new_message_content)
        dbex.close_connection()

        await message.answer("Done")
    else:
        await message.answer("Wrong format")

async def send_today_message(user_id=None):


    dbex.create_connection()
    if not user_id: user_id = dbex.get_group_id()["variable_value"]
    today_message = dbex.get_today_message(datetime.today().strftime('%Y-%m-%d'))
    dbex.close_connection()

    await bot.send_message(chat_id=user_id, text=today_message["message-content"])


async def main():

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_today_message, trigger="cron", hour=MESSAGE_HOUR, minute=MESSAGE_MINUTE, start_date=datetime.now())
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())