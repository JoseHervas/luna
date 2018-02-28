# -*- coding: utf-8 -*-
import json
from chatterbot.conversation import Statement
botParams = json.load(open('config/bot.json'))

def skip_name(bot, message):
	wordList = message.replace('.',' ').replace(',', ' ').split(' ')
	if (botParams['name'] in wordList):
		wordList.remove(botName)
		str1 = ' '.join(wordList)
		output = Statement(text=str1)
	else:
		output = message
	return output