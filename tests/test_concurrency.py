import pytest
import os
from decimal import Decimal
from main.transactions import Transaction
from main.db import *
from main.account import Account
import threading

@pytest.fixture
def concurrency_setup():
    test_db = "test_concurrency.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    account = Account(test_db)
    trans_mnger = Transaction(test_db)
    account.create_account("ACC3001","Ethan Taylor",Decimal("1000.00"))
    yield account, trans_mnger
    if os.path.exists(test_db):
        os.remove(test_db)

def test_concurrent_withdrawals_while_preventing_overdraft(concurrency_setup):
    account, trans_mnger = concurrency_setup
    results = {"success": 0, "failure": 0}
    lock = threading.Lock()

    def withdraw():
        with lock:
            try:
                trans_mnger.withdraw("ACC3001", Decimal("600.00"))
                results["success"] += 1
            except ValueError as e:
                results["failure"] += 1

    thread1 = threading.Thread(target=withdraw)
    thread2 = threading.Thread(target=withdraw)

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads to finish
    thread1.join()
    thread2.join()

    # Assertions
    assert results["success"] == 1
    assert results["failure"] == 1

    # Check final balance
    final_balance = account.get_account("ACC3001")["balance"]
    assert final_balance == Decimal("400.00")

def test_multiple_concurrent_deposits(concurrency_setup):
    account, trans_mnger = concurrency_setup
    lock = threading.Lock()
    def deposit_money():
        with lock:
            for _ in range(10):
                trans_mnger.deposite("ACC3001",Decimal("10.00")) 
    threads = [threading.Thread(target=deposit_money)for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    final_balance = account.get_account("ACC3001")["balance"]
    assert final_balance == Decimal("1500.00")