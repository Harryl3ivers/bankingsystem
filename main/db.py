import sqlite3
from decimal import Decimal
from datetime import datetime

def initialise_db(db_path = "bank.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                   account_number TEXT PRIMARY KEY,
                   account_name TEXT NOT NULL,
                   balance REAL NOT NULL DEFAULT 0.0,
                   created_at TEXT NOT NULL)
                ''')
    conn.commit()
    conn.close()

def insert_account(db_path,account_number, account_name, balance):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO accounts (account_number, account_name, balance, created_at)
                       VALUES(?,?,?,?)''',
                       (account_number, account_name, float(balance), datetime.now().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("Account already exists")
    finally:
        conn.close()

def get_account(db_path , account_number):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT account_number, account_name, balance, created_at FROM accounts WHERE account_number=?''',(account_number,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "account_number": row[0],
            "account_name": row[1],
            "balance": Decimal(str(row[2])),
            "created_at": row[3]
        }

def get_balance(db_path, account_number):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT balance FROM acccounts WHERE account_number=?''',(account_number))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Decimal(str(row[0]))
    return None

def update_balance(db_path,account_number, new_balance):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''UPDATE accounts SET balance=? WHERE account_number=?''',
                   (float(new_balance), account_number))
    conn.commit()
    conn.close()
    