from aiogram import Bot, Dispatcher, types, executor
import emoji
import wikipedia
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch

variables = {"com": ""}

bot = Bot(token="5230000984:AAFrvoQMgiwU-h7jYeDFu1u1sbHhIjxjJOs")
dp = Dispatcher(bot)
wikipedia.set_lang("ru")
index_of_video = 0
list_of_videos = []


def get_wiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if len((x.strip())) > 3:
                   wikitext2 = wikitext2+x+'.'
            else:
                break
        return wikitext2
    except:
        return 'В энциклопедии нет информации об этом \U00002639'


def get_weather(city):
    try:
        city = city.replace(" ", "-")
        url = "https://sinoptik.ua/погода-" + city.lower()
        if city.lower() == "лодзь":
            url = "https://sinoptik.ua/погода-лодзь-103093133"
        elif city.lower() == "берлин":
            url = "https://sinoptik.ua/погода-берлин-102950159"
        elif city.lower() == "буэнос-айрес":
            url = "https://sinoptik.ua/погода-буэнос-айрес-103435910"
        r = requests.get(url)
        lxml = BeautifulSoup(r.content, "lxml")

        weather = lxml.find_all("td", class_="cur")
        sky = lxml.find("tr", class_="img weatherIcoS").find("td", class_="cur").find("div").get("title")
        other_days = lxml.find_all("div", class_="main")
        sky_other = lxml.find_all("div", class_="weatherIco")
        where = lxml.find("div", class_="cityName cityNameShort").find("strong").text
        answer = f"Погода {where} на 7 дней:\n---------------------------------------\n"

        list1 = []
        list2 = []
        list3 = []

        for item in weather:
            list1.append(item.text)

        list1[1] = sky

        for item in other_days:
            list2.append(item.text)

        for item in sky_other:
            list3.append(item.get("title"))

        for i in range(7):
            list3[i] = list3[i].replace("Ясно", "Ясно \U00002600")
            list3[i] = list3[i].replace("Небольшая облачность", "Небольшая облачность \U0001F324")
            list3[i] = list3[i].replace("Переменная облачность", "Переменная облачность \U000026C5")
            list3[i] = list3[i].replace("Сплошная облачность", "Сплошная облачность \U00002601")
            list3[i] = list3[i].replace("Облачно с прояснениями", "Облачно с прояснениями \U0001F325")
            list3[i] = list3[i].replace("дождь", "дождь \U0001F327")
            list3[i] = list3[i].replace("грозы", "грозы \U000026A1")
            list3[i] = list3[i].replace("дождь, грозы", "дождь, грозы \U000026C8")

        for i in range(7):
            list2[i] = list2[i].replace("    ", f"\nНа небе: {list3[i]}\nТемпература: ")
            list2[i] = list2[i][1:]
            answer += list2[i]
            answer += "\n---------------------------------------\n"

        list1[1] = list1[1].replace("Ясно", "Ясно \U00002600")
        list1[1] = list1[1].replace("Небольшая облачность", "Небольшая облачность \U0001F324")
        list1[1] = list1[1].replace("Переменная облачность", "Переменная облачность \U000026C5")
        list1[1] = list1[1].replace("Сплошная облачность", "Сплошная облачность \U00002601")
        list1[1] = list1[1].replace("Облачно с прояснениями", "Облачно с прояснениями \U0001F325")
        list1[1] = list1[1].replace("дождь", "дождь \U0001F327")
        list1[1] = list1[1].replace("грозы", "грозы \U000026A1")
        list1[1] = list1[1].replace("дождь, грозы", "дождь, грозы \U000026C8")

        answer += f"\nСейчас {where}\nТемпература: {list1[2]}\nНа небе: {list1[1]}"
        return answer
    except:
        return "Что-то пошло не так \U00002639"


