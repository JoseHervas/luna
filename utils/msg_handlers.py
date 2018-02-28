# -*- coding: utf-8 -*-
import json
botParams = json.load(open('config/bot.json'))
userParams = json.load(open('config/user.json'))
from chatterbot.conversation import Statement
from chatterbot.comparisons import LevenshteinDistance, SynsetDistance, JaccardSimilarity

def search_commands(message, commandList):
	for commandName in commandList:
		for commandString in commandList[commandName]['Sentences']:
			Levenshtein = LevenshteinDistance.compare('self', Statement(text=commandString), Statement(text=message.text))
			#Synset = SynsetDistance(commandString, message.text)
			#Jaccard = JaccardSimilarity(commandString, message.text)
			if (Levenshtein > float(botParams['min_confidence_rate'])):
				return commandName
	return False

def learn_new_response(bot, message, telegramClient, CONVERSATION_ID):
	chat_id = message.chat.id
	botParams = json.load(open('config/bot.json'))
	input_statement = botParams['last_mssg']
	bot.learn_response(Statement(text=message.text), Statement(text=input_statement))
	bot.storage.add_to_conversation(CONVERSATION_ID, Statement(text=input_statement), Statement(text=message.text))
	response = 'Gracias! Para la próxima ya lo sabré.'
	botParams['learn_mode'] = False
	with open('config/bot.json', mode='w') as f:
	        f.write(json.dumps(botParams, indent=2))
	telegramClient.send_message(chat_id, response)
	return


def generic_text_message(bot, message, telegramClient):
	chat_id = message.chat.id
	response = bot.get_response(message.text)
	if (float(response.confidence) < float(botParams['min_confidence_rate'])):
		response1 = 'No he entendido lo que quieres decir. ¿Cuál sería una respuesta adecuada para "' + message.text + '"?' 
		botParams['learn_mode'] = True
		botParams['last_mssg'] = message.text
		with open('config/bot.json', mode='w') as f:
		        f.write(json.dumps(botParams, indent=2))
		telegramClient.send_message(chat_id, response1)
		return
	telegramClient.send_message(chat_id, response)
	return 
