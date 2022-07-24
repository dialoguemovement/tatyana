#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This file is part of Tatyana.
#
# Tatyana is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tatyana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
sys.path.insert(0, "modules/")

from generator import generateMessage
from mailer import sendMessage

from dotenv import load_dotenv
import telebot
from telebot import types
import os
import json

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode="MARKDOWN")


appeal_dict = {}

class Appeal:
    def __init__(self, city):
        self.city = city
        self.theme = None
        self.address = None
        self.attachment = None


# Handle "/start" and "/help" # TODO: remove /help, add /cancel
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привет! 👋

Меня зовут Татьяна. Для вас — просто Таня :-)

Я работаю виртуальным секретарём в Движении «Диалог» и помогаю гражданам создавать и отправлять обращения в органы местного самоуправления.

Сейчас я работаю в тестовом режиме и обрабатываю заявки только из г. Озёры и г. Коломна.

`Татьяна`
""", reply_markup=json.dumps({'remove_keyboard': True}))
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("Озёры"), types.KeyboardButton("Коломна"),
        types.KeyboardButton("Моего города нет в списке ❎"),
    )
    msg = bot.reply_to(message, """\
Давайте составим ваше обращение. Чтобы начать, выберите город или напишите /cancel, чтобы завершить диалог.

Где вы сейчас находитесь?

`Татьяна`
""", reply_markup=keyboard)
    bot.register_next_step_handler(msg, confirm_city_name_step)


def confirm_city_name_step(message):
    try:
        chat_id = message.chat.id
        city = message.text
        appeal = Appeal(city)
        appeal_dict[chat_id] = appeal
        if appeal.city == "Моего города нет в списке ❎":
            msg = bot.reply_to(message, """\
