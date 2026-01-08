from decimal import Decimal
from main.validator import Validator
from main.db import initialise_db, insert_account, get_account, update_balance, get_balance
import sqlite3


class Transaction:
    def __init__(self, db_path="bank.db"):
        self.validator = Validator()
        self.db_path = db_path
    
    def deposite(self, account_number, amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)
        account = get_account(self.db_path, account_number)
        if not account:
            raise ValueError("Account not found")
        
        conn = sqlite3.connect(self.db_path, isolation_level='IMMEDIATE')
        try:
            old_balance = get_balance(self.db_path, account_number)
            new_balance = old_balance + amount
            update_balance(self.db_path, account_number, new_balance)
            conn.commit()
            return new_balance
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def withdraw(self, account_number, amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)
        account = get_account(self.db_path, account_number)
        if not account:
            raise ValueError("Account not found")
        
        conn = sqlite3.connect(self.db_path, isolation_level='IMMEDIATE')
        try:
            old_balance = get_balance(self.db_path, account_number)
            if old_balance < amount:
                raise ValueError("Insufficient funds")
            new_balance = old_balance - amount
            update_balance(self.db_path, account_number, new_balance)
            conn.commit()
            return new_balance
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def transfer(self, from_account, to_account, amount):
        from_account = self.validator.account_number_validation(from_account)
        to_account = self.validator.account_number_validation(to_account)
        amount = self.validator.amount_validation(amount)
        
        if from_account == to_account:
            raise ValueError("Cannot transfer to the same account")
        
        from_acc = get_account(self.db_path, from_account)
        to_acc = get_account(self.db_path, to_account)
        if not from_acc or not to_acc:
            raise ValueError("One or both accounts not found")
        
        conn = sqlite3.connect(self.db_path, isolation_level='IMMEDIATE')
        try:
            from_balance = get_balance(self.db_path, from_account)
            to_balance = get_balance(self.db_path, to_account)
            
            if from_balance < amount:
                raise ValueError("Insufficient funds in the source account")
            
            new_from_balance = from_balance - amount
            new_to_balance = to_balance + amount
            
            update_balance(self.db_path, from_account, new_from_balance)
            update_balance(self.db_path, to_account, new_to_balance)
            conn.commit()
            
            return {
                'from_account': from_account,
                'to_account': to_account,
                'amount': amount,
                'from_new_balance': new_from_balance,
                'to_new_balance': new_to_balance
            }
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()