import csv
import sqlite3
import os

DB_NAME = 'excursion_bot.db'
FILE_INFO_NAME = 'test_data.csv'

def drop_db(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE excursion_names (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        description text
        );
    """)
    cursor.execute("""    
    CREATE TABLE excursion_dates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        excursion_name_id integer,
        date datetime
        );
	""")
    cursor.execute("""    
    CREATE TABLE user_in_excursion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id integer,
        excursion_date_id integer
        );
    """)
    conn.commit()
    conn.close()

def insert_info_from_file(db_name, file_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    file = open(file_name)
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    exc_names_set = set()
    for row in csv_reader:
        if row[1] not in exc_names_set:
            cursor.execute("""
                INSERT INTO excursion_names(
                name, description) VALUES (?, ?);""", (row[1], row[2]))
            exc_names_set.add(row[1])
            excursion_id = cursor.lastrowid
        else:
            cursor.execute("""
                SELECT id FROM excursion_names WHERE name = ?;""", (row[1],))
            excursion_id = cursor.fetchone()[0]
        cursor.execute("""
                INSERT INTO excursion_dates(
                excursion_name_id, date) VALUES (?, ?);""", (excursion_id, row[3]))
        conn.commit()
    conn.close()

def select_all_excursions(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM excursion_names")
    data = cursor.fetchall()
    return data

def select_all_excursion_dates(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM excursion_dates")
    data = cursor.fetchall()
    return data

def select_description_by_id(db_name, id_):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM excursion_names WHERE id = ?", (id_,))
    data = cursor.fetchone()[0]
    return data

def select_dates_by_id(db_name, id_):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date FROM excursion_dates WHERE excursion_name_id = ?", (id_,))
    data = cursor.fetchall()
    return data

def select_all_users(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_in_excursion")
    data = cursor.fetchall()
    return data

def insert_user_in_excursion(db_name, user_id, excursion_date_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_in_excursion(
    user_id,
    excursion_date_id
    ) VALUES (?, ?);""", (user_id, excursion_date_id))
    conn.commit()
    conn.close()

def reinit_scenario():
    drop_db(DB_NAME)
    create_db(DB_NAME)
    insert_info_from_file(DB_NAME, FILE_INFO_NAME)


if __name__ == '__main__':
    reinit_scenario()
    print(select_all_excursion_dates(DB_NAME))
    print(select_all_excursions(DB_NAME))
