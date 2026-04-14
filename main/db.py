import sqlite3
from decimal import Decimal
from datetime import datetime


class BankDB:
    def __init__(self, db_path="bank.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.initialise_db()
    
    def close(self):
        self.conn.close()

    def initialise_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                account_name TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_account(self, account_number, account_name, balance):
        try:
            self.cursor.execute('''
                INSERT INTO accounts (account_number, account_name, balance, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                account_number,
                account_name,
                float(balance),
                datetime.now().isoformat()
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Account already exists")

    def get_account(self, account_number):
        self.cursor.execute('''
            SELECT account_number, account_name, balance, created_at
            FROM accounts
            WHERE account_number=?
        ''', (account_number,))
        row = self.cursor.fetchone()

        if row:
            return {
                "account_number": row[0],
                "account_name": row[1],
                "balance": Decimal(str(row[2])),
                "created_at": row[3]
            }
        return None

    def get_balance(self, account_number):
        self.cursor.execute('''
            SELECT balance FROM accounts WHERE account_number=?
        ''', (account_number,))
        row = self.cursor.fetchone()
        return Decimal(str(row[0])) if row else None

    def update_balance(self, account_number, new_balance):
        self.cursor.execute('''
            UPDATE accounts SET balance=? WHERE account_number=?
        ''', (float(new_balance), account_number))
        self.conn.commit()

    