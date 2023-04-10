from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

# подключения модуля с токеном
import config  # импорт файла
# подключение модуля с кнопками
import keyboard  # импорт файла

import logging  # модуль для вывода информации


storage = MemoryStorage()  # хранилище состояний
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO, filename='log.txt')


'''обработка команды /start'''

@dp.message_handler(Command("start"), state=None)
async def welcome(message):
    joinedFile = open('user.txt', 'r')  # создаем файл, куда будет записываться id пользователя
    joinedUser = set()
    for line in joinedFile:  # цикл в котором проверяем имеется ли такой id в файле
        joinedUser.add(line.strip())

    if not str(message.chat.id) in joinedUser:  # делаем запись в файл нового id
        joinedFile = open('user.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUser.add(message.chat.id)
        joinedFile.close()

    await bot.send_message(message.chat.id, f'ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ!\n'
                                            f'Полезные ссылки - /links',
                           reply_markup=keyboard.start, parse_mode='Markdown')
    # после проверки и записи выводим сообщение с именем пользователя и отбражаем кнопки

@dp.message_handler(commands="info")
async def cmd_test2(message: types.Message):
    await message.reply('Бот создан для обучения!')


@dp.message_handler(commands='links')
async def url_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Полезные ссылки:', reply_markup=keyboard.urlkb, parse_mode='Markdown')


if __name__ == "__main__":
    print('Бот запущен!')
    executor.start_polling(dp, skip_updates=True)