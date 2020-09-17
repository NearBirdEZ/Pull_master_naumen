import asyncio
import re

from dadata import DadataAsync


class Create_address_shop():

    def start(self, address, prefix_store, view_address):
        if view_address == 1:
            print(prefix_store, view_address, address)
            return self.__full_address(prefix_store, address)
        elif view_address == 2:
            return f'{prefix_store} {address}'
        elif view_address == 3:
            return address.lower()
        else:
            print('Что-то невообразимое случилось')

    def __dadata_address_shop(self, address):
        token = "5c9f229cb333ab8a4dde5de28588d4d0a9aff404"
        secret = "14b621d1269cac31c29384eb76f318ac6d30ae9a"
        dadata = DadataAsync(token, secret)

        async def check_address(address):
            res = await dadata.suggest(name="address", query=address, count=1)
            print(res)
            try:
                return f"{res[0]['data']['city']} {res[0]['data']['street']} " #{res[0]['data']['house']}"
            except IndexError:
                return f'bad {address}'

        loop = asyncio.new_event_loop()
        address = asyncio.run(check_address(address))
        print(address)
        loop.close()


        return address

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
            'магазин', 'ситицентр', 'ситимол', 'карамель', 'трк', ' ток ', 'звездочка', 'элем. улично-дорожн.сети',
            'проспект')
        if address.startswith('\"') or address.startswith('\''):
            address = address[1:-1]
        print(address)
        for _ in range(5):
            address = self.__replace_pattern(r'((“)|(\")|(\')|(\«)|(\())[\D\d]*((\")|(\')|(\»)|(\)|(”)))',
                                             address).strip()

            address = self.__replace_pattern(r'\d{4, }', address).strip()

            address = self.__replace_pattern(r'^\d{1, }', address).strip()

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


if __name__ == '__main__':
    pass
