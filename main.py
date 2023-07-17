from aiogram import Bot, Dispatcher, types, executor
import emoji
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
    await bot.send_message(message.chat.id, kaktus())


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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
