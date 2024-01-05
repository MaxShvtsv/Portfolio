import telebot
import requests
import os
import json

import config_crypto_bot

CWD = os.path.dirname(os.path.realpath(__file__))

SERVER_SLASH = '/'
LOCALHOST_SLASH = '\\'
CURRENT_SLASH = SERVER_SLASH

URL_COIN = 'https://api.coingecko.com/api/v3/coins/'

CHAT_IDS_WHITELIST = config_crypto_bot.CHAT_IDS_WHITELIST

QUERY_CHAR = '.'

bot = telebot.TeleBot(config_crypto_bot.TOKEN)

print('Start')

@bot.message_handler(content_types=['text'])
def send_quote(message):
    if message.chat.id not in CHAT_IDS_WHITELIST.values():
        bot.send_message(message.chat.id, 'Access is blocked')
        return

    if message.text[0] == QUERY_CHAR:
        '''
        Template:
        {QUERY_CHAR}btc
        {QUERY_CHAR}0.5 btc
        '''

        message_splitted = message.text.split()

        if len(message_splitted) > 2:
            # Theare can be only 1 or 2 words in message
            return

        count = 1
        if len(message_splitted) == 1:
            # Get cryptocurrency symbol
            symbol = message_splitted[0][1:].lower()
        else:
            # Managing cryptocurrency count
            try:
                count = float(message_splitted[0][1:])
                if int(count) == count:
                    count = int(count)
            except:
                return
            symbol = message_splitted[1].lower()

        data_list = ''

        with open(CWD + f'{CURRENT_SLASH}coin_list.json', encoding='utf-8') as coin_list:
            # List of coins, their IDs, symbols from CoinGecko
            data_list = json.load(coin_list)

        token_ids = []

        for i in data_list:
            # Add all cryptocurrencies with given name without "wormhole" in name.
            if i['symbol'] == symbol and 'wormhole' not in i['id']:
                token_ids.append(i['id'])

        if len(token_ids) == 0:
            return

        text = ''

        for i in token_ids:
            # Parse tokens' prices
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }
            response_token = requests.get(URL_COIN + f'{i}', params=params)
            data = response_token.json()

            try:
                cat = data['categories']
            except:
                bot.send_message(message.chat.id, 'Зачекай трохи')
                return

            cat = data['categories']
            market_data = data['market_data']
            current_price = market_data['current_price']
            current_price_usd = current_price['usd']
            current_price_uah = current_price['uah']
            price_change_percentage_24h = market_data['price_change_percentage_24h']
            price_change_percentage_7d = market_data['price_change_percentage_7d']

            try:
                price_24h_ago = current_price_usd + -1 * current_price_usd * price_change_percentage_24h / 100
            except:
                price_24h_ago = current_price_usd
                price_change_percentage_24h = '-'

            try:
                price_7d_ago = current_price_usd + -1 * current_price_usd * price_change_percentage_7d / 100
            except:
                price_7d_ago = current_price_usd
                price_change_percentage_7d = '-'

            percent_round_number = 2
            price_round_number = 3
            temp_price = current_price_usd

            while temp_price < 0.1:
                temp_price *= 10
                price_round_number += 1

            if current_price_usd >= 1:
                price_round_number -= 1

            try:
                multiplied_usd = round(count * current_price_usd, price_round_number)
            except:
                multiplied_usd = '-'

            try:
                multiplied_uah = round(count * current_price_uah, price_round_number)
            except:
                multiplied_uah = '-'

            try:
                price_24h_ago = round(price_24h_ago, price_round_number)
            except:
                price_24h_ago = '-'

            try:
                price_7d_ago = round(price_7d_ago, price_round_number)
            except:
                price_7d_ago = '-'

            try:
                price_change_percentage_24h = round(price_change_percentage_24h, percent_round_number)
            except:
                price_change_percentage_24h = '-'

            try:
                price_change_percentage_7d = round(price_change_percentage_7d, percent_round_number)
            except:
                price_change_percentage_7d = '-'

            symbol = symbol.upper()
            is_multiply = True if count == 1 else False
            multiply_text = ''

            if not is_multiply:
                multiply_text = f'{count} {symbol} = `{multiplied_usd:.{price_round_number}f} USD`\n' \
                                f'{count} {symbol} = `{multiplied_uah:.{price_round_number}f} UAH`\n'

            current_text = f'*{symbol}* ({i})\n' \
                    f'{symbol} = `{current_price_usd:.{price_round_number}f} USD`\n' \
                    f'{symbol} = `{current_price_uah:.{price_round_number}f} UAH`\n' \
                    f'{multiply_text}' \
                    f'Добу тому: `{price_24h_ago:.{price_round_number}f}$` | `{price_change_percentage_24h}%`\n' \
                    f'Неділю тому: `{price_7d_ago:.{price_round_number}f}$` | `{price_change_percentage_7d}%`\n' \
                    f'Характеристика: {", ".join(cat)}\n' \

            text = text + '\n' + current_text

        bot.send_message(message.chat.id, text, parse_mode='Markdown')

bot.polling(none_stop=True)

print('End')