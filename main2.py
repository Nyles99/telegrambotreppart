from telegram import Bot

# Здесь укажите токен, 
# который вы получили от @Botfather при создании бот-аккаунта
bot = Bot(token='6945695697:AAEOKj6ObwjrcC34Ysgbi5sNYzLE5gCJMQA')
# Укажите id своего аккаунта в Telegram
chat_id = 831040832
text = 'Привет'
# Отправка сообщения
bot.send_message(chat_id, text)