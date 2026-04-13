from decimal import Decimal
from main.validator import Validator
import sqlite3


class Transaction:
    def __init__(self, db):
        self.validator = Validator()
        self.db = db

    def deposit(self, account_number, amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)
        balance = self.db.get_balance(account_number)
        if balance is None:
            raise ValueError("Acc not found")
        new_balance = balance + amount
        self.db.update_balance(account_number,new_balance)
        return new_balance

       
        

    def withdraw(self, account_number, amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)
        balance = self.db.get_balance(account_number)
        if balance is None:
            raise ValueError("Acc not found")
        if balance < amount:
            raise ValueError("Insufficient  funds")
        new_balance = balance - amount
        self.db.update_balance(account_number,new_balance)
        return new_balance

       
    def transfer(self, from_account, to_account, amount):
        from_account = self.validator.account_number_validation(from_account)
        to_account = self.validator.account_number_validation(to_account)
        amount = self.validator.amount_validation(amount)

        if from_account == to_account:
            raise ValueError("Cannot transfer to the same account")
        from_balance =  self.db.get_balance(from_account)
        to_balance =  self.db.get_balance(to_account)
        if from_balance is None or to_balance is None:
            raise ValueError("One or both accounts not found")
        if from_balance < amount:
            raise ValueError("Insufficient funds in the source account")
        updated_from = from_balance - amount
        updated_to =  to_balance + amount
        self.db.update_balance(from_account,updated_from)
        self.db.update_balance(to_account,updated_to)
        return{
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "from_new_balance": updated_from,
            "to_new_balance": updated_to
        }
