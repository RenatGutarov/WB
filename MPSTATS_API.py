import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv
import os
from gspread.utils import rowcol_to_a1, ValueInputOption
from datetime import datetime, timedelta
from messaging import send_message,send_message_renat
import time
from base_info import get_articles

load_dotenv()


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)


def fill_sheet(articles):
    first_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

    second_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
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
            "X-Mpstats-TOKEN": os.getenv('XMPSTASTOKEN')
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
    first_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

    second_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    max_retries = 5

    retries = 0

    date_list = []

    while retries < max_retries:

        try:

            current_date = datetime.strptime(first_date, "%Y-%m-%d")

            end_date = datetime.strptime(second_date, "%Y-%m-%d")

            while current_date <= end_date:
                date_list.append(current_date.strftime("%Y-%m-%d"))

                current_date += timedelta(days=1)

            for i, articles in enumerate(data_articles):

                sh = client.open(sheet_name).get_worksheet(i)

                r = [[str(article['brand']) + ' ' + str(article['id']) for article in articles]]

                start_row_for_date = 3

                end_row_for_date = start_row_for_date + len(date_list) - 1

                if len(date_list) > 14:
                    date_list = date_list[:14]

                start_row = 2

                start_col = 2

                end_col = start_col + len(r[0]) - 1

                letter = rowcol_to_a1(start_row, end_col)

                date_range = [[date] for date in date_list]

                time.sleep(5)

                image_formulas, result = fill_sheet(articles)

                sh.update([image_formulas], f'B1:{rowcol_to_a1(1, start_col + len(image_formulas) - 1)}',
                          value_input_option=ValueInputOption.user_entered)

                letter = rowcol_to_a1(len(result[0]) + 2, len(result) + 1)

                sh.update(list(zip(*result)), f"B3:{letter}")

                sh.update(date_range, f'A{start_row_for_date}:A{end_row_for_date}')

                sh.update(r, f'B{start_row}:{letter}')

                update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                sh.update([[update_time]], "A19")

            send_message('Анализ конкурентов обновлен')

            break

        except Exception as e:

            retries += 1

            send_message_renat(f'Ошибка {e}, перезапуск')

            time.sleep(120)

    if retries == max_retries:
        send_message_renat('Конкуренты сломаны')


if __name__ == '__main__':
    data_article = get_articles()

    sheet = "Анализ конкурентов"

    update_conc(data_article, sheet)
