import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle


class Selenium:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://mpstats.io/login?from=main-page-header")
        self.login()
        self.save_cookie()

    def login(self):
        try:
            email = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="mpstats-login-form"]/div/div[1]/div/div/div/div/div/input',
                    )
                )
            )
            email.send_keys(
                os.getenv('MP_EMAIL')
            )
            passw = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="mpstats-login-form"]/div/div[2]/div[1]/div/div/div/div/div/div/input',
                    )
                )
            )
            passw.send_keys(os.getenv("MP_PASSWORD"))
            button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="mp-stats-app"]/div[3]/div[1]/div[2]/div/div/div/div[1]/div[2]/button',
                    )
                )
            )
            button.click()
        except:
            self.driver.quit()

    def save_cookie(self):
        time.sleep(10)
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
