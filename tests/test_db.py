from main.db import initialise_db, insert_account, get_account, get_balance, update_balance
import os
import pytest
from datetime import datetime
from decimal import Decimal
import sqlite3

@pytest.fixture
def db_setup():
    test_db = "test_bank.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    initialise_db(test_db)
    yield test_db

    if os.path.exists(test_db):
        os.remove(test_db)

def test_initialise_db(db_setup):
    conn = sqlite3.connect(db_setup)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='accounts'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "accounts table should be made"

def test_insert_and_get_account(db_setup):
    insert_account(db_setup,"AC12345","John Doe",Decimal("100.50"))
    account = get_account(db_setup,"AC12345")
    assert account["account_number"] == "AC12345"
    assert account["account_name"] == "John Doe"
    assert account["balance"] == Decimal("100.50")
    assert account["created_at"] is not None


    