from decimal import Decimal
import re

class Validator:
    def account_number_validation(account_number):
        if not account_number or not account_number.strip():
            raise ValueError("Account number cannot be empty.")
        account_number = account_number.strip().upper()
        if not re.match(r'^ACC\d{3,10}$', account_number):
            raise ValueError("Account number must be ACC + digits (e.g., ACC001)")
        return account_number
    
    def account_name_validation(account_name):
        if not account_name or not account_name.strip():
            raise ValueError("Account name cannot be empty.")
        account_name = account_name.strip()
        if len(account_name) < 3:
            raise ValueError("Account name must be at least 3 characters long.")
        return account_name
         
    def amount_validation(amount):
        amount = Decimal(amount)
        if amount <=0:
            raise ValueError("Amount must be greater than zero.")