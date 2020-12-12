#!/usr/bin/env python3


import csv
import re


def search_pattern(num_shop, line):
    shop_names = ['массимо дутти', 'бершка', 'пулл энд беар','зара хом', 'страдивариус', 'ойшо', 'зара']
    for pattern in shop_names:
        if re.search(pattern, line.lower()):
            return f'{num_shop} {pattern}'


with open('pull.csv', 'w') as pull:
    writer = csv.writer(pull,  delimiter=';')
    with open('to_convert.csv', "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            row = " ".join(row).split(';')
            if len(row) < 4:
                print('Не все столбцы заполнены')
                """По хорошему raise необходим"""
                break
            num_shop, raw_name_shop, kkt, date, *_ = [x.strip().lower() for x in row]
            date, *_ = date.split(' ')
            num_shop = search_pattern(num_shop, raw_name_shop)
            writer.writerow([num_shop, kkt, date])

print('Done')