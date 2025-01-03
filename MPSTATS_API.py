import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv
import os
from gspread.utils import rowcol_to_a1, ValueInputOption
from datetime import datetime, timedelta
from base_info import get_articles
import schedule
import telebot

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(API_TOKEN)

first_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
second_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def send_message(text):
    bot.send_message(CHAT_ID, text)


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)


def fill_sheet(articles):
    sheet_data = []
    image_formulas = []

    for article in articles:
        image_url = article.get('photo')
        image_formula = f'=IMAGE("https:{image_url}")' if image_url else ''

        image_formulas.append(image_formula)

        url = f"https://mpstats.io/api/wb/get/item/{article['id']}/sales"
        params = {"d1": first_date, "d2": second_date}
        header = {
            "Content-Type": "application/json",
            "X-Mpstats-TOKEN":os.getenv('XMPSTASTOKEN')
        }
        response = requests.get(url=url, params=params, headers=header, timeout=30)
        final_price_dict = response.json()
        result = []
        for revenue in final_price_dict:
            sale = revenue["sales"]
            final_price = revenue["final_price"]
            final_revenue = sale * final_price
            result.append(final_revenue)
        result.reverse()

        sheet_data.append(result)

    return image_formulas, sheet_data


def update_conc(data_articles, sheet_name, ):
    for i, articles in enumerate(data_articles):
        sh = client.open(sheet_name).get_worksheet(i)
        r = [[str(article['brand']) + ' ' + str(article['id']) for article in articles]]
        start_row = 2
        start_col = 2
        end_col = start_col + len(r[0]) - 1
        letter = rowcol_to_a1(start_row, end_col)
        sh.update(r, f'B{start_row}:{letter}')
        image_formulas, result = fill_sheet(articles)
        sh.update([image_formulas], f'B1:{rowcol_to_a1(1, start_col + len(image_formulas) - 1)}',
                  value_input_option=ValueInputOption.user_entered)
        letter = rowcol_to_a1(len(result[0]) + 2, len(result) + 1)
        sh.update(list(zip(*result)), f"B3:{letter}")
    send_message('Анализ конкурентов обновлен')


if __name__ == '__main__':

    data_article = get_articles()

    sheet = "Анализ конкурентов"

    first_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

    second_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    update_conc(data_article, sheet)

    # schedule.every().day.at('14:35').do(update_conc)
