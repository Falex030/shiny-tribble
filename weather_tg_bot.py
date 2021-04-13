from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
from config import telegram_token, token
import requests
import datetime

API_TOKEN = telegram_token
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды!')

@dp.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    lang = 'ru'
    try:
        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric&lang={lang}')
        data = r.json()
        #pprint(data)

        city = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_max = data ['main']['temp_max']
        temp_min = data['main']['temp_min']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        wind = data['wind']['speed']
        clouds = data['clouds']['all']

        weather = data['weather'][0]['main']
        if weather in code_to_smile:
            w = code_to_smile[weather]
        else:
            w = " Я хз шо там, глянь сам в окно"



        await message.reply(f"****** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ******\n"
              f'Погода в городе {city}\n'
              f'Температура {round(temp,1)}C° {w}\nОщущается на {round(feels_like,1)}C°\n'
              #f'Минимальная температура {round(temp_min,1)}C°, максимальная {round(temp_max,1)}C°\n'
              f'Солнце встает в {sunrise}, и заходит в {sunset}, светловой день {length_of_day}\n'
              f'Скорость ветра {round(wind,1)} км/ч\n'
              f'Облачность {clouds} %\n'
              f'*** Хорошего дня! ***'
              )
    except:
       await message.reply('Проверте название города')

if __name__ == '__main__':
    executor.start_polling(dp)
