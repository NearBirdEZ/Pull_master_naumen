from dadata import DadataAsync
import asyncio
import re
import csv


class Create_address_shop:

    def __get_what_is_address(self):
        flag = input('Какой формат адреса предоставил заказчик?\n'
                     '1 - адрес\n'
                     '2 - номер магазина или код точки\n'
                     '3 - готовые адреса, сгенерированные в Naumen, например с помощью Excel и ВПР\n')
        if flag not in ['1', '2', '3']:
            print('Так, давай по-новой. Цифры от 1 до 3-х')
            return self.__get_what_is_address()
        else:
            return flag

    def __get_prefix_shop(self):
        prefix = int(input('Введите префикс магазина \n'
                           '1 - детский мир\n'
                           '2 - алькор и ко\n'
                           '3 - тами и ко\n'
                           '4 - иль де ботэ\n'
                           '5 - леви\n'
                           '6 - манго\n'
                           '7 - атак\n'
                           '8 - ашан\n'
                           '9 - нью йоркер рус'))
        if prefix in range(1, 10):

            prefixs = (
                'детский мир', 'алькор и ко', 'тами и ко', 'иль де ботэ', 'леви', 'манго', 'атак', 'ашан',
                'нью йоркер рус')
            return prefixs[prefix - 1]
        else:
            print('Ну ё-маё, давай снова. Используй цифры, которые представлены в диалоговом окне (1-9)')
            return self.__get_prefix_shop()

    def get_information(self):
        flag = self.__get_what_is_address()
        if flag in ('1', '2'):
            prefix = self.__get_prefix_shop()
        else:
            prefix = ""
        return flag, prefix

    def start(self, address, static_information: tuple):
        flag, prefix = static_information
        if flag == '1':
            return self.__full_address(prefix, address)
        elif flag == '2':
            return f'{prefix} {address}'
        elif flag == '3':
            return address.lower()
        else:
            print('Что-то невообразимое случилось')

    def __dadata_address_shop(self, address):
        token = "5c9f229cb333ab8a4dde5de28588d4d0a9aff404"
        secret = "14b621d1269cac31c29384eb76f318ac6d30ae9a"
        dadata = DadataAsync(token, secret)

        async def check_address(address):
            res = await dadata.suggest(name="address", query=address, count=1)
            try:
                """
                return f"{res[0]['data']['city']} {res[0]['data']['street']} {res[0]['data']['house']}"
                Special for New Yorker
                """
                return f"{res[0]['data']['city']} {res[0]['data']['street']}"
            except IndexError:
                return f'bad {address}'

        event_loop = asyncio.get_event_loop()
        address = event_loop.run_until_complete(asyncio.gather(asyncio.ensure_future(check_address(address))))

        return address[0]

    def __replace_pattern(self, pattern, address):
        replaces = re.search(pattern, address)
        if replaces:
            replaces = replaces.group(0)
            address = address.replace(replaces, ' ')
        return address

    def __full_address(self, name_shop, address):
        address_tmp = address

        resplaces = (
            'россия', ' из ', 'литер', 'литера', ' вл. ', 'кв-л.', 'к.лит.', 'корп.', 'микрорайон', 'мкр-н', 'владение',
            'лит.', 'тц', 'трц', 'кв-л.', 'с/п', 'x', 'l', 'к.лит', ' тк ', 'к.стр.', 'кв.', 'к.', 'афимол',
            ' км ', 'калейдоскоп', 'мега', 'атриум', ' рио ', 'водолей', 'белая дача', 'вавилон', 'орбита',
            'галерея', 'весна', 'км.', 'плаза', '№', '#', 'цум', 'премьер', 'твк', 'золотой', 'вавилон',
            'vegas', 'вегас', 'молл', 'галактика', 'гринвич', 'лента', ' окей ', 'ашан', 'атак', 'метро',
            'пассаж', 'квартал', 'атлас', 'панорама', 'европарк', ' спар  ', ' д.', 'парус', 'лайнер',
            'корабль', 'светофор', 'апельсин', 'олимпик', ' север ', 'мармелад', 'каштан', 'шоколад',
            'российская федерация', ' фо ', '-й', 'глобус', 'пр-кт.', 'наб.', ' лето ', 'ривьера', 'авиапарк',
            'европейский', 'капитолий', 'рио', 'проезд', 'олимп ', 'строение', 'дм ', 'детский мир',
            'алькор и ко', 'алькор ', ' ам ', ',', ' фо.', ' мо ', ' м.о ', ' мо.', ' форум ', 'иль де ботэ',
            'магазин', 'ситицентр', 'ситимол', 'карамель', ' трк ', ' ток ', 'звездочка', 'элем. улично-дорожн.сети')
        if address.startswith('\"') or address.startswith('\''):
            address = address[1:-1]
        for _ in range(5):
            address = self.__replace_pattern(r'((“)|(\")|(\')|(\«)|(\())[\D\d]*((\")|(\')|(\»)|(\)|(”)))',
                                             address).strip()
            address = self.__replace_pattern(r'\d{4, }', address).strip()
            address = self.__replace_pattern(r'^[\d]*', address).strip()
        address = self.__replace_pattern(r'[/][\w]*', address).strip()
        address = self.__replace_pattern(r'\w{3,}\d{1,}', address).strip()

        for rep in resplaces:
            address = address.strip().replace(rep, ' ')

        address = self.__dadata_address_shop(address)
        address = ". ".join(address.split('.')).replace('-й', ' ')
        if 'none' in address:
            address = f'bad {address_tmp}'
        if address.startswith('bad'):
            return address
        return f'{name_shop} {address}'


def main():
    shop = Create_address_shop()
    static_information = shop.get_information()

    with open('shop.txt', 'r', encoding='UTF-8') as file:
        total_line = sum(1 for _ in file)

    with open('shop.txt', 'r', encoding='UTF-8') as file:
        count = 0
        with open('test.csv', "w", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            for address in file:
                address = address.lower()
                magaz = shop.start(address, static_information)
                writer.writerow([address, magaz])
                count += 1
                print(f'\n\n\n{count} СДЕЛАНО из {total_line} \n\n\n')


if __name__ == '__main__':
    main()
