import sqlite3
import os

DB_NAME = 'button_bot.db'
FILE_INFO_NAME = 'input_data.txt'


def drop_db(db_name):
    os.remove(db_name)

def select_all(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM city_attractions")
    data = cursor.fetchall()
    print(data)

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE city_attractions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        object_type TEXT,
        description TEXT
        );
        """)
    conn.commit()
    conn.close()

def insert_info_from_file(db_name, file_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    data = open(file_name, encoding="utf-8").read().split('\n----------\n')
    for obj in data:
        fields = obj.split('\n#\n')
        cursor.execute("""
        INSERT INTO city_attractions(
        city, object_type, name, description
        ) VALUES (?, ?, ?, ?);""", fields)
        conn.commit()
    conn.close()

def init_scenario():
    drop_db(DB_NAME)
    create_db(DB_NAME)
    insert_info_from_file(DB_NAME, FILE_INFO_NAME)

def get_details(city, object_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name, description 
    FROM city_attractions
    WHERE city = ? AND object_type = ?""", (city, object_type))
    data = cursor.fetchall()
    data = ', '.join([f'{x[0]}: {x[1]}' for x in data])
    conn.close()
    return data


if __name__ == '__main__':
    # drop_db(DB_NAME)
    create_db(DB_NAME)
    insert_info_from_file(DB_NAME, FILE_INFO_NAME)
    select_all(DB_NAME)