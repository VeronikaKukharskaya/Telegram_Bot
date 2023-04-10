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

"""Настройка FMS, сразу после логирования, перед командами бота """


class Me_info(StatesGroup):
    Q1 = State()  # задаём состояние 1
    Q2 = State()  # задаём состояние 2
    save_photo_1 = State()
    save_photo_2 = State()


# Прописываем хендлер на команду me, при этом изначальное состояние не задаём
@dp.message_handler(Command('me'), state=None)  # создаём команду /me для админа
async def enter_me_info(message: types.Message):
    if message.chat.id == config.admin:  # сверяем id c id админа
        await message.answer('Начинаем настройку \n'
                             '1. Укажите ссылку на Ваш профиль')
        await Me_info.Q1.set()  # начинаем ждать наш ответ, задав состояние Й1


# задаём хендлер для состояния Q1
# к состоянию обращаемся через атрибут класса
@dp.message_handler(state=Me_info.Q1)
# нашей функции мы указываем, что хотим получить сообщение и состояние
async def answer_for_state_Q1(message: types.Message, state: FSMContext):
    # сохраняем текст полученного сообщения
    answer = message.text
    # в данном месте прописываем для нашего состояния обновление данных
    # в пространство имён для текущего состояния
    # мы добавляем ключ answer1 со значением answer
    await state.update_data(answer1=answer)
    # после чего выводим сообщение
    await message.answer('Ваша ссылка сохранена \n'
                         '2. Введите текст')
    # и задаём состояние Q2
    await Me_info.Q2.set()


# задаем хендлер для обработки данных от пользователей, находящихся во втором состоянии
# т.е. бот будет отлавливать пользователей, которые перейдут в состояние Q2
@dp.message_handler(state=Me_info.Q2)
async def answer_for_state_Q2(message: types.Message, state: FSMContext):
    # записываем ответ
    answer = message.text
    # Снова в пространство имен добавляем answer2 со значением answer, т.е. с текстом пользователя
    await state.update_data(answer2=answer)
    # говорим боту отправить сообщение
    await message.answer("Текст сохранен")
    # в переменную data получаем словарь, хранящийся в нашем хранилище состояний для текущего состояния
    data = await state.get_data()
    # print(data) увидим словарь
    # достаем значение по ключу answer1
    answer1 = data.get("answer1")
    # достаем значение по ключу answer2
    answer2 = data.get("answer2")
    # открываем файл link.txt на режим записи в кодировке UTF-8
    with open("link.txt", 'w', encoding="UTF-8") as link_txt:
        # записываем строкой ссылку в наш файл
        link_txt.write(str(answer1))
    # открываем файл text.txt в режиме записи в той же кодировке
    with open("text.txt", "w", encoding="UTF-8") as text_txt:
        # записываем в файл текст, который передал пользователь
        text_txt.write(str(answer2))
    # говорим боту отправить сообщение
    await message.answer(f"Ваша ссылка на профиль: {answer1} \n"
                         f"Ваш текст: {answer2}")
    # закрываем текущее состояние
    await state.finish()


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


@dp.message_handler(commands=['rassilka'])
async def rassilka(message: types.Message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'Рассылка началась\nБот оповестит, когда рассылку закончит',
                               parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open('user.txt', 'r')
        joinedUsers = set()
        for line in joinedFile:
            joinedUsers.add(line.strip())
        joinedFile.close()
        for user in joinedUsers:
            try:
                await bot.send_photo(user, open('photo.png', 'rb'))
                receive_users += 1
            except:
                block_users += 1
            await asyncio.sleep(0.4)  # поспи 0,4 секунды и повтори отправку, чтобы ТГ не заблокировал
        await bot.send_message(message.chat.id, f'Рассылка была завершена \n'
                                                f'Получили сообщение: {receive_users} пользователей \n'
                                                f'Заблокировали бота: {block_users}', parse_mode='Markdown')


@dp.message_handler(commands="info")
async def cmd_test2(message: types.Message):
    await message.reply('Бот создан для обучения!')


@dp.message_handler(commands='links')
async def url_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Полезные ссылки:', reply_markup=keyboard.urlkb, parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message):
    if message.text == "Информация":
        await bot.send_message(message.chat.id, text="Информация\nБот создан специально для обучения!",
                               parse_mode='Markdown')
    elif message.text == "Статистика":
        await bot.send_message(message.chat.id, text="Хочешь посмотреть статистику бота?",
                               reply_markup=keyboard.statis, parse_mode='Markdown')
    elif message.text == "Разработчик":
        with open("link.txt", encoding="UTF-8") as link_txt:
            link = link_txt.read()
        with open("text.txt", encoding="UTF-8") as text_txt:
            text = text_txt.read()
        await bot.send_message(message.chat.id, text=f"Разработчик: {link} \n {text}", parse_mode='Markdown')
    elif message.text == "Покажи пользователя":
        await bot.send_message(message.chat.id, text="Показать пользователя?", reply_markup=keyboard.show_us,
                               parse_mode='Markdown')
    elif message.text == "Отправить картинку":
        await bot.send_photo(message.chat.id, open('cat.png', 'rb'))
        await bot.send_message(message.chat.id, text="Держи картинку", reply_markup=keyboard.send_photo,
                               parse_mode='Markdown')


"""Колбэк кнопки для статистики ДА\НЕТ"""


@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        count_user = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Вот статистика бота: *{count_user}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="У Вас нет прав администратора", parse_mode='Markdown')


@dp.callback_query_handler(text_contains='cancel')
async def cancel(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Ты вернулся в Главное меню. Жми опять кнопки', parse_mode='Markdown')


"""Колбэк кнопки для кнопки Покажи пользователя"""


@dp.callback_query_handler(text_contains='show')
async def show(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Id Бота: {call.message.from_user.id}\n'
                                     f'Ваш id: {call.from_user.id}', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='exit')
async def exit(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Вы отменили выбор!', parse_mode='Markdown')


if __name__ == "__main__":
    print('Бот запущен!')
    executor.start_polling(dp, skip_updates=True)