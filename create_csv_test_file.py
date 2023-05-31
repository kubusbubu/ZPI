import pandas as pd
import json
from datetime import date, timedelta
import random
import string


with open('dda_json/contoption.json', 'r') as f:
  jsondata = json.load(f)
# with open('data_json/trader_cds_price.json', 'r') as f:
#   jsondata = json.load(f)


def random_dates(k):
    test_date1, test_date2 = date(2015, 6, 3), date(2023, 7, 1)
    dates_bet = test_date2 - test_date1
    total_days = dates_bet.days

    res = []
    for idx in range(k):
        random.seed(a=None)
        randay = random.randrange(total_days)

        res.append(test_date1 + timedelta(days=randay))
    return res


def random_integers(k):
    res = [random.randint(0, 1000) for i in range(k)]
    return res


def random_floats(k):
    res = [random.random()*1000 for i in range(k)]
    return res


def random_strings(k):
    strings = []

    for i in range(k):
        length = random.randint(1, 10)
        all_chars = string.ascii_letters + string.digits
        rand_string = ''.join(random.choice(all_chars) for _ in range(length))
        strings.append(rand_string)
    return strings


"""N - liczba wierszy csv"""
N = 100

string_data = random_strings(N)
integer_data = random_integers(N)
float_data = random_floats(N)
date_data = random_dates(N)

df = pd.DataFrame()
for atrybut in jsondata:
    col_name = atrybut['name']
    col_type = atrybut['type']
    if col_type == 'INTEGER':
        df[col_name] = integer_data
    elif col_type == 'DOUBLE':
        df[col_name] = float_data
    elif col_type == 'STRING':
        df[col_name] = string_data
    else:
        df[col_name] = date_data

df.to_csv('datasets/contoption.csv')
# print(df)