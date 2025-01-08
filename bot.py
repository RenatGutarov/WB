import telebot
import os
from telebot import types
from WB_API import update_prices, slovar
from MPSTATS_API import update_conc
from base_info import get_articles
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import gspread

from keyboards import  markup_report_danila, markup_start, markup_report_denis

sheet_name = 'Анализ конкурентов'

API_TOKEN = os.getenv('API_TOKEN')

CHAT_ID_BOT = os.getenv('CHAT_ID_BOT')

bot = telebot.TeleBot(API_TOKEN)

scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",]

time_for_sheet = (datetime.now()).strftime("%d-%m-%Y")

current_sheet = time_for_sheet.replace('-', '.')

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)

sh_danila = client.open("Прибыль LIVE Грищенко")

sh_denis = client.open("Прибыль LIVE Коротченков")

worksheet_danila = sh_danila.worksheet(current_sheet)

worksheet_denis = sh_denis.worksheet(current_sheet)

def process_report_view_danila():
    value = worksheet_danila.acell('s40').value
    if value is not None:
        return value
    else:
        value ='Ячейка пустая'
        return value

def process_report_view_denis():
    value = worksheet_denis.acell('s28').value
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
        bot.send_message(CHAT_ID_BOT,'Началось обновление, ожидайте')
        update_prices(slovar)
        bot.send_message(CHAT_ID_BOT,'Цены обновились')

    elif call.data == 'update conc':
        bot.send_message(CHAT_ID_BOT,'Началось обновление, ожидайте')
        data_articles = get_articles()
        update_conc(data_articles, sheet_name,)
        bot.send_message(CHAT_ID_BOT,'Анализ конкурентов обновлен')

    elif call.data == 'report create danila':
        bot.send_message(CHAT_ID_BOT,'Введите что добавить в последнее действие')
        bot.register_next_step_handler(call.message, process_report_danila)

    elif call.data == 'report delete danila':
        worksheet_danila.batch_clear(['s40'])
        bot.send_message(CHAT_ID_BOT,'Ячейка очищена',reply_markup=markup_report_danila)

    elif call.data == 'report add danila':
        bot.send_message(CHAT_ID_BOT,'Введите что добавить')
        bot.register_next_step_handler(call.message, process_report_add)

    elif call.data =='report view danila':
        lst = process_report_view_danila()
        bot.send_message(CHAT_ID_BOT, lst, reply_markup=markup_report_danila)

    elif call.data == 'report create denis':
        bot.send_message(CHAT_ID_BOT,'Введите что добавить в последнее действие')
        bot.register_next_step_handler(call.message,process_report_denis)

    elif call.data == 'report delete denis':
        worksheet_denis.batch_clear(['s28'])
        bot.send_message(CHAT_ID_BOT,'Ячейка очищена',reply_markup=markup_report_denis)

    elif call.data == 'report add denis':
        bot.send_message(CHAT_ID_BOT, 'Введите что добавить')
        bot.register_next_step_handler(call.message, process_report_add_denis)

    elif call.data =='report view denis':
        lst = process_report_view_denis()
        bot.send_message(CHAT_ID_BOT,lst,reply_markup=markup_report_denis)





def process_report_denis(message):
    user_input = message.text
    worksheet_denis.update([[user_input]],'s28')
    bot.send_message(CHAT_ID_BOT,'Данные добавлены в таблицу!',reply_markup=markup_report_denis)

def process_report_add_denis(message):
    user_input = message.text
    current_value = worksheet_denis.acell('s28').value
    if current_value is not None:
        update_value = f'{current_value}, {user_input}'
        worksheet_denis.update([[update_value]], 's28')
        bot.send_message(CHAT_ID_BOT, 'Добавлено!',markup_report_denis)
    else:
        update_value = f'{user_input}'
        worksheet_denis.update([[update_value]], 's28')
        bot.send_message(CHAT_ID_BOT, 'Добавлено!',markup_report_denis)

def process_report_danila(message):
    user_input = message.text
    worksheet_danila.update([[user_input]],'s40')
    bot.send_message(CHAT_ID_BOT, 'Данные добавлены в таблицу!',reply_markup= markup_report_danila)

def process_report_add(message):
    user_input = message.text
    current_value = worksheet_danila.acell('s40').value
    if current_value is not None:
        update_value = f'{current_value}, {user_input}'
        worksheet_danila.update([[update_value]],'s40')
        bot.send_message(CHAT_ID_BOT,'Добавлено!',reply_markup=markup_report_danila)
    else:
        update_value = f'{user_input}'
        worksheet_danila.update([[update_value]], 's40')
        bot.send_message(CHAT_ID_BOT, 'Добавлено!',reply_markup=markup_report_danila)

bot.polling(none_stop= True)