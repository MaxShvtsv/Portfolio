from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel
import pandas as pd
import requests
import asyncio
import random
import cfg
import os

CWD = os.path.dirname(os.path.realpath(__file__))

# Credentials
API_ID = cfg.API_ID
API_HASH = cfg.API_HASH
PHONE = cfg.PHONE
PASSWORD = cfg.PASSWORD
SESSION_NAME = cfg.SESSION_NAME

# Paraphraser
PARAPHRASER_URL = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"

PARAPHRASER_PARAMS = {
	"language": "ru",
	"strength": 3,
	"text": ''
}
PARAPHRASER_HEADERS = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "db704fc17fmsh4356da80eac91cep199c93jsnf14adb4eeefd",
	"X-RapidAPI-Host": "rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com"
}

INSPIREEDGE_MAIN_ID = 1963469667
INSPIREEDGE_DRAFT_ID = 1999290301

# Connecting client
client = TelegramClient(PHONE, API_ID, API_HASH)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(PHONE)
    try:
        client.sign_in(PHONE, input('Enter the code: '))
    except SessionPasswordNeededError as err:
        client.sign_in(password=PASSWORD)

client.start()

INSPIREEDGE_MAIN_ENTITY = client.get_entity(PeerChannel(INSPIREEDGE_MAIN_ID))
INSPIREEDGE_DRAFT_ENTITY = client.get_entity(PeerChannel(INSPIREEDGE_DRAFT_ID))

FILTER_POST_WORDS = ['Way of Millionaire✅️']

print('Start\n----------------')

def filter_post(text):
    for filter_words in FILTER_POST_WORDS:
        text = text.replace(filter_words, '')

    return text

@client.on(events.NewMessage(pattern='!get '))
async def get_posts(event):
    posts_count = 0
    try:
        posts_count = int(event.message.message.split(' ')[1])
    except:
        await client.send_message(INSPIREEDGE_DRAFT_ENTITY, message='Введено хибну кількість')
    
    if posts_count > 10:
        await client.send_message(INSPIREEDGE_DRAFT_ENTITY, message='Кількість має бути не більша за 10')
        return

    channel_list = pd.read_csv(os.path.join(CWD, 'channel_list.csv'))['channel_id'].to_list()

    for i in range(posts_count):
        current_channel_id = random.choice(channel_list)
        current_channel_entity = await client.get_entity(PeerChannel(current_channel_id))
        channel_username = current_channel_entity.username

        posts = await client.get_messages(current_channel_entity, 100)

        post_to_draft = random.choice(posts)
    
        current_post = filter_post(post_to_draft.message)

        await client.send_message(
            INSPIREEDGE_DRAFT_ENTITY,
            message=current_post + f'\nhttps://t.me/{channel_username}/{post_to_draft.id}',
            link_preview=False
        )

@client.on(events.NewMessage(pattern='!rewrite'))
async def rewrite_posts(event):
    reply_to_id = event.message.reply_to.reply_to_msg_id
    reply_to_message = await client.get_messages(INSPIREEDGE_DRAFT_ENTITY, ids=reply_to_id)
    reply_to_message_text = reply_to_message.message

    PARAPHRASER_PARAMS['text'] = reply_to_message_text
    response = requests.post(PARAPHRASER_URL, json=PARAPHRASER_PARAMS, headers=PARAPHRASER_HEADERS).json()['rewrite']

    await client.send_message(
        INSPIREEDGE_DRAFT_ENTITY,
        message=response,
        link_preview=False
    )

@client.on(events.NewMessage(pattern='!add '))
async def add_channel_to_list(event):
    channel_username = \
        event.message.message.split(' ')[1].split('t.me/')[1]
    
    current_channel_id = 0
    try:
        current_channel_entity = await client.get_input_entity(channel_username)
        current_channel_id = current_channel_entity.channel_id

        await client(JoinChannelRequest(channel=current_channel_id))

    except:
        await client.send_message(INSPIREEDGE_DRAFT_ENTITY, message='Неправильный канал')

    channel_list_df = pd.read_csv(os.path.join(CWD, 'channel_list.csv'))

    if current_channel_id in channel_list_df['channel_id'].to_list():
        await client.send_message(INSPIREEDGE_DRAFT_ENTITY, message='Уже отслеживается')
        return

    channel_list_df = pd.concat([channel_list_df, pd.DataFrame({'channel_id':[current_channel_id]})], ignore_index=True)

    channel_list_df.to_csv(os.path.join(CWD, 'channel_list.csv'), index=None)

@client.on(events.NewMessage(pattern='!list'))
async def channel_list(event):
    channel_list = pd.read_csv(os.path.join(CWD, 'channel_list.csv'))['channel_id'].to_list()

    text = ''

    for i in range(len(channel_list)):
        current_channel_entity = await client.get_entity(PeerChannel(channel_list[i]))
        text += f'{i + 1}. https://t.me/{current_channel_entity.username}\n'

    await client.send_message(
        INSPIREEDGE_DRAFT_ENTITY,
        message=text,
        link_preview=False
    )

client.run_until_disconnected()
print('----------------\nEnd')