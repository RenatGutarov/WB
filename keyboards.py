from telebot import types
import telebot
import os
from telebot.util import quick_markup


API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


markup_start = quick_markup({
    'Обновить табличку цен': {'callback_data':'update prices'},
    'Обновить анализ конкурентов':{'callback_data':'update conc'},
    'Сделать отчет за вчера':{'callback_data':'make otchet'}
}, row_width=2)

markup_report_danila = quick_markup({
    'Добавить':{'callback_data':'report create danila'},
    'Очистить':{'callback_data':'report delete danila'},
    'Добавить к уже имеющимся': {'callback_data': 'report add danila'},
    'Текущее значение ячейки ': {'callback_data': 'report view danila'}},
    row_width=2
)

markup_report_denis = quick_markup({
    'Добавить':{'callback_data':'report create denis'},
    'Очистить':{'callback_data':'report delete denis'},
    'Добавить к уже имеющимся': {'callback_data': 'report add denis'},
    'Текущее значение ячейки ': {'callback_data': 'report view denis'}},
    row_width=2
)