from bank_api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_withdraw_too_much():
    client.post("/accounts/",params={
        "account_number": "ACC2001",
        "account_name": "Test",
        "balance": 75
    })

    response = client.post("/withdraw/",params={
        "account_number": "ACC2001",
        "amount": 100

    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"

def test_invalid_account():
    client.post("/accounts/",params={
         "account_number": "ACC344401",
        "account_name": "Test",
        "balance": 75

    }) 

    response = client.post("/deposit/", params={
        "account_number": "INVALID",
        "amount": 10})
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"

def test_deposit_success():
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