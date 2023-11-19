import requests
import re


def settings(url, page=''):
    url = f'{url}{page}'

    headers = {
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'Referer': 'https://www.wildberries.ru/catalog/164614093/detail.aspx',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url=url, headers=headers, timeout=60)
    if response.status_code != 200:
        return 0

    return response.json()


def prepare_items(response):
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
                if float(product.get('salePriceU', None)) / 100 > 1000:
                    products.append({
                        'Наименование': product.get('name', None),
                        'Бренд': product.get('brand', None),
                    'Цена со скидкой': float(product.get('salePriceU', None)) / 100 if
                    product.get('salePriceU', None) != None else None,
                    'Артикул, id': product.get('id', None),
                })

    return products


def hoarder(url, page):
    response = settings(url, page)
    products = prepare_items(response) if response else []

    return products


def get_category(url):
    product_list = []
    control = True
    cnt = 1
    while True:
        products = hoarder(url, f'{cnt}')
        print(cnt)
        if products:
            product_list.extend(products)
            control = True
        else:
            if control:
                control = False
            else:
                break
        cnt += 1

    return product_list


def curl_creator(id_, vol=4, part=6):
    for number in range(0, 17):
        num = number if number >= 10 else '0' + str(number)
        url = f'https://basket-{num}.wb.ru/vol{str(id_)[:vol]}/part{str(id_)[:part]}/{str(id_)}/info/ru/card.json'
        try:
            response = settings(url)
            if response:
                break
        except Exception:
            continue
    return response, url


def get_power(description):
    pattern = r'(\d+(?:\.\d+)?)\s*(?:кВт|Вт|квт)'

    match_list = re.findall(pattern, description)
    if match_list:
        power = match_list[0]

        shortening = power.replace('.', '').replace('0', '')
        if len(shortening) >= 3:
            power = float(power) / 1000

        return float(power)
    else:
        return 0


def get_product(id_):
    response, url_ = curl_creator(id_)
    if response == 0:
        response, url_ = curl_creator(id_, 3, 5)
        if response == 0:
            response, url_ = curl_creator(id_, 2, 4)
    if response == 0:
        return 0, 0

    photo_link = url_.replace('info/ru/card.json', 'images/big/1.webp')

    grouped_options = response.get('grouped_options', None)
    description = response.get('description', None)
    power = str(get_power(description))
    power = f'Мощность : {power} кВт' if power != '0' else None

    if grouped_options:
        if type(grouped_options[0]) is not int:
            dirty_property_list = []
            for option in grouped_options:
                dirty_property_list.extend(option.get('options', None))
            property_ = ''
            properties = ['ощность', 'апряжение', 'апуск', 'корость', 'вигатель', 'борот', 'свар', 'итани',
                          'ккумулятор', 'Тип', 'нергия', 'репление', 'удар', 'рутящий']

            for item in dirty_property_list:
                for i in properties:
                    if i in item['name']:
                        property_ += item['name'] + ' : ' + item['value'] + '\n'

            if not property_:
                property_ = power
            return property_, photo_link
    else:
        return power, photo_link



