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

"""Ин-лайн кнопки"""
# for /links: 2 button inline
urlkb = InlineKeyboardMarkup(row_width=1)
inline_btn_1 = InlineKeyboardButton(text='Документация по Python', url='https://docs.python.org/3/index.html')
inline_btn_2 = InlineKeyboardButton(text='Курсы по Python',
                                    url='https://myitschool.by/kursy-it/razrabotka-veb-prilozhenij-na-python/')
urlkb.add(inline_btn_1, inline_btn_2)

# 2 button for statistic(колбэк кнопки)
statis = InlineKeyboardMarkup()
statis.add(InlineKeyboardButton('Да', callback_data='join'))  # создаем кнопку и кэлбэк к ней
statis.add(InlineKeyboardButton('Нет', callback_data='cancel'))  # создаем кнопку и кэлбэк к ней

# 2 button for Покажи пользователя(колбэк кнопки)
show_us = InlineKeyboardMarkup()
show_us.add(InlineKeyboardButton('Хочу видеть id', callback_data='show'))
show_us.add(InlineKeyboardButton('Вернуться обратно', callback_data='exit'))
