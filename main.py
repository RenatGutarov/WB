import time
from MPSTATS_API import update_conc
from base_info import get_articles
from WB_API import update_prices, slovar
from otchet import otchet
import schedule

sheet_name = 'Анализ конкурентов'




def main_def():
    otchet()


schedule.every().day.at('11:30').do(main_def)


while True:
    schedule.run_pending()
    time.sleep(1)
