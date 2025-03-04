import os
import pickle
import time
from messaging import send_message_renat
import requests
from datetime import datetime, timedelta
from selenium_manager import Selenium



def get_sku(data):
    sku = {}
    data = data[:10]
    skus = []
    for item in data:
        sku['id'] = item['id']
        sku['brand'] = item['brand']
        sku['photo'] = item['thumb']
        skus.append(sku.copy())
    print("Данные получены")
    return skus

def get_data(url):
    if not os.path.exists("cookies.pkl"):
        print("Файл с куками не найден. Пожалуйста, выполните вход.")
        return None

    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        with requests.Session() as session:
            for c in cookies:
                try:
                    c.pop("sameSite", None)
                    c.pop("httpOnly", None)
                    c.pop("expiry", None)
                except KeyError:
                    pass
                finally:
                    session.cookies.set(**c)
            response = session.get(url)
            print(f"Запрос к {url} завершился статусом {response.status_code}")
            return response.json()["data"] if response.status_code == 200 else None


def get_articles():

    first_date = (datetime.now() - timedelta(days=14)).strftime("%d.%m.%Y")

    second_date = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")

    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            result = []
            for group in [565827, 566068, 566067, 665525, 680222, 623276]:
                if len(str(group)) > 2:
                    url = f"https://mpstats.io/api/wb/get/group?path={group}&d1={first_date}&d2={second_date}"
                    print(f"Получение данных для группы: {group}")

                    if data := get_data(url):
                        result.append(get_sku(data))
                    else:
                        print("Не удалось получить данные, выполняем вход...")
                        browser = Selenium()
                        if data := get_data(url):
                            result.append(get_sku(data))
                            print("Данные получены после входа")
                        else:
                            print("Обратись к Саньку")
                else:
                    url = f"https://mpstats.io/api/wb/get/subject?d1={first_date}&d2={second_date}&path=57&fbs=0"
                    print('Получение данных для топа ниши шарфов')
                    if data := get_data(url):
                        result.append(get_sku(data))
            if result:
                return result

        except Exception as e:
            retries += 1
            send_message_renat(f'Ошибка {e}, перезапуск')
            time.sleep(120)

    if retries == max_retries:
        send_message_renat('Анализ конкурентов сломался')



