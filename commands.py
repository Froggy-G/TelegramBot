import random
import translators as ts
import requests
import settings
import json

# module "number"
def random_number():
    return 'Ваше число: '+ str(random.randint(0, 100))

# module "coin"
def random_coin():
    number = round(random.randint(0, 100))
    if number > 50:
        return 'Орёл'
    elif number < 50:
        return 'Решка'
    else:
        return 'Встала ребром'

# module "weather"
def open_weather_map_servis(city_name):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    query = {
        'q': city_name,
        'appID': settings.weather_api_token # weather_api_token
    }

    weather_data = requests.get(base_url, params = query).json()
    if weather_data['cod'] == '404':
        return 'Город не найден'
    else:
        now_weather = {
            'name': weather_data['name'],
            'main': weather_data['weather'][0]['description'],
            'temp': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'visibility': weather_data['visibility'],
            'wind': weather_data['wind']['speed']
        }

        result_weather = (f"Погода для города: {now_weather['name']}\n"
                    f"\n🌆На улице сейчас: {translate_text_into_russain(now_weather['main'].title())}" 
                    f"\n🌡Температура: {round(now_weather['temp'] - 273)}℃"
                    f"\n💧Влажность: {now_weather['humidity']}%"
                    f"\n🌫Давление: {round(now_weather['pressure'] / 1.3)}мм.рт.стлб"
                    f"\n🕴Видимость: {(now_weather['visibility']/ 1000)}км" 
                    f"\n🌬Скорость ветра: {now_weather['wind']}м/с")
        return result_weather

# module "translate"
ts._google.language_map={'en':['ru'],'ru':['en']}

def translate_text_into_russain(some_text):
    return ts.translate_html(some_text, translator = ts.google, to_language = 'ru', translator_params = {})
def translate_text_into_english(some_text):
    return ts.translate_html(some_text, translator = ts.google, to_language = 'en', translator_params = {})

# module "exchange rates"
def get_exchange_rates(): 
    try:
        exchange_rates_url = "https://www.cbr-xml-daily.ru/daily_json.js"

        def is_value_rising(diff):
            return True if diff > 0 else False

        response = requests.get(exchange_rates_url)
        data = json.loads(response.text)

        usd_diff = data['Valute']['USD']['Value'] - data['Valute']['USD']['Previous']
        eur_diff = data['Valute']['EUR']['Value'] - data['Valute']['EUR']['Previous']

        usd_rising = "📈" if is_value_rising(usd_diff) else "📉"
        eur_raising = "📈" if is_value_rising(eur_diff) else "📉"

        result = (f"Курсы валют на {data['Timestamp'][0:-15].replace('-', '/')}:\n"
                  f"\n1 Dollar 🇺🇸 = {str(round(data['Valute']['USD']['Value'], 2))} 🇷🇺 Rub's {usd_rising} {round(usd_diff, 2)}"
                  f"\n1 Euro 🇪🇺 = {str(round(data['Valute']['EUR']['Value'], 2))} 🇷🇺 Rub's {eur_raising} {round(eur_diff, 2)}")
        return result
    except json.decoder.JSONDecodeError:
        return "JSON Parsing error"