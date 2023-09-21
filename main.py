import telebot
from pytube import YouTube

# Укажите токен вашего бота
bot = telebot.TeleBot('6001527391:AAGWfHO3HoDniwJ1GC_8o9A0KyTJOulLe6w')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на видео на YouTube, и я отправлю его тебе.")


# Обработчик сообщений с ссылкой на видео
@bot.message_handler(func=lambda message: True)
def download_video(message):
    try:
        # Получаем ссылку на видео из сообщения пользователя
        video_url = message.text

        # Скачиваем видео с YouTube
        yt = YouTube(video_url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download()

        # Отправляем видео пользователю
        with open(video.default_filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при скачивании видео.")


bot.polling()
