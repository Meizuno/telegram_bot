from aiogram import Bot, Dispatcher, types, executor
import emoji
import schedule
import asyncio
from functions import *
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, emoji.emojize(f"Привет, {message.from_user.first_name} \U0001F44B\n\n"
                                                          f"/weather - для определения погоды\n"
                                                          f"/prirucka - для спряжения слова в чешском\n"
                                                          f"/kaktus - иформация о бонусе по оператору Kaktus\n"))


@dp.message_handler(commands=["weather"])
async def start_command(message: types.Message):
    set_to_db(str(message.chat.id), "weather")
    await bot.send_message(message.chat.id, "Какой город интересует?")


@dp.message_handler(commands=["prirucka"])
async def start_command(message: types.Message):
    set_to_db(str(message.chat.id), "prirucka")
    await bot.send_message(message.chat.id, "Какое слово интересует?")


@dp.message_handler(commands=["kaktus"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, users_kaktus_db(str(message.chat.id)))


@dp.message_handler(content_types=["text"])
async def text_command(message: types.Message):
    if get_from_db(str(message.chat.id)) == "weather":
        try:
            await bot.send_message(message.chat.id, get_weather(message.text))
        except CityError as e:
            await bot.send_message(message.chat.id, "Проверьте город")
    elif get_from_db(str(message.chat.id)) == "prirucka":
        try:
            await bot.send_message(message.chat.id, prirucka(message.text))
        except WordError:
           await bot.send_message(message.chat.id, "Проверьте слово") 


async def scheduled_function():
    msg = kaktus_check_bonus()
    if msg:
        try:
            with open("database.json", "r") as json_file:
                data = json.load(json_file)
                for key, value in data["kaktus"].items():
                    if value == 'false':
                        await bot.send_message(key, msg) 
                        print("send msg")
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        

schedule.every(5).seconds.do(scheduled_function)

async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_schedule())
    executor.start_polling(dp, skip_updates=True)
