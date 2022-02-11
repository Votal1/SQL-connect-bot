#!/usr/bin/python3

import telebot
from telebot import types
from flask import Flask, request
from os import environ

TOKEN = '5212114227:AAFiX_WnuBX9pxm3xlDZtuujJhVN3ukoHzo'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hi')


server = Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='18.184.40.153' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
