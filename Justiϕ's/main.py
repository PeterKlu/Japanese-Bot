# Japanese Learning Bot
import discord
import os
import random
import time
from keep_alive import keep_alive
from discord.utils import get
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot
from random import shuffle

TOKEN = 'Token'
BOT_PREFIX = '!'

client = Bot(command_prefix=BOT_PREFIX)  # discord.Client()

client.mistakes = 0  # Number of mistakes the user makes
client.kana_selection = '0'  # Stores the kana used for the question
client.choice = -1  # Keeps track of whether hiragana or english input is being taken
client.katakana_order = False  # Makes it so if someone types 0 or 1 it doesn't automatically start a katakana quiz
client.test_taker = client.user  # So the bot only takes responses from one person
client.kamoshiranai = False  # used to see if the message is at least contained within a list

katakana_list = ['ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク', 'ケ', 'コ', 'サ', 'シ', 'ス', 'セ', 'ソ', 'タ', 'チ',
                 'ツ', 'テ', 'ト', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'ヒ', 'フ', 'へ', 'ホ', 'マ', 'ミ', 'ム', 'メ',
                 'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヲ', 'ン']
hiragana_list = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち',
                 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め',
                 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん']
en_katakana_list = ['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko', 'sa', 'shi', 'su', 'se', 'so', 'ta', 'chi',
                    'tsu', 'te', 'to', 'na', 'ni', 'nu', 'ne', 'no', 'ha', 'hi', 'fu', 'he', 'ho', 'ma', 'mi', 'mu',
                    'me', 'mo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wo', 'n']
completed_list = []

client.list_length = len(katakana_list)-1


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="Teaching Japanese"))


