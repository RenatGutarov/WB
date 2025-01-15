import time
from MPSTATS_API import update_conc
from WB_API import update_prices, slovar
from otchet import otchet
import schedule
from base_info import get_articles

sheet = 'Анализ конкурентов'




def main_def():

    otchet()

    data_articles = get_articles()

    update_conc(data_articles, sheet)

    update_prices(slovar)

schedule.every().day.at('11:30').do(main_def)



while True:
     schedule.run_pending()
     time.sleep(1)

