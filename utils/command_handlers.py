# -*- coding: utf-8 -*-
import json
botParams = json.load(open('config/bot.json'))
userParams = json.load(open('config/user.json'))

def schedule_task(command, mssg, telegramClient, chat_id, type):
	import re, time, datetime, random, json
	from threading import Timer

	# Exact date now
	now = time.strftime('%D/%H/%M/%S')

	# This will split and format today's date
	now_splitted = now.split("/")
	now_formatted = datetime.datetime(int('20'+now_splitted[2]), #Year
									  int(now_splitted[0]), #Month
									  int(now_splitted[1]), #Day
									  int(now_splitted[3]), #Hours
									  int(now_splitted[4]), #Minutes
									  int(now_splitted[5])) #seconds

	# Now we'll search for the DD:DD regex on our message (the hour to wake up)
	hour_wake_up = re.search(r'\d{2}:\d{2}', mssg.text)
	# Add the seconds
	time_at_wake_up = hour_wake_up.group() + ':00'

	#Split and format the wake up date. By default it will be tomorrow at the specified time
	time_at_wake_up_splitted = time_at_wake_up.split(":")
	date_wakeup = datetime.datetime(int('20'+now_splitted[2]), #Year
									  int(now_splitted[0]), #Month
									  int(now_splitted[1]), #Day
									  int(time_at_wake_up_splitted[0]), #Hours
									  int(time_at_wake_up_splitted[1]), #Minutes
									  int(time_at_wake_up_splitted[2])) #seconds

	# If it's not already midnight, we'll have to add one day to the wakeup date
	if (now_formatted > date_wakeup):
		date_wakeup = date_wakeup + datetime.timedelta(days=1)

	# Lets calculate how many seconds to put on the countdown
	num_seconds_wait = (date_wakeup-now_formatted).total_seconds()

	wake_up_menssages = json.load(open('utils/commands.json'))['Despertar']['Mensajes']
	remember_messaes = json.load(open('utils/commands.json'))['Recordatorio']['Mensajes']

	if(type == 'remember'):
		fName = 'exports/user_data/temp/recordatorio_'+ time_at_wake_up_splitted[0] + '_' + time_at_wake_up_splitted[1] + '.txt'
		with open(fName, 'w') as file:
			file.write(mssg.text)

	def send_scheduled_message():
		if (type == 'wake_up'):
			response = random.choice(wake_up_menssages)
		elif (type == 'remember'): 
			with open(fName, 'r') as file1:
				recordatorio_ = file1.read()
			response = random.choice(remember_messaes)
			response = response + '\n' + recordatorio_
		telegramClient.send_message(chat_id, response)

	Timer(num_seconds_wait, send_scheduled_message).start()

def learn_new_association(command, mssg, telegramClient, chat_id):
	return
#	activate_response = json.load(open('utils/commands.json'))['Aprendizaje']['Responses']
#	learned_response = json.load(open('utils/commands.json'))['Aprendizaje']['Mensajes']
#	telegramClient.send_message(chat_id, activate_response)
#	fName = 'exports/learning/temp/input.txt'
#	with open(fName, 'w') as file:
#		file.write(mssg.text)

def change_conf_rate(mssg, telegramClient, chat_id):
	import random, re
	new_conf_rate = re.search(r'\d{1}.\d{2}', mssg.text)
	botParams['min_confidence_rate'] = new_conf_rate.group()
	with open('config/bot.json', mode='w') as f:
	        f.write(json.dumps(botParams, indent=2))
	return

def change_entry(bot, CONVERSATION_ID):
	last_mssg = bot.storage.get_latest_response(CONVERSATION_ID)
	bot.storage.remove(last_mssg.text)

def add_task(mssg):
	import re
	task = re.search(r": (.*)", mssg.text)
	with open('exports/user_data/taskList.txt', mode='a+') as f:
		f.write('\n- '+task.groups()[0])

def show_tasks(mssg, telegramClient, chat_id):
	with open('exports/user_data/taskList.txt', mode='r') as f:
		tasks = f.read()
	response = tasks
	telegramClient.send_message(chat_id, response)

def delete_task(mssg, telegramClient, chat_id):
	import random, re
	task = re.search(r": (.*)", mssg.text)
	task_text = '- ' + task.groups()[0]
	with open('exports/user_data/taskList.txt', mode='r+') as f:
		initialTaskList = f.read()
		taskList = initialTaskList.replace(task_text, '')
		f.seek(0)
		f.write(taskList)
		f.truncate()
	show_tasks(mssg, telegramClient, chat_id)

def handle_command(command, mssg, telegramClient, chat_id, conversation_id, bot):
	if (command == 'Despertar'):
		schedule_task(command, mssg, telegramClient, chat_id, 'wake_up')
	if (command == 'Recordatorio'):
		schedule_task(command, mssg, telegramClient, chat_id, 'remember')
	if (command == 'Aprendizaje'):
		learn_new_association(command, mssg, telegramClient, chat_id)
	if (command == 'Ajustar conf rate'):
		change_conf_rate(mssg, telegramClient, chat_id)
	if (command == 'Corregir entrada'):
		change_entry(bot, conversation_id)
	if (command == 'Add to tasks'):
		add_task(mssg)
	if (command == 'Listar tareas'):
		show_tasks(mssg, telegramClient, chat_id)
	if (command == 'Eliminar tarea'):
		delete_task(mssg, telegramClient, chat_id)
