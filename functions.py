import requests
import json
import MySQLdb
from values import*
import config


# определяем язык пользователя и возвращаем соответствующий словарь с текстом для ответа
def get_text(user_id, lang=None):
    """conn = MySQLdb.connect(host=config.host, port=config.port, user=config.user, passwd=config.passwd, db=config.db)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM languages WHERE name = %s", (user_id, ))

    row = cursor.fetchone()

    if row is not None:
        if row[1] == "ru":
            t = ru_text
        else:
            t = eng_text
    else:
        cursor.execute("INSERT INTO languages VALUES (%s, %s) ", (user_id, lang))
        conn.commit()
        if lang == "ru":
            t = ru_text
        else:
            t = eng_text

    conn.close()"""
    t = eng_text
    return t


# получает и преобразовывает json данные с курсами с коинмаркеткап
def get_cmc_json():
    try:
        json_response = requests.get(COINMARKETCAP_URL)
        cmc_data = json_response.json()

        currency_data = {}
        for dict_number in range(len(cmc_data)):
            values = {
                "name": cmc_data[dict_number]['symbol'],
                "close": cmc_data[dict_number]['price_usd'],
                "close_btc": cmc_data[dict_number]['price_btc'],
                "value_trade": cmc_data[dict_number]['24h_volume_usd'],
                "market_cap": cmc_data[dict_number]['market_cap_usd'],
                "available_coins": cmc_data[dict_number]['available_supply'],
                "all_coins": cmc_data[dict_number]['total_supply'],
                "max_coins": cmc_data[dict_number]['max_supply'],
                "1h": cmc_data[dict_number]['percent_change_1h'],
                "1d": cmc_data[dict_number]['percent_change_24h'],
                "7d": cmc_data[dict_number]['percent_change_7d'],
            }
            currency_data[cmc_data[dict_number]['id']] = values

        return currency_data
    except json.JSONDecodeError:
        return None


# !!!!!!!!!!!!!возвращает список валют типа /BTC, /ETH etc
def currency_list(message):
    t = get_text(message)
    currency_data = get_cmc_json()
    if currency_data is not None:
        all_coins = [t["choose"], ]
        for element in currency_data:
            all_coins.append(" /" + element['symbol'])
        return all_coins
    else:
        return None


# возвращает значения переданной валюты с коинмаркеткап
def currency_values(cur, currency_data):
    for element in currency_data:
        if element['symbol'].lower() == cur.lower() \
                or element['id'].lower() == cur.lower() or element['name'].lower() == cur.lower():
            return element


