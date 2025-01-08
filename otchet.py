import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from messaging import send_message
import re
import math


def otchet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    time_for_sheet = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

    current_sheet = time_for_sheet.replace('-', '.')

    creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

    client = gspread.authorize(creds)

    sh_danila = client.open("Прибыль LIVE Грищенко")

    sh_denis = client.open('Прибыль LIVE Коротченков')

    worksheet_danila = sh_danila.worksheet(current_sheet)

    worksheet_denis = sh_denis.worksheet(current_sheet)

    # val2 = worksheet.get("A1:B2")
    revenue_danila = worksheet_danila.acell('e38').value
    profit_danila = worksheet_danila.acell('n38').value
    profitability_danila = worksheet_danila.acell('O38').value
    drr_danila = worksheet_danila.acell('m38').value
    ad_danila = worksheet_danila.acell('l38').value
    actions_danila = worksheet_danila.acell('s40').value

    revenue_denis = worksheet_denis.acell('e26').value
    profit_denis = worksheet_denis.acell('n26').value
    profitability_denis = worksheet_denis.acell('o26').value
    drr_denis = worksheet_denis.acell('m26').value
    ad_denis = worksheet_denis.acell('l26').value
    actions_denis = worksheet_denis.acell('s28').value

    data_old_two_ip = [revenue_danila, profit_danila, revenue_denis, profit_denis]
    data_new_two_ip = []

    for i in data_old_two_ip:
        i = i[2:-3]
        cleaned_str = re.sub(r'\s+', '', i)
        data_new_two_ip.append(int(cleaned_str))

    ad_danila_denis = [ad_danila, ad_denis]
    ad_danila_denis_new = []

    for i in ad_danila_denis:
        i = i[2:-3]
        cleaned_str = re.sub(r'\s+', '', i)
        ad_danila_denis_new.append(int(cleaned_str))

    final_revenue = data_new_two_ip[0] + data_new_two_ip[2]
    final_profit = data_new_two_ip[1] + data_new_two_ip[3]
    final_profitability = math.floor(final_profit / final_revenue * 100)
    chet_drr = (ad_danila_denis_new[0] + ad_danila_denis_new[1]) / final_revenue
    final_drr = math.floor(chet_drr * 100)

    if actions_danila is not None and actions_denis is not None:
        send_message(f'''
Грищенко
ВЫРУЧКА = {data_new_two_ip[0]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[1]}.р
В. РЕНТА = {profitability_danila}
ДРР = {drr_danila}
Что сделали вчера:
{actions_danila}
        
Коротченков
ВЫРУЧКА = {data_new_two_ip[2]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[3]}.р
В. РЕНТА = {profitability_denis}
ДРР = {drr_denis}
Что сделали вчера:
{actions_denis}
    
ИТОГО
ВЫРУЧКА = {final_revenue}.р
В. ПРИБЫЛЬ = {final_profit}.р
В. РЕНТА = {final_profitability}%
ДРР = {final_drr}%
СПП БЫЛ = 21%
''')
    elif actions_danila is None and actions_denis is not None:
        send_message(
            f'''
Грищенко
ВЫРУЧКА = {data_new_two_ip[0]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[1]}.р
В. РЕНТА = {profitability_danila}
ДРР = {drr_danila}
Что сделали вчера:
    
Коротченков
ВЫРУЧКА = {data_new_two_ip[2]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[3]}.р
В. РЕНТА = {profitability_denis}
ДРР = {drr_denis}
Что сделали вчера:
{actions_denis}
    
ИТОГО
ВЫРУЧКА = {final_revenue}.р
В. ПРИБЫЛЬ = {final_profit}.р
В. РЕНТА = {final_profitability}%
ДРР = {final_drr}%
СПП БЫЛ = 21%
''')

    elif actions_denis is None and actions_danila is not None:
        send_message(
            f'''
Грищенко
ВЫРУЧКА = {data_new_two_ip[0]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[1]}.р
В. РЕНТА = {profitability_danila}
ДРР = {drr_danila}
Что сделали вчера:
{actions_danila}
    
Коротченков
ВЫРУЧКА = {data_new_two_ip[2]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[3]}.р
В. РЕНТА = {profitability_denis}
ДРР = {drr_denis}
Что сделали вчера:
    
    
ИТОГО
ВЫРУЧКА = {final_revenue}.р
В. ПРИБЫЛЬ = {final_profit}.р
В. РЕНТА = {final_profitability}%
ДРР = {final_drr}%
СПП БЫЛ = 21%
''')

    else:
        send_message(
f'''
Грищенко
ВЫРУЧКА = {data_new_two_ip[0]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[1]}.р
В. РЕНТА = {profitability_danila}
ДРР = {drr_danila}
Что сделали вчера:
            

Коротченков
ВЫРУЧКА = {data_new_two_ip[2]}.р
В. ПРИБЫЛЬ = {data_new_two_ip[3]}.р
В. РЕНТА = {profitability_denis}
ДРР = {drr_denis}
Что сделали вчера:


ИТОГО
ВЫРУЧКА = {final_revenue}.р
В. ПРИБЫЛЬ = {final_profit}.р
В. РЕНТА = {final_profitability}%
ДРР = {final_drr}%
СПП БЫЛ = 21%
''')


