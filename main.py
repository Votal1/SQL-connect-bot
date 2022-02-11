#!/usr/bin/python3

import telebot
from telebot import types

TOKEN = '5212114227:AAFiX_WnuBX9pxm3xlDZtuujJhVN3ukoHzo'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello')


bot.polling(none_stop=True)
