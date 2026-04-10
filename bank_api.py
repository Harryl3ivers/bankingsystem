from fastapi import FastAPI, HTTPException
from decimal import Decimal
from main.account import Account
from main.transactions import Transaction

app = FastAPI()

account_services = Account()
transaction_services = Transaction()


@app.post("/accounts/")
def create_account(account_number: str, account_name: str, balance: float):
    try:
        return account_services.create_account(
            account_number, account_name, Decimal(balance)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/accounts/{account_number}")
def get_account(account_number: str):
    account = account_services.get_account(account_number)  # ✅ fixed
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.post("/deposit/")
def deposit(account_number: str, amount: float):
    try:
        return {
            "new_balance": transaction_services.deposit(
                account_number, Decimal(amount)
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/withdraw/")
def withdraw(account_number: str, amount: float):
    try:
        return {
            "new_balance": transaction_services.withdraw(
                account_number, Decimal(amount)
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/transfer/")
def transfer(from_account: str, to_account: str, amount: float):
    try:
        return transaction_services.transfer(
            from_account, to_account, Decimal(amount)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))