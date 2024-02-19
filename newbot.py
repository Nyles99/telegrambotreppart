import requests
import telebot
from bs4 import BeautifulSoup
from PIL import Image, ImageFile, UnidentifiedImageError
import os


ImageFile.LOAD_TRUNCATED_IMAGES = True
headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
watermark = Image.open("moe.png")


bot = telebot.TeleBot("6945695697:AAEOKj6ObwjrcC34Ysgbi5sNYzLE5gCJMQA")

@bot.message_handler()
def info(message):
    try:
        if "https://bamper.by/" in message.text.lower():
            print(message.text)
            #bot.send_message(message.chat.id, f"привет, {message.text}")
            req = requests.get(url=message.text, headers=headers)
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
                            im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(f"{z}.png", quality=95)

                            img = Image.open(f"{z}.png")
                            #print(foto)
                            #img = Image.open(f"fotku/{name_href}.png")    
                            img.paste(watermark,(-265,-97), watermark)
                            img.paste(watermark,(-230,1), watermark)
                            img.save(f"{z}.png", format="png")
                            img_option.close
                        except Exception:
                                print("ошибка")
                                bot.send_message(message.chat.id, "Идешь нахуй")
                    except Exception:
                        print("ошибка")
                        bot.send_message(message.chat.id, "Идешь нахуй")     
                else:
                    bot.send_message(message.chat.id, "У ссылки, которую ты прислал, нет фотографии")
            bot.send_message(message.chat.id, f'Всего {z} фоток, реппартер!')
            for number in range(1,z+1):
                photo = open(f"{number}.png", "rb") 
                
                bot.send_photo(message.chat.id, photo)
            
        else:
            bot.send_message(message.chat.id, "Реппартёр, ты прислал что-то не то...")
    except Exception:
        print("ошибка")
@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "привет")

bot.infinity_polling(timeout=10, long_polling_timeout=5)