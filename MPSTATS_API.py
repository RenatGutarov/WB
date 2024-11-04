import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv
import os
from gspread.utils import rowcol_to_a1
from datetime import datetime, timedelta

load_dotenv()

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)

data = (
    [
        171803170,
        195325187,
        165374615,
        203597298,
        171232105,
        238455525,
        143973840,
        214791724,
        168258699,
        221885037,
    ],
    [
        228502034,
        243117262,
        243180428,
        141940975,
        168423784,
        189027878,
        154844674,
        221582470,
        159271393,
        189105078,
    ],
    [
        228502033,
        243119074,
        243181642,
        152644637,
        168423785,
        159271394,
    ],
    [
        188985842,
        244849109,
        32908979,
        191440399,
        246012884,
        44730048,
        171803170,
        218090415,
        263690356,
        173051528,
    ],
    [
        188037949,
        260251386,
        119916415,
        259028257,
        191933262,
        96815935,
        175505993,
        260251385,
        259865204,
        55597840,
    ],
    [
        188037949,
        96815935,
        70722699,
        102658625,
        120714921,
        178444557,
        247782810,
        174007288,
        175928419,
        183518683,
    ],
)


sheet_name = "АНАЛИЗ КОНКУРЕНТОВ ПИЖАМЫ АЛЯ"

first_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

second_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def fill_sheet(articles):
    sheet_data = []
    for article in articles:
        url = f"https://mpstats.io/api/wb/get/item/{article}/sales"
        params = {"d1": first_date, "d2": second_date}
        header = {
            "Content-Type": "application/json",
            "X-Mpstats-TOKEN": "66f7c93f83b340.31768105158e32ade09284f4dbb1d45dfd5631fb",
        }
        response = requests.get(url=url, params=params, headers=header)
        final_price_dict = response.json()
        result = []
        for revenue in final_price_dict:
            sale = revenue["sales"]
            final_price = revenue["final_price"]
            final_revenue = sale * final_price
            result.append(final_revenue)
        result.reverse()

        sheet_data.append(result)
    return sheet_data


for i, articles in enumerate(data):
    sh = client.open(sheet_name).get_worksheet(i)
    result = fill_sheet(articles)
    letter = rowcol_to_a1(len(result[0]) + 2, len(result) + 1)
    sh.update(list(zip(*result)), f"B3:{letter}")