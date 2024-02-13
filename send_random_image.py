from telegram import Bot
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFile, UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True
headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

"""bot = Bot(token='6945695697:AAEOKj6ObwjrcC34Ysgbi5sNYzLE5gCJMQA')
URL = 'https://api.thecatapi.com/v1/images/search'
chat_id = 831040832

# Делаем GET-запрос к эндпоинту:
response = requests.get(URL).json()
# Извлекаем из ответа URL картинки:
random_cat_url = response[0].get('url')  

# Передаём chat_id и URL картинки в метод для отправки фото:
bot.send_photo(chat_id, random_cat_url)"""
url = "https://bamper.by/zapchast_zerkalo-naruzhnoe-levoe/13607-124075456/"
req = requests.get(url=url, headers=headers)
src = req.text
soup = BeautifulSoup(src, 'html.parser')
foto_href = soup.find_all("img", itemprop="image")
#print(foto_href)
for item in foto_href:
    #print(item, "привет")
    href = "https://bamper.by" +item.get("src")
    print(href)