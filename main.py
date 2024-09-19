import telebot
from telebot import types
from extensions import CurrencyConverter, APIException
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: types.Message):
    """Обработчик команды /start и /help."""
    text = 'Привет! Я помогу тебе узнать стоимость валюты.\n\n' \
           'Чтобы узнать курс, отправь мне сообщение в формате:\n\n' \
           '<имя валюты, цену которой ты хочешь узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n\n' \
           'Например: USD RUB 100\n\n' \
           'Для получения списка доступных валют введи команду /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: types.Message):
    """Обработчик команды /values."""
    text = 'Доступные валюты:\n\n' \
           'USD - Доллар США\n' \
           'EUR - Евро\n' \
           'RUB - Российский рубль'
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: types.Message):
    """Обработчик текстовых сообщений."""
    try:
        base, quote, amount = message.text.split()
        amount = float(amount)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат ввода. Попробуйте еще раз.')
        return
    except:
        bot.send_message(message.chat.id, 'Неправильный ввод. Попробуйте еще раз.')
        return
    try:
        total = CurrencyConverter.get_price(base, quote, amount)
        text = f'{amount} {base} = {total} {quote}'
        bot.send_message(message.chat.id, text)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

bot.polling(none_stop=True)
