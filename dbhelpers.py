# Create a database and a table Houses
import sqlite3


def initialize_db():
    db = sqlite3.connect("daftinfo.sqlite")
    cur = db.cursor()
    cur.execute(''' DROP TABLE IF EXISTS Houses''')
    cur.execute('''
    CREATE TABLE Houses (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    price TEXT,
    address TEXT,
    link TEXT,
    image TEXT,
    meters_walk_to_ov INTEGER,
    time_walk_to_ov TEXT,
    time_for_sorting INTEGER,
    time_walk_to_dart TEXT,
    dart_for_sorting INTEGER,
    dart_station TEXT)''')
    db.commit()
    db.close()


def insert_house(price, address, url, image):
    db = sqlite3.connect("daftinfo.sqlite")
    cur = db.cursor()
    cur.execute("""INSERT INTO Houses (price, address, link, image) VALUES (?,?,?,?)""", (price, address, url, image))
    db.commit()
    db.close()


def update_house(id, distance, duration, sorting_time, distance_to_dart, dart_sorting, near_by_dart):
    db = sqlite3.connect("daftinfo.sqlite")
    cur = db.cursor()
    cur.execute("""UPDATE Houses SET meters_walk_to_ov = ?, time_walk_to_ov = ?, time_for_sorting = ?, time_walk_to_dart = ?, dart_for_sorting = ?, dart_station = ?  WHERE id = ?""", (distance, duration, sorting_time, distance_to_dart, dart_sorting, near_by_dart, id))
    db.commit()
    db.close()

def get_addresses():
    db = sqlite3.connect("daftinfo.sqlite")
    cur = db.cursor()
    cur.execute('''SELECT address, id FROM Houses''')
    addresses = cur.fetchall()
    db.commit()
    db.close()
    return addresses

def get_houses():
    db = sqlite3.connect("daftinfo.sqlite")
    cur = db.cursor()
    cur.execute("""SELECT time_walk_to_ov, address, price, link, dart_station, time_walk_to_dart FROM Houses ORDER BY time_for_sorting""")
    houses = cur.fetchall()
    db.commit()
    db.close()
    return houses