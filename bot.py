import telebot
import yt_dlp
import os

TOKEN = "8551612297:AAE39yEI9FBARmCyvae6AnrsvjBwQWwF7wc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎧 لینک اینستاگرام رو بفرست")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()

    if "instagram.com" not in url:
        bot.send_message(message.chat.id, "❌ فقط لینک اینستا بفرست")
        return

    bot.send_message(message.chat.id, "⏳ در حال دانلود...")

    try:
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'mp4',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists("video.mp4"):
            with open("video.mp4", "rb") as video:
                bot.send_video(message.chat.id, video)

            os.remove("video.mp4")
        else:
            bot.send_message(message.chat.id, "❌ فایل پیدا نشد")

    except Exception as e:
        bot.send_message(message.chat.id, "❌ خطا در دانلود")

bot.infinity_polling()
