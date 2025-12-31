import pytest
import os
from decimal import Decimal
from main.account import Account
from main.db import *

@pytest.fixture
def account_setup():
    test_db = "test_bank.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    manager = Account(test_db)
    yield manager

    if os.path.exists(test_db):
        os.remove(test_db)


def test_get_account(account_setup):
    # Arrange
    account_setup.create_account(
        "ACC1001",
        "Noah Smith",
        Decimal("1500.00")
    )

    # Act
    accounts = account_setup.get_account("ACC1001")

    # Assert
    assert accounts["account_number"] == "ACC1001"
    assert accounts["account_name"] == "Noah Smith"
    assert accounts["balance"] == Decimal("1500.00")
    assert accounts["created_at"] is not None

def test_get_account_not_found(account_setup):
    accounts = account_setup.get_account("ACC9999")
    assert accounts is None

def test_create_account(account_setup):
    account = account_setup.create_account("ACC001", "John Doe", Decimal('1000.00'))
    
    assert account['account_number'] == "ACC001"
    assert account['account_name'] == "John Doe"
    assert account['balance'] == Decimal('1000.00')

def test_create_account_duplicate(account_setup):
    account_setup.create_account("ACC001", "John Doe", Decimal('1000.00'))
    
    with pytest.raises(ValueError, match="Account already exists"):
        account_setup.create_account("ACC001", "Jane Smith", Decimal('500.00'))

def test_get_account_zero_balance(account_setup):
    account_setup.create_account("ACC002", "Alice Brown", Decimal('0.01'))
    
    account = account_setup.get_account("ACC002")
    
    assert account['account_number'] == "ACC002" 
    assert account['account_name'] == "Alice Brown"
    assert account['balance'] == Decimal('0.01')