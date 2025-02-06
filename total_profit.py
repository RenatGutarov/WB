import os
from datetime import datetime, timedelta
import requests
import math
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from babel.dates import format_date

from worksheet import get_sheet_yesterday
from spp import spp_finder
from meteo import get_temp


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)

load_dotenv()

def get_data(name):
    sh_ip_get = get_sheet_yesterday(name)
    rows_ip = sh_ip_get.get('1:100')
    return rows_ip



def process_rows(rows):
    result = []
    time = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
    result.append(time)
    previous_day = (datetime.now() - timedelta(days=1))
    day_of_week = format_date(previous_day, format='EEEE', locale='ru_RU')
    result.append(day_of_week)
    for row in rows:
        if 'ИТОГО' in row:
            # Находим индекс 'ИТОГО' и берем следующий элемент
            index = row.index('ИТОГО')
            if (index + 1 < len(row) and
                    index + 2 < len(row) and
                    index + 3 < len(row) and
                    index + 4 < len(row) and
                    index + 5 < len(row) and
                    index + 6 < len(row) and
                    index + 7 < len(row) and
                    index + 8 < len(row) and
                    index + 9 < len(row) and
                    index + 10 < len(row) and
                    index + 11 < len(row) and
                    index + 12 < len(row) and
                    index + 13 < len(row) and
                    index + 14 < len(row)
            ):
                # Заказы
                revenue_str = row[index + 1]
                if len(revenue_str) > 9:
                    revenue_str = revenue_str[2:-3]
                    revenue_str_cleaned = revenue_str.replace('\xa0', '').strip()
                    result.append(int(revenue_str_cleaned))
                else:
                    revenue_str = revenue_str[2:]
                    revenue_str_cleaned = revenue_str.replace('\xa0', '').strip()
                    result.append(int(revenue_str_cleaned))
                # Штуки
                pieces = row[index + 2]
                if len(pieces) > 3:
                    pieces = pieces[:-3]
                    pieces = int(pieces)
                    result.append(pieces)
                else:
                    pieces = int(pieces)
                    result.append(pieces)
                # ПВ
                procent = row[index + 3]
                if len(procent) > 3:
                    procent = procent[:-4]
                    procent = int(procent) / 100
                    result.append(procent)
                else:
                    procent = procent[:-1]
                    procent = int(procent) / 100
                    result.append(procent)
                # Выкупят
                revenue_str4 = row[index + 4]
                if len(revenue_str4) > 9:
                    revenue_str4 = revenue_str4[2:-3]
                    revenue_str_cleaned = revenue_str4.replace('\xa0', '').strip()
                    result.append(int(revenue_str_cleaned))
                else:
                    revenue_str4 = revenue_str4[2:]
                    revenue_str_cleaned = revenue_str4.replace('\xa0', '').strip()
                    result.append(int(revenue_str_cleaned))
                # Выкупят штук
                will_buy = row[index + 5]
                if len(will_buy) > 3:
                    will_buy = will_buy[:-3]
                    result.append(will_buy)
                else:
                    result.append(will_buy)
                # Себес
                cost_price_proc = row[index + 6]
                if len(cost_price_proc) > 3:
                    cost_price_proc = cost_price_proc[:-4]
                    cost_price_proc = int(cost_price_proc) / 100
                    result.append(cost_price_proc)
                else:
                    cost_price_proc = cost_price_proc[:-1]
                    cost_price_proc = int(cost_price_proc) / 100
                    result.append(cost_price_proc)
                # Комиссия
                commission = row[index + 7]
                if len(commission) > 3:
                    commission = commission[:-4]
                    commission = int(commission) / 100
                    result.append(commission)
                else:
                    commission = commission[:-1]
                    commission = int(commission) / 100
                    result.append(commission)
                # Логистика
                logistic = row[index + 8]
                if len(logistic) > 3:
                    logistic = logistic[:-4]
                    logistic = int(logistic) / 100
                    result.append(logistic)
                else:
                    logistic = logistic[:-1]
                    logistic = int(logistic) / 100
                    result.append(logistic)
                # Налог
                tax = row[index + 9]
                if len(tax) > 3:
                    tax = tax[:-4]
                    tax = int(tax) / 100
                    result.append(tax)
                else:
                    tax = tax[:-1]
                    tax = int(tax) / 100
                    result.append(tax)
                # Хранение
                storage = row[index + 10]
                storage = storage[:-1].replace(',', '.')
                result.append(float(storage) / 100)
                # Реклама
                add = row[index + 11]
                if len(add) > 9:
                    add = add[2:-3]
                    add = add.replace('\xa0', '').strip()
                    result.append(int(add))
                else:
                    add = add[2:]
                    add = add.replace('\xa0', '').strip()
                    result.append(int(add))
                # DRR
                drr = row[index + 12]
                drr = drr[:-1].replace(',', '.')
                result.append(float(drr) / 100)
                # Прибыль
                profit = row[index + 13]
                if len(profit) > 9:
                    profit = profit[2:-3]
                    profit = profit.replace('\xa0', '')
                    result.append(int(profit))
                else:
                    profit = profit[2:]
                    profit = profit.replace('\xa0', '')
                    result.append(int(profit))
                # Рентабельность
                profitability = row[index + 14]
                profitability = profitability[:-1].replace(',', '.')
                result.append(float(profitability) / 100)
                print(result)
    groups = ['57','162']

    for group in groups:
        print(f'Началась группа {group}')
        time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # #     # second_url = 'https://mpstats.io/api/wb/get/identical?&path=151784447&fbs=1' - как появится client_sale брать отсюда

        main_url = f'https://mpstats.io/api/wb/get/subject/by_date?groupBy=day&path={group}'

        params = {"d1": time, "d2": time}

        header = {
          "Content-Type": "application/json",
          "X-Mpstats-TOKEN": os.getenv('XMPSTASTOKEN')
        }

        response = requests.get(url=main_url,headers=header, params = params)
        print(response)
    # #     # response2 = requests.get(url = second_url, headers=header,params = params)
    # #     # print(response2.json())
        data = response.json()

        for index,item in enumerate(data):
              revenue = item['revenue']
              sale_price = item['avg_sale_price']
              result.append(revenue)
              result.append(math.floor(sale_price))
    result.append(spp_finder() / 100)
    result.append(get_temp())

    return result

def process_rows_delta(rows):
    result = []
    for row in rows:
        if 'ИТОГО' in row:
            index = row.index('ИТОГО')
            if index + 13 < len(row):
                profit = row[index + 13]
                profit = profit[2:-3]
                profit = profit.replace('\xa0', '')
                result.append(int(profit))
    return result


def process_rows_actions(rows):
    result = []
    for row in rows:
        if 'Общая картина действий' in row:
            index = row.index('Общая картина действий')
            if index + 1 < len(row):
                actions = row[index + 1]
                result.append(actions)
    return result






