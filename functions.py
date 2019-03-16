from values import*
import requests
import MySQLdb


# получает и преобразовывает json данные с курсами с коинмаркеткап
def json_recipient():
    json_response = requests.get(currency_url)
    currency_data = json_response.json()
    return currency_data


# возвращает список валют типа /BTC, /ETH etc
def currency_list():
    currency_data = json_recipient()
    all_coins = [t["choose"], ]
    for element in currency_data:
        all_coins.append(" /" + element['symbol'])
    return all_coins


# возвращает значения переданной валюты с коинмаркеткап
def currency_values(cur, currency_data):
    for element in currency_data:
        if element['symbol'].lower() == cur.lower() \
                or element['id'].lower() == cur.lower() or element['name'].lower() == cur.lower():
            return element



