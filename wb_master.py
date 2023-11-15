import requests


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


