import time

from wb_master import get_category
from sql_master import load_row, save_price, save_in_suitable_products_table, mixing_table, save_announced
from tg_master import message, error_message
from url_master import category_url


def countdown(minutes):
    for remaining_minutes in range(minutes, -1, -1):
        if remaining_minutes > 0:
            print(f'До новой итерации осталось ждать {remaining_minutes} минут(ы)')
            time.sleep(60)  # Подождать 60 секунд (1 минута)
        else:
            print('Начинаю новую итерацию!')


def compare(price_wb, price_search, percent=35):
    price_wb, price_search = float(price_wb), float(price_search)
    difference = (price_search - price_wb) / price_search * 100
    if 120 > difference > percent and price_search > 4000:
        check_difference = True
    else:
        check_difference = False

    return check_difference


def product_monitoring():
    mixing_table()
    product_list = load_row('suitable_products_table')

    cnt = 15
    for product in product_list:
        id_, name, price_curr, search_price, announced = product[0], product[1], product[2], product[4], product[5]
        link, photo = load_row('search_table', id_)[3], load_row('wb_table', id_)[3]
        current_price = load_row('wb_table', id_)[2]

        if price_curr != current_price:
            save_announced(id_, False)
            announced = 'True'
        if announced:
            continue
        if not link or not photo:
            continue

        message(photo=photo, name=name, id_=id_, new_price=current_price, search_price=search_price, link=link)
        save_announced(id_, True)

        cnt -= 1
        if cnt == 0:
            break

    countdown(3)


def main(url):
    category_list = get_category(url)

    for product in category_list:
        try:
            price, id_ = product['Цена со скидкой'], product['Артикул, id']

            if load_row('wb_table', id_) and load_row('search_table', id_):
                name, photo = load_row('wb_table', id_)[1], load_row('wb_table', id_)[3]
                search_price, link = load_row('search_table', id_)[2], load_row('search_table', id_)[3]
            else:
                continue

            if photo and link != '0':
                save_price(id_, price, 'wb_table')
                check_difference = compare(price, search_price)

                if check_difference:
                    save_in_suitable_products_table(id_, name, price, search_price)
        except Exception as e:
            error_message(e)


if __name__ == '__main__':
    category_dict = category_url()
    while True:
        # try:
            for key, value in category_dict.items():
                print(key)
                main(value)
            product_monitoring()
        # except Exception as e:
        #     error_message(e)
        #     continue

