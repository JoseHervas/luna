
Luna is my personal assistant chatbot.

It's build with <a href="https://github.com/gunthercox/ChatterBot">ChatterBot</a> and with <a href="https://github.com/eternnoir/pyTelegramBotAPI">pyTelegramBotAPI</a> (and, of course, with some good ❤).

#### Features

- Luna has a cool <strong>conversational dialog engine</strong>, which allows her to hold a fluid conversation (the longer the corpus training used for the initial boosting, the better quality of conversations).

- She likes to speak by <strong>Telegram</strong>.

- She learns very quickly. She has a confidence rate, located in the `config\bot.json` which determines in a scale 0-1 how sure she has to be with her answer to actually respond to you. If she can't reach a statement with that level of confidence to your message, she asks you to teach her the appropriate answer, and she adds it to the database.

- She can <strong>auto-regulate her own params</strong>. If you want her to increment the confidence ratio of her answers (and therefore reduce the number of errors), you can tell her to change it, and she edits the file for you.

- Aditionally to the normal conversations, she can also do a set of <strong>custom tasks</strong> for you, like waking you up at a certain time or taking a list of to-do notes. You can add your own custom tasks by writting them on the `utils\commands.json` and `utils\command_handlers.py` files.

#### How to use

- Clone/download the repo and run the `setup.py` file.

- Install the dependencies with `pip install requisites.txt`

- Talk to the <a href="https://telegram.me/BotFather">Bot Father</a> on Telegram and ask him to give you a Telegram API key.

- Write your Telegram API key on the `config\apis.json` file, and also add your telegram username to the `config\user.json` file (Luna will only answer to your messages).

#### Things to improve

- When she learns a new response to a sentence, if you want her to forget that response, you need to edit the SQLite database. It would be nice if she could forget that response by herself, like a custom command.

- More custom commands are on the way (search on google, music/movies recommendation, integration with some APIs like maps, calendar, etc...).

#### License

Of course! MIT License <3

have fun!
