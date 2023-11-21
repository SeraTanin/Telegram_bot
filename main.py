import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
name = ''
surname = ''
age = 0
API_TOKEN = os.getenv('API_TOKEN')
link_name = os.getenv('link_name')
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Which band is the best?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Hello':
        bot.reply_to(message, 'Hello, how are you?')
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, 'Hi, what is your name?')
        bot.register_next_step_handler(message, reg_name)

        # bot.reply_to(message, message.text)


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'What is your surname?')
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'What is your age?')
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age

    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Enter a number please')

    # make a buttons yes and no
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='Yes')
    keyboard.add(key_yes)

    key_no = types.InlineKeyboardButton(text='No', callback_data='No')
    keyboard.add(key_no)
    question = f"Are you {age} years old? Is your name {name} and surname is {surname}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'Yes':
        bot.send_message(call.message.chat.id, "Nice to meet you")
    elif call.data == 'No':
        bot.send_message(call.message.chat.id, "Can you write this correctly?")
        bot.send_message(call.message.chat.id, "What is your name?")
        bot.register_next_step_handler(call.message, reg_name)


bot.infinity_polling()