@client.event
async def on_message(message):
    compare_num = int  # for comparing answers between lists
    global completed_list

    if message.author == client.user:  # so the bot does not reply to itself
        return

    '''msg = 'client.kamoshiranai: ' + str(client.kamoshiranai)    # Used for debugging
    await client.send_message(message.channel, msg)
    msg = 'client.choice: ' + str(client.choice)
    await client.send_message(message.channel, msg)
    msg = 'client.katakana_order: ' + str(client.katakana_order)
    await client.send_message(message.channel, msg)
    msg = 'client.test_taker: ' + str(client.test_taker)
    await client.send_message(message.channel, msg)'''

    # Checks to see if the message contains a right or wrong answer to a quiz question
    # Can only come from the person who initialized the quiz
    if message.author == client.test_taker and message.content.count(BOT_PREFIX) < 1:
        if client.choice == 0 or client.choice == 2:
            for x in range(0, client.list_length):
                if message.content in en_katakana_list[x]:
                    client.kamoshiranai = True
        if client.choice == 1:
            for x in range(0, client.list_length):
                if message.content in hiragana_list[x]:
                    client.kamoshiranai = True
        if client.kamoshiranai is False:
            msg = 'Answer not accepted, try again'.format(message)
            await client.send_message(message.channel, msg)
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
            return

    if client.katakana_order and message.author == client.test_taker:
        if message.content == '0':
            client.choice = 0
            msg = '`Initializing カタカナ quiz with English Input,` {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)
            msg = '`Type ' + str(BOT_PREFIX) + 'reset to reset me`'.format(message)
            await client.send_message(message.channel, msg)

            client.kana_selection = katakana_list[random.randint(0, client.list_length)]
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
        if message.content == '1':
            client.choice = 1
            msg = '`Initializing カタカナ quiz with ひらがな Input,` {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)
            msg = '`Type ' + str(BOT_PREFIX) + 'reset to reset me`'.format(message)
            await client.send_message(message.channel, msg)

            client.kana_selection = katakana_list[random.randint(0, client.list_length)]
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
        client.katakana_order = False

    if message.content.startswith(BOT_PREFIX) and client.choice < 0:
        client.test_taker = message.author
        message.content = message.content.lower()
        if message.content == (BOT_PREFIX + 'katakana'):
            msg = '''`Hiragana or English input?
    0) English
    1) Hiragana`'''.format(message)
            await client.send_message(message.channel, msg)
            client.katakana_order = True
        if message.content == (BOT_PREFIX + 'hiragana'):
            client.choice = 2
            msg = 'Initializing ひらがな quiz, {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)

            client.kana_selection = hiragana_list[random.randint(0, client.list_length)]
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
    if message.content == (BOT_PREFIX + 'reset'):
        msg = '`Resetting`'
        await client.send_message(message.channel, msg)
        client.test_taker = client.user
        client.katakana_order = False
        client.mistakes = 0
        client.kana_selection = '0'
        client.choice = -1
        completed_list = []
        client.kamoshiranai = False

    if client.kamoshiranai is True and message.author == client.test_taker:
        # To make the content count case insensitive
        message.content = message.content.lower()

        if client.choice == 0:
            if len(completed_list) == client.list_length:
                msg = '`The quiz is now over.`'.format(message)
                await client.send_message(message.channel, msg)
                msg = '`Wrong Answers: ' + str(client.mistakes) + '`'.format(message)
                await client.send_message(message.channel, msg)
                client.mistakes = 0
                completed_list = []
                client.kana_selection = '0'
                client.choice = -1

            for x in range(0, client.list_length):
                if client.kana_selection == katakana_list[x]:
                    compare_num = x

            if str(message.content) in en_katakana_list[compare_num]:
                completed_list.append(client.kana_selection)
                msg = ':o:`Correct!`'.format(message)
                await client.send_message(message.channel, msg)
            if str(message.content) not in en_katakana_list[compare_num]:
                client.mistakes = client.mistakes + 1
                msg = ':x:`Wrong. The correct answer is "' + en_katakana_list[compare_num] + '"`'.format(message)
                await client.send_message(message.channel, msg)
                msg = '`A new kana is below: `'.format(message)
                await client.send_message(message.channel, msg)
                client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            for x in range(0, len(completed_list)):
                if client.kana_selection == completed_list[x]:
                    client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)

        if client.choice == 1:
            if len(completed_list) == client.list_length:
                msg = '`クイズがおわりだ.`'.format(message)
                await client.send_message(message.channel, msg)
                msg = '`Wrong Answers: ' + str(client.mistakes) + '`'.format(message)
                await client.send_message(message.channel, msg)
                client.mistakes = 0
                completed_list = []
                client.kana_selection = '0'
                client.choice = -1

            for x in range(0, client.list_length):
                if client.kana_selection == katakana_list[x]:
                    compare_num = x

            if str(message.content) in hiragana_list[compare_num]:
                completed_list.append(client.kana_selection)
                msg = ':o:`せいかいだ.`'.format(message)
                await client.send_message(message.channel, msg)
            if str(message.content) not in hiragana_list[compare_num]:
                client.mistakes = client.mistakes + 1
                msg = ':x:`ちがう. せいかいのこたえは「' + hiragana_list[compare_num] + '」.`'.format(message)
                await client.send_message(message.channel, msg)
                msg = '`あらたなカタカナはした：`'.format(message)
                await client.send_message(message.channel, msg)
                client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            for x in range(0, len(completed_list)):
                if client.kana_selection == completed_list[x]:
                    client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)

        if client.choice == 2:
            if len(completed_list) == client.list_length:
                msg = '`The quiz is now over.`'.format(message)
                await client.send_message(message.channel, msg)
                msg = '`Wrong Answers: ' + str(client.mistakes) + '`'.format(message)
                await client.send_message(message.channel, msg)
                client.mistakes = 0
                completed_list = []
                client.kana_selection = '0'
                client.choice = -1

            for x in range(0, client.list_length):
                if client.kana_selection == hiragana_list[x]:
                    compare_num = x

            if str(message.content) in en_katakana_list[compare_num]:
                completed_list.append(client.kana_selection)
                msg = ':o:`Correct!`'.format(message)
                await client.send_message(message.channel, msg)
            if str(message.content) not in en_katakana_list[compare_num]:
                client.mistakes = client.mistakes + 1
                msg = ':x:`Wrong. The correct answer is "' + en_katakana_list[compare_num] + '"`'.format(message)
                await client.send_message(message.channel, msg)
                msg = '`A new kana is below: `'.format(message)
                await client.send_message(message.channel, msg)
                client.kana_selection = hiragana_list[random.randint(0, client.list_length)]

            for x in range(0, len(completed_list)):
                if client.kana_selection == completed_list[x]:
                    client.kana_selection = hiragana_list[random.randint(0, client.list_length)]

            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
