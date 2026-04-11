from bank_api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_duplicate():
    client.post("/accounts/", params={
        "account_number": "ACC1",
        "account_name": "Test",
        "balance": 50
    })
    assert response.status_code == 400
    



    response = client.post("/accounts/", params={
        "account_number": "ACC1",
        "account_name": "Test",
        "balance": 50
    })

def create_account_negative_balance():
    response =client.post("/accounts/", params={
        "account_number": "ACC1",
        "account_name": "Test",
        "balance": -10
    })
    assert response.status_code == 400

def test_deposit_negative_amounts():
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
    
def test_deposit_zero():
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

def test_withdraw_exact_balance():
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


def test_withdraw_negative_amount():
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

def test_account_balance():
    client.post("/accounts/",params={
        "account_number": "ACC7001",
        "account_name": "Test",
        "balance": 200
    })
    response = client.get("/accounts/ACC7001")
    assert response.status_code == 200
    assert response.json()["balance"] == 200

def test_get_invalid_account():
    response = client.get("/accounts/DOESNOTEXIST")
    assert response.status_code ==  404

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

def test_transfer_successful():
    client.post("/accounts/", params={
        "account_number": "ACC3004",
        "account_name": "Noah",
        "balance": 0
    })