import requests

# Костыль созданный с целью нахождения СПП через gold-ss, потому что МПСТАТС не отдает, пока использую так

def spp_finder():
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

    return spp
