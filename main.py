import os
import telebot
from dotenv import load_dotenv
import openai

# Загружаем переменные окружения из .env файла
load_dotenv()

# Устанавливаем токены и ключи
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
STATUS = os.getenv('STATUS')
INFO = os.getenv('INFO')

# Проверяем, что переменные имеют значения
print(f"STATUS: {STATUS}")
print(f"INFO: {INFO}")

# Создаем клиента OpenAI
openai.api_key = OPENAI_API_KEY  # Устанавливаем API ключ для OpenAI

# Создаем бота Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Список ID пользователей, для которых бот не должен отвечать
blocked_user_ids = [111111111, 222222222]
proof_user_ids = [6492171928, 7399863804, 6414296957, 696784041, 462519865, 665170723, 697722533]
proof_NO_user_ids = [111111111, 222222222]

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Проверяем, есть ли ID пользователя в списке заблокированных
    if message.from_user.id in blocked_user_ids:
        return  # Не обрабатываем сообщение от этого пользователя

    if "/proof" in message.text.lower():
        bot.reply_to(message, "Вы подали запрос на разблокировку. Ожидайте ответа от администратора.")
        return  # Не обрабатываем сообщение от этого пользователя

    if message.from_user.id in proof_NO_user_ids:
        bot.reply_to(message, "Ваш аккаунт был заблокирован.")
        return  # Не обрабатываем сообщение от этого пользователя

    if message.from_user.id in proof_user_ids:
        bot.reply_to(message, "Вы заблокированы. Напишите /proof и ожидайте разблокировки.")
        return  # Не обрабатываем сообщение от этого пользователя

    if "пончик" in message.text.lower():
        return  # Не обрабатываем сообщение от этого пользователя

    try:
        user_text = message.text
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Используем вашу модель
            messages=[{"role": "user", "content": user_text}]
        )
        response = completion.choices[0].message['content']
        bot.reply_to(message, response)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "К сожалению, возникла непредвиденная ошибка, и я не смогу предоставить ответ. 😟")

# Запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=99)