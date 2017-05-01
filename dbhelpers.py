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
    geodata TEXT)''')
    db.commit()
    db.close()


def insert_house(price, address, url, image):

    db = sqlite3.connect("daftinfo.sqlite")
    cur = db.cursor()
    cur.execute("""INSERT INTO Houses (price, address, link, image) VALUES (?,?,?,?)""", (price, address, url, image))
    db.commit()
    db.close()