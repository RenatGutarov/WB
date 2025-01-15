import os
from datetime import datetime, timedelta
import requests
import math
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from babel.dates import format_date
from worksheet import Constants, get_sheet_yesterday, get_general

sheet_name_denis = 'Прибыль LIVE Коротченков'

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)


load_dotenv()

groups = ['57','162']

revenue_saleprice = []

time= (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")

revenue_saleprice.append(time)

previous_day = (datetime.now() - timedelta(days=1))

day_of_week = format_date(previous_day, format='EEEE', locale='ru_RU')

revenue_saleprice.append(day_of_week)

ids_danila = ['b38','c38','d38','e38','f38','g38','h38','i38','j38','k38','l38','m38','n38','o38',]

for ids in ids_danila:
    result = get_sheet_yesterday(Constants.DANILA).acell(ids).value

    if ids == 'b38' or ids == 'e38' or ids == 'l38' or ids == 'n38':
        result = result[2:-3]
        result = result.replace('\xa0', '')
        revenue_saleprice.append(int(result))

    elif ids == 'c38':
        revenue_saleprice.append(int(result))

    elif ids == 'd38' or ids == 'g38' or ids == 'h38' or ids == 'i38' or ids == 'j38':
        result = result[:-4]
        result = int(result) / 100
        revenue_saleprice.append(result)

    elif ids == 'f38':
        revenue_saleprice.append(result[:-3])

    elif ids == 'k38' or ids == 'm38' or ids == 'o38':
        result = result[:-1].replace(',','.')
        revenue_saleprice.append(float(result) / 100)


print(revenue_saleprice)

for group in groups:

    time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # second_url = 'https://mpstats.io/api/wb/get/identical?&path=151784447&fbs=1' - как появится client_sale брать отсюда

    main_url = f'https://mpstats.io/api/wb/get/subject/by_date?groupBy=day&path={group}'

    params = {"d1": time, "d2": time}

    header = {
    "Content-Type": "application/json",
    "X-Mpstats-TOKEN": os.getenv('XMPSTASTOKEN')
    }

    response = requests.get(url=main_url,headers=header, params = params)
    # response2 = requests.get(url = second_url, headers=header,params = params)
    # print(response2.json())
    data = response.json()

    for item in data:
        revenue = item['revenue']
        sale_price = item['avg_sale_price']
        revenue_saleprice.append(revenue)
        revenue_saleprice.append(math.floor(sale_price))

revenue_saleprice.append(0.21)
revenue_saleprice.append(4)
print(revenue_saleprice)

sh_danila = get_general(Constants.DANILA)
#
# sh_denis = client.open(sheet_name_denis).worksheet('Общее')
#

#sh_danila.update([revenue_saleprice],'b3:y3')

sh_danila.insert_row(revenue_saleprice,3)

# sh_denis.update([revenue_saleprice[2:]],'t3:y3')

