#!/usr/bin/python3

from os import environ
import telebot
from telebot import types
import redis
from methods import rot13_encrypt, rot13_decrypt

TOKEN = environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

r = redis.Redis(host=environ.get('REDIS_HOST'), port=18753,
                password=environ.get('REDIS_PASSWORD'), db=0)

cred_error = '\u274E You`re not configured credentials! '
db_error = '\u274E Cannot connect to database.'
p_error = '\u274E Cannot connect to database or permission denied. '


def connect(uid):
    uname = 'default'
    if r.hexists(uid, 'username') == 1:
        uname = r.hget(uid, 'username').decode()
    host, port, password = r.hmget(uid, 'host', 'port', 'password')
    return redis.Redis(host=host.decode(), port=int(port), password=password.decode(), db=0, username=uname)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '\U0001F44B Hello!\nI am SQL Connect Bot. With me you can connect to Redis database!'
                          '\n/commands\nTo configure credentials press next commands:\n/set_host [host]'
                          '\n/set_password [password]\n/set_port [port]\n/set_user [username]\n\n'
                          '<code>Source code - </code>\ngithub.com/Votal1/SQL-connect-bot ',
                 parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['commands'])
def start(message):
    bot.reply_to(message, '\U0001F916 You can use next commands to manage Redis database (recommendation - '
                          'do not use spaces in keys and values):\n'
                          '\n/hget [key] [value]'
                          '\n/hgetall [key]'
                          '\n/hmget [key] [values] ...'
                          '\n/hset [key] [value] [set_value]'
                          '\n/hdel [key] [value]'
                          '\n/hincrby [key] [value] [set_value (int)]'
                          '\n/smembers [set]'
                          '\n/scard [set]'
                          '\n/sadd [set] [member]'
                          '\n/srem [set] [member]',
                 parse_mode='HTML')


@bot.message_handler(commands=['set_host'])
def start(message):
    try:
        cred = str(message.text.split(' ')[1])
        r.hset(message.from_user.id, 'host', cred)
        bot.reply_to(message, 'Database host: ' + cred)
    except:
        bot.reply_to(message, 'You did not specify host!')


@bot.message_handler(commands=['set_password'])
def start(message):
    try:
        cred = str(message.text.split(' ')[1])
        r.hset(message.from_user.id, 'password', cred)
        bot.reply_to(message, 'Your password: ' + cred)
    except:
        bot.reply_to(message, 'You did not specify password!')


@bot.message_handler(commands=['set_port'])
def start(message):
    try:
        cred = int(message.text.split(' ')[1])
        r.hset(message.from_user.id, 'port', cred)
        bot.reply_to(message, 'Database port: ' + str(cred))
    except:
        bot.reply_to(message, 'You did not specify port!')


@bot.message_handler(commands=['set_user'])
def start(message):
    try:
        cred = str(message.text.split(' ')[1])
        r.hset(message.from_user.id, 'username', cred)
        bot.reply_to(message, 'Your username: ' + cred + '\n\nPress /set_default to set default username.')
    except:
        bot.reply_to(message, 'You did not specify username!\n\nPress /set_default to set default username.')


@bot.message_handler(commands=['set_default'])
def start(message):
    try:
        r.hdel(message.from_user.id, 'username')
        bot.reply_to(message, '\u2705')
    except:
        pass


@bot.message_handler(commands=['hget'])
def r_hget(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value = message.text.split(' ', 2)[1], message.text.split(' ', 2)[2]
            try:
                if r.hexists(key, value) == 1:
                    msg = r2.hget(key, value).decode()
                else:
                    msg = str(r2.hget(key, value))
                bot.reply_to(message, msg)
            except:
                bot.reply_to(message, db_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/hget [key] [value]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['hgetall'])
def r_hgetall(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key = message.text.split(' ')[1]
            try:
                bot.reply_to(message, str(r2.hgetall(key)))
            except:
                bot.reply_to(message, db_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/hgetall [key]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['hmget'])
def r_hmget(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value = message.text.split(' ')[1], message.text.split(' ')[2:]
            try:
                bot.reply_to(message, str(r2.hmget(key, value)))
            except:
                bot.reply_to(message, db_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/hmget [key] [values] ...')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['hset'])
def r_hset(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value, s = message.text.split(' ', 3)[1], message.text.split(' ', 3)[2], message.text.split(' ', 3)[3]
            try:
                bot.reply_to(message, str(r2.hset(key, value, s)))
            except:
                bot.reply_to(message, p_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/hset [key] [value] [set_value]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['hdel'])
def r_hdel(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value = message.text.split(' ', 2)[1], message.text.split(' ', 2)[2]
            try:
                bot.reply_to(message, str(r2.hdel(key, value)))
            except:
                bot.reply_to(message, p_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/hdel [key] [value]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['hincrby'])
def r_hincrby(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value, s = message.text.split(' ', 3)[1], message.text.split(' ', 3)[2], \
                            int(message.text.split(' ', 3)[3])
            try:
                bot.reply_to(message, str(r2.hincrby(key, value, s)))
            except:
                bot.reply_to(message, p_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/hincrby [key] [value] [set_value (int)]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['smembers'])
def r_smembers(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key = message.text.split(' ')[1]
            try:
                bot.reply_to(message, str(r2.smembers(key)))
            except:
                bot.reply_to(message, db_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/smembers [set]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['scard'])
def r_scard(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key = message.text.split(' ')[1]
            try:
                bot.reply_to(message, str(r2.scard(key)))
            except:
                bot.reply_to(message, db_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/scard [set]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['sadd'])
def r_sadd(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value = message.text.split(' ', 2)[1], message.text.split(' ', 2)[2]
            try:
                bot.reply_to(message, str(r2.sadd(key, value)))
            except:
                bot.reply_to(message, p_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/sadd [set] [member]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['srem'])
def r_srem(message):
    try:
        r2 = connect(message.from_user.id)
        try:
            key, value = message.text.split(' ', 2)[1], message.text.split(' ', 2)[2]
            try:
                bot.reply_to(message, str(r2.srem(key, value)))
            except:
                bot.reply_to(message, p_error)
        except:
            bot.reply_to(message, 'Invalid format. Usage:\n/srem [set] [member]')

    except:
        bot.reply_to(message, cred_error)


@bot.message_handler(commands=['encrypt'])
def encrypt(message):
    try:
        ciphertext = rot13_encrypt(message.text.split(' ', 1)[1])
        bot.reply_to(message, ciphertext)
    except:
        bot.reply_to(message, 'Invalid format. Usage:\n/encrypt [text]')


@bot.message_handler(commands=['decrypt'])
def decrypt(message):
    try:
        plaintext = rot13_decrypt(message.text.split(' ', 1)[1])
        bot.reply_to(message, plaintext)
    except:
        bot.reply_to(message, 'Invalid format. Usage:\n/decrypt [text]')


while True:
    try:
        bot.polling(non_stop=True)
    except:
        pass
