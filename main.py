from MPSTATS_API import update_conc
from base_info import get_articles
from WB_API import update_prices, slovar

sheet_name = 'Анализ конкурентов'

data_articles = get_articles()

update_conc(data_articles, sheet_name,)

update_prices(slovar)



