import telebot
import requests

TOKEN = "8551612297:AAH0Fr22_XgONLlS9Wyw-0vPq9VyWhtz-NE"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎧 لینک اینستاگرام رو بفرست")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text

    if "instagram.com" not in url:
        bot.send_message(message.chat.id, "❌ فقط لینک اینستا بفرست")
        return

    bot.send_message(message.chat.id, "⏳ در حال پردازش...")

    try:
        api = "https://api.instasave.app/?url=" + url
        r = requests.get(api).json()

        video = r.get("media")

        if video:
            bot.send_video(message.chat.id, video)
        else:
            bot.send_message(message.chat.id, "❌ ویدیو پیدا نشد")

    except:
        bot.send_message(message.chat.id, "❌ خطا در دانلود")

bot.infinity_polling()
