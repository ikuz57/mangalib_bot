import os
from telegram.ext import CommandHandler, Updater
from telegram import Bot, ReplyKeyboardMarkup
from dotenv import load_dotenv
from parser_mangalib import parser_mangalib
from threading import Thread

load_dotenv()
token = os.getenv('TOKEN')
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

updater = Updater(token=token)
bot = Bot(token=token)
url = 'https://mangalib.me/?section=all-updates/'


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    Thread(target=parser_mangalib, args=(bot, chat, url, login, password)).start()
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Добро пожаловать, {}!'.format(name),
        reply_markup=button
        )


def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    # updater.dispatcher.add_handler(CommandHandler('Обновить', update_mangalist))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
