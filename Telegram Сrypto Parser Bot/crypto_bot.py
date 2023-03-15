import os
import requests
from zipfile import ZipFile
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import telebot

import config_bot

plt.switch_backend('agg')

URL_PRICE = 'https://api.binance.com/api/v3/ticker/price'
URL_HISTORIC_PRICE = 'https://data.binance.vision/?prefix=data/spot/daily/klines/'
STABLECOIN = 'USDT'
TIMEFRAMES = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d']
COLUMNS = ['Open time', 'Open', 'High',
        'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume',
        'Number of trades', 'Taker buy base asset volume',
        'Taker buy quote asset volume', 'Ignore']
CWD = os.path.dirname(os.path.realpath(__file__))

global current_timeframe
current_timeframe = ''

bot = telebot.TeleBot(config_bot.TOKEN)

print('Start')

def gen_markup_timeframes():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 3
    for i in TIMEFRAMES:
        markup.add(telebot.types.InlineKeyboardButton(i.upper(), callback_data=i))
    return markup 

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    current_timeframe = call.data

@bot.message_handler(commands=['chart'])
def show_chart(message):
    
    input_data = message.text.split()
    if len(input_data) != 3:
        bot.send_message(message.chat.id, 'Error. Wrong input.')
        return

    command, quote, timeframe = input_data
    quote = quote.upper()
    timeframe = timeframe.lower()

    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day - 1
    current_year = datetime.datetime.now().year

    current_month = f'0{current_month}' if current_month < 10 else str(current_month)
    current_day = f'0{current_day}' if current_day < 10 else str(current_day)

    date = f'{current_year}-{current_month}-{current_day}'

    url = f'https://data.binance.vision/data/spot/daily/klines/{quote + STABLECOIN}/{timeframe}/{quote}USDT-{timeframe}-{date}.zip'

    response = requests.get(url)
    
    open(CWD + '/data.zip', 'wb').write(response.content)

    with ZipFile(CWD + '/data.zip', 'r') as data_zip:
        data_zip.extractall(path=CWD)

    csv_path = CWD + f'/{quote + STABLECOIN}-{timeframe}-{date}.csv'

    df = pd.read_csv(csv_path, header=None, names=COLUMNS)
    df = df[COLUMNS[1:5]]

    divider = 0
    measure_count = int(timeframe[:-1])
    measure_time = timeframe[-1]
    if measure_time == 'm':
        divider = datetime.timedelta(minutes=measure_count)
    elif measure_time == 'h':
        divider = datetime.timedelta(hours=measure_count)
    elif measure_time == 'd':
        divider = datetime.timedelta(days=measure_count)

    bars_count = int(datetime.timedelta(days=1) / divider)

    timeformat = "%H:%M"
    start = datetime.datetime(1, 1, 1, 0, 0)

    timeframe_range = []
    for i in range(bars_count + 2):
        timeframe_range.append(start.strftime(timeformat))
        start += divider

    x_axis_values = np.arange(0, bars_count)

    fig, axs = plt.subplots(figsize=(10, 5))

    xticks_range = np.arange(-1, bars_count + 1)

    axs.set_xticks(xticks_range)
    axs.set_xticklabels(timeframe_range)

    for i in x_axis_values:
        open_price = df.iloc[i, 0]
        low_price = df.iloc[i, 1]
        high_price = df.iloc[i, 2] 
        close_price = df.iloc[i, 3]
        spread = close_price - open_price
        colour = 'lime' if spread > 0 else 'tomato'

        rect_body = Rectangle((i - 0.4, open_price), 0.8, close_price - open_price,
                            color=colour)

        axs.add_patch(rect_body)
        axs.vlines(i, low_price, high_price, colors=colour, linewidth=1)

    for i, val in enumerate(timeframe_range):
        if val[-2:] != '00':
            axs.xaxis.get_major_ticks()[i].set_visible(False)
    axs.xaxis.get_major_ticks()[-1].set_visible(False)

    plt.xticks(rotation=45)

    axs.set_title(f'{quote + STABLECOIN} | {timeframe} | {date}')

    plt.savefig(CWD + '/chart.png')
    plt.close()

    image = open(CWD + '/chart.png', 'rb')

    bot.send_photo(message.chat.id, image)

    os.remove(CWD + '/data.zip')
    os.remove(CWD + f'/{quote + STABLECOIN}-{timeframe}-{date}.csv')

@bot.message_handler(content_types=['text'])
def send_quote(message):
    if len(message.text.split()) == 1:
        count = 1
        quote = message.text
    else:
        count = message.text.split()[0]
        quote = message.text.split()[1]

    query_params = {'symbol' : quote.upper() + STABLECOIN}
    response = requests.get(URL_PRICE, params=query_params)
    data = response.json()
    try:
        bot.send_message(message.chat.id, f"{count} {quote} = {round(float(count) * float(data['price']), 4)} $")
    except:
        bot.send_message(message.chat.id, 'Error. Cryptocurrenc does not exist.')

bot.polling(none_stop=True)

print('End')