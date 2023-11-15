import sqlite3 as sq


def load_row(table, wb_id=None):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        if wb_id:
            sql_query = f"""
                SELECT *
                FROM {table}
                WHERE wb_id = {wb_id};
            """
            cur.execute(sql_query)
            row = cur.fetchone()
        else:
            sql_query = f"""SELECT * FROM {table};"""
            cur.execute(sql_query)
            row = cur.fetchall()

    return row


def save_price(price, wb_id, table):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            UPDATE {table}
            SET price = {price}
            WHERE wb_id = {wb_id};
        """
        cur.execute(sql_query)
        con.commit()


def save_in_suitable_products_table(wb_id, name, current_wb_price, search_price):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query_insert = f"""
            INSERT OR REPLACE INTO suitable_products_table (wb_id, name, current_wb_price, search_price)
            VALUES('{wb_id}', '{name}', '{current_wb_price}', '{search_price}')
        """

        cur.execute(sql_query_insert)
        con.commit()


def mixing_table():
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()

        cur.execute('CREATE TABLE temp_table AS SELECT * FROM suitable_products_table ORDER BY RANDOM();')
        cur.execute('DROP TABLE suitable_products_table;')
        cur.execute('ALTER TABLE temp_table RENAME TO suitable_products_table;')

        con.commit()


def save_announced(wb_id, announced):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        if announced is True:
            sql_query = f"""
                UPDATE suitable_products_table 
                SET announced = 'True'
                WHERE wb_id = {wb_id};
            """
        else:
            sql_query = f"""
                UPDATE suitable_products_table 
                SET announced = 'True'
                WHERE wb_id = {wb_id};
            """

        cur.execute(sql_query)
        con.commit()
