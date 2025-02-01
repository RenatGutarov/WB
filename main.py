import time
from MPSTATS_API import update_conc,sheet
from WB_API import update_prices, slovar
from otchet import otchet
import schedule
from base_info import get_articles
from total_profit import process_rows,rows_denis,rows_danila
import gspread
from worksheet import get_general, Constants





def main_def():

    otchet()

    data_articles = get_articles()

    update_conc(data_articles, sheet)

    update_prices(slovar)

    result_danila = process_rows(rows_danila)

    get_general(Constants.DANILA).insert_row(result_danila, 3)

    result_denis = process_rows(rows_denis)

    del result_denis [16:18]

    get_general(Constants.DENIS).insert_row(result_denis, 3)


schedule.every().day.at('12:18').do(main_def)



while True:
     schedule.run_pending()
     time.sleep(1)