def prirucka(slovo):
    try:
        url = "https://prirucka.ujc.cas.cz/?slovo=" + slovo.lower()
        r = requests.get(url)
        lxml = BeautifulSoup(r.content, "html.parser")

        tab23 = lxml.find_all("td", class_="centrovane")
        tab1 = lxml.find_all("td", class_="vlevo")
        noun = lxml.find_all("p", class_="polozky")

        if_noun = False

        list1 = []
        result = 0

        answer = "\n"

        for item in tab1:
            result = result + 1
            list1.append(item.text)

        for item in tab23:
            list1.append(item.text)

        for item in noun:
            if "rod" in item.text:
                if_noun = True
                break

        for i in range(len(list1)):
            if list1[i][-1].isdigit():
                list1[i] = list1[i][:-1]

        if if_noun:
            answer += f"1. Nominativ(Kdo? Co?):           {list1[9]}  --  {list1[10]}\n"
            answer += f"2. Genitiv(Koho? Čeho?):          {list1[11]}  --  {list1[12]}\n"
            answer += f"3. Dativ(Komu? Čemu?):            {list1[13]}  --  {list1[14]}\n"
            answer += f"4. Akuzativ(Koho? Co?):           {list1[15]}  --  {list1[16]}\n"
            answer += f"5. Vokativ(Oslovujeme, voláme):   {list1[17]}  --  {list1[18]}\n"
            answer += f"6. Lokál(O kom? O čem?):          {list1[19]}  --  {list1[20]}\n"
            answer += f"7. Instrumentál(S kým? S čím?):   {list1[21]}  --  {list1[22]}\n"
        else:
            answer += f"{list1[0]}:  {list1[result + 2]} - {list1[result + 3]}\n"
            answer += f"{list1[1]}:  {list1[result + 4]} - {list1[result + 5]}\n"
            answer += f"{list1[2]}:  {list1[result + 6]} - {list1[result + 7]}\n\n"
            answer += f"{list1[3]}:  {list1[result + 8]} - {list1[result + 9]}\n"
            answer += f"{list1[4]}:  {list1[result + 10]}\n"

        return answer
    except:
        return "Что-то пошло не так \U00002639"


def search_youtube(search, index):
    try:
        search = VideosSearch(search, limit=10)
        list1 = search.result()

        string = str(list1).split()
        link = False

        for word in string:
            if link and "watch" in word:
                link = False
                word = word.replace("\'", '')
                word = word.replace(",", '')
                list_of_videos.append(word)
            if word == "\'link\':":
                link = True

        return list_of_videos[index]
    except:
        return "Что-то пошло не так \U00002639"


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, emoji.emojize(f"Привет, {message.from_user.first_name} \U0001F44B\n\n"
                                                          f"/weather - для определения погоды\n"
                                                          f"/wiki - для поиска слова в wikipedia\n"
                                                          f"/prirucka - для спряжения слова в чешском\n"
                                                          f"/youtube - для поиска видео в Youtube\n"))


@dp.message_handler(commands=["weather"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Какой город интересует?")
    variables["com"] = "weather"


@dp.message_handler(commands=["wiki"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Какое слово интересует?")
    variables["com"] = "wiki"


@dp.message_handler(commands=["prirucka"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Какое слово интересует?")
    variables["com"] = "prirucka"


@dp.message_handler(commands=["youtube"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Введите запрос")
    variables["com"] = "youtube"


@dp.callback_query_handler(text="plus")
async def send_random_value(call: types.CallbackQuery):
    global index_of_video
    index_of_video = index_of_video + 1
    if index_of_video > 9:
        index_of_video = 9
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="\U00002B05", callback_data="minus"),
        types.InlineKeyboardButton(text="\U000027A1", callback_data="plus")
    ]
    keyboard.add(*buttons)
    await call.message.answer(list_of_videos[index_of_video], reply_markup=keyboard)


@dp.callback_query_handler(text="minus")
async def send_random_value(call: types.CallbackQuery):
    global index_of_video
    index_of_video = index_of_video - 1
    if index_of_video < 0:
        index_of_video = 0
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="\U00002B05", callback_data="minus"),
        types.InlineKeyboardButton(text="\U000027A1", callback_data="plus")
    ]
    keyboard.add(*buttons)
    await call.message.answer(list_of_videos[index_of_video], reply_markup=keyboard)


@dp.message_handler(content_types=["text"])
async def text_command(msg: types.Message):
    if variables["com"] == "weather":
        await bot.send_message(msg.chat.id, get_weather(msg.text))
    elif variables["com"] == "wiki":
        await bot.send_message(msg.chat.id, get_wiki(msg.text))
    elif variables["com"] == "prirucka":
        await bot.send_message(msg.chat.id, prirucka(msg.text))
    elif variables["com"] == "youtube":
        global list_of_videos
        list_of_videos = []
        global index_of_video
        index_of_video = 0
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text="\U00002B05", callback_data="minus"),
            types.InlineKeyboardButton(text="\U000027A1", callback_data="plus")
        ]
        keyboard.add(*buttons)
        await bot.send_message(msg.chat.id, search_youtube(msg.text, index_of_video), reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
