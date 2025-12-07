import json
import sqlite3
import os
import datetime
DB_NAME = 'excursion_bot.db'
FILE_INFO_NAME = 'test_excursions.json'


def drop_db(db_name):
    os.remove(db_name)

def select_all_excursions(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM excursions")
    data = cursor.fetchall()
    return data

def select_all_excursion_date(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM excursions")
    data = cursor.fetchall()
    return data

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT
        );
        """)
    cursor.execute("""
           CREATE TABLE excursions (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT,
           description TEXT
           );
           """)
    cursor.execute("""
               CREATE TABLE users_in_excursions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               excursion_id INTEGER,
               date DATE
               );
               """)
    conn.commit()
    conn.close()

def select_id_by_name(db_name, name, table):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE name={name}")
    data = cursor.fetchall()
    return data

def insert_info_from_file(db_name, file_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    data = json.load(open(file_name, encoding='utf-8'))
    for obj in data:
        cursor.execute("""
        INSERT INTO excursions(
        name, description) VALUES (?, ?);""", [*obj.values()])
        conn.commit()
    dates = json.load(open(file_name, encoding='utf-8'))
    dates_temp = []
    for date in dates:
        id_ = select_id_by_name(DB_NAME, date, 'excursions')
        print(id_)
        exit()
        cursor.execute("""
                INSERT INTO users_in_excursions(
                excursion_id, date) VALUES (?);""", (id_,))
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
    init_scenario()
    select_all_excursions(DB_NAME)