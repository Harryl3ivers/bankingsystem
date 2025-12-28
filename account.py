from decimal import Decimal
from validator import Validator
from db import initialise_db, create_account, get_account

class Account:
    def __init__(self,db_path="bank.db"):
        self.db_path = db_path
        initialise_db(self.db_path)
        self.validator = Validator()
    
    def create_account(self, account_number, account_name,balance):
        account_number = self.validator.account_number_validation(account_number)
        account_name = self.validator.account_name_validation(account_name)
        save_account = create_account(self.db_path, account_number,account_name,balance)
        if not save_account:
            raise ValueError("Account creation has failed.")
        return save_account
    
    def get_account(self, account_number):
        account_number = self.validator.account_number_validation(account_number)
        return get_account(self.db_path,account_number)