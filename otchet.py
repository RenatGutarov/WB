from total_profit import process_rows, rows_denis, rows_danila, process_rows_delta, process_rows_actions
import gspread
from messaging import send_message
import re
import math
from worksheet import Constants, get_sheet_yesterday, get_delta
from spp import spp_finder

def otchet():
    danila = process_rows(rows_danila)

    keys = [
         'date', 'day_of_week', 'revenue', 'pieces', 'procent',
         'revenue_buy', 'will_buy', 'cost_price_proc', 'commission',
         'logistic', 'tax', 'storage', 'add', 'drr', 'profit',
         'profitability', 'scarfs_rinok', 'scarfs_check', 'pjms_rinok',
         'pjms_checs', 'spp', 'temp'
    ]

    denis = process_rows(rows_denis)

    data_dict_danila = dict(zip(keys, danila))

    data_dict_denis = dict(zip(keys, denis))

    delta_sheet_danila = get_delta(Constants.DANILA)

    delta_sheet_denis = get_delta(Constants.DENIS)

    actions_danila_new = get_sheet_yesterday(Constants.DANILA)

    actions_denis_new = get_sheet_yesterday(Constants.DENIS)

    actions_denis_get = actions_denis_new.get('1:100')

    actions_danila_get = actions_danila_new.get('1:100')

    delta_sheet_danila_get = delta_sheet_danila.get('1:100')

    delta_sheet_denis_get = delta_sheet_denis.get('1:100')

    profit_yesterday_danila = process_rows_delta(delta_sheet_danila_get)

    profit_yesterday_denis = process_rows_delta(delta_sheet_denis_get)

    actions_danila_yesterday = process_rows_actions(actions_danila_get)

    actions_denis_yesterday = process_rows_actions(actions_denis_get)

    print(len(actions_danila_yesterday))

    print(len(actions_denis_yesterday))

    data_old_two_ip = [data_dict_danila['revenue'],data_dict_danila['profit'],data_dict_denis['revenue'],data_dict_denis['profit'],profit_yesterday_danila[0],profit_yesterday_denis[0]]

    ad_danila_denis = [data_dict_danila['add'], data_dict_denis['add'],]

    final_revenue = data_old_two_ip[0] + data_old_two_ip[2]
    final_profit = data_old_two_ip[1] + data_old_two_ip[3]
    final_profitability = math.floor(final_profit / final_revenue * 100)
    chet_drr = (ad_danila_denis[0] + ad_danila_denis[1]) / final_revenue
    final_drr = math.floor(chet_drr * 100)
    sum_of_profits_yesterday = data_old_two_ip[4] + data_old_two_ip[5]

    delta_yesterday = final_profit - sum_of_profits_yesterday

    spp = spp_finder()

    if len(actions_danila_yesterday) > 0  and len(actions_denis_yesterday) > 0  and delta_yesterday < 0:
        actions_str_danila = '\n'.join(actions_danila_yesterday)
        actions_str_denis = '\n'.join(actions_denis_yesterday)
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
{actions_str_danila}

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:
{actions_str_denis}

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🌹 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
 СПП БЫЛ = {spp}%
''')
    elif len(actions_danila_yesterday) > 0 and len(actions_denis_yesterday) > 0  and delta_yesterday > 0:
        actions_str_danila = '\n'.join(actions_danila_yesterday)
        actions_str_denis = '\n'.join(actions_denis_yesterday)
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
{actions_str_danila}

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:
{actions_str_denis}

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🍀 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
СПП БЫЛ = {spp}%
''')
    elif len(actions_danila_yesterday) < 1  and len(actions_denis_yesterday) > 0 and delta_yesterday < 0:
        actions_str_denis = '\n'.join(actions_denis_yesterday)
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
    

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:
{actions_str_denis}

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🌹 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
СПП БЫЛ = {spp}%
''')
    elif len(actions_danila_yesterday) < 1   and len(actions_denis_yesterday) > 0  and delta_yesterday > 0:
        actions_str_danila = '\n'.join(actions_danila_yesterday)
        actions_str_denis = '\n'.join(actions_denis_yesterday)
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
{actions_str_danila}

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:
{actions_str_denis}

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🍀 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
СПП БЫЛ = {spp}%
''')
    elif len(actions_denis_yesterday) < 1 and len(actions_danila_yesterday) > 0  and delta_yesterday < 0:
        actions_str_danila = '\n'.join(actions_danila_yesterday)
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
{actions_str_danila}

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:
    

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🌹 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
СПП БЫЛ = {spp}%
''')
    elif len(actions_denis_yesterday) < 1 and len(actions_danila_yesterday) > 0 and delta_yesterday > 0:
        actions_str_danila = '\n'.join(actions_danila_yesterday)
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
{actions_str_danila}

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🍀 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
 СПП БЫЛ = {spp}%
''')
    elif len(actions_danila_yesterday) < 1  and len(actions_denis_yesterday) < 1 and delta_yesterday < 0:
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
    

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🌹 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
 СПП БЫЛ = {spp}%
''')
    elif len(actions_danila_yesterday) < 1 and len(actions_denis_yesterday) < 1  and delta_yesterday > 0:
        send_message(f'''
Грищенко
💰 ВЫРУЧКА = {data_dict_danila['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_danila['profit']}.р
💎 В. РЕНТА = {round(data_dict_danila['profitability'] * 100,2)}%
💣 ДРР = {data_dict_danila['drr'] * 100}%
Что сделали вчера:
    

Коротченков
💰 ВЫРУЧКА = {data_dict_denis['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict_denis['profit']}.р
💎 В. РЕНТА = {round(data_dict_denis['profitability'] * 100,2)}%
💣 ДРР = {data_dict_denis['drr'] * 100}%
Что сделали вчера:

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
🍀 Дельта = {delta_yesterday}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
 СПП БЫЛ = {spp}%
''')






