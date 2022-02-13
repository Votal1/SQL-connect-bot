#!/usr/bin/python3

from os import environ
import telebot
from telebot import types

TOKEN = environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello world1123')


bot.polling(none_stop=True)
