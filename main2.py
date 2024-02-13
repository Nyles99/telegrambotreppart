from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from bs4 import BeautifulSoup
from PIL import Image, ImageFile, UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True
headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

updater = Updater(token='')

def say_hi(update, context):
    if context.args:
        url = str(context.args)
        if "https://bamper.by/" in url:
            req = requests.get(url=url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'html.parser')
            foto_href = soup.find_all("div", class_="add-image")
            chat = update.effective_chat
            context.bot.send_message(chat_id=chat.id, text='Привет, если ты реппартёр, кидай ссылку, а я высру тебе фотки')
        else:
            chat = update.effective_chat
            context.bot.send_message(chat_id=chat.id, text='Реппартёр, так дела не делаются...нужна ссылка с конкретного сайта, а ты мне что присылаешь?')
    else:
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text='Привет, если ты реппартёр, кидай ссылку, а я высру тебе фотки')
def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список, 
    # даже если кнопка всего одна.
    button = ReplyKeyboardMarkup([['Dick pic']])
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что вы включили меня, {}!'.format(name),
        # Добавим кнопку в содержимое отправляемого сообщения
        reply_markup=button  
        )

# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()
updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
updater.start_polling()
updater.idle()




import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

updater = Updater(token='6945695697:AAEOKj6ObwjrcC34Ysgbi5sNYzLE5gCJMQA')
URL = 'https://api.thecatapi.com/v1/images/search'

def get_new_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image())

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

updater.start_polling()
updater.idle()