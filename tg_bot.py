import telebot
import settings
import commands

# this code for work with bot
tb = telebot.TeleBot(settings.telegram_token) # telegram_api_token

# bots keyboard
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Погода', 'Погода по координатам', 'Перевод')
keyboard.row('Монетка', 'Рандом')
keyboard.row('Курс', 'Помощь')

# 2nd branches of messages
def translate_message_step_2(message):
    tb.send_message(message.chat.id, 'Перевод: "' + commands.translate_text_into_russain(message.text) + '"')

def weather_message_step_2(message):
    tb.send_message(message.chat.id, commands.open_weather_map_service(commands.translate_text_into_english(message.text)))

def weather_coordinates_message_step_2(message):
    if message.text is not None:
        tb.send_message(message.chat.id, 'Я просил геопозицию, а не текст')
    else:
        lon = message.location.longitude
        lat = message.location.latitude
        tb.send_message(message.chat.id, commands.open_weather_map_service_coordinates(lat, lon))

# how to add new comand: ['command', 'function ', 'next step function'] 
# P.S if something is missing, leave the field '' is empty 
all_commands_tg_bot = [
    ['/start', 'Привет, я простенький бот созданный для обучения, выбери функцию из списка.', ''],
    ['Помощь', 'Список возможностей бота:\n \
    1. Погода: показывает погоду на улице.\n \
    2. Погода по координатам: отправьте боту свою геопозицию для получения погодных данных.\n \
    3. Рандом: выдает случайное число от 0 до 100.\n \
    4. Монетка: подбросить монетку.\n \
    5. Перевод: переводит текст который вы прислали на русский язык (работает с 70+ языками мира)\n \
    6. Курс: показывает текущий курс Доллара и Евро к Рублю', ''],
    ['Погода', 'Напишите название вашего города.', weather_message_step_2],
    ['Погода по координатам', 'Отправьте свою геопозицию', weather_coordinates_message_step_2],
    ['Рандом', commands.random_number, ''],
    ['Монетка', commands.random_coin, ''],
    ['Курс', commands.get_exchange_rates, ''],
    ['Перевод', 'Какой текст будем переводить?', translate_message_step_2]
]
# message sandler
@tb.message_handler()
def main(message):
    for cmds in all_commands_tg_bot:
        if cmds[0] == message.text:
            if isinstance(cmds[1], str):
                tb.send_message(message.chat.id, cmds[1], reply_markup = keyboard)
                if cmds[2] != '':
                    tb.register_next_step_handler(message, cmds[2])
            else:
                tb.send_message(message.chat.id, cmds[1](), reply_markup = keyboard)

print('Пажилой Кавбой готов к работе.')
tb.polling(none_stop = True, interval = 0)