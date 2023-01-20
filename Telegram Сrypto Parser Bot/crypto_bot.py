import telebot

import requests
import config_bot

URL_PRICE = 'https://api.binance.com/api/v3/ticker/price'
URL_HISTORIC_PRICE = 'https://data.binance.vision/?prefix=data/spot/daily/klines/'

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

    query_params = {'symbol' : quote.upper() + 'USDT'}
    data = requests.get(URL_PRICE, params=query_params)
    data = data.json()
    try:
        bot.send_message(message.chat.id, f"{count} {quote} = {round(float(count) * float(data['price']), 4)} $")
    except:
        bot.send_message(message.chat.id, 'Error. Cryptocurrenc does not exist.')

bot.polling(none_stop=True)

print('End')