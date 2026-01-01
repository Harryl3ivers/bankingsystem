import pytest
import os
from decimal import Decimal
from main.transactions import Transaction
from main.db import *
from main.account import Account

@pytest.fixture
def transaction_setup():
    test_db = "test_bank.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    account = Account(test_db)
    trans_mnger = Transaction(test_db)

    yield account, trans_mnger
    if os.path.exists(test_db):
        os.remove(test_db)

def test_deposite(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC2001","Emma Johnson",Decimal("500.00"))
    new_balance = trans_mnger.deposite("ACC2001",Decimal("200.00"))
    assert new_balance == Decimal("700.00")

def test_deposite_nonexistent_account(transaction_setup):
    _, trans_mnger = transaction_setup
    with pytest.raises(ValueError, match="Account not found"):
        trans_mnger.deposite("ACC999", Decimal('100.00'))

def test_deposite_invalid_amount(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC2003","Olivia Davis",Decimal("400.00"))
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
        trans_mnger.deposite("ACC2003",Decimal("-50.00"))
     
def test_withdraw(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC2002","Liam Williams",Decimal("800.00"))
    new_balance = trans_mnger.withdraw("ACC2002",Decimal("300.00"))
    assert new_balance == Decimal("500.00")

def test_withdraw_entire_balance(transaction_setup):
    account,trans_mnger = transaction_setup
    account.create_account("ACC2004","Harry Brown",Decimal("1200.00"))
    new_balance = trans_mnger.withdraw("ACC2004",Decimal("1200.00"))
    assert new_balance == Decimal("0.00")

def test_withdraw_and_deposite(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC2005","Sophia Wilson",Decimal("1000.00"))
    trans_mnger.deposite("ACC2005",Decimal("500.00"))
    new_balance = trans_mnger.withdraw("ACC2005",Decimal("300.00"))
    assert new_balance == Decimal("1200.00")

def test_withdraw_nonexistent_account(transaction_setup):
    _, trans_mnger = transaction_setup
    
    with pytest.raises(ValueError, match="Account not found"):
        trans_mnger.withdraw("ACC999", Decimal('100.00'))
    
def test_withdraw_insufficient_funds(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC2006","Isabella Moore",Decimal("250.00"))
    with pytest.raises(ValueError, match="Insufficient funds"):
        trans_mnger.withdraw("ACC2006",Decimal("300.00"))
        