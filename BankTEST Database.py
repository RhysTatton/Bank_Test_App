import sqlite3

db = sqlite3.connect('basic_bank.db')
cursor = db.cursor()

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username VARCHAR (255) NOT NULL UNIQUE,
        password_hash VARCHAR (255) NOT NULL,
        balance REAL NOT NULL
        )''')
    db.commit()
except Exception as e:
    print("Error creating the table has occurred", e)
    db.rollback()

try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
    )''')
    db.commit()
except Exception as e:
    print("Error creating the table has occurred", e)
    db.rollback()

db.close()
