import telebot
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID_DANILA = os.getenv('CHAT_ID')
CHAT_ID_RENAT = os.getenv('CHAT_ID_RENAT')

bot = telebot.TeleBot(API_TOKEN)

def send_message(text):
    bot.send_message(CHAT_ID_DANILA, text)

def send_message_renat(text):
    bot.send_message(CHAT_ID_RENAT,text)

