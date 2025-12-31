from decimal import Decimal
from main.validator import Validator
from main.db import initialise_db, insert_account , get_account, update_balance, get_balance
import sqlite3

class Transaction:
    def __init__(self):
        self.validator = Validator()
        self.db_path = "bank.db"
    
    def deposite(self,account_number,amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)
        account = get_account(self.db_path,account_number)
        if not account:
            raise ValueError("Account not found")
        conn = sqlite3.connect(self.db_path)
        try:
            old_balance = get_balance(self.db_path,account_number)
            new_balance = old_balance + amount
            update_balance(self.db_path,account_number,new_balance)
            return new_balance
        finally:
            conn.close()
    
    def withdraw(self,account_number,amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)
        account = get_account(self.db_path,account_number)
        if not account:
            raise ValueError("Account not found")
        conn = sqlite3.connect(self.db_path)
        try:
            old_balance = get_balance(self.db_path,account_number)
            new_balance = old_balance - amount
            if new_balance <0:
                raise ValueError("Insufficient funds")
            update_balance(self.db_path,account_number,new_balance)
            return new_balance
        finally:
            conn.close()
            

             

       
        