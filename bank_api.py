from fastapi import FastAPI, HTTPException, Depends
from decimal import Decimal
from main.account import Account
from main.transactions import Transaction
from main.db import BankDB

app = FastAPI()

def get_db():
    db= BankDB("bank.db")
    try:
        yield db
    finally:
        db.close()


def get_account_service(db: BankDB = Depends(get_db)):
    return Account(db)


def get_transaction_service(db: BankDB = Depends(get_db)):
    return Transaction(db)

@app.post("/accounts/")
def create_account(account_number: str, account_name: str, balance: float,
                   service: Account = Depends(get_account_service)):
    try:
        return service.create_account(
            account_number, account_name, Decimal(balance)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/accounts/{account_number}")
def get_account(account_number: str,
                service: Account = Depends(get_account_service)):
    account = service.get_account(account_number) 
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.post("/deposit/")
def deposit(account_number: str, amount: float,service: Account = Depends(get_transaction_service)):
    try:
        return {
            "new_balance": service.deposit(
                account_number, Decimal(amount)
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/withdraw/")
def withdraw(account_number: str, amount: float, service: Transaction = Depends(get_transaction_service)):
    try:
        return {
            "new_balance": service.withdraw(
                account_number, Decimal(amount)
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/transfer/")
def transfer(from_account: str, to_account: str, amount: float,service:Transaction = Depends(get_transaction_service)):
    try:
        return service.transfer(
            from_account, to_account, Decimal(amount)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))