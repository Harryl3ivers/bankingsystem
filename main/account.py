from decimal import Decimal
from main.validator import Validator
from main.db import initialise_db, insert_account, get_account

class Account:
    def __init__(self,db_path="bank.db"):
        self.db_path = db_path
        initialise_db(self.db_path)
        self.validator = Validator()
    
    def create_account(self, account_number, account_name,balance):
        account_number = self.validator.account_number_validation(account_number)
        account_name = self.validator.account_name_validation(account_name)
        balance = self.validator.amount_validation(balance)
        insert_account(self.db_path,account_number, account_name, balance)
        return get_account(self.db_path, account_number)

       
    
    def get_account(self, account_number):
        account_number = self.validator.account_number_validation(account_number)
        return get_account(self.db_path,account_number)