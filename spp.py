import requests
from datetime import datetime
import schedule
import time
from functools import partial
from MPSTATS_API import sheet
from worksheet import get_spp_sheet, Constants

# Костыль созданный с целью нахождения СПП через gold-ss, потому что МПСТАТС не отдает, пока использую так

def spp_finder(name):
    result = []

    url = "https://card.wb.ru/cards/v2/detail?dest=-1255987&nm=151784447"

    response = requests.get(url=url)

    prices = response.json()

    price_spawner = prices["data"]["products"][0]["sizes"][0]['price'] # мейн запрос, тут можно посмотреть две нужные цены,


    sale = 0.81

    price_after_sale = int(price_spawner['product'] / 100)  # цена после СПП

    our_price_before_sale = int(price_spawner['basic'] / 100) # наша цена ДО скидки

    final_sale = round(1 - sale,2)

    procent = our_price_before_sale * final_sale # цена после нашей скидки

    spp = int(round(1 - round(price_after_sale / procent,2),2) * 100)

    day_time = (datetime.now()).strftime("%d.%m.%Y")

    result.append(day_time)

    result.append(spp)

    sheet = get_spp_sheet(name)

    sheet_len = sheet.get('2:100')

    flat_lst = sheet_len[0]

    if len(flat_lst) > 1:
        sheet.update_acell('C2',spp)

    elif len(flat_lst) > 2:
        sheet.update_acell('d2', spp)

    elif len(flat_lst) == 0:
        sheet.update([result],'a2:b2')


def get_spp(name):
    sheet = get_spp_sheet(name)
    data = sheet.get('b3:d3')
    flat_data = data[0]
    numbers_int = []
    for i in flat_data:
        numbers_int.append(int(i))

    sum_numbers = 0
    for num in numbers_int:
        sum_numbers += num

    average = sum_numbers / len(numbers_int)

    return int(average)

def spp_join(name):
    sheet = get_spp_sheet(name)
    data = sheet.get('b3:d3')
    flat_data = data[0]
    return '-'.join(flat_data)

def rows_down(name):
    sheet = get_spp_sheet(name)
    sheet.insert_row([],2)



times = ['15:15', '15:16', '15:17']


for t in times:
    schedule.every().day.at(t).do(partial(spp_finder, Constants.DENIS))
    schedule.every().day.at(t).do(partial(spp_finder, Constants.DANILA))

ips = [Constants.DENIS,Constants.DANILA]

for i in ips:
    schedule.every().day.at('15:18').do(partial(rows_down, i))


if __name__ == '__main__':
    while True:
         schedule.run_pending()
         time.sleep(1)