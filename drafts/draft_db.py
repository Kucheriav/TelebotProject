import sqlite3
import os
def select_all():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM city_info")
    data = cursor.fetchall()
    print(data)

def drop_db():
    os.remove("test.db")

def create_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS city_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    object_type TEXT,
    name TEXT,
    description TEXT
    );
    """)
    conn.commit()
    conn.close()

def insert_from_file(filename):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    data = open(filename, encoding='utf8').read().split('\n----------\n')
    for x in data:
        fields = x.split('\n#\n')
        print(fields)
        cursor.execute(
            "INSERT INTO city_info(city, object_type, name, description) VALUES (?, ?, ?, ?);",
            fields
        )
        conn.commit()
    conn.close()



if __name__ == '__main__':
    drop_db()
    create_db()
    insert_from_file('input_data.txt')

