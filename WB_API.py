import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv
import os
import math
import time
import schedule

from MPSTATS_API import send_message

load_dotenv()



scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)

slovar = {
    0: [
        [151784447, 158392610, 165972566, 165972565, 181283677],
        [214791724, 214793869, 214799012, 214903622, 208934987],
        [165374615, 168258699, 168259885, 176355393, 171232105],
        [145000904, 64274890, 160003929, None, None],
        [203597298, 195325187, 195918811, None, None],
        [238455525, 255514974, 221812197, None, 255514720],
        [161480453, 143620679, 161480454, 179748809, 161418674],
        [154131722, 134614055, 152427337, 155449102, 143973840],
        [193739442, 59175871, 146355526, None, None],
        [None, 174553696, None, None, None],
        [None, 149127096, None, None, None],
        [197799205, None, None, None, None],
        [None, 209621295, 218360469, None, None],
    ],
    1: [
        [243117262, 228502034, 243180428, 243119074, 228502033, 243181642],
        [168423784, 141940975, 159271393, 168423785, 152644637, 159271394],
        [None, 189027878, None, None, None, None],
        [None, None, None, None, None, None],
        [None, 154844674, None, None, None, None],
        [221582470, None, None, None, None, None],
    ],
    2: [
        [102658625],
        [96815935],
        [188037949],
        [120714921],
        [70722699],
        [183518683],
        [175928419],
        [178444557],
        [247782810],
        [252918040],
        [175941311],
        [174007288],
    ],
    3: [
        [133981084],
        [191933262],
        [255040745],
        [259028257],
        [175505993],
        [172427752],
        [39685148],
        [182378668],
        [180817576],
        [183512028],
        [195656486],
    ],
    4: [
        [45140119],
        [252809729],
        [180688782],
        [102513410],
        [135675780],
        [247275282],
        [175467193],
        [252927808],
        [262046768],
    ],
}


sizes_names = [
    "0",
    "XXS",
    "2XS",
    "XS",
    "S",
    "M",
    "L",
    "XL",
    "2XL",
    "3XL",
    "4XL",
    "5XL",
    "6XL",
    "7XL",
    "8XL",
    "9XL",
    "10XL",
]


def fill_sheet(sheet, arts):
    for row_index, art in enumerate(arts, 2):
        for i, article in enumerate(art, 2):
            if article is None:
                continue
            url = f"https://card.wb.ru/cards/v2/detail?dest=-1255987&nm={article}"
            response = requests.get(url=url)

            if response.status_code != 200:
                continue
            sizes = response.json()["data"]["products"][0]["sizes"]
            result = []
            for size_name in sizes_names:
                for size in sizes:
                    if not size.get("price") or size["origName"] != size_name:
                        continue
                    price = str(math.floor(size["price"]["total"] // 100 * 0.97))
                    time.sleep(1)
                    if price not in result:
                        result.append(price)
            result = "-".join(result)

            sheet.update_cell(row_index, i, result)

def update_prices(slovar):
    print('Цены обновляются')
    for key, value in slovar.items():
        sh = client.open("Конкуренты цены 2.0")
        sheet = sh.get_worksheet(key)
        fill_sheet(sheet, value)
    send_message('Табличка цен обновлена')

if __name__ == '__main__':
    update_prices(slovar)


# def schedule_update():
#     update_prices(slovar)
#
# schedule.every().day.at('15:32').do(schedule_update)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)