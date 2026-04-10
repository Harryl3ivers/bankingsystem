from locust import HttpUser, task, between
import random

class BankUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.account_number = f"ACC{random.randint(1000,9999)}" #generates unique acc num
        self.client.post("/accounts/",params={
            "account_number": self.account_number,
            "account_name": "test user",
            "balance": 100
        })
    
    @task(3)
    def deposit(self):
        self.client.post("/deposit/",params={
            "account_number":self.account_number,
            "amount": random.randint(1,20)

        })
    
    @task(2)
    def withdraw(self):
        self.client.post("/withdraw/",params={
            "account_number":self.account_number,
            "amount": random.randint(1,10)
        })
    
    @task(1)
    def check_balance(self):
        self.client.get(f"/accounts/{self.account_number}")

  