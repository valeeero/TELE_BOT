import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config

# Connecting or adding ( if don't have ) database

try:
    connection = psycopg2.connect(user=config.user,
                                  password=config.password,
                                  host=config.host,
                                  port=config.port,
                                  database=config.database)

    cursor = connection.cursor()
    print("INFO about server PostgreSQL (Информация о сервере PostgreSQL):")
    print(connection.get_dsn_parameters(), "\n")
    # create_table_query = '''CREATE TABLE client
    #                           (ID INT PRIMARY KEY NOT NULL,
    #                           Full name TEXT NOT NULL,
    #                           Phone number TEXT NOT NULL,
    #                           City TEXT NOT NULL,
    #                           NP point TEXT NOT NULL); '''
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to (Вы подключены к) - ", record, "\n")


except (Exception, Error) as error:
    try:
        connection = psycopg2.connect(user=config.user,
                                      password=config.password,
                                      host=config.host,
                                      port=config.port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_create_database = f'create database {config.database}'
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connecting with PostgreSQL closed! (Соединение с PostgreSQL закрыто!)")

try:
    connection = psycopg2.connect(user=config.user,
                                  password=config.password,
                                  host=config.host,
                                  port=config.port,
                                  database=config.database)

    cursor = connection.cursor()
    create_table_query = '''CREATE TABLE client
                          (ID INT PRIMARY KEY NOT NULL,
                               Full_name TEXT NOT NULL,
                               Phone_number TEXT NOT NULL,
                               City TEXT NOT NULL,
                               NP_point TEXT NOT NULL);
                          CREATE TABLE product
                          (ID INT PRIMARY KEY NOT NULL,
                               client_id INT REFERENCES client(id),
                               Number_order INT NOT NULL,
                               size TEXT NOT NULL,
                               color TEXT NOT NULL,
                               url TEXT NOT NULL);'''
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")


def create_object(
        table,
        id=None, full_name=None, phone_number=None,
        city=None, np_point=None, client_id=None, number_order=None,
        size=None, color=None, url=None
):
    try:
        connection = psycopg2.connect(user=config.user,
                                      password=config.password,
                                      host=config.host,
                                      port=config.port,
                                      database=config.database)

        cursor = connection.cursor()

        if table == 'client':
            insert_query = f""" INSERT INTO client
             (id, full_name, phone_number, city, np_point) 
             VALUES 
             ({id}, '{full_name}', '{phone_number}', '{city}', '{np_point}')
                           """
            cursor.execute(insert_query)
        elif table == 'product':
            insert_query = f"""INSERT INTO product
            (id, client_id, number_order, size, color, url)
            VALUES
            ({id}, '{client_id}', '{number_order}', '{size}', '{color}', '{url}')
                           """
            cursor.execute(insert_query)
        connection.commit()
        print("1 запись успешно вставлена")

        cursor.execute("SELECT * from client; SELECT * from product;")
        print("Результат", cursor.fetchall())

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
