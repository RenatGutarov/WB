import time
from MPSTATS_API import update_conc,sheet
from WB_API import update_prices, slovar
from messaging import send_message_renat
from otchet import otchet
import schedule
from base_info import get_articles
from total_profit import process_rows
import gspread
from worksheet import get_general, Constants
from total_profit import get_data

def main_def():

    otchet()

    data_articles = get_articles()

    update_conc(data_articles, sheet)

    update_prices(slovar)

    result_danila = process_rows(get_data(Constants.DANILA))

    get_general(Constants.DANILA).insert_row(result_danila, 3)

    send_message_renat('Общее Грищенко обновилось')

    print('Общее Грищенко обновлено')

    result_denis = process_rows(get_data(Constants.DENIS))

    del result_denis [16:18]

    get_general(Constants.DENIS).insert_row(result_denis, 3)

    print('Общее Коротченков обновлено')

    send_message_renat('Общее Коротченков обновилось')

    send_message_renat('Все скрипты отработали')

    print('Все скрипты отработали')

schedule.every().day.at('11:30').do(main_def)



while True:
     schedule.run_pending()
     time.sleep(1)

