# -*- coding: utf-8 -*-

from chatterbot.trainers import ChatterBotCorpusTrainer
import os

def train_bot(bot, export_path):
	'''
	Trains a bot with the spanish corpus and exports the 
	underlying knowledge of the Bot (once trained) to a
	specific folder.
	'''
	bot.set_trainer(ChatterBotCorpusTrainer)
	bot.train(
	    "chatterbot.corpus.english"
	)
	bot.trainer.export_for_training(export_path+'/underlying_corpus.json')