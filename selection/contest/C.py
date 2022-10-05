import json
import datetime as dt


def str_to_date(s):
    return dt.date(*map(int, s.split('.')[::-1]))


def filter_maker(name_contains, price_gt, price_lt, date_after, date_before):
    def f_filter(x):
        return name_contains in x['name'].lower() and price_gt <= x['price'] <= price_lt and date_after <= str_to_date(x['date']) <= date_before
    return f_filter


def main(json_data, raw_filters):
    name_contains = raw_filters['NAME_CONTAINS'].lower()
    price_gt = int(raw_filters['PRICE_GREATER_THAN'])
    price_lt = int(raw_filters['PRICE_LESS_THAN'])
    date_after = str_to_date(raw_filters['DATE_AFTER'])
    date_before = str_to_date(raw_filters['DATE_BEFORE'])
    return json.dumps(sorted(filter(filter_maker(name_contains, price_gt, price_lt, date_after, date_before), json_data), key=lambda x: x['id']))


if __name__ == '__main__':
    json_data = json.loads(input())
    filters = {}
    for i in range(5):
        current_filter = input().split()
        filters[current_filter[0]] = current_filter[1]
    res = main(json_data, filters)
    print(res)