К сожалению, в таком случае я не смогу помочь вам составить обращение :-(

Сейчас я работаю в тестовом режиме и обрабатываю заявки только из г. Озёры и г. Коломна.

Напишите мне /start, если вы хотите составить обращение ещё раз.

`Татьяна`
""", reply_markup=json.dumps({'remove_keyboard': True}))
            return
        elif not appeal.city in ["Озёры", "Коломна"]:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.KeyboardButton("Озёры"), types.KeyboardButton("Коломна"),
                types.KeyboardButton("Моего города нет в списке ❎"),
            )
            msg = bot.reply_to(message, """\
К сожалению, я не знаю такого города. Давайте попробуем ещё раз?

`Татьяна`
""", reply_markup=keyboard)
            bot.register_next_step_handler(msg, confirm_city_name_step)
            return
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Правильно ✅", "Изменить город 🔄")
            msg = bot.reply_to(message, """\
Вы сейчас находитесь в г. {}, правильно?

`Татьяна`
""".format(appeal.city), reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_city_name_step)
        return
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так в confirm", reply_markup=json.dumps({'remove_keyboard': True}))


def process_city_name_step(message):
    chat_id = message.chat.id
    appeal = appeal_dict[chat_id]
    try:
        if message.text == "Изменить город 🔄":
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.KeyboardButton("Озёры"), types.KeyboardButton("Коломна"),
                types.KeyboardButton("Моего города нет в списке ❎"),
            )
            msg = bot.reply_to(message, """\
Где вы сейчас находитесь?

`Татьяна`
""", reply_markup=keyboard)
            bot.register_next_step_handler(msg, confirm_city_name_step)
            return
        elif message.text == "Правильно ✅":
            if appeal.city == "Моего города нет в списке ❎":
                msg = bot.reply_to(message, """\
К сожалению, в таком случае я не смогу помочь вам составить обращение :-(

Сейчас я работаю в тестовом режиме и обрабатываю заявки только из г. Озёры и г. Коломна.

Напишите мне /start, если вы хотите составить обращение ещё раз.

`Татьяна`
""", reply_markup=json.dumps({'remove_keyboard': True}))
                return
            elif not appeal.city in ["Озёры", "Коломна"]:
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(
                    types.KeyboardButton("Озёры"), types.KeyboardButton("Коломна"),
                    types.KeyboardButton("Моего города нет в списке ❎"),
                )
                msg = bot.reply_to(message, """\
К сожалению, я не знаю такого города. Давайте попробуем ещё раз?

`Татьяна`
""", reply_markup=keyboard)
                bot.register_next_step_handler(msg, confirm_city_name_step)
                return
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.KeyboardButton("Разбросанный мусор"), types.KeyboardButton("Не горит фонарь"),
                types.KeyboardButton("Вандализм"),          types.KeyboardButton("Не пришёл автобус"),
                types.KeyboardButton("Нет расписания"),     types.KeyboardButton("Плохое состояние дороги"),
                types.KeyboardButton("Нет пандуса"),        types.KeyboardButton("Оголённые провода"),
                types.KeyboardButton("Бродячие собаки"),    types.KeyboardButton("Просрочка"),
            )
            msg = bot.reply_to(message, """\
Супер!

На какую тему вам помочь составить обращение?

`Татьяна`
    """, reply_markup=keyboard)

            bot.register_next_step_handler(msg, confirm_theme_step)
            return
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Правильно ✅", "Изменить город 🔄")
            msg = bot.reply_to(message, """\
Вы сейчас находитесь в г. {}, правильно?

`Татьяна`
""".format(appeal.city), reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_city_name_step)
        return
    except Exception as e:
       bot.reply_to(message, "Что-то пошло не так", reply_markup=json.dumps({'remove_keyboard': True}))


def confirm_theme_step(message):
    try:
        chat_id = message.chat.id
        appeal = appeal_dict[chat_id]
        appeal.theme = message.text
        if not appeal.theme in [
                "Разбросанный мусор", "Не горит фонарь",
                "Вандализм",          "Не пришёл автобус",
                "Нет расписания",     "Плохое состояние дороги",
                "Нет пандуса",        "Оголённые провода",
                "Бродячие собаки",    "Просрочка"
            ]:
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.KeyboardButton("Разбросанный мусор"), types.KeyboardButton("Не горит фонарь"),
                types.KeyboardButton("Вандализм"),          types.KeyboardButton("Не пришёл автобус"),
                types.KeyboardButton("Нет расписания"),     types.KeyboardButton("Плохое состояние дороги"),
                types.KeyboardButton("Нет пандуса"),        types.KeyboardButton("Оголённые провода"),
                types.KeyboardButton("Бродячие собаки"),    types.KeyboardButton("Просрочка"),
            )
            msg = bot.reply_to(message, """\
К сожалению, пока я не могу помочь вам с этим вопросом.

Может, составим обращение на другую тему?

`Татьяна`
""", reply_markup=keyboard)
            bot.register_next_step_handler(msg, confirm_theme_step)
            return
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Правильно ✅", "Изменить тему 🔄")
            msg = bot.reply_to(message, """\
Будем составлять обращение на тему «{}», правильно?

`Татьяна`
""".format(appeal.theme), reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_theme_step)
        return
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так в confirm", reply_markup=json.dumps({'remove_keyboard': True}))


def process_theme_step(message):
    chat_id = message.chat.id
    appeal = appeal_dict[chat_id]
    try:
        if message.text == "Изменить тему 🔄":
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.KeyboardButton("Разбросанный мусор"), types.KeyboardButton("Не горит фонарь"),
                types.KeyboardButton("Вандализм"),          types.KeyboardButton("Не пришёл автобус"),
                types.KeyboardButton("Нет расписания"),     types.KeyboardButton("Плохое состояние дороги"),
                types.KeyboardButton("Нет пандуса"),        types.KeyboardButton("Оголённые провода"),
                types.KeyboardButton("Бродячие собаки"),    types.KeyboardButton("Просрочка"),
            )
            msg = bot.reply_to(message, """\
На какую тему вам помочь составить обращение?

`Татьяна`
    """, reply_markup=keyboard)
            bot.register_next_step_handler(msg, confirm_theme_step)
            return
        elif message.text == "Правильно ✅":
            if not appeal.theme in [
                    "Разбросанный мусор", "Не горит фонарь",
                    "Вандализм",          "Не пришёл автобус",
                    "Нет расписания",     "Плохое состояние дороги",
                    "Нет пандуса",        "Оголённые провода",
                    "Бродячие собаки",    "Просрочка"
                ]:
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(
                    types.KeyboardButton("Разбросанный мусор"), types.KeyboardButton("Не горит фонарь"),
                    types.KeyboardButton("Вандализм"),          types.KeyboardButton("Не пришёл автобус"),
                    types.KeyboardButton("Нет расписания"),     types.KeyboardButton("Плохое состояние дороги"),
                    types.KeyboardButton("Нет пандуса"),        types.KeyboardButton("Оголённые провода"),
                    types.KeyboardButton("Бродячие собаки"),    types.KeyboardButton("Просрочка"),
                )
                msg = bot.reply_to(message, """\
    К сожалению, пока я не могу помочь вам с этим вопросом.

    Может, составим обращение на другую тему?

    `Татьяна`
    """, reply_markup=keyboard)
                bot.register_next_step_handler(msg, confirm_theme_step)
                return
            msg = bot.reply_to(message, """\
Пришлите мне, пожалуйста, адрес места, которое я укажу в обращении.

Можно прислать несколько адресов — каждый адрес на отдельной строке.

`Татьяна`
    """, reply_markup=json.dumps({'remove_keyboard': True}))
            bot.register_next_step_handler(msg, confirm_address_step)
            return
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Правильно ✅", "Изменить тему 🔄")
            msg = bot.reply_to(message, """\
Будем составлять обращение на тему «{}», правильно?

`Татьяна`
""".format(appeal.theme), reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_theme_step)
        return
    except Exception as e:
       bot.reply_to(message, "Что-то пошло не так", reply_markup=json.dumps({'remove_keyboard': True}))


def confirm_address_step(message):
    try:
        chat_id = message.chat.id
        appeal = appeal_dict[chat_id]
        appeal.address = message.text
        if len(appeal.address.split("\n")) == 1:
            address        = appeal.address.splitlines()
            address_string = ["этот", "адрес"]
            address_string.append("•" + " " + appeal.address)
        elif len(appeal.address.split("\n")) > 1:
            address        = appeal.address.splitlines()
            address_string = ["эти", "адреса"]
            address_string.append("\n".join(list(map(lambda orig_string: "•" + " " + orig_string, address))))
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Правильно ✅", "Изменить {} 🔄".format(address_string[1]))
        msg = bot.reply_to(message, """\
Я укажу в обращении {} {}:

_{}_

Я всё правильно поняла?

`Татьяна`
""".format(address_string[0],
           address_string[1],
           address_string[2]), reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_address_step)
        return
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так", reply_markup=json.dumps({'remove_keyboard': True}))


def process_address_step(message):
    chat_id = message.chat.id
    appeal = appeal_dict[chat_id]
    try:
        if (message.text == "Изменить адрес 🔄"
        or message.text == "Изменить адреса 🔄"):
            msg = bot.reply_to(message, """\
Пришлите мне, пожалуйста, адрес места, которое я укажу в обращении.

Можно прислать несколько адресов — каждый адрес на отдельной строке.

`Татьяна`
    """, reply_markup=json.dumps({'remove_keyboard': True}))
            bot.register_next_step_handler(msg, confirm_address_step)
            return
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("У меня нет фотографии 📸")
            msg = bot.reply_to(message, """\
Почти готово!

Теперь отправьте мне фотографию, на которой видна проблема.

Если фотографии нет, нажмите _«У меня нет фотографии 📸»_.

`Татьяна`
""".format(appeal.theme), reply_markup=keyboard)
            bot.register_next_step_handler(msg, confirm_attachment_step)
            return
    except Exception as e:
       bot.reply_to(message, "Что-то пошло не так", reply_markup=json.dumps({'remove_keyboard': True}))


# attachments!
def confirm_attachment_step(message):
    try:
        chat_id = message.chat.id
        appeal = appeal_dict[chat_id]
        appeal.address = message.text
        if len(appeal.address.split("\n")) == 1:
            address        = appeal.address.splitlines()
            address_string = ["этот", "адрес"]
            address_string.append("•" + " " + appeal.address)
        elif len(appeal.address.split("\n")) > 1:
            address        = appeal.address.splitlines()
            address_string = ["эти", "адреса"]
            address_string.append("\n".join(list(map(lambda orig_string: "•" + " " + orig_string, address))))
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Правильно ✅", "Изменить {} 🔄".format(address_string[1]))
        msg = bot.reply_to(message, """\
Я укажу в обращении {} {}:

_{}_

Я всё правильно поняла?

`Татьяна`
""".format(address_string[0],
           address_string[1],
           address_string[2]), reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_address_step)
        return
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так", reply_markup=json.dumps({'remove_keyboard': True}))


def process_attachment_step(message):
    chat_id = message.chat.id
    appeal = appeal_dict[chat_id]
    try:
        if (message.text == "Изменить адрес 🔄"
        or message.text == "Изменить адреса 🔄"):
            msg = bot.reply_to(message, """\
Пришлите мне, пожалуйста, адрес места, которое я укажу в обращении.

Можно прислать несколько адресов — каждый адрес на отдельной строке.

`Татьяна`
    """, reply_markup=json.dumps({'remove_keyboard': True}))
            bot.register_next_step_handler(msg, confirm_address_step)
            return
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("У меня нет фотографии 📸")
            msg = bot.reply_to(message, """\
Почти готово!

Теперь отправьте мне фотографию, на которой видна проблема.

Если фотографии нет, нажмите _«У меня нет фотографии 📸»_.

`Татьяна`
""".format(appeal.theme), reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_attachment_step)
            return
    except Exception as e:
       bot.reply_to(message, "Что-то пошло не так", reply_markup=json.dumps({'remove_keyboard': True}))


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = appeal_dict[chat_id]
        if (sex == u"Male") or (sex == u"Female"):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, "Nice to meet you " + user.name + "\n Age:" + str(user.age) + "\n Sex:" + user.sex)
    except Exception as e:
        bot.reply_to(message, "oooops", reply_markup=json.dumps({'remove_keyboard': True}))


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# Добавить функцию добавления электронного адреса для получения копии письма
# + добавления в табличку комментария, что нужен ответ на адрес эл. почты

# Хотите посмотреть, что получилось? <Отправляем> <Предпросмотр>

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()

# subject, message = generateMessage("trash", "Автобусная остановка «Текстильщики»\nАвтобусная остановка «Дом быта»\nАвтобусная остановка «Дом № 15»\nАвтобусная остановка «Фирма Ока»\nАвтобусная остановка «Общежития»")
# sendMessage(subject, message)
