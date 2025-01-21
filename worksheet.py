import gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

class Constants:
    DENIS = 'denis'
    DANILA = 'danila'

scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",]


creds = ServiceAccountCredentials.from_json_keyfile_name("google_keys.json", scope)

client = gspread.authorize(creds)

slovar = {
    Constants.DENIS : client.open("Прибыль LIVE Коротченков"),
    Constants.DANILA : client.open("Прибыль LIVE Грищенко"),
 }


def get_sheet(name):
    sh = slovar[name]
    current_sheet = (datetime.now()).strftime("%d.%m.%Y")
    return sh.worksheet(current_sheet)

def get_sheet_yesterday(name):
    sh = slovar[name]
    current_sheet = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
    return sh.worksheet(current_sheet)

def get_general(name):
    if name == Constants.DANILA:
        sh = slovar[name]
        current_sheet = "ОБЩЕЕ"
        return sh.worksheet(current_sheet)
    else:
        sh = slovar[name]
        current_sheet = "Общее"
        return sh.worksheet(current_sheet)

def get_delta(name):
    sh = slovar[name]
    current_sheet = (datetime.now() - timedelta(days=2)).strftime("%d.%m.%Y")
    return sh.worksheet(current_sheet)
