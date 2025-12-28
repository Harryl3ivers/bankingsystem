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
