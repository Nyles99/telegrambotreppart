import telegram
from pyrogram import Client

api_id = 23175536
api_hash = "20dc93aecff0bb360c2b1aeeff2f60a3"

# Создаём программный клиент, передаём в него
# имя сессии и данные для аутентификации в Client API
app = Client('my_account', api_id, api_hash)

app.start()
# Отправляем сообщение
# Первый параметр - это id чата или имя получателя.
# Зарезервированное слово 'me' означает собственный аккаунт отправителя.
app.send_message('me', 'Привет, это я!')
app.stop()