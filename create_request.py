from api_naumen import API_Naumen
import time


class Flag_error(Exception):
    pass


def create_request(address: str,
                   serial_number: str,
                   contact_human: str,
                   contact_phone: str,
                   contact_email: str,
                   flag_kkt: int):
    api = API_Naumen()
    driver = api.driver
    api.search_by_shop(address)
    """Заполнение выпадающих списков 
        - Привязать к Плановая замена ФН
        - Тип запроса New
        - Канал приема заявки Email"""

    lst_xpath = ['//*[@id="link_object"]/option[@nonshifted="ККТ: Плановая замена ФН"]',
                 '// *[ @ id = "servicecall_case"] / option[@nonshifted="new"]',
                 '//*[@id="valuefabaseo2k2u0o0000lch8jk1k366sge8"]/option[@nonshifted="По электронной почте"]']
    for xpath in lst_xpath:
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.5)

    """Заполнение полей словами"""
    serial_numbers_area = ["ККТ № " + line.split("_")[0] + " Срок действия " + line.split("_")[1]
                           for line in serial_number.split()]

    serial_numbers_area = "\n".join(serial_numbers_area)

    text_area = f"""Требуется заменить ФН
Работы необходимо выполнить не ранее, чем за 21 день, и не позднее чем за 10 дней до доты блокировки ФН, указанной в \
описаниии заявки

{serial_numbers_area}"""

    dict_id_area = {"call_description": text_area,
                    "contact_human": contact_human,
                    "contact_phone": contact_phone,
                    "contact_email": contact_email}

    for id_object in dict_id_area:
        api.enter_words(id_object, dict_id_area[id_object])
    driver.find_element_by_id("add").click()

    """добавление ресурсов к заявке и перевод в статус "зарегистрирована"""

    "Сохраняем сылку на зарегистрированную заявку и ее номер"
    link_request = driver.find_element_by_xpath('//*[@id="navpath"]/a[3]').get_attribute("href")

    link_resource = driver.find_element_by_xpath('//*[@id="Resources"]').get_attribute("href")

    number = driver.find_element_by_xpath('//*[@id="title_td"]').text

    time.sleep(1)
    driver.get(link_resource)

    link_add_resource = driver.find_element_by_xpath('//*[@id="Resources.ServiceCallResourcesList.ServiceCallResou' +
                                                     'rcesListActionContainer.ObjectListReport.tableListAndButtons.' +
                                                     'ServiceCallResourcesListServiceCallResourcesList.SetRelationWi' +
                                                     'zard"]').get_attribute("href")
    driver.get(link_add_resource)

    """Добавить серийные номера"""
    serial_numbers = [sn.split("_")[0] for sn in serial_number.split()]
    for sn in serial_numbers:
        if flag_kkt == 1:
            sn = f'KKT_PILOT_FP{sn[3:6]}-Ф_SN:{sn}'
        elif flag_kkt == 2:
            sn = f'KKT_SHTRIH_РИТЕЙЛ-01Ф_SN:{sn}'
        elif flag_kkt == 3:
            sn = f'KKT_VIKI_MINI_SN:{sn}'
        else:
            print(f'Херня какая-то: не верно присвоен флаг {flag_kkt} для магазина {address}')
            raise Flag_error
        # вставка по названию
        api.enter_words('//*[@id="titleSearchString"]',
                        sn,
                        '//*[@id="titleSearchRB"]')
        """api.enter_words("invNumberSearchString", sn)
        driver.find_element_by_id('invNumberSearchRB').click()"""
        driver.find_element_by_xpath('//*[@id="Resources.ServiceCallResourcesList.ServiceCallResourcesListActionConta' +
                                     'iner.ObjectListReport.tableListAndButtons.ServiceCallResourcesListServiceCallRe' +
                                     'sourcesList.SetRelationWizard.tableContainer.SearchResultsListParent.SearchResu' +
                                     'ltsList.selectedObjects__chkbox"]').click()
        driver.find_element_by_xpath('//*[@id="add"]/img').click()
    driver.find_element_by_id("next").click()

    driver.get(link_request)

    link_change_type = driver.find_element_by_xpath('//*[@id="ServiceCall.ServiceCallCard.SetServiceCallCase"]'
                                                    ).get_attribute("href")
    driver.get(link_change_type)

    xpath_restore = '//*[@id="case"]/option[@nonshifted="Восстановление работоспособности"]'
    driver.find_element_by_xpath(xpath_restore).click()
    time.sleep(0.3)
    xpath_category_fn = '//*[@id="valuefabasefs000080000kcn652egnnr2opk"]/option[@nonshifted="ККТ: Замена ФН"]'
    driver.find_element_by_xpath(xpath_category_fn).click()
    time.sleep(0.1)
    driver.find_element_by_xpath('//*[@id="edit"]').click()
    driver.get(link_request)

    time.sleep(1)
    return number


if __name__ == '__main__':
    pass
