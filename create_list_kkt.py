import csv
from create_address_shop import Create_address_shop
from api_naumen import API_Naumen
from selenium.common.exceptions import NoSuchElementException
import time


def transfer_kostil(prefix_store_, view_address_):
    """Костыль необдуманности"""
    global prefix_store, view_address
    prefix_store = prefix_store_
    view_address = view_address_


def create_dict_with_kkt(scale_amount_zero):
    """Создание словаря вида 'Адрес магазина: [ккт_магазина, ккт_магазина2]'
    """
    store_kkt = {}
    final_list = []
    bad_list = []
    with open('./pull.csv', "r", newline="") as pull:
        reader = csv.reader(pull)
        for row in reader:
            row = " ".join(row).split(';')
            if len(row) < 3:
                print('Не все столбцы заполнены')
                """По хорошему raise необходим"""
                break
            raw_store, kkt, date = [x.strip().lower() for x in row]
            date, *_ = date.split(' ')
            kkt = '0' * scale_amount_zero + kkt

            if store_kkt.get(raw_store):
                store_kkt[raw_store].append(f'{kkt}_{date}')
            else:
                store_kkt[raw_store] = [f'{kkt}_{date}']

    shop = Create_address_shop()  # Создание экземпляра класса для вызова функции, которая преобразует адрес, предоставленный заказчиков в корректный

    """Отсключенная функция, должен был быть счетчик провереных магазинов"""
    total_lines = len(store_kkt)

    api = API_Naumen()  # Создание экземпляра класса взаимодействия с науменом
    count = 0  # Обнуляем счетчик выполенных
    for address, kkts in store_kkt.items():
        count += 1
        address_from_api = shop.start(address, prefix_store,
                                      view_address)  # Получение адреса происходит тут через API dadata
        api.search_by_shop(address_from_api)  # Поиск по адресу в наумене

        """Блок проверки наличия ккт в магазине. Проискходит сверка ккт, которые есть в наумене и представленных"""
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
            """Отсеиваем лишнее из таблицы на странице магазина. Выбираем только инвентарные номера больше 6 символов"""
            kkt_list = [serial_number for serial_number in kkt_list if
                        serial_number.isdigit() and len(serial_number) > 6]
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
        """Если список с какими-то ошибками пуст, то создаем файл bad.csv
        Ошибки:
        1. Магазин не найдет в системе наумен, либо есть дубли
        2. В магазине нет какой-то из ккт
        """
        with open('bad.csv', "w", newline="") as file:
            writer = csv.writer(file, delimiter=';')
            for value in bad_list:
                writer.writerow(value)
    """Возвращаем корректный список для заведения заявок, где по каждому индексу почти готовая заявка"""
    return final_list


if __name__ == '__main__':
    pass
