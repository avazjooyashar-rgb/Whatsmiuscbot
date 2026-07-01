import os
import telebot
import yt_dlp

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN variable not found!")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎧 لینک اینستاگرام رو بفرست."
    )


@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()

    if "instagram.com" not in url:
        bot.send_message(message.chat.id, "❌ فقط لینک اینستاگرام بفرست.")
        return

    bot.send_message(message.chat.id, "⏳ در حال دانلود...")

    try:
        ydl_opts = {
            "outtmpl": "video.%(ext)s",
            "format": "mp4/best",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None
        for file in os.listdir():
            if file.startswith("video."):
                video_file = file
                break

        if video_file:
            with open(video_file, "rb") as video:
                bot.send_video(message.chat.id, video)

            os.remove(video_file)
        else:
            bot.send_message(message.chat.id, "❌ فایل پیدا نشد.")

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "❌ خطا در دانلود ویدیو.")


print("Bot Started...")
bot.infinity_polling(skip_pending=True)
