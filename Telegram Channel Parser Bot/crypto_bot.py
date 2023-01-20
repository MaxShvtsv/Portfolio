import telebot

import requests
import config_bot

url = 'https://api.binance.com/api/v3/ticker/price?symbol='

bot = telebot.TeleBot(config_bot.TOKEN)

print('Start')

@bot.message_handler(content_types=['text'])
def send_quote(message):
    if len(message.text.split()) == 1:
        count = 1
        quote = message.text
    else:
        count = message.text.split()[0]
        quote = message.text.split()[1]
    data = requests.get(url + quote.upper() + 'USDT')
    data = data.json()
    try:
        bot.send_message(message.chat.id, f"{count} {quote} = {round(float(count) * float(data['price']), 4)} $")
    except:
        bot.send_message(message.chat.id, 'Error')

bot.polling(none_stop=True)

print('End')