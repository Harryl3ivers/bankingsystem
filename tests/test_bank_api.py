from bank_api import app
from fastapi.testclient import TestClient
from bank_api import app, get_db
from main.db import BankDB
import os
import pytest
import tempfile


test_db = ("test_bank_db")

@pytest.fixture
def client():
    db_file = tempfile.NamedTemporaryFile(delete=False)
    test_db = db_file.name
    db_file.close()

    def override_get_db():
        db = BankDB(test_db)
        try: 
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    app.dependency_overrides.clear()

    if os.path.exists(test_db):
        os.remove(test_db)


def test_create_duplicate(client):
    client.post("/accounts/", params={
        "account_number": "ACC1",
        "account_name": "Test",
        "balance": 50
    })

    response = client.post("/accounts/", params={
        "account_number": "ACC1",
        "account_name": "Test",
        "balance": 50
    })

    assert response.status_code == 400


def test_create_account_negative_balance(client):
    response = client.post("/accounts/", params={
        "account_number": "ACC_NEG",
        "account_name": "Test",
        "balance": -10
    })

    assert response.status_code == 400


def test_account_balance(client):
    client.post("/accounts/", params={
        "account_number": "ACC7001",
        "account_name": "Test",
        "balance": 200
    })

    response = client.get("/accounts/ACC7001")

    assert response.status_code == 200
    assert response.json()["balance"] == 200


def test_get_invalid_account(client):
    response = client.get("/accounts/DOESNOTEXIST")
    assert response.status_code == 404




def test_deposit_negative_amounts(client):
    client.post("/accounts/", params={
        "account_number": "ACC3",
        "account_name": "Test",
        "balance": 50
    })

    response = client.post("/deposit/", params={
        "account_number": "ACC3",
        "amount": -20
    })

    assert response.status_code == 400


def test_deposit_zero(client):
    client.post("/accounts/", params={
        "account_number": "ACC4",
        "account_name": "Test",
        "balance": 50
    })

    response = client.post("/deposit/", params={
        "account_number": "ACC4",
        "amount": 0
    })

    assert response.status_code == 400


def test_deposit_success(client):
    client.post("/accounts/", params={
        "account_number": "ACC3001",
        "account_name": "User",
        "balance": 0
    })

    response = client.post("/deposit/", params={
        "account_number": "ACC3001",
        "amount": 100
    })

    assert response.status_code == 200
    assert response.json()["new_balance"] == 100






def test_withdraw_exact_balance(client):
    client.post("/accounts/", params={
        "account_number": "ACC5001",
        "account_name": "Test",
        "balance": 50
    })

    response = client.post("/withdraw/", params={
        "account_number": "ACC5001",
        "amount": 50
    })

    assert response.status_code == 200
    assert response.json()["new_balance"] == 0


def test_withdraw_negative_amount(client):
    client.post("/accounts/", params={
        "account_number": "ACC6001",
        "account_name": "Test",
        "balance": 100
    })

    response = client.post("/withdraw/", params={
        "account_number": "ACC6001",
        "amount": -10
    })

    assert response.status_code == 400


def test_withdraw_too_much(client):
    client.post("/accounts/", params={
        "account_number": "ACC2001",
        "account_name": "Test",
        "balance": 75
    })

    response = client.post("/withdraw/", params={
        "account_number": "ACC2001",
        "amount": 100
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"



def test_transfer_successful(client):
    client.post("/accounts/", params={
        "account_number": "ACC3004",
        "account_name": "Noah",
        "balance": 100
    })

    client.post("/accounts/", params={
        "account_number": "ACC3005",
        "account_name": "Bob",
        "balance": 50
    })

    response = client.post("/transfer/", params={
        "from_account": "ACC3004",
        "to_account": "ACC3005",
        "amount": 30   # FIXED TYPO
    })

    assert response.status_code == 200

    account_a = client.get("/accounts/ACC3004")
    account_b = client.get("/accounts/ACC3005")

    assert account_a.json()["balance"] == 70
    assert account_b.json()["balance"] == 80


def test_transfer_insufficient_funds(client):
    client.post("/accounts/", params={
        "account_number": "ACC3004",
        "account_name": "Noah",
        "balance": 100
    })

    client.post("/accounts/", params={
        "account_number": "ACC3005",
        "account_name": "Bob",
        "balance": 50
    })

    response = client.post("/transfer/", params={
        "from_account": "ACC3004",
        "to_account": "ACC3005",
        "amount": 999
    })

    assert response.status_code == 400