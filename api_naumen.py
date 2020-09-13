from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time


class API_Naumen:
    driver = webdriver.Chrome(ChromeDriverManager().install())

    def start_naumen(self, login, password):
        """Функция старта наумена"""
        self.driver.get('http://sdn.pilot.ru:8080/fx')
        time.sleep(0.5)
        self.enter_words('login', login)
        self.enter_words("password", password,
                         '//*[@id="LogonForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/input')

    def enter_words(self, id_xpath_area, words, id_xpath_button=None, t=0.5):
        """Функция для заполнения полей по ID или XPATH
           При необходимости нажатие на кнопку. По-умолчанию без нажатия"""
        try:
            if id_xpath_area.startswith('//*[@'):
                self.driver.find_element_by_xpath(id_xpath_area).clear()
                self.driver.find_element_by_xpath(id_xpath_area).send_keys(words)
            else:
                self.driver.find_element_by_id(id_xpath_area).clear()
                self.driver.find_element_by_id(id_xpath_area).send_keys(words)
            time.sleep(t)

            if id_xpath_button:
                if id_xpath_button.startswith('//*[@'):
                    self.driver.find_element_by_xpath(id_xpath_button).click()
                else:
                    self.driver.find_element_by_id(id_xpath_button).click()
            time.sleep(t)
        except NoSuchElementException:
            raise NoSuchElementException('Вы находитесь в специфическом окне, где нельзя что либо вставить или нажать'
                                         'кнопку, может быть ошибка в пути')

    """


    Три самый часто используемые запроса поиска
    - По номеру запроса
    - По названию магазина
    - По серийному номеру


    """

    def search_by_request(self, request):
        self.enter_words('//*[@id="sdsearch_ServiceCallIdSearchType"]',
                         request,
                         '//*[@id="dosearchsdsearch_ServiceCallIdSearchType"]')

    def search_by_shop(self, shop):
        self.enter_words('//*[@id="searchString"]',
                         shop,
                         '//*[@id="doSearch"]')

    def search_by_serial_number(self, serial_number):
        self.enter_words('//*[@id="sdsearch_CMDBObjectInvNumberSearchTypeCMDBObjectAdvSearch"]',
                         serial_number,
                         '//*[@id="dosearchsdsearch_CMDBObjectInvNumberSearchTypeCMDBObjectAdvSearch"]')

    '''

    При необходимости можно удалить

    '''

    def back_to_request(func):
        # Выход на главную и переход по номеру запроса
        # Функция декоратор
        def wrapper(self, *args, **kwargs):
            print(*args)
            print(**kwargs)
            request, *_ = args
            print(request)
            self.driver.get(
                'http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid=corebofs000080000ikhm8pnur5l85oc')
            self.search_by_request(request)

            link_request = self.driver.find_element_by_xpath('//*[@id="navpath"]/a[3]').get_attribute('href')

            func(self, *args, **kwargs)

            self.driver.get(link_request)
            return

        return wrapper

    def description_body(self, request):
        """Получение текста заявки"""
        self.search_by_request(request)
        time.sleep(1)
        description = self.driver.find_element_by_class_name("servicecall_description_inner").text
        return description

    def shop_request(self, request):
        """Получить магазин у заявки"""
        self.search_by_request(request)
        time.sleep(1)
        shop = self.driver.find_element_by_xpath('//*[@id="ServiceCall.Container.Column_2.CustomerProps.'
                                                 'client"]/a/span').text
        return shop

    @back_to_request
    def send_mail(self, request, text, description):

        """Функция для отправки почты. Передается номер, текст письма(с переносами) и тело заявки
        Получение ссылки на отправку комментария
        пример:
        Здравствуйте!\nПросьба подтвердить выполенние работ ответным письмо по заявке № {query}\n{description}"""
        link_mail = self.driver.find_element_by_id("ServiceCall.MailingList.SCMailing").get_attribute("href")
        self.driver.get(link_mail)

        text = f"""{text} {request}\n{description}
                    \n\nС уважением,\nСлужба Поддержки Пользователей\nООО \"Пилот - бизнес решения для 
торговли\"\n107023, Москва, 
                    Барабанный переулок, дом 3\nтел. +7 495 564-8794\nфакс +7 495 564-8369\ne-mail: service_desk@pilot.ru """
        self.enter_words('//*[@id="mailText"]', text, '//*[@id="send"]')
        time.sleep(1)

    @back_to_request
    def send_comments(self, request, comment_text):
        link_comment = self.driver.find_element_by_id("ServiceCall.SDCommentList.AddSDComment").get_attribute("href")

        self.driver.get(link_comment)
        self.enter_words('//*[@id="text"]', comment_text, '//*[@id="add"]')
        time.sleep(1)


if __name__ == '__main__':
    pass
