# -*- coding: utf-8 -*-

# Config. Params
import json, os
botParams = json.load(open('config/bot.json'))
userParams = json.load(open('config/user.json'))
logsParams = json.load(open('config/logging.json'))
apiParams = json.load(open('config/apis.json'))
available_commands = json.load(open('utils/commands.json'))
wd = os.path.dirname(os.path.realpath(__file__))
exports = wd + '/exports'
utils = wd + '/utils'

# Logging
import logging, logging.config
logging.config.dictConfig(logsParams)

# Main chatbot UI
from chatterbot import ChatBot
from utils import training, msg_handlers, custom_preprocessors
import telebot
telegram = telebot.TeleBot(apiParams['Telegram']['API-key'])


# Create a new instance of a ChatBot
bot = ChatBot(
    botParams['name'],
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="../database.db",
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        }
    ]
)

# Initial training
if (botParams['initial_training']):
    training.train_bot(bot, exports)

# Start a new conversation
CONVERSATION_ID = bot.storage.create_conversation()

print("Type something to start...")

# This will determine the response function to which derive the message
def handle_message(message):
    mssg = message[0]
    chat_id = mssg.chat.id
    username = mssg.chat.username
    if (username == userParams['username']):
        command = msg_handlers.search_commands(mssg, available_commands)
        if (command):
            import random
            from utils import command_handlers
            command_handlers.handle_command(command, mssg, telegram, chat_id, CONVERSATION_ID, bot)
            response = random.choice(available_commands[command]['Responses'])
            telegram.send_message(chat_id, response)
            return
        botParams = json.load(open('config/bot.json'))
        learn_mode_on = botParams['learn_mode']
        if (learn_mode_on):
            msg_handlers.learn_new_response(bot, mssg, telegram, CONVERSATION_ID)
        else:
            msg_handlers.generic_text_message(bot, mssg, telegram)
    else:
        response = 'Lo siento, no estoy autorizada para responder a tus mensajes.'
        telegram.send_message(chat_id, response)

# This will attach the handle_message fuction to every message sent by Telegram
telegram.set_update_listener(handle_message)

while True:
    try:
        telegram.polling(none_stop=True)
    except:
        telegram.polling(none_stop=True)