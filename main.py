import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv
import os

load_dotenv()

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:\\Users\\gutar\\Downloads\\my-project-prices-438418-bdb101fef134.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Конкуренты цены 2.0").sheet1

headers = {
    "Content-Type": 'application/json',
    "X-Mpstats-TOKEN": os.getenv('MPSTATS_TOKEN')
}

art = [214791724, 214793869, 208934987]

# Начинаем с 2-й строки
row_index = 2

for i in art:
    url = f"https://mpstats.io/api/wb/get/item/{i}/sales"
    result = requests.get(url=url, headers=headers)

    if result.status_code == 200:
        data = result.json()[0]['final_price']

        # Запись данных в столбцы B и F
        if row_index <= 14:  # Убедитесь, что не превышаете 14-ю строку
            sheet.update_cell(row_index, 2, data)  # Запись в столбец B
            sheet.update_cell(row_index, 6, data)  # Запись в столбец F (столбец 6)
            row_index += 1  # Переход к следующей строке
        else:
            break  # Выход, если достигаем 14-й строки
    else:
        print(f"Error fetching data for {i}: {result.status_code}")

print("Данные записаны в Google Таблицу!")

