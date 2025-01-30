import os
from datetime import datetime, timedelta
import requests
import math
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from babel.dates import format_date
from worksheet import Constants, get_sheet_yesterday, get_general
from spp import spp_finder
from meteo import get_temp

sheet_name_denis = 'Прибыль LIVE Коротченков'

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)


load_dotenv()

groups = ['57','162']

revenue_saleprice_danila= []

revenue_saleprice_denis = []

time= (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")

revenue_saleprice_danila.append(time)
revenue_saleprice_denis.append(time)

previous_day = (datetime.now() - timedelta(days=1))

day_of_week = format_date(previous_day, format='EEEE', locale='ru_RU')

revenue_saleprice_danila.append(day_of_week)
revenue_saleprice_denis.append(day_of_week)

ids_danila = ['b38','c38','d38','e38','f38','g38','h38','i38','j38','k38','l38','m38','n38','o38',]

for ids in ids_danila:
    result = get_sheet_yesterday(Constants.DANILA).acell(ids).value

    if ids == 'b38' or ids == 'e38' or ids == 'l38' or ids == 'n38':
        result = result[2:-3]
        result = result.replace('\xa0', '')
        revenue_saleprice_danila.append(int(result))

    elif ids == 'c38':
        revenue_saleprice_danila.append(int(result))

    elif ids == 'd38' or ids == 'g38' or ids == 'h38' or ids == 'i38' or ids == 'j38':
        result = result[:-4]
        result = int(result) / 100
        revenue_saleprice_danila.append(result)

    elif ids == 'f38':
        revenue_saleprice_danila.append(result[:-3])

    elif ids == 'k38' or ids == 'm38' or ids == 'o38':
        result = result[:-1].replace(',','.')
        revenue_saleprice_danila.append(float(result) / 100)

ids_denis = ['b18','c18','d18','e18','f18','g18','h18','i18','j18','k18','l18','m18','n18','o18']

for ids in ids_denis:
    result = get_sheet_yesterday(Constants.DENIS).acell(ids).value

    if ids == 'b18' or ids == 'e18' or ids == 'l18' or ids == 'n18':
        result = result[2:-3]
        result = result.replace('\xa0', '')
        revenue_saleprice_denis.append(int(result))

    elif ids == 'c18':
        revenue_saleprice_denis.append(int(result))

    elif ids == 'd18' or ids == 'g18' or ids == 'h18' or ids == 'i18' or ids == 'j18':
        result = result[:-4]
        result = int(result) / 100
        revenue_saleprice_denis.append(result)


    elif ids == 'f18':
        revenue_saleprice_denis.append(result[:-3])

    elif ids == 'k18' or ids == 'm18' or ids == 'o18':
        result = result[:-1].replace(',', '.')
        revenue_saleprice_denis.append(float(result) / 100)

print('Отчет ИП Грищенко:', revenue_saleprice_danila)
print('Отчет ИП Коротченков:', revenue_saleprice_denis)

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

    for index,item in enumerate(data):
        revenue = item['revenue']
        sale_price = item['avg_sale_price']
        revenue_saleprice_danila.append(revenue)
        revenue_saleprice_danila.append(math.floor(sale_price))
        revenue_saleprice_denis.append(revenue)
        revenue_saleprice_denis.append(math.floor(sale_price))

revenue_saleprice_danila.append(spp_finder()/100)
revenue_saleprice_danila.append(get_temp())

revenue_saleprice_denis.append(spp_finder()/100)
revenue_saleprice_denis.append(get_temp())


del revenue_saleprice_denis[16]
del revenue_saleprice_denis[16]



print('Отчет ИП Грищенко с рынками:', revenue_saleprice_danila)
print('Отчет ИП Коротченков с рынком:', revenue_saleprice_denis)



sh_danila = get_general(Constants.DANILA)

sh_denis = get_general(Constants.DENIS)

sh_danila.insert_row(revenue_saleprice_danila,3)

sh_denis.insert_row(revenue_saleprice_denis,3)