# получаем и обрабатываем данные по крипте с трейдингвью
def get_crypto_data():
    crypto_data = {}

    json_request = dict(columns=[   # формируем запрос трейдингвью
        "exchange",
        "description",
        "name",
        "close",
        "volume",
        "total_value_traded",  # объём тогов
        "market_cap_calc",  # рыночная капитализация
        "total_shares_diluted",  # всего монет
        "total_shares_outstanding",  # доступно монет
        "Recommend.All",
        "change_abs|1",
        "change|1",
        "change_abs|5",
        "change|5",
        "change_abs|15",
        "change|15",
        "change_abs|60",
        "change|60",
        "change_abs|240",
        "change|240",
        "change_abs",
        "change",
        "Perf.W",
        "Perf.1M",
        "Perf.3M",
        "Perf.6M",
        "Perf.Y",
    ])

    resp = requests.post(TRAIDINGVIEW_CRYPTO_URL, data=json.dumps(json_request)).json()  # делаем запрос на трейдингвью

    for dict_number in range(len(resp["data"])):  # перебираем все полученные значения и формируем из них словарь

        values = {  # создаём самый глубокий словарь со значениями текущей итерации
                  "name": resp["data"][dict_number]['d'][2],
                  "close": resp["data"][dict_number]['d'][3],
                  "volume": resp["data"][dict_number]['d'][4],
                  "value_trade": resp["data"][dict_number]['d'][5],
                  "market_cap": resp["data"][dict_number]['d'][6],
                  "all_coins": resp["data"][dict_number]['d'][7],
                  "available_coins": resp["data"][dict_number]['d'][8],
                  "recommend": resp["data"][dict_number]['d'][9],
                  "1m_abs": resp["data"][dict_number]['d'][10],
                  "1m": resp["data"][dict_number]['d'][11],
                  "5m_abs": resp["data"][dict_number]['d'][12],
                  "5m": resp["data"][dict_number]['d'][13],
                  "15m_abs": resp["data"][dict_number]['d'][14],
                  "15m": resp["data"][dict_number]['d'][15],
                  "1h_abs": resp["data"][dict_number]['d'][16],
                  "1h": resp["data"][dict_number]['d'][17],
                  "4h_abs": resp["data"][dict_number]['d'][18],
                  "4h": resp["data"][dict_number]['d'][19],
                  "1d_abs": resp["data"][dict_number]['d'][20],
                  "1d": resp["data"][dict_number]['d'][21],
                  "7d": resp["data"][dict_number]['d'][22],
                  "1 month": resp["data"][dict_number]['d'][23],
                  "3 month": resp["data"][dict_number]['d'][24],
                  "6 month": resp["data"][dict_number]['d'][25],
                  "12 month": resp["data"][dict_number]['d'][26]}

        """Трейдингвью возвращает словарь, в котором все значения лежат одной куче.
        На выходе мы должны получить словарь, состоящий из вложенных словарей.
        Пример обращения к этому словарю: crypto_data[Binance][Bitcoin][USDT][close]
        Мы обращаемся ко словарю с ключом биржи Binance, в его значениях находим ключ первой валюты - Bitcoin,
        а в её значениях находим значения по ключу второй валюты - USDT, 
        из которой берём текущее значение пары Bitcoin/USDT - close"""

        market = resp["data"][dict_number]['d'][0].lower()  # получаем название биржи текущей итерации

        # в description делим пару (например, Bitcoin/Dollar) на две части и избавляемся от пробелов в названии
        description = resp["data"][dict_number]['d'][1].lower().replace(' / ', '/').replace(' ', '-').split("/")

        second_currency = {description[1]: values}  # создаём словарь, в котром присваиваем второй валюте значения
        currency = {description[0]: second_currency}  # создаём словарь, в котором присваеваем первой валюте вторую
        try:
            crypto_data[market]  # проверяем, создан ли уже словарь с ключом биржи для этой итерации
            try:
                # пытаемся обратиться по ключу к первой валюте и сохранить в неё вторую валюту со значениями
                crypto_data[market][description[0]][description[1]] = values
            except KeyError:
                # Если первая валюта отсутствует в словаре, создаём её и сохраняем в неё вторую валюту со значениями
                crypto_data[market][description[0]] = second_currency
        except KeyError:
            # если ключа текущей биржи нет в словаре, создаём его и добавляем всю цепочку со значениями
            crypto_data[market] = currency

    return crypto_data


def recommendation(recommend, t):
    recommend *= 100
    response = [str(round(recommend, 2)), ]
    if recommend > 50:
        response.append(t["strong_buy"])
    elif recommend > 0:
        response.append(t["buy"])
    elif recommend < -50:
        response.append(t["strong_sell"])
    elif recommend < 0:
        response.append(t["sell"])

    return response


# выводим основные показатели валютной пары в crypto
def crypto_main_response(crypto_data, path, t):
    values = crypto_data[path[1]][path[2]][path[3]]
    str_path = '/' + ' '.join(path)

    recommend = recommendation(values["recommend"], t)

    response = "<i>" + str_path + "</i>" + "\n" + \
               " " * 53 + recommend[1] + "\n" \
               + t["now"] + values["name"] + ":  " + value_processing(values["close"]) + "\n   \U000025AB" \
               + t["recommend"] + recommend[0] + "\n   \U000025AB" \
               + t["1h"] + str(round(values["1h"], 2)) + "\n   \U000025AB" \
               + t["24h"] + str(round(values["1d"], 2)) + "\n   \U000025AB" \
               + t["7d"] + str(round(values["7d"], 2)) + "\n"

    return response


