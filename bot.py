import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import threading
from flask import Flask

# 🔐 Вставь сюда свой токен
TOKEN = "7357522794:AAHqsKsbtForBWBF9bzve6FUx-AXggD5dDc"
print(f"TOKEN is: {TOKEN}")
bot = telebot.TeleBot(TOKEN)


def download_video_if_needed(name, url):
    path = f"videos/{name}"
    if not os.path.exists(path):
        print(f"Скачиваю: {name}")
        response = requests.get(url)
        with open(path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Файл уже есть: {name}")

# 📚 Список уроков (видео и табы)
lessons = [
    ("урок01-знакомство.mp4", "https://drive.google.com/uc?export=download&id=1Iyl7ujjeEn-V93svPkz1mmlQwD-GYU5K"),
    ("урок02-подготовка.mp4", "https://drive.google.com/uc?export=download&id=1u4pHTFO7Q25GaW1kXgUuLSsxJubSsNZ4"),
    ("урок03-правильная_посадка.mp4", "https://drive.google.com/uc?export=download&id=1UTLnKOVgPCqOFPcCXzaE5GVLvkf4x0Yr"),
    ("урок04-правая_рука.mp4", "https://drive.google.com/uc?export=download&id=14AI8kPiZ3hrCn0TAFTjRBoU_kGEEca2h"),
    ("урок05-левая_рука.mp4", "https://drive.google.com/uc?export=download&id=1MsbsQsV1G8wUn7ibQJm2a0-V7ndOuJ5b"),
    ("урок06-Первое произведение.mp4", "https://drive.google.com/uc?export=download&id=1sirmU7Kg4kb8Iq3U8bCzH8rgWrvXgTXw"),
    ("урок07-Миссия невыполнима.mp4", "https://drive.google.com/uc?export=download&id=1x_5ukYQCBto9iZ8E2CPv4YDClI2iA7fP"),
    ("урок08-Читаем табы.mp4", "https://drive.google.com/uc?export=download&id=1iHAu5XxC2Kizu4yhjxqw7QRc3JqSw4Ra"),
    ("урок08-Prayer in C.mp4", "https://drive.google.com/uc?export=download&id=1ZQflDQlXXmJFDxeQ0atOWewToe9SswMv"),
    ("урок09-Чередование пальцев.mp4", "https://drive.google.com/uc?export=download&id=1iGAfWKSw0fOP8GqsoL2vgh4SJu1PWcfZ"),
    ("урок10-навалим баса.mp4", "https://drive.google.com/uc?export=download&id=1TSlb12gJ8_wLKetYYvaUPtKG12uNRGLY"),
    ("урок11-Счет и ритм.mp4", "https://drive.google.com/uc?export=download&id=1nt8Im6wSPvMSPMvfpel3VLhFZww39w-Q"),
    ("урок12-Вырабатываем правильный ритм.mp4", "https://drive.google.com/uc?export=download&id=1AvjUWfvr5E7EAuEPA_6epw8r4GHj8VXm"),
    ("урок13-Закрепляем пройденное.mp4", "https://drive.google.com/uc?export=download&id=1j1Ppv0Ikb1c5NVC_-dJ8ty6wxhiDnAc"),
    ("урок14-Итоги обучения.mp4", "https://drive.google.com/uc?export=download&id=1zbrJEVysFwaEcYe844zzhgWHuanEaJDx"),
    ("урок15-Развитие.mp4", "https://drive.google.com/uc?export=download&id=1zbrJEVysFwaEcYe844zzhgWHuanEaJDx"),
]

# 💾 Храним, какой урок был у пользователя
user_progress = {}

app = Flask(__name__)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# 📍 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Учиться 🎸", callback_data="learn")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы начать обучение:", reply_markup=keyboard)

for name, url in lessons:
    download_video_if_needed(name, url)

# 📌 Обработка кнопки "Учиться"
@bot.callback_query_handler(func=lambda call: call.data == "learn")
def handle_learn(call):
    user_id = call.from_user.id
    index = user_progress.get(user_id, 0)

    if index >= len(lessons):
        bot.send_message(call.message.chat.id, "Ты прошёл все уроки! Молодец! 🎉")
        return

    lesson = lessons[index]
    bot.answer_callback_query(call.id, text="Отправляю урок...")

    # Отправка видео (может быть одно или два)
    for video in lesson["videos"]:
        bot.send_message(call.message.chat.id, video)

    # Если есть таб — отправить файл
    if "tab" in lesson:
        tab_path = os.path.join("tabs", lesson["tab"])
        if os.path.exists(tab_path):
            with open(tab_path, 'rb') as f:
                bot.send_document(call.message.chat.id, f)
        else:
            bot.send_message(call.message.chat.id, f"Таб {lesson['tab']} не найден 😢")

    # Обновить прогресс
    user_progress[user_id] = index + 1


def run_bot():
    bot.infinity_polling()

# ▶ Запуск
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_bot).start()