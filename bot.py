import telebot
import os
from WB_API import update_prices, slovar
from MPSTATS_API import update_conc
from base_info import get_articles
from worksheet import get_sheet, Constants
from keyboards import  markup_report_danila, markup_start, markup_report_denis
from otchet import otchet

sheet_name = 'Анализ конкурентов'

API_TOKEN = os.getenv('API_TOKEN')

CHAT_ID_BOT = os.getenv('CHAT_ID_BOT')

bot = telebot.TeleBot(API_TOKEN)


def process_report_view_danila():
    value = get_sheet(Constants.DANILA).acell('s40').value
    if value is not None:
        return value
    else:
        value ='Ячейка пустая'
        return value

def process_report_view_denis():
    value = get_sheet(Constants.DENIS).acell('s28').value
    if value is not None:
        return value
    else:
        value ='Ячейка пустая'
        return value

@bot.message_handler(commands=['start'])
def get_new_prices(message):
    bot.send_message(message.chat.id, 'Автоматизированные таблички by Гутаров', reply_markup = markup_start)

@bot.message_handler(commands=['report_danila'])
def get_new_report_danila(message):
    bot.send_message(message.chat.id,'Последнее действие Грищенко',reply_markup= markup_report_danila)

@bot.message_handler(commands= ['report_denis'])
def get_new_report_denis(message):
    bot.send_message(message.chat.id, 'Последнее действие Коротченков', reply_markup=markup_report_denis)

@bot.callback_query_handler(func = lambda call: True)
def prices_and_reports(call):
    if call.data == 'update prices':
        bot.send_message(call.message.chat.id,'Началось обновление, ожидайте')
        update_prices(slovar)
        bot.send_message(call.message.chat.id,'Цены обновились',reply_markup=markup_start)

    elif call.data == 'update conc':
        bot.send_message(call.message.chat.id,'Началось обновление, ожидайте')
        data_articles = get_articles()
        update_conc(data_articles, sheet_name,)
        bot.send_message(call.message.chat.id,'Анализ конкурентов обновлен',reply_markup=markup_start)

    elif call.data == 'make otchet':
        bot.send_message(call.message.chat.id,'Отчет составляется, ожидайте')
        otchet()
        bot.send_message(call.message.chat.id,'Отчет сделан', reply_markup=markup_start)

    elif call.data == 'report create danila':
        bot.send_message(call.message.chat.id,'Введите что добавить в последнее действие')
        bot.register_next_step_handler(call.message, process_report_danila)

    elif call.data == 'report delete danila':
        get_sheet(Constants.DANILA).batch_clear(['s40'])
        bot.send_message(call.message.chat.id,'Ячейка очищена',reply_markup=markup_report_danila)

    elif call.data == 'report add danila':
        bot.send_message(call.message.chat.id,'Введите что добавить')
        bot.register_next_step_handler(call.message, process_report_add)

    elif call.data =='report view danila':
        lst = process_report_view_danila()
        bot.send_message(call.message.chat.id, lst, reply_markup=markup_report_danila)

    elif call.data == 'report create denis':
        bot.send_message(call.message.chat.id,'Введите что добавить в последнее действие')
        bot.register_next_step_handler(call.message,process_report_denis)

    elif call.data == 'report delete denis':
        get_sheet(Constants.DENIS).batch_clear(['s28'])
        bot.send_message(call.message.chat.id,'Ячейка очищена',reply_markup=markup_report_denis)

    elif call.data == 'report add denis':
        bot.send_message(call.message.chat.id, 'Введите что добавить')
        bot.register_next_step_handler(call.message, process_report_add_denis)

    elif call.data =='report view denis':
        lst = process_report_view_denis()
        bot.send_message(call.message.chat.id,lst,reply_markup=markup_report_denis)





def process_report_denis(message):
    user_input = message.text
    get_sheet(Constants.DENIS).update([[user_input]],'s28')
    bot.send_message(message.chat.id,'Данные добавлены в таблицу!',reply_markup=markup_report_denis)

def process_report_add_denis(message):
    user_input = message.text
    current_value = get_sheet(Constants.DENIS).acell('s28').value
    if current_value is not None:
        update_value = f'{current_value}, {user_input}'
        get_sheet(Constants.DENIS).update([[update_value]], 's28')
        bot.send_message(message.chat.id, 'Добавлено!',reply_markup = markup_report_denis)
    else:
        update_value = f'{user_input}'
        get_sheet(Constants.DENIS).update([[update_value]], 's28')
        bot.send_message(message.chat.id, 'Добавлено!',reply_markup= markup_report_denis)

def process_report_danila(message):
    user_input = message.text
    get_sheet(Constants.DANILA).update([[user_input]],'s40')
    bot.send_message(message.chat.id, 'Данные добавлены в таблицу!',reply_markup= markup_report_danila)

def process_report_add(message):
    user_input = message.text
    current_value = get_sheet(Constants.DANILA).acell('s40').value
    if current_value is not None:
        update_value = f'{current_value}, {user_input}'
        get_sheet(Constants.DANILA).update([[update_value]],'s40')
        bot.send_message(message.chat.id,'Добавлено!',reply_markup=markup_report_danila)
    else:
        update_value = f'{user_input}'
        get_sheet(Constants.DANILA).update([[update_value]], 's40')
        bot.send_message(message.chat.id, 'Добавлено!',reply_markup=markup_report_danila)

bot.polling(none_stop= True)