# Japanese Learning Bot
import discord
import os
import random
import time
import io
from keep_alive import keep_alive
from discord.ext.commands import Bot
from random import shuffle
from kana_lists import katakana_list
from kana_lists import hiragana_list
from kana_lists import en_katakana_list
from kanji_lists import kanji_list_level_one

TOKEN = TOKEN HERE AS STRING
BOT_PREFIX = '!J'

client = Bot(command_prefix=BOT_PREFIX)  # discord.Client()

client.mistakes = 0  # Number of mistakes the user makes
client.kana_selection = '0'  # Stores the kana used for the question
client.choice = -1  # Keeps track of whether hiragana or english input is being taken
client.katakana_order = False  # Makes it so if someone types 0 or 1 it doesn't automatically start a katakana quiz
client.test_taker = client.user  # So the bot only takes responses from one person
client.kamoshirenai = False  # used to see if the message is at least contained within a list
client.chart = False  # To check if a chart will be uploaded
client.first_run = True  # To check if it's the first run of a quiz
completed_list = []
client.list_length = len(katakana_list) - 1  # To store the length of the kana list
client.kanji_one_list_length = len(kanji_list_level_one) - 1  # To store the length of the first kanji list


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=BOT_PREFIX + 'commands', type=0))


@client.event
async def on_message(message):
    compare_num = int  # for comparing answers between lists
    global completed_list

    if message.author == client.user:  # so the bot does not reply to itself
        return

    if client.katakana_order and message.author == client.test_taker:
        if message.content == '0':
            client.choice = 0
            msg = '`Initializing カタカナ quiz with English Input,` {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)
            msg = ''.join('`Type ' + BOT_PREFIX + 'reset to reset me. If I get stuck reset me.`\n'
                                                  '`Type ' + BOT_PREFIX + 'chart to see a chart of kana (fu = hu)`\n'
                                                                          '`Type in the English pronunciation of the Katakana below`\n'
                                                                          '`----------------------------------------------------------`')
            await client.send_message(message.channel, msg)
            client.kana_selection = katakana_list[random.randint(0, client.list_length)]
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
        if message.content == '1':
            client.choice = 1
            msg = '`Initializing カタカナ quiz with ひらがな Input,` {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)
            msg = ''.join('`Type ' + BOT_PREFIX + 'reset to reset me. If I get stuck reset me.`\n'
                                                  '`Type ' + BOT_PREFIX + 'chart to see a chart of kana (fu = hu)`\n'
                                                                          '`Type in the Hiragana equivalent of the Katakana below`\n'
                                                                          '`----------------------------------------------------------`')
            await client.send_message(message.channel, msg)
            client.kana_selection = katakana_list[random.randint(0, client.list_length)]
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
        client.katakana_order = False

    # Checks to see if the message contains a right or wrong answer to a quiz question
    # Can only come from the person who initialized the quiz
    if message.author == client.test_taker and message.content.count(BOT_PREFIX) < 1 and client.chart is False:
        if client.choice == 0 or client.choice == 2:
            for x in range(0, client.list_length):
                if message.content in en_katakana_list[x]:
                    client.kamoshirenai = True
        if client.choice == 1:
            for x in range(0, client.list_length):
                if message.content in hiragana_list[x]:
                    client.kamoshirenai = True
        if client.kamoshirenai is False and client.first_run is False:
            msg = 'Answer not accepted, try again'.format(message)
            await client.send_message(message.channel, msg)
            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)
            return

    if message.content.startswith(BOT_PREFIX):
        client.test_taker = message.author
        message.content = message.content.lower()
        if client.choice < 0:
            if message.content.count('katakana') == 1:
                msg = ''.join('`Hiragana or English input?\n'
                              '0) English\n'
                              '1) Hiragana`')
                await client.send_message(message.channel, msg)
                client.katakana_order = True
            if message.content.count('hiragana') == 1:
                client.choice = 2
                msg = 'Initializing ひらがな quiz, {0.author.mention}'.format(message)
                await client.send_message(message.channel, msg)
                msg = ''.join('`Type' + BOT_PREFIX + 'reset to reset me. If I get stuck reset me.`\n'
                                                     '`Type ' + BOT_PREFIX + 'chart to see a chart of kana`\n'
                                                                             '`Type in the English pronunciation of the Hiragana below`\n'
                                                                             '`----------------------------------------------------------`')
                await client.send_message(message.channel, msg)
                client.kana_selection = hiragana_list[random.randint(0, client.list_length)]
                msg = '`' + client.kana_selection + '`'.format(message)
                await client.send_message(message.channel, msg)
        if message.content.count('commands') == 1:
            msg = ''.join('`!Jkatakana - Initiates a quiz on Katakana\n!Jhiragana - Initiates a quiz on Hirgana\n'
                          '!Jchart - Uploads a chart of Katakana or Hiragana\n!Jkanji - A random Kanji appears\n'
                          '!Jop - Listen to my OP\n!Jreset - Resets me if a quiz is in progress`').format(message)
            await client.send_message(message.channel, msg)
        if message.content.count('chart') == 1:
            msg = ''.join('`Hiragana or Katakana Chart?\n'
                          '0) Hiragana\n'
                          '1) Katakana`')
            await client.send_message(message.channel, msg)
            client.chart = True
        if message.content.count('kanji') == 1:
            kanji_info_list_level_one = open('kanji_info_one.txt', 'r+', encoding='utf_8')
            all_kanji_info_one_lines = kanji_info_list_level_one.readlines()

            compare_num = random.randint(0, client.kanji_one_list_length)
            kanji_info_str_one = all_kanji_info_one_lines[compare_num * 3]
            kanji_info_str_two = all_kanji_info_one_lines[(compare_num * 3) + 1]
            kanji_info_str_three = all_kanji_info_one_lines[(compare_num * 3) + 2]
            msg = ''.join(kanji_list_level_one[
                              compare_num] + '\n' + kanji_info_str_one + kanji_info_str_two + kanji_info_str_three).format(
                message)
            await client.send_message(message.channel, msg)

            kanji_info_list_level_one.close()
        if message.content.count('op') == 1:
            msg = '`Here is a link to my OP:` https://www.youtube.com/watch?v=GRhg6P1xq4I'
            await client.send_message(message.channel, msg)
        if message.content.count('reset') == 1:
            msg = '`Resetting`'
            await client.send_message(message.channel, msg)
            client.test_taker = client.user
            client.katakana_order = False
            client.mistakes = 0
            client.kana_selection = '0'
            client.choice = -1
            client.first_run = True
            completed_list = []
            client.kamoshirenai = False

    if client.chart is True:
        if message.content == '0':
            msg = '(hu = fu)\nhttps://www.jpdrills.com/img/hiragana.jpg'
            await client.send_message(message.channel, msg)
            client.chart = False
        if message.content == '1':
            msg = '(hu = fu)\nhttps://www.jpdrills.com/img/katagana.jpg'
            await client.send_message(message.channel, msg)
            client.chart = False

    if client.kamoshirenai is True and message.author == client.test_taker and message.content.find(BOT_PREFIX) < 1:
        # To make the content count case insensitive
        message.content = message.content.lower()

        if client.choice == 0:
            if len(completed_list) == client.list_length:
                msg = '`The quiz is now over.`'.format(message)
                await client.send_message(message.channel, msg)

            for x in range(0, client.list_length):
                if client.kana_selection == katakana_list[x]:
                    compare_num = x

            if str(message.content) in en_katakana_list[compare_num] and len(completed_list) < client.list_length + 1:
                completed_list.append(client.kana_selection)
                msg = ':o:`Correct!`'.format(message)
                await client.send_message(message.channel, msg)
            if str(message.content) not in en_katakana_list[compare_num] and client.first_run is False:
                client.mistakes = client.mistakes + 1
                msg = ''.join(':x:`Wrong. The correct answer is "' + en_katakana_list[compare_num] + '"`\n'
                                                                                                     '`A new kana is below: `').format(
                    message)
                await client.send_message(message.channel, msg)
                client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            for x in range(0, len(completed_list)):
                if client.kana_selection == completed_list[x]:
                    client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)

        if client.choice == 1:
            for x in range(0, client.list_length):
                if client.kana_selection == katakana_list[x]:
                    compare_num = x

            if str(message.content) in hiragana_list[compare_num] and len(completed_list) < client.list_length + 1:
                completed_list.append(client.kana_selection)
                msg = ':o:`せいかいだ.`'.format(message)
                await client.send_message(message.channel, msg)
            if str(message.content) not in hiragana_list[compare_num] and client.first_run is False:
                client.mistakes = client.mistakes + 1
                msg = ''.join(':x:`ちがう. せいかいのこたえは「' + hiragana_list[compare_num] + '」.`\n'
                                                                                   '`あらたなカタカナはした：`').format(message)
                await client.send_message(message.channel, msg)
                client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            for x in range(0, len(completed_list)):
                if client.kana_selection == completed_list[x]:
                    client.kana_selection = katakana_list[random.randint(0, client.list_length)]

            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)

        if client.choice == 2:
            for x in range(0, client.list_length):
                if client.kana_selection == hiragana_list[x]:
                    compare_num = x

            if str(message.content) in en_katakana_list[compare_num] and len(completed_list) < client.list_length + 1:
                completed_list.append(client.kana_selection)
                msg = ':o:`Correct!`'.format(message)
                await client.send_message(message.channel, msg)
            if str(message.content) not in en_katakana_list[compare_num] and client.first_run is False:
                client.mistakes = client.mistakes + 1
                msg = ''.join(':x:`Wrong. The correct answer is "' + en_katakana_list[compare_num] + '"`\n'
                                                                                                     '`A new kana is below: `').format(
                    message)
                await client.send_message(message.channel, msg)
                client.kana_selection = hiragana_list[random.randint(0, client.list_length)]

            for x in range(0, len(completed_list)):
                if client.kana_selection == completed_list[x]:
                    client.kana_selection = hiragana_list[random.randint(0, client.list_length)]

            msg = '`' + client.kana_selection + '`'.format(message)
            await client.send_message(message.channel, msg)

        client.first_run = False
        if len(completed_list) == client.list_length:
            if client.choice == 1:
                msg = '`クイズがおわりだ.`'.format(message)
                await client.send_message(message.channel, msg)
            if client.choice == 2:
                msg = '`The quiz is now over.`'.format(message)
                await client.send_message(message.channel, msg)
            msg = '`Wrong Answers: ' + str(client.mistakes) + '`'.format(message)
            await client.send_message(message.channel, msg)
            client.mistakes = 0
            completed_list = []
            client.kana_selection = '0'
            client.choice = -1
            client.first_run = True


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
