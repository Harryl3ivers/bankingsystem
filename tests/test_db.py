from main.db import BankDB
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
    db = BankDB(test_db)
    yield test_db
    db.close()

    if os.path.exists(test_db):
        os.remove(test_db)

def test_initialise_db(db_setup):
    conn = sqlite3.connect("test_bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='accounts'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "accounts table should be made"

def test_insert_and_get_account(db):
    db.insert_account("AC12345","John Doe",Decimal("100.50"))
    account = db.get_account("AC12345")
    assert account["account_number"] == "AC12345"
    assert account["account_name"] == "John Doe"
    assert account["balance"] == Decimal("100.50")
    assert account["created_at"] is not None


def test_insert_duplicate_account(db):
    db.insert_account(
        db_setup,
        "ACC5002",
        "User One",
        Decimal("500.00")
    )

    with pytest.raises(ValueError, match="Account already exists"):
        db.insert_account(
            db_setup,
            "ACC5002",
            "User Two",
            Decimal("300.00")
        )