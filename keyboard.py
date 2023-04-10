from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)  # основа для кнопок

info = types.KeyboardButton(text="Информация")
stats = types.KeyboardButton(text="Статистика")
develop = types.KeyboardButton(text="Разработчик")
show_user = types.KeyboardButton(text="Покажи пользователя")
send_photo = types.KeyboardButton(text="Отправить картинку")

start.add(stats, info, develop, show_user, send_photo)