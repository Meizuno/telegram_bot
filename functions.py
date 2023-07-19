import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime
from config import WEATHER_API
import json

class CityError(Exception):
    def __init__(self, message):
        self.message = message
        
class WordError(Exception):
    def __init__(self, message):
        self.message = message

def get_weather(city):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city.lower()}&appid={WEATHER_API}&lang=ru&units=metric"
        )
        data = r.json()
        return f"Погода             {city}\nТемпература  {data['main']['temp']}°C\nВлажность      {data['main']['humidity']}%\nВетер                {data['wind']['speed']} м/c"
    except Exception as e:
        raise CityError("City invalid")



def prirucka(word):
    try:
        url = "https://prirucka.ujc.cas.cz/?slovo=" + word.lower()
        r = requests.get(url)
        lxml = BeautifulSoup(r.content, "html.parser")
        
        list_of_pads = [
            "1. Nominativ (Kdo? Co?)\n ~ ",
            "2. Genetiv (Koho? Čeho?)\n ~ ",
            "3. Dativ (Komu? Čemu?)\n ~ ",
            "4. Akuzativ (Koho? Co?)\n ~ ",
            "5. Vokativ (Voláme)\n ~ ",
            "6. Lokál (O kom? O čem?)\n ~ ",
            "7. Instrumentál (S kým? S čím?)\n ~ ",
        ] 

        table = lxml.find("table").find_all("tr")
        content = []
        for index, tr in enumerate(table):
            for td in tr:
                if re.search(r"\d\. pád", td.getText()) and index != 0:
                    content.append(list_of_pads[index - 1])
                else: 
                    if td.getText() and td.getText()[-1].isdigit():
                        content.append(f"{td.getText()[:-1]} ~ ")
                    else:
                        content.append(f"{td.getText()} ~ ")
            content.append('\n')
            

        return ''.join(content)
    except Exception:
        raise WordError("Invalid word")


def kaktus_check_bonus():
    page = requests.get("http://www.mujkaktus.cz")
    soup = BeautifulSoup(page.content, 'lxml')
    article = soup.find("div", {'class': 'article'})
    pattern = r"\b\d{1,2}\.\s?\d{1,2}\."

    matches = re.findall(pattern, article.text)
    date = [int(part.strip()) for part in matches[0].split(".") if part.strip().isdigit()]

    if int(date[0]) == datetime.now().day and int(date[1]) == datetime.now().month:
        return article.text

    return None


def set_to_db(key, value):
    try:
        with open("database.json", "r") as json_file:
            data = json.load(json_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        data = {"data": {}, "kaktus": {}}
    data["data"][key] = value
    with open("database.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    
def get_from_db(key):
    with open("database.json", "r") as json_file:
        data = json.load(json_file)
    return data["data"][key]


def users_kaktus_db(key):
    try:
        with open("database.json", "r") as json_file:
            data = json.load(json_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        data = {"data": {}, "kaktus": {}}
    msg = ""
    if key in data["kaktus"]:
        del data["kaktus"][key]
        msg = "Успешно удаленны из рассылки"
    else:
        data["kaktus"][key] = "true"
        msg = "Успешно добавлены в рассылку"
    with open("database.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
        
    return msg
