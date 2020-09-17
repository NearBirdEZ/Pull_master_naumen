import csv
from create_address_shop import Create_address_shop
from api_naumen import API_Naumen
from selenium.common.exceptions import NoSuchElementException
import time


def take_tmp(prefix_store_, view_address_):
    global prefix_store, view_address
    prefix_store = prefix_store_
    view_address = view_address_

    print(prefix_store, view_address)


def create_dict_with_kkt(scale_amount_zero):
    store_kkt = {}
    final_list = []
    bad_list = []
    with open('pull.csv', "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            row = " ".join(row).split(';')
            if len(row) < 3:
                break
            bad_store, kkt, date = [x.strip().lower() for x in row]
            date, *_ = date.split(' ')
            if not kkt.startswith('0'):
                kkt = '0' * scale_amount_zero + kkt

            if store_kkt.get(bad_store):
                store_kkt[bad_store].append(f'{kkt}_{date}')
            else:
                store_kkt[bad_store] = [f'{kkt}_{date}']
    shop = Create_address_shop()

    total_lines = len(store_kkt)

    api = API_Naumen()
    count = 0
    for address, kkts in store_kkt.items():
        count += 1

        address = shop.start(address, prefix_store, view_address)
        api.search_by_shop(address)
        try:
            store_naumen = api.driver.find_element_by_xpath('//*[@id="ServiceCallRegistrationNew.RegForm.'
                                                            'MainContainer.LeftColumn.clientProperties.title"]'
                                                            '/a').text
            api.driver.find_element_by_xpath('//*[@id="ServiceCallRegistrationNew.RegForm.MainContainer.LeftColumn.'
                                             'clientProperties.title"]/a').click()

            api.driver.get(api.driver.find_element_by_xpath('//*[@id="CfgResources"]').get_attribute('href'))

            api.driver.find_element_by_xpath('//*[@id="pageSize"]/option[@nonshifted="100"]').click()

            kkt_list = api.driver.find_element_by_xpath('//*[@id="ListByConsumerListByConsumer_outer"]/td/'
                                                        'div[1]').text.split()
            kkt_list = [sn for sn in kkt_list if sn.isdigit() and len(sn) > 6]
            flag = 0
            for kkt in kkts:
                if kkt.split('_')[0] in kkt_list:
                    flag += 1
            if flag == len(kkts):
                final_list.append([store_naumen, kkts])
            else:
                bad_list.append([f'Не_достаточно_ккт {store_naumen}', kkts])


        except NoSuchElementException:
            store_naumen = f'Не_найден {address}'
            bad_list.append([store_naumen, kkts])

    if len(bad_list) > 0:
        with open('bad.csv', "w", newline="") as file:
            writer = csv.writer(file, delimiter=';')
            for value in bad_list:
                writer.writerow(value)
    return final_list


if __name__ == '__main__':
    create_dict_with_kkt()
