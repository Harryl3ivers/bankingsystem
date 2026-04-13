from decimal import Decimal
from main.validator import Validator
from main.db import BankDB
class Account:
    def __init__(self,db):
        self.db = db
        self.validator = Validator()
    
    def create_account(self, account_number, account_name,balance):
        account_number = self.validator.account_number_validation(account_number)
        account_name = self.validator.account_name_validation(account_name)
        balance = self.validator.amount_validation(balance)
        self.db.insert_account(account_number, account_name, balance)
        return self.db.get_account(account_number)

       
    
    def get_account(self, account_number):
    #    account_number = self.validator.account_number_validation(account_number) 
       return self.db.get_account(account_number)
    '''just looks up records
 doesn’t reject people for looking “wrong so doesnt need validator”'''

 
         
