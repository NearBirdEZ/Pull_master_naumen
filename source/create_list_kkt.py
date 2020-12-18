from api_naumen import API_Naumen
import csv
from create_address_shop import Create_address_shop
import os
from selenium.common.exceptions import NoSuchElementException


def create_dict_with_kkt(prefix_store, view_address):
    """Создание словаря вида 'Адрес магазина: [ккт_магазина, ккт_магазина2]'
    """
    store_kkt = {}  # Перевести файл CSV в словарь.
    final_list = []
    bad_list = []
    os.chdir(os.getcwd() + '\\Directory_for_CSV_files')

    with open(os.getcwd() + '\\pull.csv', "r", newline="") as pull:
        reader = csv.reader(pull)
        for row in reader:
            row = " ".join(row).split(';')
            if len(row) < 3:
                print('Не все столбцы заполнены')
                """По хорошему raise необходим"""
                break
            raw_store, kkt, date, *_ = [x.strip().lower() for x in row]
            date, *_ = date.split(' ')

            if store_kkt.get(raw_store):
                store_kkt[raw_store].append(f'{kkt}*{date}')
            else:
                store_kkt[raw_store] = [f'{kkt}*{date}']
    # Создание экземпляра класса для вызова функции, которая преобразует адрес, предоставленный заказчиков в корректный
    shop = Create_address_shop()

    """Отсключенная функция, должен был быть счетчик провереных магазинов"""
    total_lines = len(store_kkt)

    api = API_Naumen()  # Создание экземпляра класса взаимодействия с науменом
    count = 0  # Обнуляем счетчик выполенных
    for address, kkts in store_kkt.items():
        count += 1
        # Получение адреса происходит тут через API dadata
        address_from_api = shop.start(address, prefix_store, view_address)
        if not address_from_api.startswith('bad'):
            api.search_by_shop(address_from_api)  # Поиск по адресу в наумене
        else:
            bad_list.append([address_from_api, kkts])
            continue

        """Блок проверки наличия ккт в магазине. Проискходит сверка ккт, которые есть в наумене и представленных"""
        try:

            store_naumen = api.driver.find_element_by_xpath('//*[@id="ServiceCallRegistrationNew.RegForm.'
                                                            'MainContainer.LeftColumn.clientProperties.title"]'
                                                            '/a').text
            uuid_store = api.driver.current_url.split('ServiceCallRegistrationNew&contractUuid=')[1]

            api.driver.get(
                f'http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid={uuid_store}&activeComponent=Cfg'
                f'Resources&contractUuid={uuid_store}')

            api.driver.find_element_by_xpath('//*[@id="pageSize"]/option[@nonshifted="100"]').click()

            kkt_list = api.driver.find_element_by_xpath('//*[@id="ListByConsumerListByConsumer_outer"]/td/'
                                                        'div[1]').text.split()
            """Новый вариант"""
            """Отсеиваем лишнее из списка"""
            names_kkt_list = []  # Хранятся ккт вида 	KKT_PILOT_FP510-Ф_SN:0255100102020 со страницы
            for serial_number in kkt_list:
                if serial_number.endswith('(P)'):
                    serial_number = serial_number[:-3]
                if serial_number[-9:].isdigit() and serial_number.startswith('KKT'):
                    names_kkt_list.append(serial_number)
            kkts_final_list = []
            for serial_number in kkts:
                for names_serial_number in names_kkt_list:
                    if names_serial_number.endswith(serial_number.split('*')[0]):
                        kkts_final_list.append(f"{names_serial_number}*{serial_number.split('*')[1]}")
                        break
            if len(kkts_final_list) == len(kkts):
                final_list.append([store_naumen, kkts_final_list])
            else:
                bad_list.append([f'Не_достаточно_ккт {store_naumen}', kkts])

        except NoSuchElementException:
            store_naumen = f'Не_найден {address}'
            bad_list.append([store_naumen, kkts])
        print(f'Проверено адресов: {count} из {total_lines}')

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
