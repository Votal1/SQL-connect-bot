#!/usr/bin/python3

from os import environ
import telebot
from telebot import types
import redis

TOKEN = environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

r = redis.Redis(host=environ.get('REDIS_HOST'), port=16801,
                password=environ.get('REDIS_PASSWORD'), db=0)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello world1123' + str(r.keys()))


bot.polling(none_stop=True)
