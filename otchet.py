from total_profit import process_rows, process_rows_delta, process_rows_actions, get_data
from messaging import send_message
import math
from worksheet import Constants, get_sheet_yesterday, get_delta
from spp import get_spp


# Ключи для преобразования списка в словарь
keys = [
    'date', 'day_of_week', 'revenue', 'pieces', 'procent',
    'revenue_buy', 'will_buy', 'cost_price_proc', 'commission',
    'logistic', 'tax', 'storage', 'add', 'drr', 'profit',
    'profitability', 'scarfs_rinok', 'scarfs_check', 'pjms_rinok',
    'pjms_checs', 'spp', 'temp'
]


def get_user_data(user_constants):
    """Получает данные для пользователя и преобразует их в словарь."""
    data_list = process_rows(get_data(user_constants))
    return dict(zip(keys, data_list))


def get_actions(user_constants):
    """Получает действия пользователя за вчерашний день."""
    actions_sheet = get_sheet_yesterday(user_constants)
    actions = actions_sheet.get('1:100')
    return process_rows_actions(actions)


def get_profit_yesterday(user_constants):
    """Получает прибыль за вчерашний день."""
    delta_sheet = get_delta(user_constants)
    delta_data = delta_sheet.get('1:100')
    return process_rows_delta(delta_data)[0]


def calculate_metrics(data_dict, profit_yesterday):
    """Вычисляет метрики для пользователя."""
    final_revenue = data_dict['revenue']
    final_profit = data_dict['profit']
    final_profitability = math.floor(final_profit / final_revenue * 100)
    final_drr = math.floor((data_dict['add'] / final_revenue) * 100)
    delta_yesterday = final_profit - profit_yesterday
    return final_revenue, final_profit, final_profitability, final_drr, delta_yesterday


def generate_user_report(data_dict, actions, delta_yesterday):
    """Формирует отчет для пользователя."""
    report = f'''
💰 ВЫРУЧКА = {data_dict['revenue']}.р
💵 В. ПРИБЫЛЬ = {data_dict['profit']}.р
💎 В. РЕНТА = {round(data_dict['profitability'] * 100, 2)}%
💣 ДРР = {round(data_dict['drr'] * 100, 2)}%
Что сделали вчера:
{'\n'.join(actions) if actions else "Нет данных"}
'''
    if delta_yesterday < 0:
        report += f'🌹 Дельта = {delta_yesterday}.р\n'
    else:
        report += f'🍀 Дельта = {delta_yesterday}.р\n'
    return report


def calculate_final_metrics(danila_metrics, denis_metrics, danila_data, denis_data, profit_yesterday_danila, profit_yesterday_denis):
    """Вычисляет итоговые метрики."""
    final_revenue = danila_metrics[0] + denis_metrics[0]
    final_profit = danila_metrics[1] + denis_metrics[1]
    final_profitability = math.floor(final_profit / final_revenue * 100)
    final_drr = math.floor((danila_data['add'] + denis_data['add']) / final_revenue * 100)
    delta_yesterday = danila_metrics[4] + denis_metrics[4]
    total_delta = final_profit - (profit_yesterday_danila + profit_yesterday_denis)
    return final_revenue, final_profit, final_profitability, final_drr, delta_yesterday, total_delta


def send_final_report(danila_report, denis_report, final_metrics, spp):
    """Отправляет итоговый отчет."""
    final_revenue, final_profit, final_profitability, final_drr, delta_yesterday, total_delta = final_metrics

    # Определяем значок для общей дельты
    delta_icon = '🌹' if total_delta < 0 else '🍀'

    message = f'''
{danila_report}

{denis_report}

ИТОГО
💰 ВЫРУЧКА = {final_revenue}.р
💵 В. ПРИБЫЛЬ = {final_profit}.р
{delta_icon} Общая дельта = {total_delta}.р
💎 В. РЕНТА = {final_profitability}%
💣 ДРР = {final_drr}%
СПП БЫЛ = {spp}%
'''
    send_message(message)


def otchet():
    # Получение данных для каждого пользователя
    danila_data = get_user_data(Constants.DANILA)
    denis_data = get_user_data(Constants.DENIS)

    # Получение действий за вчерашний день
    actions_danila = get_actions(Constants.DANILA)
    actions_denis = get_actions(Constants.DENIS)

    # Получение прибыли за вчерашний день
    profit_yesterday_danila = get_profit_yesterday(Constants.DANILA)
    profit_yesterday_denis = get_profit_yesterday(Constants.DENIS)

    # Расчет метрик для каждого пользователя
    danila_metrics = calculate_metrics(danila_data, profit_yesterday_danila)
    denis_metrics = calculate_metrics(denis_data, profit_yesterday_denis)

    # Формирование отчетов для каждого пользователя
    danila_report = generate_user_report(danila_data, actions_danila, danila_metrics[4])
    denis_report = generate_user_report(denis_data, actions_denis, denis_metrics[4])

    # Расчет итоговых метрик
    final_metrics = calculate_final_metrics(
        danila_metrics, denis_metrics, danila_data, denis_data, profit_yesterday_danila, profit_yesterday_denis
    )

    # Получение данных о СПП
    spp = get_spp(Constants.DENIS)

    # Отправка итогового отчета
    send_final_report(danila_report, denis_report, final_metrics, spp)


if __name__ == '__main__':
    otchet()