# выводим все показатели валютной пары в crypto
def crypto_more_response(crypto_data, path, t):
    values = crypto_data[path[1]][path[2]][path[3]]
    str_path = '/' + ' '.join(path)
    recommend = recommendation(values["recommend"], t)

    response = "<i>" + str_path + "</i>" + "\n" + \
               " " * 53 + recommend[1] + "\n" \
               + t["now"] + values["name"] + ":  " + str(values["close"]) + "\n"

    for value in list(values)[2:]:
        if values[value] is not None:
            response += "    \U000025AB" + value + ":  " + str(values[value]) + "\n"

    return response


# определяем количество знаков после запятой выводимых значений
def value_processing(value):
    str_value = str("{0:.5f}".format(value))
    list_value = str_value.split('.')

    if len(list_value[0]) == 1:
        if list_value[0] == '0':
            indent = 4
            for position in range(len(list_value[1])):
                if list_value[1][position] != '0':
                    break
                indent += 1
            result_value = format(value, '.'+str(indent)+'f')

        else:
            result_value = str(float("{0:.3f}".format(value)))

    elif len(list_value[0]) < 5:
        result_value = str(float("{0:.2f}".format(value)))

    elif len(list_value[0]) < 7:
        result_value = str(float("{0:.1f}".format(value)))

    else:
        result_value = list_value[0]

    return result_value


# сортирует первую валюту по алфавиту и поднимет вверх 16 валют с наибольшей капитализацией
def crypto_sort(dict_currencies, coinmarketcap_data):
    list_currencies = list(dict_currencies)

    if coinmarketcap_data is not None:
        top_currencies = []
        coinmarketcap_list = list(coinmarketcap_data)
        for number in range(20):
            element = 0
            cmc_cur = coinmarketcap_data[coinmarketcap_list[number]]["name"]
            for currency in list_currencies:
                second_currency = list(dict_currencies[currency].keys())

                cur_abbr = dict_currencies[currency][second_currency[0]]["name"]
                if cur_abbr[:len(cmc_cur)] == cmc_cur:
                    top_currencies.append(currency)
                    list_currencies.pop(element)
                    break
                element += 1

        currencies = top_currencies + sorted(list_currencies)
        return currencies
    else:
        return sorted(list_currencies)


# создаём кнопку пользователя
def create_user_button(recipient, path, cur_name):
    conn = MySQLdb.connect(host=config.host, port=config.port, user=config.user, passwd=config.passwd, db=config.db)
    conn.set_character_set('utf8')
    cursor = conn.cursor()

    def button_name():
        list_path = path.split()
        but_name = list_path[1] + "| " + cur_name
        print(but_name)
        return but_name

    cursor.execute("SELECT * FROM buttons_amount WHERE name = %s", (recipient,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO buttons_amount VALUES(%s,%s)", (recipient, 1))
        cursor.execute("INSERT INTO buttons VALUES(0,%s,%s,%s)", (recipient, path[:-16], button_name()))

    elif row[1] >= MAX_USER_BUTTONS:
        conn.close()
        return "! button_limit"

    else:
        cursor.execute("UPDATE buttons_amount SET amount = %s WHERE name = %s", (row[1] + 1, recipient))
        cursor.execute("INSERT INTO buttons VALUES(0,%s,%s,%s)", (recipient, path[:-16], button_name()))

    conn.commit()
    conn.close()

    return "! done_button"


# возвращаем список кнопок пользователя
def get_user_button(recipient):
    conn = MySQLdb.connect(host=config.host, port=config.port, user=config.user, passwd=config.passwd, db=config.db)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buttons WHERE name = %s", (recipient,))
    rows = cursor.fetchall()
    return rows


# удаляем пользовательскую кнопку
def del_user_button(recipient, button_id):
    conn = MySQLdb.connect(host=config.host, port=config.port, user=config.user, passwd=config.passwd, db=config.db)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM buttons WHERE id = %s", (button_id,))
    print(button_id)
    cursor.execute("SELECT * FROM buttons_amount WHERE name = %s", (recipient,))
    row = cursor.fetchone()
    cursor.execute("UPDATE buttons_amount SET amount = %s WHERE name = %s", (row[1] - 1, recipient))

    conn.commit()
    conn.close()
