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

def test_transfer(transaction_setup):
    account, trans_mnger = transaction_setup

    account.create_account("ACC3001", "Mia Taylor", Decimal("1000.00"))
    account.create_account("ACC3002", "Noah Anderson", Decimal("500.00"))

    result = trans_mnger.transfer("ACC3001", "ACC3002", Decimal("300.00"))

    assert result["from_new_balance"] == Decimal("700.00")
    assert result["to_new_balance"] == Decimal("800.00")
    assert result["amount"] == Decimal("300.00")

def test_transfer_entire_balance(transaction_setup):
    account,trans_mnger = transaction_setup
    account.create_account("ACC3003","Ava Thomas",Decimal("600.00"))
    account.create_account("ACC3004","Elijah Jackson",Decimal("400.00"))
    result = trans_mnger.transfer("ACC3003","ACC3004",Decimal("600.00"))
    assert result["from_new_balance"] == Decimal("0.00")
    assert result["to_new_balance"] == Decimal("1000.00")

def test_transfer_insufficient_funds(transaction_setup):
    account,trans_mnger = transaction_setup
    account.create_account("ACC3005","Charlotte White",Decimal("200.00"))
    account.create_account("ACC3006","James Harris",Decimal("300.00"))
    with pytest.raises(ValueError,match="Insufficient funds in the source account"):
        trans_mnger.transfer("ACC3005","ACC3006",Decimal("250.00"))

def test_transfer_same_account(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC3007","Amelia Martin", Decimal("700.00"))
    with pytest.raises(ValueError,match="Cannot transfer to the same account"):
        trans_mnger.transfer("ACC3007","ACC3007",Decimal("100.00"))

def test_transfer_nonexistent_account(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC3008","Ethan Lee",Decimal("400.00"))
    with pytest.raises(ValueError,match="One or both accounts not found"):
        trans_mnger.transfer("ACC3008","ACC999",Decimal("50.00"))

# def test_both_accounts_fail_atomcity(transaction_setup):
#     account, trans_mnger = transaction_setup
#     account.create_account

def test_multiple_transfers(transaction_setup):
    account, trans_mnger = transaction_setup
    account.create_account("ACC3009","Logan Perez",Decimal("1000.00"))
    account.create_account("ACC3010","Lucas Thompson",Decimal("400.00"))
    trans_mnger.transfer("ACC3009","ACC3010",Decimal("200.00"))
    trans_mnger.transfer("ACC3010","ACC3009",Decimal("140.00"))
    acc1 = account.get_account("ACC3009")
    acc2 = account.get_account("ACC3010")
    assert acc1['balance'] == Decimal("940.00")
    assert acc2['balance'] == Decimal("460.00")

def test_conservation_of_money(transaction_setup):
    account, trans_mnger = transaction_setup

    # Arrange
    account.create_account("ACC4001", "Sender", Decimal("1000.00"))
    account.create_account("ACC4002", "Receiver", Decimal("500.00"))

    initial_total = (
        account.get_account("ACC4001")['balance'] +
        account.get_account("ACC4002")['balance']
    )

    # Act
    trans_mnger.transfer("ACC4001", "ACC4002", Decimal("200.00"))
    trans_mnger.transfer("ACC4002", "ACC4001", Decimal("100.00"))
    trans_mnger.transfer("ACC4001", "ACC4002", Decimal("50.00"))

    # Assert
    final_total = (
        account.get_account("ACC4001")['balance'] +
        account.get_account("ACC4002")['balance']
    )

    assert final_total == initial_total
