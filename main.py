from aiogram import Bot, Dispatcher, types, executor
import emoji
from functions import get_weather, prirucka, kaktus, CityError, WordError

variables = {}

bot = Bot(token="5230000984:AAFrvoQMgiwU-h7jYeDFu1u1sbHhIjxjJOs")
dp = Dispatcher(bot)
index_of_video = 0
list_of_videos = []


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, emoji.emojize(f"Привет, {message.from_user.first_name} \U0001F44B\n\n"
                                                          f"/weather - для определения погоды\n"
                                                          f"/prirucka - для спряжения слова в чешском\n"
                                                          f"/kaktus - иформация о бонусе по оператору Kaktus\n"))


@dp.message_handler(commands=["weather"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Какой город интересует?")
    variables[message.chat.id] = "weather"


@dp.message_handler(commands=["prirucka"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Какое слово интересует?")
    variables[message.chat.id] = "prirucka"


@dp.message_handler(commands=["kaktus"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, kaktus())


@dp.message_handler(content_types=["text"])
async def text_command(message: types.Message):
    if variables[message.chat.id] == "weather":
        try:
            await bot.send_message(message.chat.id, get_weather(message.text))
        except CityError as e:
            await bot.send_message(message.chat.id, "Проверьте город")
    elif variables[message.chat.id] == "prirucka":
        try:
            await bot.send_message(message.chat.id, prirucka(message.text))
        except WordError:
           await bot.send_message(message.chat.id, "Проверьте слово") 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
