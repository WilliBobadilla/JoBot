# from dotenv import load_dotenv, dotenv_values #pip install python-dotenv
# import telebot #pip install pyTelegramBotAPI

# # make sqlite3 import
# import sqlite3
# import pandas as pd

# from flask import Flask, request, send_file

# load_dotenv(dotenv_path='../.env')

# app = Flask(__name__)

# TOKEN = dotenv_values()['TELEGRAM_TOKEN']

# bot = telebot.TeleBot(TOKEN, parse_mode=None)

# # sqlite config
# # bot.set_webhook('https://test-bot-penguin.herokuapp.com', certificate=open('../cert.pem', 'r'))

# @app.route('/scraper', methods=['GET', 'POST'])
# def get_request():
#     if request.method == 'GET':
#         return '<h1>Hello World!</h1>'
#     elif request.method == 'POST':
#         print(request.get_json())
#         return 'Sí'
        


# @bot.message_handler(commands=['ayuda', 'sub', 'lista', 'desub'])
# def send_welcome(message):
#     # print(dict.keys(message._dict_))
#     if (len(message.text.split(' ')) > 1 or message.text == '/ayuda' or message.text == '/lista'):
#         conn = sqlite3.connect('./databaseee/tasks.db')
#         c = conn.cursor()
#         c.execute("CREATE TABLE IF NOT EXISTS keywords_user (id INTEGER PRIMARY KEY, user_id INTEGER, keyword TEXT)")

#         if message.text.startswith('/sub '):
#             keywords = message.text.replace('/sub ', '').split(';')
#             # save keywords_user relation in db
#             for keyword in keywords:
#                 c.execute("INSERT INTO keywords_user (user_id, keyword) VALUES (?, ?)", (message.from_user.id, keyword))
#                 conn.commit()

#             bot.send_message(message.chat.id, 'Te suscribiste a las ofertas relacionadas a: ' + ', '.join(keywords))
#         elif message.text.startswith('/lista'):
#             c.execute("SELECT keyword FROM keywords_user WHERE user_id = ?", (message.from_user.id,))
#             conn.commit()
#             keywords = c.fetchall()
#             if len(keywords) > 0:
#                 bot.send_message(message.chat.id, 'Tus suscripciones son: ' + ', '.join([keyword[0] for keyword in keywords]))
#             else:
#                 bot.send_message(message.chat.id, 'No te has suscrito a ninguna oferta')
        
#     else:
#         bot.send_message(message.chat.id, 'Command not allowed')
#     # close db
#     conn.close()


# # @bot.message_handler(func=lambda m: True)
# # def echo_all(message):
#     # print(message)
#     # bot.reply_to(message, 'hey!')

# #bot.infinity_polling()

# # intialize flask server
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
        
#         return 'ok'
#     else:
#         return 'ok'

# @app.route('/.well-known/pki-validation/<txt>', methods=['GET'])
# def pki():
#     # return send_file('./72FFA409D09DA39BEF5EC6FB20100061.txt')
#     return send_file(request.args.get('txt'))

# if (__name__) == "__main__":
#     app.run(debug=True, port=5001)


from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    # here we call our super AI
    response = get_response(text)
    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    return 'ok'

SECRET = "9XYLmhbvXF"

URL = 'https://test-bot-penguin.herokuapp.com/' + SECRET

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.add_webhook(url=URL)

# sqlite config

@app.route('/' + SECRET, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['ayuda', 'sub', 'lista', 'desub'])
def send_welcome(message):
    # print(dict.keys(message._dict_))
    if (len(message.text.split(' ')) > 1 or message.text == '/ayuda' or message.text == '/lista'):
        conn = sqlite3.connect('./databaseee/tasks.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS keywords_user (id INTEGER PRIMARY KEY, user_id INTEGER, keyword TEXT)")

        if message.text.startswith('/sub '):
            keywords = message.text.replace('/sub ', '').split(';')
            # save keywords_user relation in db
            for keyword in keywords:
                c.execute("INSERT INTO keywords_user (user_id, keyword) VALUES (?, ?)", (message.from_user.id, keyword))
                conn.commit()

            bot.send_message(message.chat.id, 'Te suscribiste a las ofertas relacionadas a: ' + ', '.join(keywords))
        elif message.text.startswith('/lista'):
            c.execute("SELECT keyword FROM keywords_user WHERE user_id = ?", (message.from_user.id,))
            conn.commit()
            keywords = c.fetchall()
            if len(keywords) > 0:
                bot.send_message(message.chat.id, 'Tus suscripciones son: ' + ', '.join([keyword[0] for keyword in keywords]))
            else:
                bot.send_message(message.chat.id, 'No te has suscrito a ninguna oferta')
        
    else:
        return "webhook setup failed"


# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
    # print(message)
    # bot.reply_to(message, 'hey!')

#bot.infinity_polling()

# if (__name__) == "__main__":
#     app.run()
