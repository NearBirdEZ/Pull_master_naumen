import csv
from selenium.common.exceptions import NoSuchElementException
import create_list_kkt
import create_request
from api_naumen import API_Naumen
from config import login, password


def main():
    api = API_Naumen()
    api.start_naumen(login, password)
    store_kkt_date = create_list_kkt.create_dict_with_kkt()
    flag_kkt = int(input('Требуется уточнить какия ККТ у данного контрагента?\n'
                         '1- ККТ Pilot, вида KKT_PILOT_FP510-Ф_SN:0255100193912\n'
                         '2- KKT Шрих, вида KKT_SHTRIH_РИТЕЙЛ-01Ф_SN:0478930012035313\n'
                         '3- KKT Viki mini, вида KKT_VIKI_MINI_SN:0491002948\n'))
    contact_human = input("Введите контактное лицо в формате ФАМИЛИЯ ИМЯ ДОЛЖНОСТЬ\n")
    contact_phone = input("Введите контактный НОМЕР ТЕЛЕФОНА в без лишний символов, пожалуйста\n")
    contact_email = input("Введите контактный EMAIL формата test@test.ru\n")
    with open('final.csv', "w", newline="") as final:
        with open('what_happened.csv', "w", newline="") as bad:
            writer_final = csv.writer(final, delimiter=';')
            writer_bad = csv.writer(bad, delimiter=';')

            for row in store_kkt_date:
                address, kkt = row
                serial_number = ' '.join(kkt)
                try:
                    number = create_request.create_request(address,
                                                           serial_number,
                                                           contact_human,
                                                           contact_phone,
                                                           contact_email,
                                                           flag_kkt)
                    writer_final.writerow([address, serial_number, number])
                except NoSuchElementException:
                    writer_bad.writerow(row)


if __name__ == '__main__':
    main()
