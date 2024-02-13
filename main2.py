import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from bs4 import BeautifulSoup
from PIL import Image, ImageFile, UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True
headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
watermark = Image.open("moe.png")
updater = Updater(token='6945695697:AAEOKj6ObwjrcC34Ysgbi5sNYzLE5gCJMQA')


def say_hi(update, context):
    print(context.text)
    if context.args:
        url = str(context.args)
        if "https://bamper.by/" in url:
            req = requests.get(url=url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'html.parser')
            foto_href = soup.find_all("img", itemprop="image")
            #print(foto_href)
            z=0
            for item in foto_href:

                #print(item, "привет")
                href = "https://bamper.by" +item.get("src")
                z += 1
                if href != "https://bamper.by/local/templates/bsclassified/images/nophoto_car.png":
                                try:
                                    img = requests.get(url=href, headers=headers)
                                    img_option = open(f"{z}.png", 'wb')
                                    img_option.write(img.content)
                                    img_option.close
                                    try:
                                        im = Image.open(f"{z}.png")
                                        pixels = im.load()  # список с пикселями
                                        x, y = im.size  # ширина (x) и высота (y) изображения
                                        min_line_white = []
                                        n=0
                                        for j in range(y):
                                            white_pix = 0
                            
                                            for m in range(x):
                                                # проверка чисто белых пикселей, для оттенков нужно использовать диапазоны
                                                if pixels[m, j] == (248,248,248):         # pixels[i, j][q] > 240  # для оттенков
                                                    white_pix += 1
                                            if white_pix == x:
                                                n += 1
                                            #print(white_pix, x, n)

                                            #print(white_pix)
                                            min_line_white.append(white_pix)
                                        left_border = int(min(min_line_white)/2)
                                        #print(left_border)
                                        im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(f"{folder_name}/{name_href}.png", quality=95)

                                        img = Image.open(f"{z}.png")
                                        #print(foto)
                                        #img = Image.open(f"fotku/{name_href}.png")    
                                        img.paste(watermark,(-272,-97), watermark)
                                        img.paste(watermark,(-230,1), watermark)
                                        img.save(f"{z}.png", format="png")
                                        img_option.close
                                    except Exception:
                                         pass
                                except Exception:
                                    pass     
                else:
                    chat = update.effective_chat
            for number in range(1,z+1):
                context.bot.send_message(chat_id=chat.id, text=f'Всего {z} фоток, реппартер!') 
                chat = update.effective_chat
                context.bot.send_photo(chat_id=chat.id, foto = f"{z}.png")
            #context.bot.send_message(chat_id=chat.id, text='Привет, если ты реппартёр, кидай ссылку, а я высру тебе фотки')
        else:
            chat = update.effective_chat
            context.bot.send_message(chat_id=chat.id, text='Реппартёр, фоток нет СОВСЕМ')
    else:
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text='Привет, если ты реппартёр, кидай ссылку, а я высру тебе фотки')
def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список, 
    # даже если кнопка всего одна.
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что вы включили меня, {}!'.format(name),
        # Добавим кнопку в содержимое отправляемого сообщения 
        )

# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()
updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
updater.start_polling()
updater.idle()
